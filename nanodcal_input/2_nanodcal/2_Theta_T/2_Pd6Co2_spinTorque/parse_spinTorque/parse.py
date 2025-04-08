import sys
import numpy as np
import junpy as jp
from junpy.util import SimpleTable

#--------------------------------------
# reading user input
# e.g.
#    files = 'files_l4_NC_theta90_dep-bias_eta1e-2.txt' or 'file.pickle'
#    slices = '[:,11,:]'

if len(sys.argv) != 3:
    raise RuntimeError('Usage: filename interface')

files = sys.argv[1]
slices = sys.argv[2]

if files.endswith('.pickle'):
    files = [files]
else:
    files = np.loadtxt(files, dtype=str)

#--------------------------------------
# read data

print('Loading files...')

data = []
for i, filename in enumerate(files):
    print(i, filename)
    calcr = jp.load(filename)
    data.append(np.c_[
        calcr.spin_torque(hamiltonian='Hxc')[0,0],
        calcr.spin_torque(hamiltonian='Hso')[0,0],
        calcr.spin_accumulation(hamiltonian='H0')[0,0],
        calcr.spin_accumulation(hamiltonian='Hso')[0,0],
        calcr.spin_accumulation()[0,0],
        calcr.spin_accumulation(hamiltonian='Hxc')[0,0],
    ])
data = np.array(data)

print(f'data(#file, #site, #column) = {data.shape}')
print()

#--------------------------------------
# print results

path = '../Result_output_Slices.txt'
store_pos = open(path, 'w')

print(f'Slices = {slices}')
print(f'Slices = {slices}', file=store_pos)

data2 = eval(f'data{slices}')
table = jp.SimpleTable()
table.set_header(['Txc_x_eV', 'Txc_y_eV', 'Txc_z_eV', 'Tso_x_eV', 'Tso_y_eV', 'Tso_z_eV', 'A0_x_eV', 'A0_y_eV', 'A0_z_eV', 'Aso_x_eV', 'Aso_y_eV', 'Aso_z_eV', 'Atot_x_eV', 'Atot_y_eV', 'Atot_z_eV', 'Axc_x_eV', 'Axc_y_eV', 'Axc_z_eV'], fmt='{:>13s} ')
table.set_data(data2, fmt='{: .6e} ')
print(table)
print(table, file=store_pos)
print()

path = '../Result_output_SumAll.txt'
store_pos = open(path, 'w')

print(f'Sum all sites')
print(f'Sum all sites', file=store_pos)

data3 = np.sum(data, axis=1)
table = jp.SimpleTable()
table.set_header(['Txc_x_eV', 'Txc_y_eV', 'Txc_z_eV', 'Tso_x_eV', 'Tso_y_eV', 'Tso_z_eV', 'A0_x_eV', 'A0_y_eV', 'A0_z_eV', 'Aso_x_eV', 'Aso_y_eV', 'Aso_z_eV', 'Atot_x_eV', 'Atot_y_eV', 'Atot_z_eV', 'Axc_x_eV', 'Axc_y_eV', 'Axc_z_eV'], fmt='{:>13s} ')
table.set_data(data3, fmt='{: .6e} ')
print(table)
print(table, file=store_pos)
print()

