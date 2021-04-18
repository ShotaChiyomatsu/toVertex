# -*- coding: utf-8 -*-
from maya import cmds
from PySide2.QtWidgets import * 
from PySide2.QtCore import * 
from PySide2.QtCore import Qt
from shiboken2 import wrapInstance
from maya import OpenMayaUI
#-------------------------------------------------------
# Base Window
#-------------------------------------------------------
def baseWindow():
    mainWindow = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(long(mainWindow), QWidget)
#-------------------------------------------------------
# Main
#-------------------------------------------------------                   
class Gui(QDialog):
    
    def __init__(self, parent=baseWindow()):
        super(Gui, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
        self.setWindowTitle("To Vertex Tool")
        self.design()
        self.alphabetList()
        self.prefCheck()

    def design(self):
        self.outputLayout = QVBoxLayout(self)
        self.upperLayout = QHBoxLayout()
        self.lowerLayout = QHBoxLayout()
        self.widgets = []
        for i in range(5):
            # ウィジェットの作成
            if i == 0:
                self.widgets.append(QCheckBox("Chain Mode"))
                self.widgets[i].setChecked(True)
            elif i == 1:
                self.widgets.append(QLabel("Type :"))
            elif i == 2:
                self.widgets.append(QComboBox())
                self.widgets[i].addItems(["Joint","Locator"])
                self.widgets[i].setFixedSize(80, 25)
            elif i == 3:
                self.widgets.append(QLineEdit())
            elif i == 4:
                self.widgets.append(QComboBox())
                self.widgets[i].addItems(["0-9", "A-Z", "a-z"])
                self.widgets[i].setFixedSize(50, 25)
            # レイアウト
            if i <= 2:
                self.upperLayout.addWidget(self.widgets[i])
            else:
                self.lowerLayout.addWidget(self.widgets[i])
            # カラー
            self.widgets[i].setStyleSheet("font-weight:bold")
        self.outputLayout.addLayout(self.upperLayout)
        self.outputLayout.addLayout(self.lowerLayout)
        # 接続
        self.widgets[3].returnPressed.connect(self.create)

    def alphabetList(self):
        self.ALPHALIST = [chr(i) for i in range(65,65+26)]
        self.alphalist = [chr(i) for i in range(97,97+26)]  

    def prefCheck(self):
        # 設定の確認
        if not cmds.selectPref(q=True, tso=True):
            cmds.selectPref(tso=True) 
    
    def create(self):
        cmds.undoInfo(openChunk=True)
        selection = cmds.ls(os=True, fl=True)
        selection_pos = []
        create_obj = []
        # 選択しているコンポーネントが２６個以内か確認
        if len(selection) > 25 and self.widgets[4].currentText() == "A-Z" or \
            len(selection) > 25 and self.widgets[4].currentText() == "a-z":
            print("When using Alphabet for suffixes Must not exceed 26 vertices"),
        
        else:
            # 位置の取得
            for i in range(len(selection)):
                selection_pos.append(cmds.pointPosition(selection[i]))

            # オブジェクトを配置
            for i in range(len(selection)):
                cmds.select(None)
                # ジョイントを配置
                if self.widgets[2].currentText() == "Joint":
                    if self.widgets[4].currentText() == "0-9":
                        create_obj.append(cmds.joint(n=self.widgets[3].text() + str(i), 
                        p=[selection_pos[i][0], selection_pos[i][1], selection_pos[i][2]]))
                    
                    elif self.widgets[4].currentText() == "A-Z":
                        create_obj.append(cmds.joint(n=self.widgets[3].text() + self.ALPHALIST[i], 
                        p=[selection_pos[i][0], selection_pos[i][1], selection_pos[i][2]]))
                    
                    elif self.widgets[4].currentText() == "a-z":
                        create_obj.append(cmds.joint(n=self.widgets[3].text() + self.alphalist[i], 
                        p=[selection_pos[i][0], selection_pos[i][1], selection_pos[i][2]]))
                
                # ロケーターを配置
                elif self.widgets[2].currentText() == "Locator":
                    if self.widgets[4].currentText() == "0-9":
                        create_obj.append(cmds.spaceLocator(n=self.widgets[3].text() + str(i), a=True))
                        cmds.move(selection_pos[i][0], selection_pos[i][1], selection_pos[i][2])
                    
                    elif self.widgets[4].currentText() == "A-Z":
                        create_obj.append(cmds.spaceLocator(n=self.widgets[3].text() + self.ALPHALIST[i], a=True))
                        cmds.move(selection_pos[i][0], selection_pos[i][1], selection_pos[i][2])
                    
                    elif self.widgets[4].currentText() == "a-z":
                        create_obj.append(cmds.spaceLocator(n=self.widgets[3].text() + self.alphalist[i], a=True))
                        cmds.move(selection_pos[i][0], selection_pos[i][1], selection_pos[i][2])

            # オブジェクトを鎖状に親子付け
            if self.widgets[0].isChecked():
                for i in range(len(create_obj)-1):
                    cmds.parent(create_obj[i+1], create_obj[i])

        cmds.select(None)
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
