import sys
import numpy as np
import junpy as jp

#==============================================================================
# load data

calcr = jp.load('bias_batch_runner.pickle')

biases = calcr.biases
Iup, Idn = calcr.get_by_attribute('current', kwargs={'spin': 'diag'}).T

#--------------------------------------
# print results

header = ['Bias_V', 'I_tot_A', 'I_up_A', 'I_dn_A', 'I_s_A', 'I_sp_%']
data = np.c_[biases, Iup+Idn, Iup, Idn, Iup-Idn, (Iup-Idn)/(Iup+Idn)*100]
table = jp.SimpleTable(data, header, datafmt='{: .6e} ', headerfmt='{:>13s} ')
print(table)
print()

