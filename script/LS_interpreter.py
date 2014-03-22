#!/usr/bin/env python
'''
    L-System Geometric Interpretation Module:    <LS_interpreter.py>
'''

import maya.cmds as cmds
import random
import math
import copy
import LS_string_rewriting
reload(LS_string_rewriting)

def makeSegment(pRad, pStep, posX, posY, posZ, rotX, rotY, rotZ, subDivs, atenuation, indexBranch):
    """ Creates a step, a cylinder, representing a brach segment of the actual L-System.

        pW :      Axiom, the initial state.
        pP :      Production rules, set as a 2-item tuple. The first one indicates the condition and the
                  second one the value the first item should be replaced with.
        pDepth :  Recursive index.
        On Exit : Will return a result string. Thus it is recommendable binding the call to a variable.
    """
    cmds.polyCylinder (n='segment#',r=pRad, h=pStep, sx=subDivs, sy=1, sz=1, ax=[0, 1, 0])
    cmds.xform(piv=[0,-pStep/2, 0], r=True, os=True)
    for i in range(0,indexBranch+1):
        cmds.xform(scale=[atenuation,atenuation,atenuation], r=True)
    cmds.move(0, pStep/2, 0)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.move(posX, posY, posZ)  
    cmds.xform(ro=[rotX, rotY, rotZ], os=True)
    # TO DO: PARENT THIS BRANCH TO ITS DAD
    return cmds.polyEvaluate(v = True)

def createGeometry(LSysString, pRad, pStep, pAngle, subDivs, atenuation):
    """ Translates the string into maya commands in order to generate the final LSystem plant.
    
    pStep :   Axiom, the initial state.
    pAngle :  Production rules, set as a 2-item tuple. The first one indicates the condition and the
              second one the value the first item should be replaced with.
    pDepth :  Recursive index.
    On Exit : Creates the geometry.
    """
    if cmds.objExists('segment1'):
        cmds.select('segment*')
        cmds.delete()

    class position:
        x = 0
        y = 0
        z = 0
    POS = position()
    class rotation:
        x = 0
        y = 0
        z = 0
    ROT = rotation()
    indexBranch = 0
    segment = 1
    
    for i in range(0,len(LSysString)):
        if LSysString[i] == chr(43):     # chr(43) is +
            ROT.x += pAngle
            ROT.x += (5*random.random())
        elif LSysString[i] == chr(45):   # chr(43) is -
            ROT.x -= pAngle
            ROT.x += (5*random.random())
        elif LSysString[i] == chr(38):   # chr(38) is &
            ROT.z += pAngle
            ROT.z += (5*random.random())
        elif LSysString[i] == chr(94):   # chr(94) is ^
            ROT.z -= pAngle
            ROT.z += (5*random.random())
        elif LSysString[i] == chr(60):   # chr(47) is <
            ROT.y += pAngle
            ROT.y += (5*random.random())
        elif LSysString[i] == chr(62):   # chr(92) is >
            ROT.y -= pAngle
            ROT.y += (5*random.random())
        elif LSysString[i] == chr(124):  # chr(124) is |
            ROT.x += 180
            ROT.x += (5*random.random())
        elif LSysString[i] == chr(91):   # chr(93) is [
            exec "storedPOS_%s = copy.copy(POS)" % (indexBranch)
            exec "storedROT_%s = copy.copy(ROT)" % (indexBranch)
            indexBranch +=1
        elif LSysString[i] == chr(93):   # chr(93) is ]
            indexBranch -= 1
            exec "POS = copy.copy(storedPOS_%s)" % (indexBranch)
            exec "ROT = copy.copy(storedROT_%s)" % (indexBranch)
        else:
            lastVtx = makeSegment(pRad, pStep, POS.x, POS.y, POS.z, ROT.x, ROT.y, ROT.z, subDivs, atenuation, indexBranch)
            POS.x = cmds.xform('segment%s.vtx[%s]' % (segment, lastVtx), q=True, ws=True, t=True)[0]
            POS.y = cmds.xform('segment%s.vtx[%s]' % (segment, lastVtx), q=True, ws=True, t=True)[1]
            POS.z = cmds.xform('segment%s.vtx[%s]' % (segment, lastVtx), q=True, ws=True, t=True)[2]
            segment += 1
            # atenuation -= 0.05