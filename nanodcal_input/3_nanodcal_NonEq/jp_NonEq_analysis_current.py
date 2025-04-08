import numpy as np # type: ignore
import os


class jp_analysis():
    def __init__(self, pickle_path):
        self.pickle_path = pickle_path

    def Writting_parseFile(self):
        with open("parse_current/Current_pickle.txt", 'w') as W_File:
            lines = self.pickle_path
            W_File.writelines(lines)

    def Making_parsingFile(self):
        lines = [
                "import sys\n",
                "import numpy as np     #type: ignore\n",
                "import junpy as jp     #type: ignore\n",
                "from junpy.util import SimpleTable     #type: ignore\n",
                '\n',
                "#======================================\n",
                "# read user inputs\n",
                '\n',
                "if len(sys.argv) == 1:\n",
                "   raise RuntimeError('Usage: FILENAME [SLICES]')\n",
                '\n',
                "files = sys.argv[1]\n",
                "if files.endswith('.pickle'):\n",
                "   files = [files]\n",
                "else:\n",
                "   files = np.loadtxt(files, dtype=str)\n",
                '\n',
                "#--------------------------------------\n",
                "# read data\n",
                '\n',
                "print('loading files...')\n",
                '\n',
                "data = []\n",
                "for i, filename in enumerate(files):\n",
                "   print('\t', i, filename)\n",
                "   calcr = jp.load(filename)\n",
                "   data.append(calcr.current())\n",
                "data = np.array(data)\n",
                '\n',
                "print(f'data.shape: {data.shape} # (#file, #site, #column)')\n",
                "print()\n",
                '\n',
                "#======================================\n",
                '# print results\n',
                '\n',
                'path = \'../Result_output_Current.txt\'\n',
                'store_pos = open(path, \'w\')\n',
                '\n',
                "header = ['I_tot[A]']\n",
                '\n',
                "table = jp.SimpleTable()\n",
                "table.set_header(header, fmt='{:>13s} ')\n",
                "table.set_data(data, fmt='{: .6e} ')\n",
                "print(table, '\\n')\n",
                'print(table, file=store_pos)\n',
        ]
        with open('parse_current/parse.py', 'w') as W_File:
            W_File.writelines(lines)


    def parsesh(self):
        os.system("cp ~/Example_Lab/nanodcal_input/3_nanodcal_NonEq/parse.sh parse_current/.")