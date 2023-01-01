from math import e
#weight
w41,w42,w43,w32,w31=0.2,-0.2,-0.4,-0.4,0.2
#thershold
theta3,theta4=0.8,0.3
n=0.1

def get_error(x1,x2,Yd):
    global w41
    global w32
    global w31
    global w42
    global w43
    global theta3
    global theta4
    #z3
    z3= x1*w31+x2*w32-theta3
    #a3
    a3=1/(1+e**-z3)
    #z4
    z4=x1*w41+x2*w42+a3*w43-theta4
    #a4
    a4=1/(1+e**-z4)
    #print(a4)
    error=Yd-a4
    print("error:",error )
    get_weight_change(error,x1,x2,a3,a4)
    
def get_weight_change(e,x1,x2,a3,a4):
    global w31
    global w32
    global w41
    global w42
    global w43
    global theta3
    global theta4
    delta4=-n*e*(1-a4)*a4
    delta3=(1-a3)*a3
    w43_change=-delta4*a3
    w41_change=-delta4*x1
    w42_change=-delta4*x2
    w31_change=-delta4*delta3*w43*x1
    w32_change=-delta4*delta3*w43*x2
    theta3_change=delta4*delta3*w43
    theta4_change=delta4
    w43+=w43_change
    w31+=w31_change
    w32+=w32_change
    w41+=w41_change
    w42+=w42_change
    theta3+=theta3_change
    theta4+=theta4_change
if __name__ == "__main__":
    x1=[-1,-1,1,1]
    x2=[-1,1,-1,1]
    Yd=[0,1,1,0]
    #correct=0
    #while(correct!=4):
       # correct=0
    for j in range (0,10000):
        for i in range(0,4):
            get_error(x1[i],x2[i],Yd[i])
    print("w31:",w31,"w32:",w32,"w42:",w42,"w41:",w41,"w43:",w43)
    print("theta3:",theta3,"theta4:",theta4)
       

