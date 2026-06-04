import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pylab import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from openpyxl import Workbook
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon

# Increase overall quality
plt.rcParams.update({
    "font.size": 5,
    "axes.labelsize": 5,
    "axes.titlesize": 6,
    "legend.fontsize": 5,
    "figure.dpi": 200,            # High resolution
    "savefig.dpi": 200,
})


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=15, height=10, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class SecondWindow(QWidget):
    def __init__(self,x,y1,y2):
        super().__init__()
        #self.setStyleSheet("background-color: #336699; color: blue;")
        self.setWindowIcon(QIcon('Screenshot 2023-11-15 145854.png'))
        self.setWindowTitle('Ballast Mechanical Behavior')
        self.setFixedSize(950,900)


        mainLayout = QVBoxLayout()
        
        
        self.fig = Figure()
        
        self.canvas= FigureCanvas (self.fig)
        toolbar = NavigationToolbar(self.canvas,self)
        
        mainLayout.addWidget(toolbar)
        mainLayout.addWidget(self.canvas)
        
        
        self.axes= self.fig.add_subplot (211)
        self.axes.grid(linestyle='--')
        self.axes.figsize=(7,7)
        self.fig.tight_layout(pad=7.0)
        self.line = self.axes.plot (x , y1,'k')
        self.axes.set_title('Stress - Strain curve')
        self.axes.set_ylabel('Stress Deviator (kPa)')
        self.axes.set_xlabel('Axial strain(%)')
        #self.axes.set_ylim([0,800])
        self.axes.set_xlim([0,22.5])
        self.axes= self.fig.add_subplot (212)
        self.axes.grid(linestyle='--')
        self.line = self.axes.plot (x , y2,'k')
        self.axes.set_title('Volumetric deformation - Strain curve')
        self.axes.set_ylabel('Volumetric Deformation (%)')
        self.axes.set_xlabel('Axial strain (%)')
        #self.axes.set_ylim([-6,6])
        self.axes.set_xlim([0,22.5])
        self.axes.invert_yaxis() 
        self.setLayout(mainLayout)
        
       
    def displayInfo(self):
        print('ok_s3')
        self.show()
class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)        

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #self.setStyleSheet("background-color: #FFFFFF; color: black;")
        self.setWindowTitle("RNN Model for Ballast Mechanical Behavior")
        self.setWindowIcon(QIcon('Screenshot 2023-11-15 145854.png'))
        self.setFixedSize(600,350)
       

        self.layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(0)
        label_1 = QLabel("                                   ")
        grid.addWidget(label_1,1,0,Qt.AlignCenter)
        grid.addWidget(QHLine(), 1,0,1,2)
        
        D50 = QLabel("Enter particle's diameter (mm): ")
        Cu = QLabel('Enter the coefficient of uniformity: ')
        Cc = QLabel('Enter the coefficient of curvature: ')
        e = QLabel('Enter the void ratio: ')
        gamma = QLabel('Enter the unit weight of soil (kN/m3): ')
        sigma3 = QLabel('Enter the confining pressure (kPa):')

        self.D50_edit = QLineEdit()
        self.Cu_edit = QLineEdit()
        self.Cc_edit = QLineEdit()
        self.e_edit = QLineEdit()
        self.gamma_edit = QLineEdit()
        self.sigma3_edit = QLineEdit()
        print(self.D50_edit.text())
        grid.setSpacing(5)
        grid.addWidget (D50, 2, 0)
        grid.addWidget (self.D50_edit , 2, 1)
        grid.addWidget (Cu, 3, 0)
        grid.addWidget (self.Cu_edit , 3, 1)
        grid.addWidget (Cc, 4, 0)
        grid.addWidget (self.Cc_edit , 4, 1)
        grid.addWidget (e, 5, 0)
        grid.addWidget (self.e_edit , 5, 1)
        grid.addWidget (gamma, 6, 0)
        grid.addWidget (self.gamma_edit , 6, 1)
        grid.addWidget (sigma3, 7, 0)
        grid.addWidget (self.sigma3_edit , 7, 1)
        grid.addWidget(QHLine(), 5,0,5,2)
        grid.addWidget(self.run(),8,1,Qt.AlignRight)
        
        
        label_2 = QLabel("\u00A9 Mohamed SHAHIN and Rodaina ABOUL HOSN")
        grid.addWidget(label_2,9,0,Qt.AlignLeft)
        self.layout.addLayout(grid)
        print('Done')
        self.setLayout(self.layout)



    
    def run(self):
        self.layout.stretch(2)
        self.button = QPushButton('Run', self)
        self.button.setGeometry(470,280,100,40)
        self.button.resize(100,40)
        self.button.setStyleSheet("background-color : lightblue")
        self.button.clicked.connect(self.on_click)
       
    def on_click(self):
        self.Str = [0.0]
        self.Qi=[0.0]
        self.ev=[0.0]
        self.inp = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] 
        self.feature2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        self.feature4 = [0.0,0.0]
        self.Delta_Ei = 0.2
        self.outp = [0.0,0.0]
        self.nincr = 19
        self.Ei=0.1  
        self.inp[0]= float(self.D50_edit.text())
        self.inp[1]= float(self.Cu_edit.text())
        self.inp[2]= float(self.Cc_edit.text())
        self.inp[3]= float(self.e_edit.text())
        self.inp[4]= float(self.gamma_edit.text())
        self.inp[5]= float(self.sigma3_edit.text())
        print('Done')
        
        if float(self.inp[0])<17.4:
            self.inp[0]=17.4
        elif float(self.inp[0])>38.9:
            self.inp[0]=38.9

        self.inp[0]=(self.inp[0]-17.4)/21.5
        print("inp0",self.inp[0])
        if float(self.inp[1])<1.5:
            self.inp[1]=1.5
        elif float(self.inp[1])>2.93:
            self.inp[1]=2.93

        self.inp[1]=(self.inp[1]-1.5)/1.43
        print("inp1",self.inp[1])
        if float(self.inp[2])<0.84:
            self.inp[2]=0.84
        elif float(self.inp[2])>1.0:
            self.inp[2]=1.0

        self.inp[2]=(self.inp[2]-0.84)/0.16
        print("inp2",self.inp[2])
        if float(self.inp[3])<0.64:
            self.inp[3]=0.64
        elif float(self.inp[3])>0.835:
            self.inp[3]=0.835

        self.inp[3]=(self.inp[3]-0.64)/0.195
        print("inp3",self.inp[3])
        if float(self.inp[4])<14.7:
            self.inp[4]=14.7
        elif float(self.inp[4])>17.0:
            self.inp[4]=17.0

        self.inp[4]=(self.inp[4]-14.7)/2.3
        print("inp4",self.inp[4])

        if float(self.inp[5])<15.0:
            self.inp[5]=15.0
        elif float(self.inp[5])>310.3:
            self.inp[5]=310.3

        self.inp[5]=(self.inp[5]-15.0)/295.3
        print("inp5",self.inp[5])
        
        for i in range(0,self.nincr):
            print('New iteration')
            self.inp[6]=self.Ei
            self.inp[7]=self.Delta_Ei
            
            if float(self.inp[6])<0.1:
                self.inp[6]=0.1
            elif float(self.inp[6])>19.0:
                self.inp[6]=19.0
            print("Ei",self.Ei)
            
            self.inp[6]=(self.inp[6]-0.1)/18.9
            print("inp6",self.inp[6])
            if float(self.inp[7])<0.2:
                self.inp[7]=0.2
            elif float(self.inp[7])>2.0:
                self.inp[7]=2.0

            self.inp[7]=(self.inp[7]-0.2)/1.8
            print("inp7",self.inp[7])
            
            netsum=0.4322068
            netsum = netsum + self.inp[0]*(5.601646E-02)
            netsum = netsum + self.inp[1]*(1.050061)
            netsum = netsum + self.inp[2]*0.1750519
            netsum = netsum + self.inp[3]*(-0.8122872)
            netsum = netsum + self.inp[4]*(-1.177922)
            netsum = netsum + self.inp[5]*(-1.281783)
            netsum = netsum + self.inp[6]*(0.4490109)
            netsum = netsum + self.inp[7]*1.485617
            netsum = netsum + 0.9245018
            netsum = netsum + self.feature4[0] * (-1.141728E-03)
            netsum = netsum + self.feature4[1] * (3.975101E-02)
            self.feature2[0]=math.tanh(netsum)
            print('f1',self.feature2[0])
            print("net",netsum)
            netsum = 1.398888
            netsum = netsum + self.inp[0] * 0.4030881
            netsum = netsum + self.inp[1] * (-1.145678)
            netsum = netsum + self.inp[2] * 1.7514
            netsum = netsum + self.inp[3] * (-4.851397E-02)
            netsum = netsum + self.inp[4] * 0.600504
            netsum = netsum + self.inp[5] * (-1.25401)
            netsum = netsum + self.inp[6] * 0.1212502
            netsum = netsum + self.inp[7] * (-1.370505)
            netsum = netsum + 1.409978
            netsum = netsum + self.feature4[0] * (-0.8171972)
            netsum = netsum + self.feature4[1] * (-0.2031538)
            self.feature2[1]= math.tanh(netsum)
            
            netsum = -0.5928574
            netsum = netsum + self.inp[0] * (-0.3640539)
            netsum = netsum + self.inp[1] * (-0.1992462)
            netsum = netsum + self.inp[2] * (-0.5953705)
            netsum = netsum + self.inp[3] * 0.9727836
            netsum = netsum + self.inp[4] * 0.5522084
            netsum = netsum + self.inp[5] * 0.4467421
            netsum = netsum + self.inp[6] * 0.190355
            netsum = netsum + self.inp[7] * 1.531258
            netsum = netsum + (-0.59403)
            netsum = netsum + self.feature4[0] * (-0.3724768)
            netsum = netsum + self.feature4[1] * 0.5388053
            self.feature2[2] = math.tanh(netsum)
            
            netsum = 0.1444716
            netsum = netsum + self.inp[0] * 0.3665255
            netsum = netsum + self.inp[1] * 0.3444198
            netsum = netsum + self.inp[2] * (-0.3420203)
            netsum = netsum + self.inp[3] * 0.2631427
            netsum = netsum + self.inp[4] * 0.5113632
            netsum = netsum + self.inp[5] * (-8.797734E-02)
            netsum = netsum + self.inp[6] * (-0.6501069)
            netsum = netsum + self.inp[7] * (-0.8124169)
            netsum = netsum + (-0.2340354)
            netsum = netsum + self.feature4[0] * 0.7072874
            netsum = netsum + self.feature4[1] * (-0.2255989)
            self.feature2[3] = math.tanh(netsum)
             
                     
            netsum = 0.5202681
            netsum = netsum + self.inp[0] * 0.1600636
            netsum = netsum + self.inp[1] * 0.243405
            netsum = netsum + self.inp[2] * (-0.5737442)
            netsum = netsum + self.inp[3] * 0.4030233
            netsum = netsum + self.inp[4] * (-0.2666483)
            netsum = netsum + self.inp[5] * (-1.497535)
            netsum = netsum + self.inp[6] * 1.621032
            netsum = netsum + self.inp[7] * (-0.8956463)
            netsum = netsum + 0.6595912
            netsum = netsum + self.feature4[0] * 8.659312E-02
            netsum = netsum + self.feature4[1] * (-0.0738372)
            self.feature2[4] = math.tanh(netsum)
           
            netsum = 1.042258
            netsum = netsum + self.inp[0] * 0.4779588
            netsum = netsum + self.inp[1] * 1.185758
            netsum = netsum + self.inp[2] * 9.611069E-02
            netsum = netsum + self.inp[3] * (-0.1345853)
            netsum = netsum + self.inp[4] * (-1.261218)
            netsum = netsum + self.inp[5] * 2.678253
            netsum = netsum + self.inp[6] * 0.8559374
            netsum = netsum + self.inp[7] * (-2.43513)
            netsum = netsum + 1.03949
            netsum = netsum + self.feature4[0] * (-7.752682E-02)
            netsum = netsum + self.feature4[1] * 0.6434758
            self.feature2[5] = math.tanh(netsum)
            
            netsum = 0.2147741
            netsum = netsum + self.inp[0] * (-1.746428)
            netsum = netsum + self.inp[1] * (-1.621715E-02)
            netsum = netsum + self.inp[2] * (-0.5050035)
            netsum = netsum + self.inp[3] * (-0.2943828)
            netsum = netsum + self.inp[4] * 0.1160996
            netsum = netsum + self.inp[5] * 1.312003
            netsum = netsum + self.inp[6] * 0.5568389
            netsum = netsum + self.inp[7] * (-0.6059821)
            netsum = netsum + 9.793694E-02
            netsum = netsum + self.feature4[0] * 0.1731099
            netsum = netsum + self.feature4[1] * 0.1616357
            self.feature2[6] = math.tanh(netsum)
            
            netsum = -0.6616849
            netsum = netsum + self.inp[0] * 5.509186E-02
            netsum = netsum + self.inp[1] * 0.8722677
            netsum = netsum + self.inp[2] * (-0.6158577)
            netsum = netsum + self.inp[3] * 0.8295627
            netsum = netsum + self.inp[4] * (-0.2739595)
            netsum = netsum + self.inp[5] * (-2.699235)
            netsum = netsum + self.inp[6] * 0.384888
            netsum = netsum + self.inp[7] * 1.136404
            netsum = netsum + (-0.8969032)
            netsum = netsum + self.feature4[0] * 0.568903
            netsum = netsum + self.feature4[1] * 5.099271E-02
            self.feature2[7] = math.tanh(netsum)
            
            netsum = -0.2869954
            netsum = netsum + self.inp[0] * (-0.2505337)
            netsum = netsum + self.inp[1] * (-6.212543E-02)
            netsum = netsum + self.inp[2] * (-0.9941342)
            netsum = netsum + self.inp[3] * 0.7242925
            netsum = netsum + self.inp[4] * (-0.4818746)
            netsum = netsum + self.inp[5] * 0.0344972
            netsum = netsum + self.inp[6] * (-0.1126954)
            netsum = netsum + self.inp[7] * 0.8301603
            netsum = netsum + ( -0.3414904)
            netsum = netsum + self.feature4[0] * 2.318101E-02
            netsum = netsum + self.feature4[1] * (-0.4897337)
            self.feature2[8] = math.tanh(netsum)
            
            netsum = 0.4857446
            netsum = netsum + self.inp[0] * (-0.5971019)
            netsum = netsum + self.inp[1] * 0.474021
            netsum = netsum + self.inp[2] * 0.5300007
            netsum = netsum + self.inp[3] * (-1.086891)
            netsum = netsum + self.inp[4] * (-1.107612)
            netsum = netsum + self.inp[5] * 0.1851085
            netsum = netsum + self.inp[6] * (-0.2056437)
            netsum = netsum + self.inp[7] * (-0.4852493)
            netsum = netsum + 0.2811413
            netsum = netsum + self.feature4[0] * (-4.750614E-02)
            netsum = netsum + self.feature4[1] * (-5.554906E-02)
            self.feature2[9] = math.tanh(netsum)
            
             
            netsum = -0.5142042
            netsum = netsum + self.feature2[0] * 1.786009
            netsum = netsum + self.feature2[1] * (-1.439854)
            netsum = netsum + self.feature2[2] * 0.980323
            netsum = netsum + self.feature2[3] * (-3.670824E-03)
            netsum = netsum + self.feature2[4] * (-2.066014)
            netsum = netsum + self.feature2[5] * 2.347498E-02
            netsum = netsum + self.feature2[6] * (-0.4720106)
            netsum = netsum + self.feature2[7] * (-1.267853)
            netsum = netsum + self.feature2[8] * 0.63671
            netsum = netsum + self.feature2[9] * (-0.6820487)
            self.outp[0] = 1.0 / (1.0 + math.exp(-netsum))

            netsum = 4.520982E-02
            netsum = netsum + self.feature2[0] * 0.4744908
            netsum = netsum + self.feature2[1] * (-1.890552)
            netsum = netsum + self.feature2[2] * 0.7917076
            netsum = netsum + self.feature2[3] * 0.7901414
            netsum = netsum + self.feature2[4] * (-0.7322906)
            netsum = netsum + self.feature2[5] * 2.547449
            netsum = netsum + self.feature2[6] * (-1.116966)
            netsum = netsum + self.feature2[7] * (-1.09265)
            netsum = netsum + self.feature2[8] * 1.136998
            netsum = netsum + self.feature2[9] * (0.87844)
            self.outp[1] = 1.0 / (1.0 + math.exp(-netsum))
            
            self.feature4[0] = self.feature4[0] + self.feature4[0] * -0.9
            self.feature4[0] = self.feature4[0] + self.outp[0] * 0.9
            self.feature4[1] = self.feature4[1] + self.feature4[1] * -0.9
            self.feature4[1] = self.feature4[1] + self.outp[1] * 0.9
            print("f1",self.feature4[0])
            print("f2",self.feature4[1])
            self.outp[0] = 1449.45 *  (self.outp[0] - 0.1) / 0.8  + 44.01553
            if (self.outp[0]<44.01553):
                self.outp[0] = 44.01553
            elif (self.outp[0]>1493.466):
                self.outp[0] = 1493.466
            
            
            
            self.outp[1] = 16.00923 *  (self.outp[1] - 0.1) / 0.8  + (-11.26868)
            
            if self.outp[1]<(-11.26868):
                self.outp[1] = -11.26868
            elif self.outp[1]>4.74055:
                self.outp[1] = 4.74055
            
            self.Ei=self.Delta_Ei+self.Ei
            self.Delta_Ei=self.Delta_Ei+0.1
            
            if i >0: 
               self.ev.append(self.outp[1])
            
               self.Str.append(self.Ei)
               self.Qi.append(self.outp[0])
            
            
            
                
            
            
        
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(['Axial strain (%)','stress (kPa)','Volumetric deformation (%)'])
        for i in range(len(self.Qi)):
            sheet.append([str(round(self.Str[i],2)),str(round(self.Qi[i],2)),str(round(self.ev[i],2))])
        
        self.secondWindow = SecondWindow(self.Str,self.Qi,self.ev)

        self.secondWindow.x=self.Str
        self.secondWindow.y1=self.Qi
        self.secondWindow.y2=self.Qi
        self.secondWindow.displayInfo()
        workbook.save(filename = "output.xlsx")
        print("str",self.Str)
        print("Qi",self.Qi)
        print("ev",self.ev)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Fenetre()
    demo.show()
    sys.exit(app.exec_())

