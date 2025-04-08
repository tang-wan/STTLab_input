import numpy as np # type: ignore
import os


class jp_analysis():
    def __init__(self, pickle_path):
        self.pickle_path = pickle_path

    def Writting_parseFile(self):
        with open("parse_spinTorque/SOC_zx_R.txt", 'w') as W_File:
            lines = self.pickle_path
            W_File.writelines(lines)

    def Making_parsingFile(self):
        lines = [
                'import sys\n',
                'import numpy as np     #type:ignore\n',
                'import junpy as jp     #type:ignore\n',
                'from junpy.util import SimpleTable     #type:ignore\n',
                '\n',
                '#--------------------------------------\n',
                '# reading user input\n',
                '# e.g.\n',
                '#    files = \'files_l4_NC_theta90_dep-bias_eta1e-2.txt\' or \'file.pickle\'\n',
                '#    slices = \'[:,11,:]\'\n',
                '\n',
                'if len(sys.argv) != 3:\n',
                '    raise RuntimeError(\'Usage: filename interface\')\n',
                '\n',
                'files = sys.argv[1]\n',
                'slices = sys.argv[2]\n',
                '\n',
                'if files.endswith(\'.pickle\'):\n',
                '    files = [files]\n',
                'else:\n',
                '    files = np.loadtxt(files, dtype=str)\n',
                '\n',
                '#--------------------------------------\n',
                '# read data\n',
                '\n',
                "print('Loading files...')\n",
                '\n',
                'data = []\n',
                'for i, filename in enumerate(files):\n',
                '    print(i, filename)\n',
                '    calcr = jp.load(filename)\n',
                '    data.append(np.c_[\n',
                '        calcr.spin_torque(hamiltonian=\'Hxc\')[0,0],\n',
                '        calcr.spin_torque(hamiltonian=\'Hso\')[0,0],\n',
                '        calcr.spin_accumulation(hamiltonian=\'H0\')[0,0],\n',
                '        calcr.spin_accumulation(hamiltonian=\'Hso\')[0,0],\n',
                '        calcr.spin_accumulation()[0,0],\n',
                '        calcr.spin_accumulation(hamiltonian=\'Hxc\')[0,0],\n',
                '    ])\n',
                'data = np.array(data)\n',
                '\n',
                "print(f'data(#file, #site, #column) = {data.shape}')\n",
                'print()\n',
                '\n',
                '#--------------------------------------\n',
                '# print results\n',
                '\n',
                'path = \'../Result_output_Slices.txt\'\n',
                'store_pos = open(path, \'w\')\n',
                '\n',
                "print(f'Slices = {slices}')\n",
                "print(f'Slices = {slices}', file=store_pos)\n",
                '\n',
                "data2 = eval(f'data{slices}')\n",
                'table = jp.SimpleTable()\n',
                "table.set_header([\'Txc_x_eV\', \'Txc_y_eV\', \'Txc_z_eV\', \'Tso_x_eV\', \'Tso_y_eV\', \'Tso_z_eV\', \'A0_x_eV\', \'A0_y_eV\', \'A0_z_eV\', \'Aso_x_eV\', \'Aso_y_eV\', \'Aso_z_eV\', \'Atot_x_eV\', \'Atot_y_eV\', \'Atot_z_eV\', \'Axc_x_eV\', \'Axc_y_eV\', \'Axc_z_eV\'], fmt='{:>13s} ')\n",
                "try:\n",
                "   table.set_data(data2, fmt='{: .6e} ')\n",
                "except RuntimeError:\n",
                "   print('Data must be a 2-d array.')\n",
                # "table.set_data(data2, fmt='{: .6e} ')\n",
                'print(table)\n',
                'print(table, file=store_pos)\n',
                'print()\n',
                '\n',
                'path = \'../Result_output_SumAll.txt\'\n',
                'store_pos = open(path, \'w\')\n',
                '\n',
                'print(f\'Sum all sites\')\n',
                'print(f\'Sum all sites\', file=store_pos)\n',
                '\n',
                "data3 = np.sum(eval(f'data{slices}'), axis=1)\n",
                'table = jp.SimpleTable()\n',
                "table.set_header([\'Txc_x_eV\', \'Txc_y_eV\', \'Txc_z_eV\', \'Tso_x_eV\', \'Tso_y_eV\', \'Tso_z_eV\', \'A0_x_eV\', \'A0_y_eV\', \'A0_z_eV\', \'Aso_x_eV\', \'Aso_y_eV\', \'Aso_z_eV\', \'Atot_x_eV\', \'Atot_y_eV\', \'Atot_z_eV\', \'Axc_x_eV\', \'Axc_y_eV\', \'Axc_z_eV\'], fmt='{:>13s} ')\n",
                "table.set_data(data3, fmt='{: .6e} ')\n",
                'print(table)\n',
                'print(table, file=store_pos)\n',
                'print()\n',
                '\n'
        ]
        with open('parse_spinTorque/parse.py', 'w') as W_File:
            W_File.writelines(lines)

    def parsesh(self):
        os.system("cp ~/Example_Lab/nanodcal_input/2_nanodcal/2_Theta_T/parse.sh parse_spinTorque/.")

if __name__ == '__main__':

    if not(os.path.isdir('parse_spinTorque')):
        os.system("mkdir parse_spinTorque")

    pickle_path = []
    for theta in [0, 15, 30]:
        pickle_path.append(f'../../1_Theta_E/2_PdCo2_f/{theta:>003}_theta/analysis/spintorque/bulk_spin_torque.pickle\n')
        test = jp_analysis(pickle_path = pickle_path
                           )
        test.Writting_parseFile()
    test.Making_parsingFile()
    test.parsesh()

    os.chdir('parse_spinTorque')
    # os.system('./parse.sh SOC_zx_R.txt [:,0,:]')