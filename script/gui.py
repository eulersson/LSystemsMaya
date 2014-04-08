#!/usr/bin/env python
"""
    GUI module                                   <gui.py>

    Responsible for the user interface layout. I used some framed layouts so that it doesn't go off screen. Moreover I added
    an Instructions button and a Help Line underneath so that the user doesn't get lost at the beginning. The structure it
    follows is not too complicated:

        Instructions and Presets:     Quick guide for the users.
        Rules:                        Setting the predecessor, successor and probability for the rule to happen.
        Geometric interpretation:     Attributes and parameters for the geometry.
        Warnings and helpline:        Self-explanatory.

"""

import maya.cmds as cmds
import pydoc
from LS_string_rewriting import *
from LS_interpreter import *

__author__ = "Ramon Blanquer Ruiz"
__version__ = "1.0.0"
__email__ = "ramon@ramonblanquer.com"
__status__ = "Maintaned"

def createUI():
    # Check to see if our window exists
    if cmds.window( "myWindow", exists = True ):
        cmds.deleteUI( "myWindow" )

    # Create our main window
    window = cmds.window( "myWindow", title="L-System Interpreter", s=False, w=450, h=650, mnb=False, mxb=False )
    mainLayout = cmds.columnLayout( w=450, h=650 )
    import os
    pathVar = os.path.dirname(__file__) # This stores the current working directory
    imagePath = pathVar+"banner.png" # I designed a nice header for it
    cmds.image( w=450, h=160, image=imagePath )

    #--- MAIN FRAME LAYOUT ---#
    mainFrame = cmds.frameLayout( l="L-System String Operations", lv=False, cll=False, cl=True, mw=10, mh=10 )

    #////////////////////////////////////////INSTRUCTIONS//AND//PRESETS////////////////////////////////////////////////////#
    def displayInstructions(*pArgs):
        """Shows in an independent window a list of instructions for the user to set things up quickly"""
        if cmds.window( "instructions_window", exists=True ):
            cmds.deleteUI( "instructions_window" )
        instructions_window = cmds.window( "instructions_window", title="Instructions", s=False, mnb=False, mxb=False )
        instructionsLayout = cmds.frameLayout( l="Instructions", collapsable=False, cl=False, mw = 10, mh=10 )
        cmds.rowColumnLayout( nc=3, cw=[(1,20),(2,480),(3,20)], cal=[(2,"left")], parent=instructionsLayout )
        cmds.separator( st="none" )
        cmds.text( l="1. Write an axiom (or initial word), depth and rules. If you don't know what it is put the mouse over the parameter and read the help line.\n2. Click Generate String. Then you will see the result in the text field below, this is just mere text. Now the string needs to be interpreted.\n3. Set all the 'Geometric Interpretation' attributes (Angle, Segment Length...). Remember to put the mouse over it if your are confused.\n4. Click Create Geometry. You will see the result in your scene. If you want to clean the last plant\n\tclick Clean Plant. If you click Create Geometry again you will get another plant.\n6. Always remember to pay attention to the help line and warnings field." )
        cmds.separator( st="none" )
        cmds.separator( st="none" )
        cmds.text( l="\nThis is the meaning for each character you enter in the rules section:" )
        cmds.separator( st="none" )
        cmds.separator( st="none" )
        cmds.text( l="""        
        F    Move forward
        f    Move forward
        L    Leaf
        B    Blossom
        +    Rotate +X (yaw right)
        -    Rotate -X (yaw left)
        ^    Rotate +Y (roll right)
        &    Rotate -Y (roll left)
        <    Rotate +Z (pitch down)
        >    Rotate -Z (pitch up)
        *    Turtle rotates 180 (as it was facing backwards)
        [    Push current turtle state on the stack
        ]    Pop the current turtle state from the stack""" )
        cmds.showWindow( instructions_window )
    cmds.rowColumnLayout( numberOfColumns=4, cal=[(2,"left")], columnWidth=[(1,5),(2,320),(3,100),(4,5)], parent=mainFrame )
    cmds.separator( st="none" )
    cmds.text( l="You might feel a bit lost, I recommend you to read a quick guide" )
    cmds.button( l="Instructions", en=True, command=displayInstructions )
    cmds.separator( st="none" )

    cmds.rowColumnLayout( nc=7, cw=[(1,103),(2,5),(3,103),(4,5),(5,102),(6,5),(7,102)], parent=mainFrame )

    def preset1Action(*args):
        import presets
        set1 = presets.preset1()
    cmds.button( l="Preset1", c=preset1Action, ann="Loads Preset #1." )
    cmds.separator( st="none" )

    def preset2Action(*args):
        import presets
        set2 = presets.preset2()
    cmds.button( l="Preset2", c=preset2Action, ann="Loads Preset #2." )
    cmds.separator( st="none" )

    def preset3Action(*args):
        import presets
        set3 = presets.preset3()
    cmds.button( l="Preset3", c=preset3Action, ann="Loads Preset #3." )
    cmds.separator( st="none" )

    def preset4Action(*args):
        import presets
        set4 = presets.preset4()
    cmds.button( l="Preset4", c=preset4Action, ann="Loads Preset #4." )


    # !!!!!!!!!!!!!!!!!!!!!!! TO DO --> PRESETS

    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 425)], parent=mainFrame )
    cmds.separator( h=1, st="none" )

    #////////////////////////////////////////////////RULES//TAB////////////////////////////////////////////////////////////#
    rulesLayout = cmds.frameLayout( label = "Rules", collapsable=True, cl=False, mw = 10, mh = 10, w=425 )

    #--- Axiom ---#
    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 43), (2, 363)], parent=rulesLayout )
    cmds.text( l="Axiom ", align="right" )
    cmds.textField( "axiomTextField", tx="F", ann="Type the initial word you want to start with. The rules will replace each char of the word." )
    
    #--- Depth ---#
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 406)], parent=rulesLayout )
    cmds.intSliderGrp( "depthIntField", l="Depth: ", v=4, cw3=[40,30,350], min=1, max=10, fmx=20, f=True,
        ann="Set the index of recursion. The number of iterations over the generated string. How many times do you want to seach and replace chars in the string?" )

    #--- Probabilities header ---#
    cmds.rowColumnLayout( numberOfColumns=3, cal=[(1,"right")], columnWidth=[(1,325),(2,50),(3,45)], parent=rulesLayout )
    cmds.separator( st="none" )
    cmds.text( l="Prob.(%)", en=True, ebg=True, bgc=[0.0,0.153,0.0666] )
    cmds.separator( st="none" )
 
    #--- Collection of rules ---#
    cmds.rowColumnLayout( nc=7, cal=[(1,"right")], cw=[(1,40),(2,30),(3,20),(4,245),(5,40),(6,5),(7,20)], p=rulesLayout )

     #--- RULE 1 ---#
    cmds.text( l="Rule 1: ", en=True )
    cmds.textField( "prodRulePred1", en=True, tx="F", ann="Enter predecessor string for production rule 1. If this character is found in the string it will be replaced." )
    cmds.text( l="->", en=True )
    cmds.textField( "prodRuleSucc1", en=True, tx="F[&+F]F[->FL][&FB]", ann="Enter successor string for production rule 1. The value you want to replace the predecessor with." )
    cmds.intField( "prodRuleProb1", minValue=0, maxValue=100, value=100,
        ann="Enter the probability (in percentage %) in which you want this rule to be executed. Applies just if you write the same predecessors in different rules." )
    cmds.separator( st="none" )
    cmds.separator( st="none" )

    #--- RULE 2 ---#
    cmds.text( "prodRule2Text_A", l="Rule 2: ", en=False )
    cmds.textField( "prodRulePred2", en=False, ann="Enter predecessor string for production rule 2. If this character is found in the string it will be replaced." )
    cmds.text( "prodRule2Text_B", l="->", en=False )
    cmds.textField( "prodRuleSucc2", en=False, ann="Enter successor string for production rule 2. The value you want to replace the predecessor with." )
    cmds.intField( "prodRuleProb2", minValue=0, maxValue=100, value=0, en=False,
        ann="Enter the probability (in percentage %) in which you want this rule to be executed. Applies just if you write the same predecessors in different rules." )
    cmds.separator( st="none" )
    cmds.checkBox( "prodRuleCheckBox2", l="", value=False, ann="Activates the 2st production rule." )
    def toggleGreyingOut2(*pArgs):
        valueCB2 = cmds.checkBox( "prodRuleCheckBox2", q=True, value=True )
        if valueCB2 == True:
            cmds.text( "prodRule2Text_A", edit=True, en=True )
            cmds.textField( "prodRulePred2", edit=True, en=True )
            cmds.text( "prodRule2Text_B", edit=True, en=True )
            cmds.textField( "prodRuleSucc2", edit=True, en=True )
            cmds.intField( "prodRuleProb2", edit=True, en=True )
            cmds.intField( "prodRuleProb2", edit=True, v=100 )
        if valueCB2 == False:
            cmds.text( "prodRule2Text_A", edit=True, en=False )
            cmds.textField( "prodRulePred2", edit=True, en=False )
            cmds.text( "prodRule2Text_B", edit=True, en=False )
            cmds.textField( "prodRuleSucc2", edit=True, en=False )
            cmds.intField( "prodRuleProb2", edit=True, en=False )
            cmds.intField( "prodRuleProb2", edit=True, v=0 )
    cmds.checkBox( "prodRuleCheckBox2", edit=True, changeCommand=toggleGreyingOut2 )

    #--- RULE 3 ---#
    cmds.text( "prodRule3Text_A", l="Rule 3: ", en=False )
    cmds.textField( "prodRulePred3", en=False, ann="Enter predecessor string for production rule 3. If this character is found in the string it will be replaced." )
    cmds.text( "prodRule3Text_B", l="->", en=False )
    cmds.textField( "prodRuleSucc3", en=False, ann="Enter successor string for production rule 3. The value you want to replace the predecessor with." )
    cmds.intField( "prodRuleProb3", minValue=0, maxValue=100, value=0, en=False,
        ann="Enter the probability (in percentage %) in which you want this rule to be executed. Applies just if you write the same predecessors in different rules." )
    cmds.separator( st="none" )
    cmds.checkBox( "prodRuleCheckBox3", l="", value=False, ann="Activates the 3rd production rule." )
    def toggleGreyingOut3(*pArgs):
        valueCB3 = cmds.checkBox( "prodRuleCheckBox3", q=True, value=True )
        if valueCB3 == True:
            cmds.text( "prodRule3Text_A", edit=True, en=True )
            cmds.textField( "prodRulePred3", edit=True, en=True )
            cmds.text( "prodRule3Text_B", edit=True, en=True )
            cmds.textField( "prodRuleSucc3", edit=True, en=True )
            cmds.intField( "prodRuleProb3", edit=True, en=True )
            cmds.intField( "prodRuleProb3", edit=True, v=100 )
        if valueCB3 == False:
            cmds.text( "prodRule3Text_A", edit=True, en=False )
            cmds.textField( "prodRulePred3", edit=True, en=False )
            cmds.text( "prodRule3Text_B", edit=True, en=False )
            cmds.textField( "prodRuleSucc3", edit=True, en=False )
            cmds.intField( "prodRuleProb3", edit=True, en=False )
            cmds.intField( "prodRuleProb3", edit=True, v=0 )
    cmds.checkBox( "prodRuleCheckBox3", edit=True, changeCommand=toggleGreyingOut3 )

    #--- RULE 4 ---#
    cmds.text( "prodRule4Text_A", l="Rule 4: ", en=False )
    cmds.textField( "prodRulePred4", en=False, ann="Enter predecessor string for production rule 4. If this character is found in the string it will be replaced." )
    cmds.text( "prodRule4Text_B", l="->", en=False )
    cmds.textField( "prodRuleSucc4", en=False, ann="Enter successor string for production rule 4. The value you want to replace the predecessor with." )
    cmds.intField( "prodRuleProb4", minValue=0, maxValue=100, value=0, en=False,
        ann="Enter the probability (in percentage %) in which you want this rule to be executed. Applies just if you write the same predecessors in different rules." )
    cmds.separator( st="none" )
    cmds.checkBox( "prodRuleCheckBox4", l="", value=False, ann="Activates the 4th production rule." )
    def toggleGreyingOut4(*pArgs):
        valueCB4 = cmds.checkBox( "prodRuleCheckBox4", q=True, value=True )
        if valueCB4 == True:
            cmds.text( "prodRule4Text_A", edit=True, en=True )
            cmds.textField( "prodRulePred4", edit=True, en=True )
            cmds.text( "prodRule4Text_B", edit=True, en=True )
            cmds.textField( "prodRuleSucc4", edit=True, en=True )
            cmds.intField( "prodRuleProb4", edit=True, en=True )
            cmds.intField( "prodRuleProb4", edit=True, v=100 )
        if valueCB4 == False:
            cmds.text( "prodRule4Text_A", edit=True, en=False )
            cmds.textField( "prodRulePred4", edit=True, en=False )
            cmds.text( "prodRule4Text_B", edit=True, en=False )
            cmds.textField( "prodRuleSucc4", edit=True, en=False )
            cmds.intField( "prodRuleProb4", edit=True, en=False )
            cmds.intField( "prodRuleProb4", edit=True, v=0 )
    cmds.checkBox( "prodRuleCheckBox4", edit=True, changeCommand=toggleGreyingOut4 )

    #--- Generate String / Clear String  ---#
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,196), (2,10), (3,196)], parent=rulesLayout )
    cmds.button( l="Generate String", ann="Click to run the L-System string procedure.", c=generateStringButtonAction )
    cmds.separator( h=5, st="none" )
    cmds.button( l="Clear String", ann="Click to reset the generated string", command=clearStringButtonAction )

    #--- String Output ---#
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 402)], parent=rulesLayout )
    cmds.textField( "output", editable=True, ann="This is the generated string. When you get it proceed to construct the geometry.")
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 402)], parent=mainFrame )
    cmds.separator( h=5, st='none' )

    #//////////////////////////////////////GEOMETRIC//INTERPRETATION///////////////////////////////////////////////////////#
    mInterpret = cmds.frameLayout( label = "Geometric Interpretation", collapsable=True, cl=True, mw = 10, mh = 10, w=425 )
 
    #--- Set of geometric parameters ---#
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1,406)], parent=mInterpret )
    cmds.floatSliderGrp( "angle", l="Angle: ", pre=1, v=25.2, cal=[2,'center'], cw3=[92,40,788], min=0, max=100, fmx=360,
        f=True, ann="The turtle will yaw, roll or pitch by this angular (degrees) amount each time it finds each corresponding symbol.")
    cmds.floatSliderGrp( "length", l="Segment Length: ", pre=2, v=1.20, cw3=[92,40,788], min=0, max=10, fmx=100, f=True,
        ann= "The length of each turtle's step or segment.")
    cmds.floatSliderGrp( "radius", l="Segment Radius: ", pre=2, v=0.20, cw3=[92,40,788], min=0, max=0.5, fmx=2, f=True,
        ann="The radius of each cylinder (segment) that is placed." )
    cmds.intSliderGrp( "cylSubdivs", l="Cylinder Subdivs: ", v=5, cw3=[92,40,788], min=4, max=20, fmx=20, f=True,
        ann="No. of subdivisions for each cylinder." )
    cmds.intSliderGrp( "length_atenuation", l="Len. Atenuation: ", v=95, cw3=[92,40,788], min=0, max=100, fmx=100, f=True,
        ann="Next's index branch's segment's length will be (this field) percent the length of the previous one." )
    cmds.intSliderGrp( "radius_atenuation", l="Rad. Atenuation: ", v=85, cw3=[92,40,788], min=0, max=100, fmx=100, f=True,
        ann="Next's index branch's segment's radius will be (this field) percent the length of the previous one." )
    cmds.floatSliderGrp( "turtleSpeed", l="Turtle speed: ", v=0, cw3=[92,40,288], min=0, max=1, pre=2, fmx=5, f=True,
        ann="Before proceeding to the next turtle command it will be frozen for this amount of time (in seconds). Useful for keeping track of everything that happens." )
    cmds.separator( h=2, st="none" )

    #--- Colour Fields ---#
    global rgb_branchField, rgb_leafField, rgb_branchField
    cmds.colorSliderGrp( "rgb_branchField", l="Branches", rgb=(0.430,0.230,0.11), cw3=[52,30,328], ann="Branch colour." )
    cmds.separator( h=6, st="none" )
    cmds.colorSliderGrp( "rgb_leafField", l="Leaves", rgb=(0,0.624,0), cw3=[52,30,328], ann="Leaf colour." )
    cmds.separator( h=6, st="none" )
    cmds.colorSliderGrp('rgb_blossomField', l="Blossoms", rgb=(0.624,0,0), cw3=[52,30,328], ann="Blossoms colour." )

    #--- Create Geometry / Clean Plant ---#
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,196), (2,10), (3,196)], parent=mInterpret )
    cmds.button( l="Create Geometry", command=createGeometryButtonAction, ann="Go turtle! Go!" )
    cmds.separator( h=5, st="none" )
    cmds.button( l="Clean Plant", command=cleanPlantButtonAction, ann='Deletes the lastest generated plant.' )

    #/////////////////////////////////////WARNINGS//AND//HELPLINE//////////////////////////////////////////////////////////#
    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,55), (2, 5), (3, 366)], parent=mainFrame )
    cmds.text( l="Warnings" )
    cmds.separator( st="none" )
    cmds.textField( "warningsTextField", editable=False, tx="None" )
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=mainFrame )
    cmds.helpLine( bgc=[0.0,0.0,0.0] ) 

    #--- Credits Layout ---#
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=mainFrame )
    cmds.text( l="Ramon Blanquer - www.ramonblanquer.com - NCCA 2014" )
    cmds.showWindow()
    cmds.showWindow(window)

#////////////////////////////////////////////BUTTON//ACTIONS///////////////////////////////////////////////////////////////#
#--- GENERATE STRING ---#
def generateStringButtonAction(*pArgs):
    ''' Queries all the fields related to the string generation and calls the procedure. '''
    pAxiom = cmds.textField( "axiomTextField", q=True, tx=True )

    pP = []

    prodRuleProb1 = str(cmds.intField( "prodRuleProb1", q=True, v=True ))
    prodRulePred1 = str(cmds.textField( "prodRulePred1", q=True, tx=True ))
    prodRuleSucc1 = str(cmds.textField("prodRuleSucc1", q=True, tx=True))

    prodRuleCheckBox2 = cmds.checkBox( "prodRuleCheckBox2", q=True, value=True )
    prodRuleProb2 = str(cmds.intField( "prodRuleProb2", q=True, v=True ))
    prodRulePred2 = str(cmds.textField( "prodRulePred2", q=True, tx=True ))
    prodRuleSucc2 = str(cmds.textField("prodRuleSucc2", q=True, tx=True))

    prodRuleCheckBox3 = cmds.checkBox( "prodRuleCheckBox3", q=True, value=True )
    prodRuleProb3 = str(cmds.intField( "prodRuleProb3", q=True, v=True ))
    prodRulePred3 = str(cmds.textField( "prodRulePred3", q=True, tx=True ))
    prodRuleSucc3 = str(cmds.textField("prodRuleSucc3", q=True, tx=True))

    prodRuleCheckBox4 = cmds.checkBox( "prodRuleCheckBox4", q=True, value=True )
    prodRuleProb4 = str(cmds.intField( "prodRuleProb4", q=True, v=True ))
    prodRulePred4 = str(cmds.textField( "prodRulePred4", q=True, tx=True ))
    prodRuleSucc4 = str(cmds.textField("prodRuleSucc4", q=True, tx=True))

    pP.append([prodRuleProb1, prodRulePred1, prodRuleSucc1])
    if prodRuleCheckBox2 == True:
        pP.append([prodRuleProb2, prodRulePred2, prodRuleSucc2]) 
    if prodRuleCheckBox3 == True:
        pP.append([prodRuleProb3, prodRulePred3, prodRuleSucc3]) 
    if prodRuleCheckBox4 == True:
        pP.append([prodRuleProb4, prodRulePred4, prodRuleSucc4])

    pDepth = cmds.intSliderGrp( "depthIntField", q=True, v=True )

    # This bit makes sure the sum of all probabilities is 100.
    if prodRulePred1 == prodRulePred2 or prodRulePred1 == prodRulePred3 or prodRulePred1 == prodRulePred4 or prodRulePred2 == prodRulePred3 or prodRulePred2 == prodRulePred4 or prodRulePred3 == prodRulePred4:
        probSum = int(prodRuleProb1) + int(prodRuleProb2) + int(prodRuleProb3) + int(prodRuleProb4)
        if probSum == 100 or ((prodRulePred1 != prodRulePred2) or (prodRulePred1 != prodRulePred3) or (prodRulePred1 != prodRulePred4) or (prodRulePred2 != prodRulePred3) or (prodRulePred2 != prodRulePred4) or (prodRulePred3 != prodRulePred4)):
            global LStringVar
            LStringVar = writeLS(pAxiom, pP, pDepth)
            cmds.textField( "output", edit=True, tx=LStringVar )
            cmds.textField( "warningsTextField", edit=True, tx="None" )
        else:
            cmds.textField( "warningsTextField", edit=True, tx="Be careful with percentages. They don't add to 100." )
            cmds.textField( "output", edit=True, tx="ERROR. Take a look at the warning text line." )

#--- CLEAR STRING BUTTON ACTION ---#
def clearStringButtonAction(*pArgs):
    """ Clears the string field. """ 
    cmds.textField( "output", edit=True, tx="" )

#--- GENERATE GEOMETRY ACTION ---#
def createGeometryButtonAction(*pArgs):
    """ Queries all the fields related to the geometry interpretation and calls the procedure. """
    pAngle = cmds.floatSliderGrp( "angle", q=True, v=True )
    pStep = cmds.floatSliderGrp( "length", q=True, v=True )
    pRad = cmds.floatSliderGrp( "radius", q=True, v=True )
    subDivs = cmds.intSliderGrp( "cylSubdivs", q=True, v=True )
    length_atenuation = cmds.intSliderGrp( "length_atenuation", q=True, v=True )
    radius_atenuation = cmds.intSliderGrp( "radius_atenuation", q=True, v=True )
    turtleSpeed = cmds.floatSliderGrp( "turtleSpeed", q=True, v=True)
    rgb_blossom = cmds.colorSliderGrp( "rgb_blossomField", q=True, rgb=True )
    rgb_leaf = cmds.colorSliderGrp( "rgb_leafField", q=True, rgb=True )
    rgb_branch = cmds.colorSliderGrp( "rgb_branchField", q=True, rgb=True )

    if pAngle == 0 or pStep == 0 or pRad == 0 or subDivs == 0 or LStringVar == '':
        cmds.textField('warningsTextField', edit=True, tx='Please, revise all the fields again')  
    else:
        import globalVar
        reload(globalVar)
        globalVar.plantNumber += 1
        cmds.textField('warningsTextField', edit=True, tx='None.')
        print "CACACACAAAAAAAAAAAAAAAAAAAAAA"
        createBranchShader(rgb_branch)
        createLeafShader(rgb_leaf)
        createBlossomShader(rgb_blossom)
        createGeometry(LStringVar, pRad, pStep, pAngle, subDivs, length_atenuation/100.0, radius_atenuation/100.0,
            turtleSpeed, rgb_branch, rgb_leaf, rgb_blossom)


#--- CLEAN ACTION ---#
def cleanPlantButtonAction(*pArgs):
    """ Will delete the last plant that has been generated. """
    import globalVar
    reload(globalVar)
    
    cmds.select( "plant"+str(globalVar.plantNumber) )
    cmds.delete()