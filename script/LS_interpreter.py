#!/usr/bin/env python
'''
    L-System Geometric Interpretation Module:    <LS_interpreter.py>

    This module reads a string of characters and performs actions in function of what they are. This will follow the turtle
    method as it's the best way to represent a bunch of characters as geometric objects, therefore characters are treated as
    commands.
    
    The turtle can be considered as an object or instance which moves in the three-dimensional space according to the 
    executed commands. I will write below the interpretation which is given to any of the possible characters we have
    enerated in the previous string (the one generated in LS_string_rewriting).

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
        [    Push current turtle state on the stack
        ]    Pop the current turtlestate from the stack

        The rest of letters (AaCcDdEeGgHhIiJjKkMmNnOoPpQqRrSsTtUuVvXxYyZz) will be interpreted as move forward as well.
    
    The position and rotation are stored as parameters of the object instance, so that it is easily accessible. Both position
    and rotation will be updated each time a character is read. 
'''

import maya.cmds as cmds
import random
import math
import copy
import time
import LS_string_rewriting
reload(LS_string_rewriting)
import globalVar
reload(globalVar)

#--- SHADER AND MATERIALS DEFINITIONS ---#
def createBranchShader(rgb_branch):

    '''It creates a shading network for the branch material.

    rgb_branch:   RGB values for the diffuse colour of the branches.

    On Exit:      Creates a Shading Group which connects a Lambert, fractal map, 2dplace texture node and the bump.

    '''

    global branchMat, branchSG, fractalMap, placeTexture, bumpUtility
    # Creating Lambert Node (branch)
    branchMat = cmds.shadingNode( 'lambert', asShader=True, name='branchMat'+str(globalVar.plantNumber) ) 
    cmds.setAttr( branchMat + '.color', rgb_branch[0], rgb_branch[1], rgb_branch[2] ) 
    # Creating Shading Group (branch)
    branchSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='branchSG'+str(globalVar.plantNumber) )
    # Connecting the Lambert colour to the Shading Group's surface colour.
    cmds.connectAttr( branchMat + '.outColor', branchSG + '.surfaceShader', f=True )
    fractalMap = cmds.shadingNode( 'fractal', asTexture=True, n='fractalMap'+str(globalVar.plantNumber) ) # Fractal Map
    placeTexture = cmds.shadingNode( 'place2dTexture', asUtility=True, n='P2DTEX'+str(globalVar.plantNumber) ) # Place 2DText
    cmds.connectAttr( placeTexture + '.outUV', fractalMap + '.uv', force=True ) # Connecting the UVs to the Texture
    cmds.connectAttr (placeTexture + '.outUvFilterSize', fractalMap + '.uvFilterSize', force=True)
    cmds.setAttr ( str(fractalMap)+'.alphaIsLuminance', True) # The white areas are understood as alpha in the fractal map
    bumpUtility = cmds.shadingNode( 'bump2d', asUtility=True) # We create a bump utility
    cmds.connectAttr ( fractalMap + '.outAlpha', bumpUtility + '.bumpValue', f=True) # Fractal map's alpha will drive bump
    cmds.connectAttr ( bumpUtility + '.outNormal', branchMat + '.normalCamera', f=True)

def createLeafShader(rgb_leaf):

    '''It creates a shading network for the leaf material.

    rgb_leaf:   RGB values for the diffuse colour of the branches.

    On Exit:      Creates a Shading Group which connects a Lambert, fractal map, 2dplace texture node and the bump.

    '''

    global leafMat, leafSG
    leafMat = cmds.shadingNode( 'lambert', asShader=True, name='leafMat'+str(globalVar.plantNumber) ) # lambert node (leaf)
    cmds.setAttr( leafMat + '.color', rgb_leaf[0], rgb_leaf[1], rgb_leaf[2] )
    leafSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='leafSG'+str(globalVar.plantNumber) ) # shading net (leaf)
    cmds.connectAttr( leafMat + '.outColor', leafSG + '.surfaceShader', f=True )

def createBlossomShader(rgb_blossom):

    '''It creates a shading network for the branch material.

    rgb_blossom:   RGB values for the diffuse colour of the branches.

    On Exit:      Creates a Shading Group which connects a Lambert, fractal map, 2dplace texture node and the bump.

    '''

    global blossomMat, blossomSG
    blossomMat = cmds.shadingNode( 'lambert', asShader=True, name='blossomMat' ) # lambert node (blossom)
    cmds.setAttr( blossomMat + '.color', rgb_blossom[0], rgb_blossom[1], rgb_blossom[2] )
    blossomSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='blossomSG' ) # shading net (blossom)
    cmds.connectAttr( blossomMat + '.outColor', blossomSG + '.surfaceShader', f=True )

def applyShader(geometricObj, materialType):
    if materialType == 'branch':
        cmds.sets( geometricObj, fe='branchSG'+str(globalVar.plantNumber) )
    if materialType == 'leaf':
        cmds.sets( geometricObj, fe='leafSG'+str(globalVar.plantNumber) )
    if materialType == 'blossom':
        cmds.sets( geometricObj, fe='blossomSG'+str(globalVar.plantNumber) )
    
def makeSegment(pRad, pStep, posX, posY, posZ, rotX, rotY, rotZ, subDivs, indexBranch, length_atenuation, radius_atenuation,
    rgb_branch):

    """ Creates a step, a cylinder, representing a brach segment of the actual L-System.

        pRad :    Axiom, the initial state.
        pStep :   Production rules, set as a 2-item tuple. The first one indicates the condition and the second one the value
                  the first item should be replaced with.
        posX :    X-position we want the cylinder's origin to be.
        posY :    Y-position we want the cylinder's origin to be.
        posZ :    Z-position we want the cylinder's origin to be.
        rotX :    X-rotation we want the cylinder's origin to be.
        rotY :    X-rotation we want the cylinder's origin to be.
        rotZ :    X-rotation we want the cylinder's origin to be.
        subDivs :        Number of subdivisions for each segment (or step).
        indexBranch :    Keeps track of the level this segment lays on. Very useful for the atenuation prameters.
        length_atenuation:    Next's segment's length will be 'this value' percent the length of the previous one. But if the
                              segment is located in the same branch level as the previous one it will have the dimensions of
                              the previous one. This scales depending on which branch level you are.
        radius_atenuation:    Next's segment's radius will be 'this value' percent the radius of the previous one. But if the
                              segment is located in the same branch level as the previous one it will have the dimensions of
                              the previous one. This scales depending on which branch level you are.
        rgb_branch:    Colour information which will be applied to a material that will shade the branches.

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
    cmds.parent(branchGeo, 'plant' + str(globalVar.plantNumber))
    return cmds.polyEvaluate(v = True)

def createGeometry(LStringVar, pRad, pStep, pAngle, subDivs, length_atenuation, turtleSpeed, radius_atenuation,
    rgb_branch, rgb_leaf, rgb_blossom):
    """ Translates the string into maya commands in order to generate the final LSystem plant.

    LStringVar :    The L-System-generated string which will be interpreted by the turtle.
    pRad :          The radius of the segments left by each turtle's step.
    pStep :         The length of the segments left by each turtle's step.
    pAngle :        The turtle will yaw, roll or pitch by this angular amount each time it finds its corresponding  symbol.
    subDivs :       Number of subdivisions for each segment (or step).
    length_atenuation :     Next's segment's length will be 'this value' percent the length of the previous one. But if the
                           segment is located in the same branch level as the previous one it will have the dimensions of
                           the previous one. This scales depending on which branch level you are.
    radius_atenuation :    Next's segment's radius will be 'this value' percent the radius of the previous one. But if the
                           segment is located in the same branch level as the previous one it will have the dimensions of
                           the previous one. This scales depending on which branch level you are.
    rgb_branch :    RGB values for the diffuse colour of the branches.
    rgb_leaf :      RGB values for the diffuse colour of the leaves.
    rgb_blossom :   RGB values for the diffuse colour of blossoms.




    On Exit :  Creates the geometry.
    """
    cmds.group( em=True, name='plant'+str(globalVar.plantNumber) )

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
            #ROT.x += (5*random.random())
        elif LStringVar[i] == chr(45):   # chr(43) is -
            ROT.x -= pAngle
            #ROT.x += (5*random.random())
        elif LStringVar[i] == chr(38):   # chr(38) is &
            ROT.z += pAngle
            #ROT.z += (5*random.random())
        elif LStringVar[i] == chr(94):   # chr(94) is ^
            ROT.z -= pAngle
            #ROT.z += (5*random.random())
        elif LStringVar[i] == chr(60):   # chr(47) is <
            ROT.y += pAngle
            #ROT.y += (5*random.random())
        elif LStringVar[i] == chr(62):   # chr(92) is >
            ROT.y -= pAngle
            #ROT.y += (5*random.random())
        elif LStringVar[i] == chr(124):  # chr(124) is |
            ROT.x += 180
            #ROT.x += (5*random.random())
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
            if turtleSpeed != 0:
                print turtleSpeed
                time.sleep(turtleSpeed)
                cmds.refresh(force=True)
            # atenuation -= 0.05
    globalVar.plantNumber += 1

def createAnimation(keyEvery, angleVar):
    pass #TO DO