import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import skfuzzy.control as fuzz_ctrl
from mpl_toolkits.mplot3d import Axes3D

desired_temp=25
x_temp_range = np.arange(5,41,1,np.float32)
x_temp_difference_range=np.arange(0,20.5,0.5,np.float32)
x_humidity_range = np.arange(20,91,1,np.float32)
y_time_range=np.arange(0,10.5,0.5,np.float32)

##　variable and membership functions
x_temp_difference = fuzz_ctrl.Antecedent(x_temp_difference_range,"temp difference")
x_humidity= fuzz_ctrl.Antecedent(x_humidity_range,"humidity")
y_time = fuzz_ctrl.Consequent(y_time_range,"time")


x_temp_difference["small"] = fuzz.trapmf(x_temp_difference_range,[0,0,3.5,7.5])
x_temp_difference["med"] = fuzz.trimf(x_temp_difference_range,[4,9.5,15])
x_temp_difference["big"] = fuzz.trapmf(x_temp_difference_range,[10,15.5,20,20])
'''
x_temp_difference["warm"] = fuzz.trimf(x_temp_range,[68,86,104])
x_temp["hot"] = fuzz.trapmf(x_temp_range,[86,104,122,122])
'''
x_humidity["dry"] = fuzz.trapmf(x_humidity_range,[20,20,34,48])
x_humidity["good"] = fuzz.trapmf(x_humidity_range,[37,48,59,72])
x_humidity["wet"] = fuzz.trapmf(x_humidity_range,[62,76,90,90])

y_time["short"] = fuzz.trapmf(y_time_range,[0,0,1.5,3])
y_time["med"] = fuzz.trapmf(y_time_range,[2,3.5,5,6.5])
y_time["long"] = fuzz.trapmf(y_time_range,[5.5,7.5,10,10])
## 質心模糊
y_time.defuzzify_method = "centroid"
## 輸出規則 
rule_long=fuzz_ctrl.Rule(antecedent=((x_temp_difference["big"]&x_humidity["wet"])|(x_temp_difference["med"]&x_humidity["wet"])),consequent=y_time["long"],label="long")
rule_med=fuzz_ctrl.Rule(antecedent=((x_temp_difference["small"]&x_humidity["wet"])|(x_temp_difference["big"]&x_humidity["good"])|(x_temp_difference["big"]&x_humidity["dry"])),consequent = y_time["med"],label="medium")
rule_short=fuzz_ctrl.Rule(antecedent=((x_temp_difference["med"]&x_humidity["good"])|(x_temp_difference["small"]&x_humidity["good"])|(x_temp_difference["small"]&x_humidity["dry"])|(x_temp_difference["med"]&x_humidity["dry"])),consequent=y_time["short"],label="short")

system=fuzz_ctrl.ControlSystem(rules=[rule_long,rule_med,rule_short])
sys_sim=fuzz_ctrl.ControlSystemSimulation(system)

# Visualize these universes and membership functions
fig,(figure1,figure2,figure3)=plt.subplots(nrows=3,figsize=(8,9))
figure1.plot(x_temp_difference_range,fuzz.trapmf(x_temp_difference_range,[0,0,3.5,7.5]),'b',linewidth=1.5,label='small')
figure1.plot(x_temp_difference_range,fuzz.trimf(x_temp_difference_range,[4,9.5,15]),'g',linewidth=1.5,label='medium')
figure1.plot(x_temp_difference_range,fuzz.trapmf(x_temp_difference_range,[10,15.5,20,20]),'r',linewidth=1.5,label='big')
figure1.legend()

figure2.plot(x_humidity_range,fuzz.trapmf(x_humidity_range,[20,20,34,48]),'b',linewidth=1.5,label='dry')
figure2.plot(x_humidity_range,fuzz.trapmf(x_humidity_range,[37,48,59,72]),'g',linewidth=1.5,label='good')
figure2.plot(x_humidity_range,fuzz.trapmf(x_humidity_range,[62,76,90,90]),'r',linewidth=1.5,label='wet')
figure2.set_title('humidity')
figure2.legend()

figure3.plot(y_time_range,fuzz.trapmf(y_time_range,[0,0,1.5,3]),'b',linewidth=1.5,label='short')
figure3.plot(y_time_range,fuzz.trapmf(y_time_range,[2,3.5,5,6.5]),'g',linewidth=1.5,label='medium')
figure3.plot(y_time_range,fuzz.trapmf(y_time_range,[5.5,7.5,10,10]),'r',linewidth=1.5,label='long')
figure3.set_title('running time')
figure3.legend()

# plot 2d figures
for fi in (figure1,figure2,figure3):
  fi.spines['top'].set_visible(False)
  fi.spines['right'].set_visible(False)
  fi.get_xaxis().tick_bottom()
  fi.get_yaxis().tick_left()

plt.tight_layout()

from mpl_toolkits.mplot3d import Axes3D# Required for 3D plotting
def funz(x,y):
  sys_sim.input["temp difference"] = y
  sys_sim.input["humidity"] = x 
  sys_sim.compute()
  z=sys_sim.output["time"]
  return z

fig1=plt.figure()#建立一個繪圖物件
ax=Axes3D(fig1)#用這個繪圖物件建立一個Axes物件(有3D座標)

X,Y=np.meshgrid(x_humidity_range,x_temp_difference_range)
Z=funz(X,Y)
ax.plot_surface(X, Y, Z, rstride=1,cstride=1,cmap=plt.cm.coolwarm)#用取樣點(x,y,z)去構建曲面
ax.set_xlabel('humidity',color='r')
ax.set_ylabel('temp difference',color='g')
ax.set_zlabel('running time',color='b')#給三個座標軸註明

plt.show()#顯示模組中的所有繪圖物件
