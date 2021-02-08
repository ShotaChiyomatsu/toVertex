# -*- coding: utf-8 -*-
from maya import cmds
from PySide2.QtWidgets import * 
from PySide2.QtCore import * 
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
from maya import OpenMayaUI
import pymel.core.datatypes as dt
#-------------------------------------------------------
# Base Window
#-------------------------------------------------------
def baseWindow():
    mainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(mainWindow), QWidget)
#-------------------------------------------------------
# Main
#-------------------------------------------------------  
backColor = "background:qlineargradient(x2:1, y1:0, x2:1, y2:1, stop:0.4#659999 stop:0.8#f4791f)"
widgetColor = "background:rgba(158, 200, 226, 0.3);color:#f5f5f5;border-color:#f5f5f5;font-weight:bold"
                  
class Gui(QDialog):
    
    def __init__(self, parent=baseWindow()):
        super(Gui, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
        self.setWindowTitle("To Vertex ver2.0")
        self.design()
        self.alphabetList()
    #---------------------------------------------------
    # Design
    #---------------------------------------------------
    def design(self):
        self.setStyleSheet(backColor)
        self.outputLayout = QGridLayout(self)
        self.widgets = []
        for i in range(4):
            # Widget
            if i == 0:
                self.widgets.append(QComboBox())
                self.widgets[0].addItems(["Locator", "Joint"])
                self.widgets[0].setFixedSize(80, 25)
            elif i == 1:
                self.widgets.append(QLineEdit())
            elif i == 2:
                self.widgets.append(QComboBox())
                self.widgets[2].addItems(["0-9", "A-Z", "a-z"])
                self.widgets[2].setFixedSize(50, 25)
            elif i == 3:
                self.widgets.append(QPushButton("Chain"))
            
            # Layout
            if i <= 2:
                self.outputLayout.addWidget(self.widgets[i], 0, i)
            elif i == 3:
                self.outputLayout.addWidget(self.widgets[i], 1, 0, 1, 3)
   
            self.widgets[i].setStyleSheet(widgetColor)
        
        # Connect
        self.widgets[1].returnPressed.connect(self.create)
        self.widgets[3].clicked.connect(self.chain)
    #---------------------------------------------------
    # Processing
    #---------------------------------------------------
    def alphabetList(self):
        self.ALPHALIST = [chr(i) for i in range(65,65+26)]
        self.alphalist = [chr(i) for i in range(97,97+26)]  

    def create(self):
        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        items = selection[0].split(".", 1)
        # Get Components
        component = []
        try:
            vtxList = cmds.filterExpand(sm=31)
            for i in range(len(vtxList)):
                vtx = cmds.xform(vtxList[i], ws=True, q=True, t=True)
                component.append(dt.Vector(vtx[0], vtx[1], vtx[2]))
                 
        except:
            cvList = cmds.filterExpand(sm=28)
            for i in range(len(cvList)):
                cv = cmds.xform(cvList[i], ws=True, q=True, t=True)
                component.append(dt.Vector(cv[0], cv[1], cv[2]))
            
        # Error
        if len(component) > 25 and self.widgets[2].currentText() == "A-Z" or \
            len(component) > 25 and self.widgets[2].currentText() == "a-z":
            
            print("When using Alphabet for suffixes Must not exceed 26 vertices"),
            
        # Create
        else:
            for i in range(len(component)):
                cmds.select(None)
                if self.widgets[0].currentText() == "Locator":
                    if self.widgets[2].currentText() == "0-9":
                        cmds.spaceLocator(n=self.widgets[1].text() + str(i), a=True)
                        cmds.move(component[i][0], component[i][1], component[i][2]) 
                    elif self.widgets[2].currentText() == "A-Z":
                        cmds.spaceLocator(n=self.widgets[1].text() + self.ALPHALIST[i], a=True)
                        cmds.move(component[i][0], component[i][1], component[i][2])
                    elif self.widgets[2].currentText() == "a-z":
                        cmds.spaceLocator(n=self.widgets[1].text() + self.alphalist[i], a=True)
                        cmds.move(component[i][0], component[i][1], component[i][2])
                
                elif self.widgets[0].currentText() == "Joint":
                    if self.widgets[2].currentText() == "0-9":
                        cmds.joint(n=self.widgets[1].text() + str(i), 
                        p=[component[i][0], component[i][1], component[i][2]])
                    elif self.widgets[2].currentText() == "A-Z":
                        cmds.joint(n=self.widgets[1].text() + self.ALPHALIST[i], 
                        p=[component[i][0], component[i][1], component[i][2]])
                    elif self.widgets[2].currentText() == "a-z":
                        cmds.joint(n=self.widgets[1].text() + self.alphalist[i], 
                        p=[component[i][0], component[i][1], component[i][2]])
            
            cmds.select(None)            
            cmds.undoInfo(closeChunk=True)

    def chain(self):
        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        try:
            for i in range(len(selection)-1):
                cmds.parent(selection[i+1], selection[i])
        except:
            cmds.undo()
            print("There is a node with the same name"), 
        cmds.undoInfo(closeChunk=True)
#-------------------------------------------------------
# Show
#-------------------------------------------------------
def main():
    
    G = Gui()
    G.show()
    
if __name__ == '__main__':
    
    G = Gui()
    G.show()
