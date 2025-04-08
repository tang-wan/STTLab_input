import numpy as np
import matplotlib.pyplot as plt
import scipy.io as scio

print()
print('====== Loading Charge.mat ......')
print()

degree = "000"

Charge_dataFile = '../../Theta_Energy/{}_theta/analysis/charge/Charge.mat'.format(degree)
atoms_datafile = "../../Theta_Energy/{}_theta/atoms.xyz".format(degree)
torque_datafile = "../../Theta_torque/Result_output_SumAll.txt"

#Charge_dataFile = 'Charge.mat'
#atoms_datafile = "atoms.xyz"
#torque_datafile = "Result_output_SumAll.txt"

data = scio.loadmat(Charge_dataFile)['data'][0][0]
#======================
uB_J = 9.274*1e-24
uB_eV = 5.788*1e-5
A_m = 1e10


#======================
# Total MagneticMomennt
'''
'totalCharge',
'Polarized_r',
'Polarized_theta',
'Polarized_phi',
'MagneticMoment',
'''
Polarized_theta = np.transpose(data[2])[0]
Polarized_phi = np.transpose(data[3])[0]
MagneticMoment = np.transpose(data[4])[0]
# print(Polarized_theta)
# print(MagneticMoment)

theta_0 = Polarized_theta[0]
phi_0 = Polarized_phi[0]
MagneticMoment_list = []
for i in range(len(Polarized_theta)):
    theta = Polarized_theta[i]
    phi = Polarized_phi[i]
    moment = MagneticMoment[i]
    # 以第一顆原子的 moment 方向訂為正
    if (np.pi*3/4 < np.abs(theta-theta_0) and np.pi*5/4 > np.abs(theta-theta_0)):
        MagneticMoment_list.append(-float(moment))

    elif (np.pi*3/4 < np.abs(phi-phi_0) and np.pi*5/4 > np.abs(phi-phi_0)):
        MagneticMoment_list.append(-float(moment))

    else:
        MagneticMoment_list.append(float(moment))

MagneticMoment_array = np.array(MagneticMoment_list)

#-----------------------------
print('====== Each MagneticMoment is (Unit is eV/T)======')
print(MagneticMoment_array)
print()

print('====== Each MagneticMoment is (Unit is uB)======')
print(MagneticMoment_array/uB_eV)
print()

print('====== Total MagneticMoment is (Unit is eV/T)======')
t_MagMoment_eV = np.sum(MagneticMoment_array)
print(t_MagMoment_eV)
print()

print('====== Total MagneticMoment is (Unit is uB)======')
t_MagMoment_uB = np.sum(MagneticMoment_array)/uB_eV
print(t_MagMoment_uB)
print()

print('====== Total MagneticMoment is (Unit is J/T)======')
t_MagMoment_J = t_MagMoment_uB*uB_J
print(t_MagMoment_J)
print()


#======================
# Volume
print('====== Loading atoms.xyz ......')

f = open(atoms_datafile, 'r')
datas = f.readlines()
z_list = []
for i in datas[2:]:
    if len(i) > 3:
        z_list.append(float(i.split()[3]))
# print(z_list)
f.close()
#--------------------------------------
print('====== Loading Lattice_Constant.txt ......')
height = np.max(z_list)-np.min(z_list)
vect = np.loadtxt("Lattice_Constant.txt")
a1, a2, a3 = vect[0:]
a3[2] = height
#--------------------------------------
Volume = np.abs(np.dot(np.cross(a1, a2), a3)) # Unit: Å^3
Volume = Volume/(A_m)**3 # Unit: m^3
print()
print('====== Volume is (Unit is m^3) ======')
print(Volume)
print()


#======================
# Torque

print('====== Result_output_SumAll.txt ......')
print()
f = open(torque_datafile, 'r')
datas = f.readlines()
'''
degree
__, __, 000, 022, 045, 066, 090, 112, 135, 157, 180
'''
'''
which parameter
Txc_x_eV, Txc_y_eV, Txc_z_eV
Tso_x_eV, Tso_y_eV, Tso_z_eV
A0_x_eV, A0_y_eV, A0_z_eV
Aso_x_eV, Aso_y_eV, Aso_z_eV
Atot_x_eV, Atot_y_eV, Atot_z_eV
Axc_x_eV, Axc_y_eV, Axc_z_eV
'''
# datas[degree].split()[which parameter]
Txc_45 = abs(float(datas[4].split()[1]))
f.close()

print('====== Torque at 45 degree is (Unit is eV) ======')
print(Txc_45)
print()

#======================
print("===========================================")
print()
print('====== Magnetization is (Unit is A/m)======')
print(t_MagMoment_J / Volume)
print()
print('====== Surface anisotropy is (Unit is T)======')
print(Txc_45 / t_MagMoment_eV)
print()

#======================
print('====== Writing output ......')
path = 'parameter_Result.txt'
f = open(path, 'w')

print('====== Each MagneticMoment is (Unit is uB)======', file=f)
print(MagneticMoment_array/uB_eV, file=f)
print(file=f)

print('====== Total MagneticMoment is (Unit is uB)======', file=f)
print(t_MagMoment_uB, file=f)
print(file=f)

print('====== Volume is (Unit is m^3)======', file=f)
print(Volume, file=f)
print(file=f)

print('====== Magnetization is (Unit is A/m)======', file=f)
print(t_MagMoment_J / Volume, file=f)
print(file=f)

print('====== Torque at 45 degree is (Unit is eV) ======', file=f)
print(Txc_45, file=f)
print(file=f)

print('====== Surface anisotropy is (Unit is T)======', file=f)
print(Txc_45 / t_MagMoment_eV, file=f)
print(file=f)

print('==== Output Finish ! ! ! ! ====')
print()
f.close()




