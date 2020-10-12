# -*- coding: utf-8 -*-
from maya import cmds

cmds.undoInfo(openChunk=True)
selection = cmds.ls(sl=True)
try:
    for i in range(len(selection)-1):
        cmds.parent(selection[i+1], selection[i])
except:
    cmds.undo()
    print("There is a node with the same name"), 
cmds.undoInfo(closeChunk=True)