#!/bin/sh
module load junpy/0.16
module load anaconda/2024.02-py311
python _TB_INPUTpy/_021_TB_Field_Rparse.py $@
python _TB_INPUTpy/_022_TB_Field_Organize.py $@
