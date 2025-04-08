import os
import numpy as np # type: ignore

# ========================================================
if os.path.isfile('MAE_OUTPUT.txt'):
    os.system('rm MAE_OUTPUT.txt')
else:
    pass

if os.path.isfile('MAE_Energy.txt'):
    os.system('rm MAE_Energy.txt')
else:
    pass
# ======================
class parseMAE():
    def __init__(self, theta_list, atom_type):
        self.theta_list = theta_list
        self.atom_aype  = atom_type
    
    def parsingCAR(self, num):
        self.num = num
        for theta in self.theta_list:
            os.system(f'echo {theta} >> MAE_OUTPUT.txt')
            os.system(f"grep -{6+num} magnetization\ \(x\) {theta:.1f}_theta_{self.atom_aype}_f/OUTCAR | tail -{6+num+2} >> MAE_OUTPUT.txt")
            os.system(f"grep -{6+num} magnetization\ \(z\) {theta:.1f}_theta_{self.atom_aype}_f/OUTCAR | tail -{6+num+2} >> MAE_OUTPUT.txt")

            os.system(f"grep F {theta:.1f}_theta_{self.atom_aype}_f/OSZICAR >> MAE_Energy.txt")        

    def parsingTHETA(self, set_num=0):
        num = self.num
        if set_num == 0:
            set_num = 19+2*(num-1)
        else:
            set_num = set_num

        with open("MAE_OUTPUT.txt", 'r') as R_File:
            data = R_File.readlines()

        theta_list = []
        Mx_tot = []
        Mz_tot = []
        
        print(data[set_num])
        print(data[6])
        for i in range(int(len(data)/(set_num))):
            theta = float(data[i*(set_num)])
            theta_list.append(theta)
            for n in range(num):
                print(data[i*(set_num)+6+n-1].split())
                mx_tot = np.float64(data[i*(set_num)+6+n-1].split())[-1]
                mz_tot = np.float64(data[i*(set_num)+6+num+8+n].split())[-1]
                Mx_tot.append(mx_tot)
                Mz_tot.append(mz_tot)
        Mx_tot = np.array(Mx_tot)
        Mz_tot = np.array(Mz_tot)
        theta_array = np.array(theta_list)

        print("## initial theta")
        print("## scfed theta")
        print("## total moment")
        print("# ==========")

        new_theta = []
        for n in range(len(theta_array)):
            
            Mx_tot_n = Mx_tot[num*(n):num*(n+1)]
            Mz_tot_n = Mz_tot[num*(n):num*(n+1)]
                        
            print(theta_array[n])
            
            if (len(np.where(Mz_tot_n==0))==0):
                _theta_ = np.arctan(Mx_tot_n/Mz_tot_n)*180/np.pi
            else:
                Mz_tot_n[Mz_tot_n==0] = 1e-12
                _theta_ = np.arctan(Mx_tot_n/Mz_tot_n)*180/np.pi
            
            if np.mean(Mx_tot_n) >= 0 and np.mean(Mz_tot_n) >= 0:    
                new_theta.append( np.mean(_theta_) )
                print(_theta_)

            elif np.mean(Mx_tot_n) < 0 and np.mean(Mz_tot_n) > 0:
                new_theta.append(abs(np.mean(_theta_)))
                print(np.abs(_theta_))

            elif np.mean(Mx_tot_n) >= 0 and np.mean(Mz_tot_n) < 0:
                new_theta.append(180 + np.mean(_theta_))
                print(180 + _theta_)

            elif np.mean(Mx_tot_n) < 0 and np.mean(Mz_tot_n) <= 0:
                new_theta.append( 180 - np.mean(_theta_) )
                print(180 - _theta_)
            
            print(np.sqrt(Mx_tot_n**2+Mz_tot_n**2))
            print('# ==========')
        
        self.theta_array = theta_array
        self.Mx_tot      = Mx_tot
        self.Mz_tot      = Mz_tot
        self.new_theta   = new_theta

    def parsingENERGY(self):
        with open("MAE_Energy.txt", 'r') as R_File:
            data = R_File.readlines()
        Energy_list = []
        for i in data:
            Energy = float(i.split()[4])
            Energy_list.append(Energy)
        Energy_array = np.array(Energy_list)
        new_Energy_array = (Energy_array-np.min(Energy_array))*1000 # meV

        print('# ==========')
        print("Total Energy (eV): ")
        print(f"{Energy_array}")
        print()
        print("Shifting Energy (meV): ")
        print(f"{new_Energy_array}")
        print('# ==========')

        self.Energy_array     = Energy_array     # eV, woShift
        self.new_Energy_array = new_Energy_array # meV, wShift
    
    def WritingFile(self):
        num = self.num

        theta_array = self.theta_array
        new_theta   = self.new_theta
        Mx_tot      = self.Mx_tot
        Mz_tot      = self.Mz_tot

        Energy_array     = self.Energy_array
        new_Energy_array = self.new_Energy_array

        with open("AM_afterscf.txt", 'w') as W_File:
            W_File.write("## initial theta\n")
            W_File.write("## scfed theta\n")
            W_File.write("## total moment\n")
            W_File.write("# ==========\n")
        
        for n in range(len(theta_array)):
    
            Mx_tot_n = Mx_tot[num*(n):num*(n+1)]
            Mz_tot_n = Mz_tot[num*(n):num*(n+1)]
            
            with open("AM_afterscf.txt", 'a') as A_File:
                A_File.write(f"{theta_array[n]}\n")

                if np.mean(Mx_tot_n) >= 0 and np.mean(Mz_tot_n) > 0:
                    A_File.write(f"{np.arctan(Mx_tot_n/Mz_tot_n)*180/np.pi}\n")
                elif np.mean(Mx_tot_n) < 0 and np.mean(Mz_tot_n) > 0:
                    A_File.write(f"{np.abs(np.arctan(Mx_tot_n/Mz_tot_n)*180/np.pi)}\n")
                elif np.mean(Mx_tot_n) >= 0 and np.mean(Mz_tot_n) < 0:
                    A_File.write(f"{180+(np.arctan(Mx_tot_n/Mz_tot_n)*180/np.pi)}\n")
                elif np.mean(Mx_tot_n) < 0 and np.mean(Mz_tot_n) < 0:
                    A_File.write(f"{180-(np.arctan(Mx_tot_n/Mz_tot_n)*180/np.pi)}\n")
                
                A_File.write(f"{np.sqrt(Mx_tot_n**2+Mz_tot_n**2)}\n")
                A_File.write("# ==========\n")

        np.savetxt("New_theta_E.txt", np.c_[new_theta, Energy_array, new_Energy_array])
        with open("New_theta_E.txt", 'a') as A_File:
            A_File.seek(0)
            A_File.write("# theta       Raw_Energy (eV)      Shift_Rnergy (meV)")
# ======================
if __name__ == '__main__':
    Pd6 = parseMAE(theta_list=[0, 10, 20, 30, 40, 45, 50, 60, 70, 80, 90],
                   atom_type='Pd6'
                   )
    Pd6.parsingCAR()
    Pd6.parsingTHETA(num=6)
    Pd6.parsingENERGY()
    Pd6.WritingFile()
