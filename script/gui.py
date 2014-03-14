#!/usr/bin/env python
'''
   GUI module
'''

import maya.cmds as cmds
from LS_string_rewriting import *
from LS_interpreter import *


__author__ = "Ramon Blanquer Ruiz"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "ramon@ramonblanquer.com"
__status__ = "Unmaintained"

def createUI():
    # Check to see if our window exists
    if cmds.window('myWindow', exists = True):
        cmds.deleteUI('myWindow')

    # Create our window
    window = cmds.window('myWindow', title='L-System Interpreter', s=False, w=450, h=650, mnb=False, mxb=False)

    # Our layout will be 450 px width and 650 px height. I set an image as well.
    mainLayout = cmds.columnLayout(w=450, h=650)
    imagePath = cmds.internalVar(upd = True) + "icons/banner.png"
    cmds.image(w=450, h=160, image=imagePath)

    # Here I create 3 tabs. 'Standard', 'Context Sensitive', 'Stochastic', and 'Instructions'
    # form = cmds.formLayout()
    # tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    # cmds.formLayout(form, edit=True, attachForm=((tabs, 'Standard', 0), (tabs, 'Context Sensitive', 0), (tabs, 'Stochastic', 0), (tabs, 'Instructions', 0)))

    # String Operations Layouts
    stringOp = cmds.frameLayout(label = 'L-System String Operations', labelVisible=False, collapsable=False, cl=True, mw = 10, mh = 10)

    cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 43), (2, 383)], parent=stringOp)
    cmds.text(l='Axiom ', align='right')
    cmds.textField('axiomTextField', tx='F',ann='Type the initial word you want to start with. The initialiser.')
 
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=stringOp)
    cmds.intSliderGrp('depthIntField', l="Depth: ", v=3, cw3=[40,30,350], min=1, max=10, fmx=20, f=True, ann='Set the index of recursion. The number of iterations over the generated string.')

    cmds.rowColumnLayout( numberOfColumns=3, cal=[(1,"right")], columnWidth=[(1,355),(2,50),(3,25)], parent=stringOp)
    cmds.separator(st='none')
    cmds.text(l='Prob.(%)', en=True, ebg=True, bgc=[0.0,0.153,0.0666])
    cmds.separator(st='none')

    cmds.rowColumnLayout( numberOfColumns=7, cal=[(1,"right")], columnWidth=[(1,70),(2,30),(3,30),(4,235),(5,40),(6,5),(7,20)], parent=stringOp)
   # RULE 1
    cmds.text(l='Prod. Rule 1: ', en=True)
    cmds.textField('prodRulePred1', en=True, tx='F', ann='Enter predecessor string for production rule 1')
    cmds.text(l='->', en=True)
    cmds.textField('prodRuleSucc1', en=True, tx='F[&+F]F[->F][->F][&F]', ann='Enter successor string for production rule 1')
    cmds.floatField('prodRuleProb1', minValue=0, pre=1, maxValue=100, value=100, ann='Enter the probability (in percentage %) in which you want this rule to be executed')
    cmds.separator(st='none')
    cmds.separator(st='none')

    # RULE 2
    cmds.text('prodRule2Text_A', l='Prod. Rule 2: ', en=False)
    cmds.textField('prodRulePred2', en=False, ann='Enter predecessor string for production rule 2')
    cmds.text('prodRule2Text_B', l='->', en=False)
    cmds.textField('prodRuleSucc2', en=False, ann='Enter successor string for production rule 2')
    cmds.floatField('prodRuleProb2', minValue=0, pre=1, maxValue=100, value=0, en=False, ann='Enter the probability (in percentage %) in which you want this rule to be executed')
    cmds.separator(st='none')
    cmds.checkBox('prodRuleCheckBox2', l='', value=False, ann='Activates the 2st production rule')
    def toggleGreyingOut2(*pArgs):
        valueCB2 = cmds.checkBox('prodRuleCheckBox2', q=True, value=True)
        if valueCB2 == True:
            cmds.text('prodRule2Text_A', edit=True, en=True)
            cmds.textField('prodRulePred2', edit=True, en=True)
            cmds.text('prodRule2Text_B', edit=True, en=True)
            cmds.textField('prodRuleSucc2', edit=True, en=True)
            cmds.floatField('prodRuleProb2', edit=True, en=True)
        if valueCB2 == False:
            cmds.text('prodRule2Text_A', edit=True, en=False)
            cmds.textField('prodRulePred2', edit=True, en=False)
            cmds.text('prodRule2Text_B', edit=True, en=False)
            cmds.textField('prodRuleSucc2', edit=True, en=False)
            cmds.floatField('prodRuleProb2', edit=True, en=False)
    cmds.checkBox('prodRuleCheckBox2', edit=True, changeCommand=toggleGreyingOut2)

    # RULE 3
    cmds.text('prodRule3Text_A', l='Prod. Rule 3: ', en=False)
    cmds.textField('prodRulePred3', en=False, ann='Enter predecessor string for production rule 2')
    cmds.text('prodRule3Text_B', l='->', en=False)
    cmds.textField('prodRuleSucc3', en=False, ann='Enter successor string for production rule 3')
    cmds.floatField('prodRuleProb3', minValue=0, pre=1, maxValue=100, value=0, en=False, ann='Enter the probability (in percentage %) in which you want this rule to be executed')
    cmds.separator(st='none')
    cmds.checkBox('prodRuleCheckBox3', l='', value=False, ann='Activates the 3rd production rule')
    def toggleGreyingOut3(*pArgs):
        valueCB3 = cmds.checkBox('prodRuleCheckBox3', q=True, value=True)
        if valueCB3 == True:
            cmds.text('prodRule3Text_A', edit=True, en=True)
            cmds.textField('prodRulePred3', edit=True, en=True)
            cmds.text('prodRule3Text_B', edit=True, en=True)
            cmds.textField('prodRuleSucc3', edit=True, en=True)
            cmds.floatField('prodRuleProb3', edit=True, en=True)
        if valueCB3 == False:
            cmds.text('prodRule3Text_A', edit=True, en=False)
            cmds.textField('prodRulePred3', edit=True, en=False)
            cmds.text('prodRule3Text_B', edit=True, en=False)
            cmds.textField('prodRuleSucc3', edit=True, en=False)
            cmds.floatField('prodRuleProb3', edit=True, en=False)
    cmds.checkBox('prodRuleCheckBox3', edit=True, changeCommand=toggleGreyingOut3)

    # RULE 4
    cmds.text('prodRule4Text_A', l='Prod. Rule 4: ', en=False)
    cmds.textField('prodRulePred4', en=False, ann='Enter predecessor string for production rule 4')
    cmds.text('prodRule4Text_B', l='->', en=False)
    cmds.textField('prodRuleSucc4', en=False, ann='Enter successor string for production rule 4')
    cmds.floatField('prodRuleProb4', minValue=0, pre=1, maxValue=100, value=0, en=False, ann='Enter the probability (in percentage %) in which you want this rule to be executed')
    cmds.separator(st='none')
    cmds.checkBox('prodRuleCheckBox4', l='', value=False, ann='Activates the 4th production rule')
    def toggleGreyingOut4(*pArgs):
        valueCB4 = cmds.checkBox('prodRuleCheckBox4', q=True, value=True)
        if valueCB4 == True:
            cmds.text('prodRule4Text_A', edit=True, en=True)
            cmds.textField('prodRulePred4', edit=True, en=True)
            cmds.text('prodRule4Text_B', edit=True, en=True)
            cmds.textField('prodRuleSucc4', edit=True, en=True)
            cmds.floatField('prodRuleProb4', edit=True, en=True)
        if valueCB4 == False:
            cmds.text('prodRule4Text_A', edit=True, en=False)
            cmds.textField('prodRulePred4', edit=True, en=False)
            cmds.text('prodRule4Text_B', edit=True, en=False)
            cmds.textField('prodRuleSucc4', edit=True, en=False)
            cmds.floatField('prodRuleProb4', edit=True, en=False)
    cmds.checkBox('prodRuleCheckBox4', edit=True, changeCommand=toggleGreyingOut4)

    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,208), (2,10), (3,208)], parent=stringOp)
    cmds.button(l='Generate String', ann='Click to run the L-System string calculation', command=generateStringButtonAction)
    cmds.separator(h=5, st='none')
    cmds.button(l='Clear String', ann='Click to reset the generated string')

    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=stringOp)
    cmds.textField("output", editable=False, ann='This is the generated string. Now Proceed to build the geometry.')

    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=stringOp)
    cmds.separator(h=5, st='none')

    #cmds.setParent( '..' )

    mInterpret = cmds.frameLayout(label = "Geometric Interpretation", collapsable=True, cl=False, mw = 10, mh = 10)
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1,406)], parent=mInterpret)
    cmds.floatSliderGrp("angle", l="Angle: ", pre=1, v=28, cal=[2,'center'], cw3=[92,40,788], min=0, max=100, fmx=360, f=True)
    cmds.floatSliderGrp("length", l="Segment Length: ", pre=2, v=1.2, cw3=[92,40,788], min=0, max=10, fmx=100, f=True)
    cmds.floatSliderGrp("radius", l="Segment Radius: ", pre=2, v=0.2, cw3=[92,40,788], min=0, max=0.5, fmx=2, f=True)
    cmds.intSliderGrp("cylSubdivs", l="Cylinder Subdivs: ", v=8, cw3=[92,40,788], min=4, max=20, fmx=20, f=True)
    cmds.floatSliderGrp("atenuation", l="Atenuation: ", v=1, cw3=[92,40,788], min=0, max=1, fmx=1, f=True, pre=2, ann='This number will multiply the length of the next segment, recursively')

    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,196), (2,10), (3,196)], parent=mInterpret)
    cmds.button(l='Create Geometry', command=createGeometryButtonAction)
    cmds.separator(h=5, st='none')
    cmds.button(l='Clean Scene', command=cleanSceneButtonAction)

    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=stringOp)
    cmds.separator(h=5, st='none')

    kAnimation = cmds.frameLayout(label = "Animation Settings", collapsable=True, cl=True, mw = 10, mh = 10)
    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1,406)], parent=kAnimation)
    cmds.intSliderGrp('keyEvery', l='K every (frames):', v=0, cw3=[92,30,798], min=1, max=10, fmx=20, f=True)
    cmds.intSliderGrp('angleVar', l='Angle Oscilation: ', v=0, cw3=[92,30,278], min=1, max=10, fmx=20, f=True)

    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,196), (2,10), (3,196)], parent=kAnimation)
    cmds.button(l='Add Animation')
    cmds.separator(h=5, st='none')
    cmds.button(l='Clear Keyframes')

    cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1,55), (2, 5), (3, 366)], parent=stringOp)
    cmds.text(l='Warnings')
    cmds.separator(st='none')
    cmds.textField('warningsTextField', editable=False, tx='None') 


    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=stringOp)
    cmds.helpLine(bgc=[0.0,0.0,0.0]) 

    cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 426)], parent=stringOp)
    cmds.text(l='Ramon Blanquer - www.ramonblanquer.com - NCCA 2014') 

    cmds.showWindow()
    # Show Window
    cmds.showWindow(window)

def generateStringButtonAction(*pArgs):
    pAxiom = cmds.textField('axiomTextField', q=True, tx=True)
    pP = []

    pP.append([str(cmds.textField('prodRulePred1', q=True, tx=True)),str(cmds.textField('prodRuleSucc1', q=True, tx=True))])

    if cmds.checkBox('prodRuleCheckBox2', q=True, value=True) == True:
        pP.append([str(cmds.textField('prodRulePred2', q=True, tx=True)),str(cmds.textField('prodRuleSucc2', q=True, tx=True))])

    if cmds.checkBox('prodRuleCheckBox3', q=True, value=True) == True:
        pP.append([str(cmds.textField('prodRulePred3', q=True, tx=True)),str(cmds.textField('prodRuleSucc3', q=True, tx=True))])
    
    if cmds.checkBox('prodRuleCheckBox4', q=True, value=True) == True:
        pP.append([str(cmds.textField('prodRulePred4', q=True, tx=True)),str(cmds.textField('prodRuleSucc4', q=True, tx=True))])
    
    pDepth = cmds.intSliderGrp('depthIntField', q=True, v=True)

    global LStringVar
    LStringVar = writeLS(pAxiom, pP, pDepth, False)
    
    cmds.textField('output', edit=True, tx=LStringVar)

def clearStringButtonAction(*pArgs):
    cmds.textField('output', edit=True, tx='')

def createGeometryButtonAction(*pArgs):

    pAngle = cmds.floatSliderGrp("angle", q=True, v=True)
    pStep = cmds.floatSliderGrp("length", q=True, v=True)
    pRad = cmds.floatSliderGrp("radius", q=True, v=True)
    subDivs = cmds.intSliderGrp("cylSubdivs", q=True, v=True)
    atenuation = cmds.floatSliderGrp("atenuation", q=True, v=True)

    if pAngle == 0 or pStep == 0 or pRad == 0 or subDivs == 0 or LStringVar == '':
        cmds.textField('warningsTextField', edit=True, tx='Please, revise all the fields again')  
    else:
        cmds.textField('warningsTextField', edit=True, tx='All is fine so far. You are doing it right.') 
        createGeometry(LStringVar, pRad, pStep, pAngle, subDivs, atenuation)

def cleanSceneButtonAction(*pArgs):
    cmds.select('segment*')
    cmds.delete()

def newScene( *pArgs ):
    '''Clears the scene file.

    On Exit  : returns an empty scene file
       
    '''
    cmds.file(f=True, new=True)
    # END #
    return 