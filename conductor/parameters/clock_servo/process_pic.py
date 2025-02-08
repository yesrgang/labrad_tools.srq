#%% Load Libs
import os
import sys
import time

import h5py
import numpy as np

DATADIR = '/srqdata2/data/'


#%% Picture Processing Functions

def extract_eval_shape(pic_filt):
  """
  Extract the minimal array shape required to accomodate all data masked by
  pic_filt.

  Parameters
  ----------
  pic_filt : 2d bool array
      True where the data is accepted, False otherwise.

  Returns
  -------
  pic_shape : 2-element numpy array of integers
      Shape of required data array to accomodate filtered data.
  pic_offset : 2-element numpy array of integers
      Offset indices in original data set of the cutout of the filtered data.
  """
  
  x_inds = np.where(pic_filt.max(0))[0]
  (x_min, x_max) = (x_inds[0], x_inds[-1])
  y_inds = np.where(pic_filt.max(1))[0]
  (y_min, y_max) = (y_inds[0], y_inds[-1])
  
  pic_offset = np.array([int(x_min), int(y_min)])
  pic_shape = np.array([int(x_max - x_min + 1), int(y_max - y_min + 1)])
  
  return pic_shape, pic_offset


def gen_square_pic_filt(pic_shape, cut_offset, cut_radius):
  """
  Generate a picture filter and array shape for holding the corresponding data.
  
  Patameters
  ----------
  pic_shape : 2-element array of integers
    x- and y-size of pictures to which the filter will be applied (size of filter array, x: 2nd dimension, y: 1st dimension)
  cut_offset : 2-element array of integers
    x- and y-position of the filter's center (x: 2nd dimension, y: 1st dimension)
  cut_radius : integer
    Radius of cutout (size of the cutout: 2*cut_radius+1)
  
  Returns
  -------
  cut_filter : pic_shape[0] x pic_shape[1] bool array
    Picture filter
  cut_shape : 2-element numpy array of integers
    Shape of the filtered pictures
  """
  
  x, y = np.meshgrid(range(pic_shape[0]), range(pic_shape[1]))
  dx = x - cut_offset[0]
  dy = y - cut_offset[1]
  cut_filter = (np.abs(dx) < cut_radius) & (np.abs(dy) < cut_radius)
  cut_shape = extract_eval_shape(cut_filter)[0]
  return cut_filter, cut_shape


def gen_circ_pic_filt(pic_shape, cut_offset, cut_radius):
  """
  Generate circular picture filter (c.f. gen_square_pic_filt for more information)
  
  Returns
  -------
  filt : pic_shape[0] x pic_shape[1] bool array
    Picture filter
  shape : 2-element numpy array of integers
    Shape of the filtered pictures
  filt_cut : shape[0] x shape[1] bool array
    Picture filter cut down to the size referenced by shape
  """
  
  x, y = np.meshgrid(range(pic_shape[0]), range(pic_shape[1]))
  dx = x - cut_offset[0]
  dy = y - cut_offset[1]
  filt = (dx**2 + dy**2) < cut_radius**2
  shape = extract_eval_shape(filt)[0]
  filt_cut = filt[(np.abs(dx) < cut_radius) & (np.abs(dy) < cut_radius)].reshape(shape)
  return filt, shape, filt_cut


def calc_absorption_density(pics, bright_pics, pics_dark, bright_pics_dark, norm, dx, dy, dx2, dy2,
                            pixel_size, cross_section, gain, linewidth, pulse_length):
  # all pictures are 3d arrays (1st dim: picture #, 2nd dim: y, 3rd dim: x)
  # pics:    absorption pictures (with atoms)
  # brights: reference pictures (without atoms)
  # darks:   pictures without light (dark current + ADC offset)
  #          (takes either a single picture or as many as in pics/bright_pics)
  
  # norm:    normalization filter
  # dx/dy:   meshgrid arrays: x-x0 / y-y0 (coordinate relative to the center (x0,y0) of the atom cloud)
  # dx2/dy2: dx2=dx**2, dy2=dy**2 square of the relative coordinate
  
  # subtract dark counts
  np.subtract(pics, pics_dark)
  np.subtract(bright_pics, bright_pics_dark)
  # pics -= pics_dark
  # bright_pics -= bright_pics_dark
  
  # normalize reference pictures
  # bright_pics *= (pics[:,norm].mean(1) / bright_pics[:,norm].mean(1))[:,None,None]
  bright_pics = bright_pics * (pics[:,norm].mean(1) / bright_pics[:,norm].mean(1))[:,None,None]
  
  # subtract intensity gradient (between pics + bright_pics) in normalization area
  mx = (dx[None,norm] * (pics[:,norm] - bright_pics[:,norm])).mean(1) / dx2[None,norm].mean(1)
  my = (dy[None,norm] * (pics[:,norm] - bright_pics[:,norm])).mean(1) / dy2[None,norm].mean(1)
  bright_pics += mx[:,None,None] * dx + my[:,None,None] * dy
  
  # claculate densities
  dens = np.full(pics.shape, np.nan)
  valid = (pics > 0) & (bright_pics > 0)
  # Lambert-Beer absorption
  dens[valid] = np.log(bright_pics[valid] / pics[valid]) * pixel_size**2 / cross_section
  # saturation correction
  dens[valid] += (bright_pics[valid] - pics[valid]) * gain / (np.pi * linewidth * pulse_length)
  
  return dens


def calc_absorption_density_kuro(pics, bright_pics, pics_dark, bright_pics_dark, norm, dx, dy, dx2, dy2):
  # kuro imaging parameters
  pixel_size = 16e-6 / (3.88 * 10)
  gain = 2.79 / 0.85 / 0.65
  cross_section = 0.1014e-12 * 0.46
  linewidth = 30.5e6 * 1.71
  #linewidth = 32e6 * 1.75
  pulse_length = 1.0e-6 - 150e-9
  fluorescence_gain = 1.28e-6
  
  return calc_absorption_density(pics, bright_pics, pics_dark, bright_pics_dark, norm, dx, dy, dx2, dy2, pixel_size, cross_section, gain, linewidth, pulse_length)


def calc_absorption_density_pixelfly(pics, bright_pics, pics_dark, bright_pics_dark, norm, dx, dy, dx2, dy2):
  # pixelfly imaging parameters
  pixel_size = 6.45e-6 / 11.4
  gain = 1.0 / 0.55 / 0.72
  cross_section = 0.1014e-12 * 0.78
  linewidth = 30.5e6
  pulse_length = 10e-6
  
  return calc_absorption_density(pics, bright_pics, pics_dark, bright_pics_dark, norm, dx, dy, dx2, dy2, pixel_size, cross_section, gain, linewidth, pulse_length)


#%% Load+Process Pic
def process_pic(picpath, x0y0, eval_size=400, cloud_size=60):
  ### Load Pic
  
  x0, y0 = x0y0[0], x0y0[1]
  eval_size  = 400 # radius for picture extraction
  cloud_size = 60 # radius for cloud eval (defines cloud and normalization regions)
  
  # picture arrays
  _,tmp_pic_shape = gen_square_pic_filt([1200, 1200], [600, 600], eval_size) # coordinates are irrelevant here; important: the cutout needs to fit inside
  pic_center = ((tmp_pic_shape-1) / 2).astype(int)
  pics_dx, pics_dy = np.meshgrid(range(tmp_pic_shape[1]), range(tmp_pic_shape[0]))
  pics_dx -= pic_center[1]
  pics_dy -= pic_center[0]
  pics_dx2 = pics_dx**2
  pics_dy2 = pics_dy**2
  
  cloud_filt, cloud_shape, cloud_filt_cut = gen_circ_pic_filt(tmp_pic_shape, pic_center, cloud_size)
  
  eval_area, eval_shape = gen_square_pic_filt([1200, 1200], [x0, y0], eval_size) # kuro
  # eval_area, _ = gen_square_pic_filt([1040, 1392], [x0, y0], eval_size) # pixelfly
  tmp_eval_mask = np.ones(tmp_pic_shape).astype(bool) # for broadcasting filtered pic to 2d numpy array
  
  
  # load raw pictue data
  camera = 'kuro'
  kdata = {
    'g': np.empty([1, eval_shape[0], eval_shape[1]]),
    'e': np.empty([1, eval_shape[0], eval_shape[1]]),
    'b': np.empty([1, eval_shape[0], eval_shape[1]]),
    's': np.empty([1, eval_shape[0], eval_shape[1]]),
    }
  eval_area_mask = np.ones(eval_shape).astype(bool) # for broadcasting filtered pic to 2d numpy array
  #with h5py.File(os.path.join(DATADIR, picpath), 'r') as infile:
  with h5py.File(picpath, 'r') as infile:
      for k in infile:
        kdata[k][0][eval_area_mask] = infile[k][eval_area]
  
  
  """ Calculate atoms numbers """
  if camera == 'kuro':
    ## load old dark pics
    #dark_path = os.path.join('/', 'srqdata1/data/20220913/scan#14', 'packed.hdf5')
    #dark_data = h5py.File(dark_path, 'r')
    #g_dark = dark_data['processed/g.mean'][:]
    #b_dark = dark_data['processed/b.mean'][:]
    #e_dark = dark_data['processed/e.mean'][:]
    #s_dark = dark_data['processed/s.mean'][:]
    #dark_data.close()
    #
    ## cut to eval area
    #g_dark = np.reshape(g_dark[eval_area], eval_shape)
    #b_dark = np.reshape(b_dark[eval_area], eval_shape)
    #e_dark = np.reshape(e_dark[eval_area], eval_shape)
    #
    #pic_g = calc_absorption_density_kuro(kdata['g'].astype(np.float64), kdata['b'].astype(np.float64), g_dark, b_dark, ~cloud_filt, pics_dx, pics_dy, pics_dx2, pics_dy2)[0]
    #pic_e = calc_absorption_density_kuro(kdata['e'].astype(np.float64), kdata['b'].astype(np.float64), e_dark, b_dark, ~cloud_filt, pics_dx, pics_dy, pics_dx2, pics_dy2)[0]

    g_dark = kdata['s'].astype(np.float64)
    e_dark = g_dark
    b_dark = g_dark
    pic_g = calc_absorption_density_kuro(kdata['g'].astype(np.float64), kdata['b'].astype(np.float64), g_dark, b_dark, ~cloud_filt, pics_dx, pics_dy, pics_dx2, pics_dy2)[0]
    pic_e = calc_absorption_density_kuro(kdata['e'].astype(np.float64), kdata['b'].astype(np.float64), e_dark, b_dark, ~cloud_filt, pics_dx, pics_dy, pics_dx2, pics_dy2)[0]

  if camera == 'pixelfly':
    dark_path = os.path.join('/', 'srqdata2/data/20221120', 'mean.pixelfly.npy')
    with open(dark_path, 'rb') as f:
      image_dark  = np.load(f)
      bright_dark = np.load(f)
    
    pic_g = calc_absorption_density_pixelfly(kdata['image'], kdata['bright'], kdata['dark'], kdata['dark'], ~cloud_filt, pics_dx, pics_dy, pics_dx2, pics_dy2)[0]
  
  def get_centr_and_idxs(shape):
    center = np.array([np.mean((range(0, shape[1]))), np.mean((range(0, shape[0])))])
    xax = np.arange(0, shape[1]) - center[0] # axes (in px) centered around center
    yax = np.arange(0, shape[0]) - center[1]
    xinds = (xax + center[0]).astype(int)
    yinds = (yax + center[1]).astype(int)
    return center, xax, yax, xinds, yinds
  
  # position and indexing of pics
  pic_center, pic_xaxis, pic_yaxis, pic_xinds, pic_yinds = get_centr_and_idxs(pic_g.shape)
  
  
  ### Show Pic + Eval
  
  tmp_circ_phis = np.linspace(0, 2*np.pi, 500)
  tmp_circ_x    = pic_center[0] + cloud_size*np.cos(tmp_circ_phis)
  tmp_circ_y    = pic_center[1] + cloud_size*np.sin(tmp_circ_phis)
  
  ntot_pic = pic_g + pic_e
  ef_pic   = pic_e / (pic_g + pic_e)
  
  ntot = ntot_pic[cloud_filt].sum()
  ef = pic_e[cloud_filt].sum() / ntot_pic[cloud_filt].sum()
  
  return ef, ntot


#%% Execute Picture Processing

# test...
#print(process_pic('20250206/scan#12/2.kuro.hdf5', (572,707)))

if __name__ == '__main__':
  #print(sys.argv[1])
  #print(sys.argv[2])
  #print(sys.argv[3])
  picpath = os.path.join(DATADIR, sys.argv[1])

  sleep_duration = 1e-3 # (in s)
  timeout = 4. # (in ~s)

  # wait until file is created
  sleep_counter = 0
  while not os.path.isfile(picpath): # wait for pic to be saved...
    if sleep_counter >= timeout:
      raise Exception('File \'{:s}\' does not exist! (yet?)'.format(picpath))
    sleep_counter += sleep_duration
    time.sleep(sleep_duration)
  
  # wait until file contents are ready (usual Kuro picture size: ~3MB)
  sleep_counter = 0
  while os.path.getsize(picpath) < 2.8e6:
    if sleep_counter >= timeout:
      raise Exception('File \'{:s}\' contents are not ready (file too small)!'.format(picpath))
    sleep_counter += sleep_duration
    time.sleep(sleep_duration)

  ef,ntot = process_pic(picpath, (int(sys.argv[2]), int(sys.argv[3])), eval_size=400, cloud_size=40)
  print('{:.6f} {:.3f}'.format(ef, ntot))

