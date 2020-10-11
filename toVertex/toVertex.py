# -*- coding: utf-8 -*-
from maya import cmds
from PySide2.QtWidgets import * 
from PySide2.QtCore import * 
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
from maya import OpenMayaUI
import pymel.core.datatypes as dt
import string
#-------------------------------------------------------
# Base Window
#-------------------------------------------------------
def baseWindow():
    mainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(mainWindow), QWidget)
#-------------------------------------------------------
# Main
#-------------------------------------------------------  
backColor = "background:qlineargradient(x2:1, y1:0, x2:1, y2:1, stop:0.5#2b5876 stop:0.8#4e4376)"
groupColor = "background:rgba(158, 200, 226, 0.2);color:#f5f5f5;border-style:solid;border-width:0px;border-color:#f5f5f5;border-radius:2px;"
editColor = "background:rgba(158, 200, 226, 0.2);color:#f5f5f5;border-color:#f5f5f5;font-weight:bold"
                   
class Gui(QDialog):
    
    def __init__(self, parent=baseWindow()):
        super(Gui, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
        self.setWindowTitle("To Vertex ver1.0")
        self.design()
    #---------------------------------------------------
    # Design
    #---------------------------------------------------
    def design(self):
        # Create
        self.createLayout = QHBoxLayout()
        self.createGroup = QGroupBox()
        self.createGroup.setLayout(self.createLayout)
        self.widgets = []
        for i in range(3):
            if i == 0:
                self.widgets.append(QComboBox())
                self.widgets[0].addItems(["Locator", "Joint"])
                self.widgets[0].setFixedSize(75, 20)
                self.createLayout.addWidget(self.widgets[0])
            
            elif i == 1:
                self.widgets.append(QLineEdit())
                self.createLayout.addWidget(self.widgets[1])
            
            elif i == 2:
                self.widgets.append(QComboBox())
                self.widgets[2].addItems(["0-9", "A-Z", "a-z"])
                self.widgets[2].setFixedSize(50, 20)
                self.createLayout.addWidget(self.widgets[2])
            
            self.widgets[i].setStyleSheet(editColor)
        
        self.setStyleSheet(backColor)
        self.createGroup.setStyleSheet(groupColor)
                      
        # output
        self.outputLayout = QVBoxLayout(self)
        self.outputLayout.addWidget(self.createGroup)
        # Connect
        self.widgets[1].returnPressed.connect(self.create)
        # Alphabet
        self.ALPHALIST = [chr(i) for i in range(65,65+26)]
        self.alphalist = [chr(i) for i in range(97,97+26)]
    #---------------------------------------------------
    # Processing
    #---------------------------------------------------    
    def create(self):
        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(sl=True)
        items = selection[0].split(".", 1)
        component = []
        try:
            # Get Componants
            if cmds.objectType(items[0]) == "mesh":
                vtxList = cmds.filterExpand(sm=31)
                for i in range(len(vtxList)):
                    vtx = cmds.xform(vtxList[i], ws=True, q=True, t=True)
                    component.append(dt.Vector(vtx[0], vtx[1], vtx[2]))
                    
            else:
                cvList = cmds.filterExpand(sm=28)
                for i in range(len(cvList)):
                    cv = cmds.xform(cvList[i], ws=True, q=True, t=True)
                    component.append(dt.Vector(cv[0], cv[1], cv[2]))
        
        except:
            vtxList = cmds.filterExpand(sm=31)
            for i in range(len(vtxList)):
                vtx = cmds.xform(vtxList[i], ws=True, q=True, t=True)
                component.append(dt.Vector(vtx[0], vtx[1], vtx[2]))
            
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
#-------------------------------------------------------
# Show
#-------------------------------------------------------  
if __name__ == '__main__':
    
    G = Gui()
    G.show()