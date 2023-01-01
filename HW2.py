import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt
import skfuzzy.control as fuzz_ctrl
from mpl_toolkits.mplot3d import Axes3D

# Range

## range of temp. & soil & watering 
x_temp_range = np.arange(0,51,1,np.float32)
x_soil_range = np.arange(0,101,1,np.float32)
y_time_range=np.arange(0,31,1,np.float32)
##　variable and membership functions
x_temp = fuzz_ctrl.Antecedent(x_temp_range,"temp")
x_soil= fuzz_ctrl.Antecedent(x_soil_range,"soil")
y_time = fuzz_ctrl.Consequent(y_time_range,"time")

x_temp["cold"] = fuzz.trapmf(x_temp_range,[0,0,12,20])
x_temp["cool"] = fuzz.trimf(x_temp_range,[15,21,27])
x_temp["normal"] = fuzz.trimf(x_temp_range,[23,30,36])
x_temp["warm"] = fuzz.trimf(x_temp_range,[31,39,47])
x_temp["hot"] = fuzz.trapmf(x_temp_range,[39,45,50,50])

x_soil["dry"] = fuzz.trapmf(x_soil_range,[0,0,16.5,49.5])
x_soil["moist"] = fuzz.trapmf(x_soil_range,[28.5,52.5,65.5,88.6])
x_soil["wet"] = fuzz.trapmf(x_soil_range,[65.5,88.6,100,100])

y_time["short"] = fuzz.trapmf(y_time_range,[0,0,6,10])
y_time["medium"] = fuzz.trapmf(y_time_range,[6,11,21,26])
y_time["long"] = fuzz.trapmf(y_time_range,[22,25,30,30])
## 質心模糊
y_time.defuzzify_method = "centroid"
## 輸出規則 
rule_long=fuzz_ctrl.Rule(antecedent=((x_temp["hot"]&x_soil["dry"])|(x_temp["warm"]&x_soil["dry"]|x_temp["normal"]&x_soil["dry"])),consequent=y_time["long"],label="long")

rule_med=fuzz_ctrl.Rule(antecedent=((x_temp["cool"]&x_soil["dry"])|(x_temp["hot"]&x_soil["moist"])|(x_temp["warm"]&x_soil["moist"])|
(x_temp["normal"]&x_soil["moist"])),consequent = y_time["medium"],label="medium")
rule_short=fuzz_ctrl.Rule(antecedent=((x_temp["cool"]&x_soil["moist"])|(x_temp["cold"]&x_soil["moist"])|(x_temp["hot"]&x_soil["wet"])|(x_temp["warm"]&x_soil["wet"])|(x_temp["normal"]&x_soil["wet"])|(x_temp["cool"]&x_soil["wet"])|(x_temp["cold"]&x_soil["wet"])|(x_temp['cold']&x_soil['dry'])),consequent=y_time["short"],label="short")
system=fuzz_ctrl.ControlSystem(rules=[rule_long,rule_med,rule_short])
sys_sim=fuzz_ctrl.ControlSystemSimulation(system)
# Visualize these universes and membership functions
fig,(figure1,figure2,figure3)=plt.subplots(nrows=3,figsize=(8,9))
figure1.plot(x_temp_range,fuzz.trapmf(x_temp_range,[0,0,12,20]),'b',linewidth=1.5,label='cold')
figure1.plot(x_temp_range,fuzz.trimf(x_temp_range,[15,21,27]),'g',linewidth=1.5,label='cool')
figure1.plot(x_temp_range,fuzz.trimf(x_temp_range,[23,30,36]),'r',linewidth=1.5,label='normal')
figure1.plot(x_temp_range,fuzz.trimf(x_temp_range,[31,39,47]),'y',linewidth=1.5,label='warm')
figure1.plot(x_temp_range,fuzz.trapmf(x_temp_range,[39,45,50,50]),'k',linewidth=1.5,label='hot')
figure1.set_title('air temperature')
figure1.legend()

figure2.plot(x_soil_range,fuzz.trapmf(x_soil_range,[0,0,16.5,49.5]),'b',linewidth=1.5,label='dry')
figure2.plot(x_soil_range,fuzz.trapmf(x_soil_range,[16.5,40.5,62.5,88.6]),'g',linewidth=1.5,label='moist')
figure2.plot(x_soil_range,fuzz.trapmf(x_soil_range,[65.5,88.6,100,100]),'r',linewidth=1.5,label='wet')
figure2.set_title('soil moisture')
figure2.legend()

figure3.plot(y_time_range,fuzz.trapmf(y_time_range,[0,0,6,10]),'b',linewidth=1.5,label='short')
figure3.plot(y_time_range,fuzz.trapmf(y_time_range,[6,11,21,26]),'g',linewidth=1.5,label='medium')
figure3.plot(y_time_range,fuzz.trapmf(y_time_range,[22,25,30,30]),'r',linewidth=1.5,label='long')
figure3.set_title('watering duration')
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
  sys_sim.input["temp"] = y
  sys_sim.input["soil"] = x 
  sys_sim.compute()
  z=sys_sim.output["time"]
  return z

fig1=plt.figure()#建立一個繪圖物件
ax=Axes3D(fig1)#用這個繪圖物件建立一個Axes物件(有3D座標)

X,Y=np.meshgrid(x_soil_range,x_temp_range)
Z=funz(X,Y)
ax.plot_surface(X, Y, Z, rstride=1,cstride=1,cmap=plt.cm.coolwarm)#用取樣點(x,y,z)去構建曲面
ax.set_xlabel('soil',color='r')
ax.set_ylabel('air temperature',color='g')
ax.set_zlabel('watering',color='b')#給三個座標軸註明
plt.show()#顯示模組中的所有繪圖物件