
import random as r
import torch
import matplotlib.pyplot as plt
import torch.nn.functional as F
epoch=10
batchsize=100
Input=2
Output=1
test_loss=[]
X=[]
Y=[]
Z=[]
x_test=[]
y_test=[]
z_test=[]
# train data,test data
def data(num,list1,list2,list3):
    for i in range(num):
        x=r.uniform(-5,5)
        y=r.uniform(-5,5)
        list1.append(x)
        list2.append(y)
        z=(4-2.1*x**2+(x**4)/3)*x**2+x*y+(-4+4*y**2)*y**2
        list3.append(z)
#build module
class NN(torch.nn.Module):
    def __init__(self,Input,Output):
        super(NN,self).__init__()
        self.fc1=torch.nn.Linear(Input,400)
        self.fc2=torch.nn.Linear(400,400)
        self.fc3=torch.nn.Linear(400,400)
        self.fc4=torch.nn.Linear(400,400)
        self.final=torch.nn.Linear(400,Output)
        self.float()
    
    def forward(self, x):
        x=self.fc1(x)
        x=F.relu(self.fc2(x))
        x=F.relu(self.fc3(x))
        x=F.relu(self.fc4(x))
        x=self.final(x)
        return x
#create a module
net=NN(Input=Input,Output=Output)
loss_fn=torch.nn.MSELoss()
#print("initial weight:",net[0].weight,net[2].weight)
optimizer=torch.optim.Adam(net.parameters(),lr=1e-3)
data(batchsize,X,Y,Z)
data(epoch,x_test,y_test,z_test)
train_loss=[]
for i in range (epoch):
    loss_averagre=0
    for j in range(int(batchsize)):
            input=torch.Tensor([[X[j],Y[j]]])
            output=torch.Tensor([[Z[j]]])
            #get loss funtion
            z_predict=net(input)
            loss=loss_fn(z_predict,output.float())
            loss_averagre+=loss.item()
            # renew weight
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    loss_averagre=loss_averagre/batchsize
    train_loss.append(loss_averagre)            
    print(i+1)
    with torch.no_grad():
            input=torch.Tensor([[x_test[i],y_test[i]]])
            output=torch.Tensor([[z_test[i]]])
            z_pre=net(input)
            loss=(output-z_pre).item()
            test_loss.append(loss/batchsize)       
print(test_loss)

plt.figure(1)
plt.title('train loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.plot(train_loss,'r')
plt.figure(2)
plt.boxplot([train_loss,test_loss]) #
plt.set
plt.show()



    