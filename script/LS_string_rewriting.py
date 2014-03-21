#!/usr/bin/env python
'''
    L-System String Rewriting Module:    <LS_string_rewriting.py>

    This module will generate a text string which later will  be used by the interpreter module to
    generate all the geometry according to certain conventions.

    Fix issues:
        - The probabilities are forced to be integers, a way to operate with float could improve it.
'''

import maya.cmds as cmds
import random
import math
import copy
import LS_interpreter
reload(LS_interpreter)

def writeLS(pW, pP, pDepth):

    ''' Iterates through the string. It will create a global string variable called "result" which is a
        concatenation of various additions done when reading the Axiom or Word entered by the user (W).

        pW :      Axiom, the initial state.
        pP:       Number of production rules. Production rules are used to replace letters by another
                  sequence of them. For instance 'F --> F+F-F' means if you find an F, replace it by
                  F+F-F. You don't need to know the meaning of the symbols yet, just get the idea.
                  LSystems on their own are not more than that, a set of rules which iterate recursively.
                  They are set as a 3-item tuple. The first one indicates the probability for this rule
                  to apply. The second one is the letter that must be replaced and the third one, the
                  content to be replaced with. (We can have multiple rules which apply for a same
                  letter, that's why we take into account the percentages --> Stochastic).
        pDepth :  Recursive index or number of iterations over the string.

        On Exit : Will return a result string. Thus it is recommendable binding the call to a variable.

        For example:
            >>> W = 'F'                            # The initial word. It is properly called Axiom
            >>> pPNum = 1                          # We will have just one production rule
            >>> P = [100, 'F', 'F[+F]F[-F]F']      # Means: ALWAYS when you find 'F', replace it with ~
            >>> depth = 1                          # Depth of the procedure, number of iterations
            >>> variable1 = writeLS(W, pPNum, P, depth) 
                                                   # Binds the return value to a variable...
            >>> print variable1                    # ... which now is printed
            F[+F]F[-F]F
            >>>

        As we have seen here above ^ we started with an initial axiom F, and it has been replaced
        following a production rule.

        If the depth increases we carry the recursion one step further:
            >>> W = 'F'
            >>> pPNum = 1
            >>> P = [100, 'F', 'F[+F]F[-F]F']
            >>> depth = 2
            >>> variable2 = writeLS(W, pPNum, P, depth)
            >>> print variable2
            F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]F[-F]F
            >>>

        This last example would be the same as we run writeLS(variable1, pPNum, P, depth), that is to say,
        it is the same as running again the procedure over the generated string in the previous example.
    '''
    if pDepth == 0:
        return pW

    else:
        tempList = ''
        coincidence = []
        for i in range(0, len(pW)):    # Search for coincidences in the string
            for j in range(0, len(pP)):
                if pW[i] == pP[j]:
                    coincidence.append([i,j])    # Appends the index of the string in which the rule applies and the rule index

            if len(coincidence) == 0:    # If coincidence is empty
                pass
            elif len(coincidence) == 1:
                pW.replace(coincidence[0][0],pP[coincidence[0][1])
            else:
                tempList += pW[:coincidence[0][0]] # Add tp the temp list what we have before the 1st coincidence
                choiceList = []
                for item in coincidence:
                    choiceList.append(int(pP[0])*[pP[j][1],pP[j][2]])
                pickedRule = random.choice(choiceList)
                tempList += pickedRule[1]
        pW = tempList
        return writeLS(pW, pP, pDepth-1)


'''
    if pDepth == 0:
        return pW
    else:
        tempList = ''
        for i in range(0,len(pW)):
            for j in range(0,len(pP)):
                if pW[i] == pP[j][1]:
                    tempList += pP[j][2]
                    replacingDone = True
                    break
            if replacingDone == False:
                tempList += pW[i]
            replacingDone = False
        pW = tempList
        return 'writeLS(pW, pPNum, pP, pDepth-1, replacingDone)'
'''