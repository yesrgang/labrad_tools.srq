
def calc_sr2_fnc_box_ref_freq(mjm_comb_demod, drive_freq):
    if mjm_comb_demod is None:
        return
    
    # aom on comb table. 0th order goes to comb. double passed, +1 order 
    # goes back through fiber.
    comb_table_offset_aom = 30.0e6
    
    # beat frequency for distribution center -> comb table fiber noise 
    # cancellation.
    comb_dist_fnc_beat = -95.524640e6
    
    # implied frequency of aom between distribution center and comb.
    # light travelling from distribution center to comb table is shifted 
    # down in frequency.
    comb_dist_aom = (comb_dist_fnc_beat - 2.0 * comb_table_offset_aom) / 2.0
    
    # frequency of the injection locked diode in the distribution center,
    # relative to the stable comb tooth.
    dist_diode = -comb_dist_aom - mjm_comb_demod
    
    # between diode and atoms
    srq_dist_fnc = drive_freq - dist_diode
    
    # 100 MHz AOM after fiber on SrQ table.
    srq_table_offset_aom = -100e6
    
    # fix output of FNC box VCO to 77.77 MHz
    srq_dist_aom = -77.77e6
    
    # second aom on SrQ table to keep FNC VCO within output bandwidth.
    srq_steer = srq_dist_aom + srq_table_offset_aom - srq_dist_fnc
    
    srq_dist_fnc_demod = -2 * srq_dist_fnc

    f_0 = -235.610600e6 + 110.6 #20240209 calibration
    delta_p = 1.431e3
    f_pump = f_0 - delta_p
    f_aom3 = 39.9642716e6 
    f_offset = f_aom3 - f_pump
    output_f_if_directDriveAOM3 = drive_freq + f_offset
    return float(output_f_if_directDriveAOM3)

    # retrurn float(srq_dist_fnc_demod) when the DDS goes to Christian's box
#    return float(srq_dist_fnc_demod)

