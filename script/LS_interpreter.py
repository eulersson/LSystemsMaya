#!/usr/bin/env python
"""
    L-System Geometric Interpretation Module:    <LS_interpreter.py>

    This module reads a string of characters and performs actions in function of what they are. This will follow the turtle
    method as it's the best way to represent a bunch of characters as geometric objects, therefore, characters are treated
    as commands.
    
    The turtle can be considered as an object or instance which moves in the three-dimensional space according to the 
    executed commands. I will write below the interpretation which is given to any of the possible characters we have
    generated in the previous string (the one generated in the LS_string_rewriting module).

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
        ]    Pop the current turtlestate from the stack

        The rest of letters (AaCcDdEeGgHhIiJjKkMmNnOoPpQqRrSsTtUuVvXxYyZz) will be interpreted as move forward as well.
    
    The position and rotation are stored as parameters of the object instance, so that it is easily accessible. Both
    position and rotation will be updated each time a character is read. 
"""
import maya.cmds as cmds
import random
import math
import copy
import time

#--- SHADER AND MATERIALS DEFINITIONS ---#
def createBranchShader(rgb_branch):
    """
    It creates a shading network for the branch material. In the beginning I wanted to have a slight bump map on the
    branch surface, but then I realised it was not visually pleasing, so I left it commented just in case. It was good
    practice.

    rgb_branch:   RGB values (0-1) for the diffuse colour of the branches.

    On Exit:      Creates a Lambert node connected to a Shading Group.
    """
    import globalVar
    reload(globalVar)

    global branchMat, branchSG, fractalMap, placeTexture, bumpUtility
    # Creating Lambert Node (branch)
    branchMat = cmds.shadingNode( 'lambert', asShader=True, name='branchMat'+str(globalVar.plantNumber) ) 
    cmds.setAttr( branchMat + '.color', rgb_branch[0], rgb_branch[1], rgb_branch[2] ) 
    # Creating Shading Group (branch)
    branchSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='branchSG'+str(globalVar.plantNumber) )
    # Connecting the Lambert colour to the Shading Group's surface colour.
    cmds.connectAttr( branchMat + '.outColor', branchSG + '.surfaceShader', f=True )
    #fractalMap = cmds.shadingNode( 'fractal', asTexture=True, n='fractalMap'+str(globalVar.plantNumber) ) # Fractal Map
    #placeTexture = cmds.shadingNode( 'place2dTexture', asUtility=True, n='P2DTEX'+str(globalVar.plantNumber) ) # Place 2DText
    #cmds.connectAttr( placeTexture + '.outUV', fractalMap + '.uv', force=True ) # Connecting the UVs to the Texture
    #cmds.connectAttr (placeTexture + '.outUvFilterSize', fractalMap + '.uvFilterSize', force=True)
    #cmds.setAttr ( str(fractalMap)+'.alphaIsLuminance', True) # The white areas are understood as alpha in the fractal map
    #bumpUtility = cmds.shadingNode( 'bump2d', asUtility=True) # We create a bump utility
    #cmds.connectAttr ( fractalMap + '.outAlpha', bumpUtility + '.bumpValue', f=True) # Fractal map's alpha will drive bump
    #cmds.connectAttr ( bumpUtility + '.outNormal', branchMat + '.normalCamera', f=True)

def createLeafShader(rgb_leaf):
    """
    It creates a shading network for the leaf material.

    rgb_branch:   RGB values (0-1) for the diffuse colour of the branches.

    On Exit:      Creates a Lambert node connected to a Shading Group.
    """
    global leafMat, leafSG
    import globalVar
    reload(globalVar)

    leafMat = cmds.shadingNode( 'lambert', asShader=True, name='leafMat'+str(globalVar.plantNumber) ) # lambert node (leaf)
    cmds.setAttr( leafMat + '.color', rgb_leaf[0], rgb_leaf[1], rgb_leaf[2] )
    leafSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='leafSG'+str(globalVar.plantNumber) ) # SG
    cmds.connectAttr( leafMat + '.outColor', leafSG + '.surfaceShader', f=True )

def createBlossomShader(rgb_blossom):
    """
    It creates a shading network for the blossom material.

    rgb_branch:   RGB values (0-1) for the diffuse colour of the branches.

    On Exit:      Creates a Lambert node connected to a Shading Group which will be applied to the petals. Furthermore, two
                  non-customizable additional shaders will be created and applied to the stamen and pedicel of the blossom. 
    """
    global blossomMat, blossomSG
    import globalVar
    reload(globalVar)

    blossomPetalsMat = cmds.shadingNode( 'lambert', asShader=True, name='blossomPetalsMat'+str(globalVar.plantNumber) )
    cmds.setAttr( blossomPetalsMat + '.color', rgb_blossom[0], rgb_blossom[1], rgb_blossom[2] )
    blossomPetalsSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='blossomPetalsSG'+str(globalVar.plantNumber) )
    cmds.connectAttr( blossomPetalsMat + '.outColor', blossomPetalsSG + '.surfaceShader', f=True )

    blossomStamenMat = cmds.shadingNode( 'lambert', asShader=True, name='blossomStamenMat'+str(globalVar.plantNumber) )
    cmds.setAttr( blossomStamenMat + '.color', 0.848, 0.8484, 0.186 )
    blossomStamenSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='blossomStamenSG'+str(globalVar.plantNumber) )
    cmds.connectAttr( blossomStamenMat + '.outColor', blossomStamenSG + '.surfaceShader', f=True )

    blossomPedicelMat = cmds.shadingNode( 'lambert', asShader=True, name='blossomPedicelMat'+str(globalVar.plantNumber) )
    cmds.setAttr( blossomPedicelMat + '.color', 0, 0.494, 0 )
    blossomPedicelSG = cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name='blossomPedicelSG'+str(globalVar.plantNumber) )
    cmds.connectAttr( blossomPedicelMat + '.outColor', blossomPedicelSG + '.surfaceShader', f=True )

def applyShader(geometricObj, materialType):

    import globalVar
    reload(globalVar)

    if materialType == 'branch':
        cmds.sets( geometricObj, fe='branchSG'+str(globalVar.plantNumber) )
    if materialType == 'leaf':
        cmds.sets( geometricObj, fe='leafSG'+str(globalVar.plantNumber) )
    if materialType == 'blossomPetals':
        cmds.sets( geometricObj, fe='blossomPetalsSG'+str(globalVar.plantNumber) )
    if materialType == 'blossomStamen':
        cmds.sets( geometricObj, fe='blossomStamenSG'+str(globalVar.plantNumber) )
    if materialType == 'blossomPedicel':
        cmds.sets( geometricObj, fe='blossomPedicelSG'+str(globalVar.plantNumber) )
    
def makeSegment(pRad, pStep, posX, posY, posZ, rotX, rotY, rotZ, subDivs, indexBranch, length_atenuation,
    radius_atenuation, rgb_branch, segmentNum):
    """ Creates a step, a cylinder, representing a brach segment of the actual L-System.

        pRad :    Axiom, the initial state.
        pStep :   Production rules, set as a 2-item tuple. The first one indicates the condition and the second one the
                  value the first item should be replaced with.
        posX :    X-position we want the cylinder's origin to be.
        posY :    Y-position we want the cylinder's origin to be.
        posZ :    Z-position we want the cylinder's origin to be.
        rotX :    X-rotation we want the cylinder's origin to be.
        rotY :    X-rotation we want the cylinder's origin to be.
        rotZ :    X-rotation we want the cylinder's origin to be.
        subDivs :        Number of subdivisions for each segment (or step).
        indexBranch :    Keeps track of the level this segment lays on. Very useful for the atenuation prameters.
        length_atenuation:    Next's segment's length will be 'this value' percent the length of the previous one. But if
                              the segment is located in the same branch level as the previous one it will have the
                              dimensions of the previous one. This scales depending on which branch level you are.
        radius_atenuation:    Next's segment's radius will be 'this value' percent the radius of the previous one. But if 
                              the segment is located in the same branch level as the previous one it will have the
                              dimensions of the previous one. This scales depending on which branch level you are.
        rgb_branch:    Colour information which will be applied to a material that will shade the branches.

        On Exit : It will have created the geometry AND IT RETURNS THE POSITION OF THE LAST VERTEX.
    """
    import globalVar
    reload(globalVar)
    branchGeo = cmds.polyCylinder ( n='segment'+str(globalVar.plantNumber)+'_'+str(indexBranch)+'_'+str(segmentNum),r=pRad,
        h=pStep, sx=subDivs, sy=1, sz=1, ax=[0, 1, 0] )[0]
    print branchGeo, 'has been created.'

    cmds.xform( piv=[0,-pStep/2, 0], r=True, os=True )
    for i in range(0,indexBranch+1):
        cmds.xform( scale=[radius_atenuation,1,radius_atenuation], r=True )
        cmds.xform( scale=[1,length_atenuation,1], r=True )

    cmds.move(0, pStep/2, 0)
    cmds.makeIdentity( apply=True, t=1, r=1, s=1, n=0 )
    cmds.move( posX, posY, posZ )  
    cmds.xform( ro=[rotX, rotY, rotZ], os=True )

    #--- Apply shader to the branch ---#
    applyShader(branchGeo, 'branch')

    # TO DO: PARENT THIS BRANCH TO ITS DAD
    cmds.parent( branchGeo, 'plant' + str(globalVar.plantNumber ))
    return cmds.polyEvaluate( v = True ) # Returns the position of the last vertex, which will be the origin for next segment

def createGeometry(LStringVar, pRad, pStep, pAngle, subDivs, length_atenuation, radius_atenuation, turtleSpeed,
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
    turtleSpeed :   (in seconds) Is the time Maya will wait until placing the next segment.
    rgb_branch :    RGB values for the diffuse colour of the branches.
    rgb_leaf :      RGB values for the diffuse colour of the leaves.
    rgb_blossom :   RGB values for the diffuse colour of blossoms.

    On Exit :  Creates the geometry. Everything will be collected and parented to a group which will have the plant unique
               name with its number.
    """
    import globalVar
    reload(globalVar)

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
    
    indexBranch = 0         # keeps track of the branch level
    segmentNum = 1          # unique ID for each segment or internode

    rotationLeaves = 0      # we initialise a variable that will be useful for adding slight random rotation to the leaves
    leafNum = 1             # unique ID for each leaf

    blossomNum = 1          # unique ID for each blossoms
    
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
        elif LStringVar[i] == chr(42):  # chr(42) is *
            ROT.x += 180
            #ROT.x += (5*random.random())

        elif LStringVar[i] == 'B': # Create blossom
            # Import geometry from external file and rename it
            blossomName = "blossom_"+str(globalVar.plantNumber)+"_"+str(blossomNum)
            """ The blossoms' names will follow this template:
                    - blossom_X_Y
                Where X will be the plant number and Y the unique blossom number (ID).
            """
            cmds.file( "C:/GitHub/LSystemsMaya/script/blossom_geo.mb", i=True )
            cmds.rename( "polySurface1", blossomName )
            # Places the blossom to the right position and rotates it according to the last branch orientation
            cmds.select( blossomName )
            cmds.move( POS.x, POS.y, POS.z, r=True, os=True )
            cmds.xform( ro=flaggedSegmentRot, os=True )
            cmds.parent( blossomName, "plant"+str(globalVar.plantNumber) )
            cmds.scale( pRad, pRad, pRad )
            # We reduce a iteratively the size of the blossoms when they are in a deep level
            for i in range(0,indexBranch+1):
                cmds.scale( 0.95, 0.95, 0.95, r=True )
            # Assigns materials to petals, stamen and pedicel
            applyShader( blossomName+".f[50:109]", "blossomStamen")
            applyShader( blossomName+".f[0:49]", "blossomPedicel")
            cmds.select( blossomName+".f[*]", r=True )
            cmds.select( blossomName+".f[50:109]", deselect=True )
            cmds.select( blossomName+".f[0:49]", deselect=True )
            objectList = cmds.ls(sl=True)
            for item in objectList:
                applyShader( item, "blossomPetals")
            # Increments the blossoms counter
            blossomNum += 1

        elif LStringVar[i] == 'L': # Create leaf
            leafName = "leaf_"+str(globalVar.plantNumber)+"_"+str(leafNum)
            """ The leave's names will follow this template:
                    - leaf_X_Y
                Where X will be the plant number and Y the unique leaf number (ID).
            """
            cmds.file( "C:/GitHub/LSystemsMaya/script/leaf_geo.mb", i=True )
            cmds.rename( "pPlane1", leafName )
            # Places the leaf to the right position and rotates it according to the last branch orientation
            cmds.select( leafName )
            cmds.move( POS.x, POS.y, POS.z, r=True, os=True )
            cmds.xform( ro=flaggedSegmentRot, os=True )
            cmds.rotate( rotationLeaves%48, rotationLeaves, rotationLeaves%15, r=True, os=True )
            cmds.parent( leafName, "plant"+str(globalVar.plantNumber) )
            # Assigns the material to leaves
            applyShader(leafName, "leaf")
            cmds.scale( pRad*0.5, pRad*0.5, pRad*0.5 )
            # We reduce a iteratively the size of the leaves when they are in a deep level
            for i in range(0,indexBranch+1):
                cmds.scale( 0.85, 0.85, 0.85, r=True )
            # We change the random value for the slight rotation value we add
            rotationLeaves += random.randint(0,720)
            leafNum += 1

        elif LStringVar[i] == chr(91):   # chr(93) is [
            exec "storedPOS_%s = copy.copy(POS)" % (indexBranch)
            exec "storedROT_%s = copy.copy(ROT)" % (indexBranch)
            indexBranch +=1

        elif LStringVar[i] == chr(93):   # chr(93) is ]
            indexBranch -= 1
            exec "POS = copy.copy(storedPOS_%s)" % (indexBranch)
            exec "ROT = copy.copy(storedROT_%s)" % (indexBranch)
        else:
            # Have in mind that makeSegment apart from creating the geometry it also returns the position of the last vertex.
            lastVtx = makeSegment(pRad, pStep, POS.x, POS.y, POS.z, ROT.x, ROT.y, ROT.z, subDivs, indexBranch,
                length_atenuation, radius_atenuation, rgb_branch, segmentNum)

            import globalVar
            reload(globalVar)

            """
            I do a little trick in this part. If I changed the POS object using number additions and so on I would lose a
            lot of precision when the segment count is so great. So, what I do is query the positon for the middle top
            vertex for each segment when it is just created and update the POS instance according to this value.
            """

            POS.x = cmds.xform( 'segment%s_%s_%s.vtx[%s]' % (globalVar.plantNumber, indexBranch, segmentNum, lastVtx),
                q=True, ws=True, t=True )[0]
            POS.y = cmds.xform( 'segment%s_%s_%s.vtx[%s]' % (globalVar.plantNumber, indexBranch, segmentNum, lastVtx),
                q=True, ws=True, t=True )[1]
            POS.z = cmds.xform( 'segment%s_%s_%s.vtx[%s]' % (globalVar.plantNumber, indexBranch, segmentNum, lastVtx),
                q=True, ws=True, t=True )[2]
            
            flaggedSegment = "segment%s_%s_%s" % (globalVar.plantNumber, indexBranch, segmentNum)
            flaggedSegmentRot = cmds.xform( flaggedSegment, q=True, ro=True )

            segmentNum += 1
            if turtleSpeed != 0:
                time.sleep( turtleSpeed )
                cmds.refresh( force=True )