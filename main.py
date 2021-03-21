#importing modules

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


import sys
import operator

#importing UI
from mainwindow import Ui_MainWindow

#global states
READY = 0
INPUT = 1
PI=3.14
DECI_START=0
DECI_POS=1
DIGIT_COUNTER=1
OP_FLAG=0
FUNC_SWITCH=0


#The mainwindow class
class MainWindow(QMainWindow):
    #constructor
    def __init__(self):
        #running the constructor of parent class
        QMainWindow.__init__(self)
        #making object of UI_MainWindow Class
        self.ui = Ui_MainWindow()
        #setting up the UI  
        self.ui.setupUi(self)
        #Input holding stack
        self.stack=[0]
        #Default state
        self.state=READY
        #Operation variable
        self.last_operation=0
        #current operation
        self.current_op=0
        #operation container
        self.op_container= ["equals","dl","add","minus","div","mul","deci","pow","c","pi","upon","root","percent","back"]
        #connecting the theme changer function
        self.ui.dl_pushButton.pressed.connect(lambda: self.themeselector()) 
        # Setup numbers.
        for n in range(0, 10):
            getattr(self.ui, 'pushButton%s' % n).pressed.connect(lambda input_num=n: self.input_number(input_num))
        #connecting operations
        self.ui.c_pushButton.pressed.connect(lambda : self.clear())
        self.ui.back_pushButton.pressed.connect(lambda: self.back())
        self.ui.pi_pushButton.pressed.connect(lambda: self.input_number(PI))
        self.ui.deci_pushButton.pressed.connect(lambda : self.deci())
        self.ui.add_pushButton.pressed.connect(lambda: self.operation(operator.add))
        self.ui.minus_pushButton.pressed.connect(lambda : self.operation(operator.sub))
        self.ui.mul_pushButton.pressed.connect(lambda : self.operation(operator.mul))
        self.ui.div_pushButton.pressed.connect(lambda : self.operation(operator.truediv))
        self.ui.equals_pushButton.pressed.connect(lambda: self.equals())
        self.ui.pow_pushButton.pressed.connect(lambda: self.power())
        self.ui.root_pushButton.pressed.connect(lambda : self.root())
        self.ui.upon_pushButton.pressed.connect(lambda: self.upon())
        self.ui.percent_pushButton.pressed.connect(lambda : self.percent())
  
        
       #Show UI
        ########################################################################
        self.show()

    #######################################################################################################################################
    def percent(self):
        global FUNC_SWITCH
        FUNC_SWITCH=4
        self.stack.append(0)
    def upon(self):
        global FUNC_SWITCH
        FUNC_SWITCH=3
        self.equals()

    def root(self):
        global FUNC_SWITCH
        FUNC_SWITCH=2
        self.stack.append(0)
   
    def power(self):
        global FUNC_SWITCH
        FUNC_SWITCH=1
        self.stack.append(0)

    def equals(self):
        global FUNC_SWITCH
        if FUNC_SWITCH==0:
            global DIGIT_COUNTER
            DIGIT_COUNTER=1
            if self.current_op:
                self.last_operation=self.current_op
            print("before equal function run",self.stack)
            self.stack= [self.last_operation(*self.stack)]
            print("equal function stack",self.stack)
            self.current_op=None
            self.state=READY
        elif FUNC_SWITCH==1:
            self.stack= [self.stack[0]**self.stack[1]]
            self.state=READY
            FUNC_SWITCH=0
        elif FUNC_SWITCH==2:
            self.stack= [self.stack[1]**(1/self.stack[0])]
            self.state=READY
            FUNC_SWITCH=0
        elif FUNC_SWITCH==3:
            self.stack=[1/self.stack[-1]]
            self.state=READY
            FUNC_SWITCH=0
        elif FUNC_SWITCH==4:
            self.stack=[(self.stack[0]*self.stack[1])/100]
            self.state=READY
            FUNC_SWITCH=0


        self.display()


    def operation(self,op):
        global DIGIT_COUNTER
        DIGIT_COUNTER=1
        global OP_FLAG
        if self.current_op:
            
            self.equals()
        self.current_op=op
        if OP_FLAG==0:
            self.last_operation=self.current_op
            OP_FLAG=1
        self.stack.append(0)
        print(self.stack)


    #Function for dcimal
    def deci(self):
        global DECI_START
        if DECI_START==0:
            self.stack[-1]=float(self.stack[-1])
            print(self.stack)
            self.display()
            DECI_START=1
    #Function to clear the display (c)
    def clear(self):
        global DIGIT_COUNTER
        DIGIT_COUNTER=1
        self.state=READY
        self.stack=[0]
        self.current_op=None
        self.display()
    #Function to clear the recent number ( backspace)
    def back(self):
        global DIGIT_COUNTER
        global DECI_POS
        DIGIT_COUNTER-=1
        if DECI_START==0:
            self.stack[-1]= self.stack[-1]//10
            self.display()
        elif DECI_START==1:
            
            self.stack[-1]=((self.stack[-1]*(10**(DECI_POS-1)))//10)/(10**(DECI_POS-2))
            DECI_POS-=1
            self.display()
    #Function to display the changes on the screen
    def display(self):
        self.ui.lcdNumber.display(self.stack[-1])
    #Function to take the input
    def input_number(self, input_num):
        global DIGIT_COUNTER
        if DECI_START==1 and DIGIT_COUNTER<9:
            global DECI_POS
            self.stack[-1]=self.stack[-1]+ input_num/(10**DECI_POS)
            print(self.stack)
            DECI_POS+=1


        #checking for the first digit
        if self.state == READY and DECI_START==0 and DIGIT_COUNTER<9:
             self.state = INPUT
             self.stack[-1] = input_num
        #checking for the further digits
        elif self.stack[-1]<214748364 and self.stack[-1]>-214748364 and DECI_START==0 and DIGIT_COUNTER<9:
             self.stack[-1] = self.stack[-1] * 10 + input_num
             print(self.stack)
        #displaying numbers
        DIGIT_COUNTER+=1
        self.display()
    #Function for selecting the theme
    def themeselector(self):
            #Checking the states of themebutton to switch between themes
            if self.ui.dl_pushButton.isChecked():
                    self.themechangerdark()
            else:
                    self.themechangerlight()
    #Function to apply light theme
    def themechangerlight(self):
        #Setting style sheets
        self.ui.lcdNumber.setStyleSheet("color: rgb(0,0,0);")
        self.setStyleSheet("background-color: rgb(201,191,189);")
        
        
        for i in self.op_container:
                getattr(self.ui, "%s_pushButton" % i).setStyleSheet("QPushButton{\n"
"background-color: rgb(230,226,221);\n"
"\n"
"color: rgb(0,0,0);\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"\n"
"    background-color: rgb(166, 151, 155);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(166, 151, 155);\n"
"}")


        for i in range(0,10):
                getattr(self.ui,"pushButton%s" % i).setStyleSheet("QPushButton{background-color: rgb(243,242,242);\n"
"color: rgb(0,0,0);}\n"
"\n"
"QPushButton::hover{\n"
"\n"
"    background-color: rgb(166, 151, 155);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(166, 151, 155);\n"
"}")

    #Function to apply dark theme
    def themechangerdark(self):
        #setting up style sheets
        self.ui.lcdNumber.setStyleSheet("color: rgb(255, 255, 255);")
        self.setStyleSheet("background-color: rgb(48, 38, 38);")


        for i in self.op_container:
                getattr(self.ui, "%s_pushButton" % i).setStyleSheet("QPushButton{\n"
"background-color: rgb(29, 25, 26);\n"
"\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton::hover{\n"
"\n"
"    background-color: rgb(166, 151, 155);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(166, 151, 155);\n"
"}")

        for i in range(0,10):
                getattr(self.ui,"pushButton%s" % i).setStyleSheet("QPushButton{background-color: rgb(9, 8, 8);\n"
"color: rgb(255, 255, 255);}\n"
"\n"
"QPushButton::hover{\n"
"\n"
"    background-color: rgb(166, 151, 155);\n"
"}\n"
"\n"
"QPushButton::pressed{\n"
"background-color: rgb(166, 151, 155);\n"
"}")
#END OF THE CLASS

#Checking for the main domain
if __name__ == "__main__":
    #creating the object of QApplication class 
    app = QApplication(sys.argv)
    #creating the object of MainWindow Class
    window = MainWindow()
    #Code for exit after app execution
    sys.exit(app.exec_())