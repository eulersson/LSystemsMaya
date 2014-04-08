#!/usr/bin/env python

""" DISCLAIMER: This startScript.py file is adapted from Jared Auty's scripting project "L-System Plant Generator". All the
    copyrights belong to him, just on this file, of course. I just tweaked some procedures to get them working in my script.
     
    You can access his source code here: 

        https://docs.google.com/file/d/0B75Ij6W0fkuidkxhY1ozanFzVEU/

    // 

    Start Up Script                              <startScript.py>

In order to get it running easily I suggest following these simple steps:

        1. Copy all the text inside startScript.py and paste it to Maya's Script Editor, a window will pop up asking you to
            select the folder which the script files are. Hit accept.
        2. Click on the "Instructions" button to get started by reading first a quick guide.
"""

import maya.cmds as cmds
class findPathWindow:
    """
    This class is responsible for managing the module-fininding window. This window is run when the script can't find the
    modules it needs. It asks the user to locate the modules. The user-inputted path is then saved in python's temporary
    system paths. This means that next time it tries to load the modules it will look in the right path.
    """
    def __init__(self):
        """
         This function initialises all the needed values and creates the GUI. It is run automatically when a new instance
         of the class is run.
        """
        self.fileName = []
        self.fileType = []
        #---Create UI elements---#
        self.loadDirWin = cmds.window( title="L-System Interpreter", sizeable=False)
        self.loadDirForm = cmds.formLayout( numberOfDivisions=100 )
        self.loadDirColumns = cmds.columnLayout( parent=self.loadDirForm, adjustableColumn=True, rowSpacing=5 )
        self.loadDirText = cmds.text( parent=self.loadDirColumns, font='boldLabelFont',
            label="""Welcome to Ramon\'s L-System Interpreter\n\nTo start using the script simply browse the directory
            containing the modules and then press \'Continue\'\n\n|\n|\nv""" )
        self.loadDirPath = cmds.textField( parent = self.loadDirColumns )
        self.loadDirBrowse= cmds.button( parent = self.loadDirColumns, label='Browse', command=self.openFile )
        self.loadDirLoad = cmds.button( parent = self.loadDirColumns, label ='Continue', command=self.appendPath)
        #---Make sure the colums layout stretches with the window---#
        cmds.formLayout( self.loadDirForm, edit=True, attachForm=[
            (self.loadDirColumns, 'top', 20),
            (self.loadDirColumns, 'left', 20),
            (self.loadDirColumns, 'right', 20),
            (self.loadDirColumns, 'bottom', 20),
            ] )

    def appendPath(self, *args):
        """
        This function queries the text field and puts the path in the system paths. It then runs the 'closeAll' function.
        """
        # Query textfield and save in self.fileName
        self.fileName = cmds.textField( self.loadDirPath, query=True, text=True )
        print self.fileName
        sys.path.append( self.fileName ) # Append to system paths
        if self.fileName: # If the fileName is not empty
            self.closeAll()
      
    def openFile(self, *args):
        """
        This opens the file browser and takes the path and puts it in the text field. This is run when the Browse button is
        pressed.
        """
        self.fileName = cmds.fileDialog2( fileMode=2, caption="Import Image" ) # Open the file browser
        cmds.textField( self.loadDirPath, edit=True, text=str(self.fileName[0]) ) # Put path in text field
      
    def closeAll(self, *args):
        """
        This function closes the window and starts up the main GUI. This is run when the Continue button is pressed.
        """
        cmds.deleteUI( self.loadDirWin, window=True ) # Close window
        import random
        import math
        import copy
        import LS_string_rewriting
        reload(LS_string_rewriting)
        import LS_interpreter
        reload(LS_interpreter)
        import gui
        reload(gui)
        import globalVar
        reload(globalVar)
        globalVar.plantNumber = 0
        import presets
        reload(presets)
        import gui
        gui.createUI() # Start UI

class errorWindow:
    """
    This class creates an error window that displays a message passed it at creation time.
    """
    def __init__(self, message):
        """
        This function creates the window. This is run when a new instance of the class is created. When creating a new
        instance a string called message is passed in, this is then displayed on the window.
        """
        self.win = cmds.window( title="Error" )
        self.form = cmds.formLayout( numberOfDivisions=100, w=300, h=100 )
        self.text = cmds.text( label=message )
        self.okButton = cmds.button( label='OK', command=self.close )
        cmds.formLayout( self.form, edit=True,attachForm=[[self.text, 'left', 0], [self.text, 'right', 0],
            [self.okButton, 'left', 0], [self.okButton, 'right', 0]] )
        cmds.formLayout( self.form, edit=True,attachPosition=[[self.text, 'top', 0, 0], [self.text, 'bottom', 0, 70],
            [self.okButton, 'top', 0, 70], [self.okButton, 'bottom', 0, 100]] )
        cmds.showWindow( self.win )
    def close(self, *args):
        """
        This function closed the window and is run when the 'OK' button is run
        """
        cmds.deleteUI(self.win)

try: # If a gui is already open close it
    if cmds.window( win.window, exists=True ):
        cmds.deleteUI( win.window, window=True )
except:
    pass

import maya.cmds as cmds
import sys
load = findPathWindow()
cmds.showWindow(load.loadDirWin)
