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

#--- SHADER AND MATERIALS DEFINITIONS ---#
def createBranchShader(rgb_branch): # It creates a shading network for the branch material.
    global branchMat, branchSG, fractalMap, placeTexture, bumpUtility
    branchMat = cmds.shadingNode( 'lambert', asShader=True, name='branchMat' ) # lambert node (branch)
    cmds.setAttr( branchMat + '.color', rgb_branch[0], rgb_branch[1], rgb_branch[2] ) 
    branchSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='branchSG' ) # shading net (branch)
    cmds.connectAttr( branchMat + '.outColor', branchSG + '.surfaceShader', f=True )
    fractalMap = cmds.shadingNode( 'fractal', asTexture=True ) # fractal map
    placeTexture = cmds.shadingNode( 'place2dTexture', asUtility=True ) # place texture
    cmds.connectAttr( placeTexture + '.outUV', fractalMap + '.uv', force=True )
    cmds.connectAttr (placeTexture + '.outUvFilterSize', fractalMap + '.uvFilterSize', force=True)
    cmds.setAttr ( 'fractal1.alphaIsLuminance', True)
    bumpUtility = cmds.shadingNode( 'bump2d', asUtility=True) # bump utility
    cmds.connectAttr (fractalMap + '.outAlpha', bumpUtility + '.bumpValue', f=True)
    cmds.connectAttr ( bumpUtility + '.outNormal', branchMat + '.normalCamera', f=True)

def createLeafShader(rgb_leaf): # It creates a shading network for the leaf material.
    global leafMat, leafSG
    leafMat = cmds.shadingNode( 'lambert', asShader=True, name='leafMat' ) # lambert node (leaf)
    cmds.setAttr( leafMat + '.color', rgb_leaf[0], rgb_leaf[1], rgb_leaf[2] )
    leafSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='leafSG' ) # shading net (leaf)
    cmds.connectAttr( leafMat + '.outColor', leafSG + '.surfaceShader', f=True )

def createBlossomShader(rgb_blossom): # It creates a shading network for the blossom material.
    global blossomMat, blossomSG
    blossomMat = cmds.shadingNode( 'lambert', asShader=True, name='blossomMat' ) # lambert node (blossom)
    cmds.setAttr( blossomMat + '.color', rgb_blossom[0], rgb_blossom[1], rgb_blossom[2] )
    blossomSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='blossomSG' ) # shading net (blossom)
    cmds.connectAttr( blossomMat + '.outColor', blossomSG + '.surfaceShader', f=True )

def applyShader(geometricObj, materialType):
    if materialType == 'branch':
        cmds.sets( geometricObj, fe='branchSG' )
    if materialType == 'leaf':
        cmds.sets( geometricObj, fe='leafSG' )
    if materialType == 'blossom':
        cmds.sets( geometricObj, fe='blossomSG' )
    
def makeSegment(pRad, pStep, posX, posY, posZ, rotX, rotY, rotZ, subDivs, indexBranch, length_atenuation, radius_atenuation, rgb_branch):
    """ Creates a step, a cylinder, representing a brach segment of the actual L-System.

        pW :      Axiom, the initial state.
        pP :      Production rules, set as a 2-item tuple. The first one indicates the condition and the
                  second one the value the first item should be replaced with.
        pDepth :  Recursive index.
        On Exit : Will return a result string. Thus it is recommendable binding the call to a variable.
    """
    branchGeo = cmds.polyCylinder (n='segment#',r=pRad, h=pStep, sx=subDivs, sy=1, sz=1, ax=[0, 1, 0])[0]
    cmds.xform(piv=[0,-pStep/2, 0], r=True, os=True)
    for i in range(0,indexBranch+1):
        cmds.xform(scale=[length_atenuation,length_atenuation,length_atenuation], r=True)
    cmds.move(0, pStep/2, 0)
    cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
    cmds.move(posX, posY, posZ)  
    cmds.xform(ro=[rotX, rotY, rotZ], os=True)

    #--- Apply shader to the branch ---#
    applyShader(branchGeo, 'branch')

    # TO DO: PARENT THIS BRANCH TO ITS DAD
    cmds.parent(branchGeo, 'plant')
    return cmds.polyEvaluate(v = True)

def createGeometry(LStringVar, pRad, pStep, pAngle, subDivs, length_atenuation, radius_atenuation, rgb_flowers, rgb_leaves, rgb_branch):
    """ Translates the string into maya commands in order to generate the final LSystem plant.
    
    pStep :   Axiom, the initial state.
    pAngle :  Production rules, set as a 2-item tuple. The first one indicates the condition and the
              second one the value the first item should be replaced with.
    pDepth :  Recursive index.
    On Exit : Creates the geometry.
    """

    cmds.group( em=True, name='plant')

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
    
    for i in range(0,len(LStringVar)):
        if LStringVar[i] == chr(43):     # chr(43) is +
            ROT.x += pAngle
            ROT.x += (5*random.random())
        elif LStringVar[i] == chr(45):   # chr(43) is -
            ROT.x -= pAngle
            ROT.x += (5*random.random())
        elif LStringVar[i] == chr(38):   # chr(38) is &
            ROT.z += pAngle
            ROT.z += (5*random.random())
        elif LStringVar[i] == chr(94):   # chr(94) is ^
            ROT.z -= pAngle
            ROT.z += (5*random.random())
        elif LStringVar[i] == chr(60):   # chr(47) is <
            ROT.y += pAngle
            ROT.y += (5*random.random())
        elif LStringVar[i] == chr(62):   # chr(92) is >
            ROT.y -= pAngle
            ROT.y += (5*random.random())
        elif LStringVar[i] == chr(124):  # chr(124) is |
            ROT.x += 180
            ROT.x += (5*random.random())
        elif LStringVar[i] == chr(91):   # chr(93) is [
            exec "storedPOS_%s = copy.copy(POS)" % (indexBranch)
            exec "storedROT_%s = copy.copy(ROT)" % (indexBranch)
            indexBranch +=1
        elif LStringVar[i] == chr(93):   # chr(93) is ]
            indexBranch -= 1
            exec "POS = copy.copy(storedPOS_%s)" % (indexBranch)
            exec "ROT = copy.copy(storedROT_%s)" % (indexBranch)
        else:
            lastVtx = makeSegment(pRad, pStep, POS.x, POS.y, POS.z, ROT.x, ROT.y, ROT.z, subDivs, indexBranch, length_atenuation, radius_atenuation, rgb_branch)
            POS.x = cmds.xform('segment%s.vtx[%s]' % (segment, lastVtx), q=True, ws=True, t=True)[0]
            POS.y = cmds.xform('segment%s.vtx[%s]' % (segment, lastVtx), q=True, ws=True, t=True)[1]
            POS.z = cmds.xform('segment%s.vtx[%s]' % (segment, lastVtx), q=True, ws=True, t=True)[2]
            segment += 1
            # atenuation -= 0.05