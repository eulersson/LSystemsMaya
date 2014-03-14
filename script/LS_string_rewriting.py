#!/usr/bin/env python
'''
    L-System String Rewriting Module:    "LS_string_rewriting.py"
'''

import maya.cmds as cmds
import random
import math
import copy
import LS_interpreter
reload(LS_interpreter)

def writeLS(pW, pP, pDepth, replacingDone):

    """ Iterates through the string. It will create a global string variable called "result" which is a
        concatenation of various additions done when reading the Axiom or Word entered by the user (W).

        pW :      Axiom, the initial state.
        pP :      Production rules, set as a 2-item tuple. The first one indicates the condition and the
                  second one the value the first item should be replaced with.
        pDepth :  Recursive index.
        On Exit : Will return a result string. Thus it is recommendable binding the call to a variable.

        For example:
            >>> W = 'F'                           # The initial word. It is properly called Axiom.
            >>> P = ['F', 'F[+F]F[-F]F']          # Means: When you find 'F', replace it with
            >>> depth = 1                         # Depth of the procedure, number of iterations
            >>> variable1 = writeLS(W, P, depth)   # Binds the return value to a variable...
            >>> print variable1                    # ... which now is printed
            F[+F]F[-F]F
            >>>

        If the depth increases we carry the recursion one step further:
            >>> W = 'F'                           # The initial word. It is properly called Axiom.
            >>> P = ['F', 'F[+F]F[-F]F']          # Means: When you find 'F', replace it with
            >>> depth = 2                         # Depth of the procedure, number of iterations
            >>> variable2 = writeLS(W, P, depth)   # Binds the return value to a variable...
            >>> print variable2                    # ... which now is printed
            F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]F[-F]F
            >>>

        This last example would be the same as we run writeLS(variable1, P, depth), that is to say,
        it is the same as running again the procedure over the generated string in the previous example.
    """
    if pDepth == 0:
        return pW
    else:
        tempList = ''
        for i in range(0,len(pW)):
            for j in range(0,len(pP)):
                if pW[i] == pP[j][0]:
                    tempList += pP[j][1]
                    replacingDone = True
                    break
            if replacingDone == False:
                tempList += pW[i]
            replacingDone = False
        pW = tempList
        return writeLS(pW, pP, pDepth-1, replacingDone)