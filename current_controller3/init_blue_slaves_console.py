import visa
rm = visa.ResourceManager()
rmlist = rm.list_resources()
f = rm.open_resource(rmlist[-1])

print('')
print('Current settings of blue slaves:')
print('Usage: f.write(\':SLOT <channel>;:ILD:SET .<current_in_mA>\')')
