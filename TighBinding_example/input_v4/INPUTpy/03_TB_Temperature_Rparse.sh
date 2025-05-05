#!/bin/sh
module load junpy/0.16
module load anaconda/2024.02-py311
python _TB_INPUTpy/_031_TB_Temp_Rparse.py $@
python _TB_INPUTpy/_032_TB_Temp_Organize.py $@
