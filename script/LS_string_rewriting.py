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
            >>> P = [100, 'F', 'F[+F]F[-F]F']      # Means: ALWAYS when you find 'F', replace it with ~
            >>> depth = 1                          # Depth of the procedure, number of iterations
            >>> string = writeLS(W, pPNum, P, depth) 
                                                   # Binds the return value to a variable...
            >>> print string                       # ... which now is printed
            F[+F]F[-F]F
            >>>

        As we have seen here above ^ we started with an initial axiom F, and it has been replaced
        following a production rule.

        If the depth increases we carry the recursion one step further:
            >>> W = 'F'
            >>> P = [100, 'F', 'F[+F]F[-F]F']
            >>> depth = 2
            >>> string = writeLS(W, pPNum, P, depth)
            >>> print string
            F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]F[-F]F
            >>>

        This last example would be the same as we run writeLS(variable1, pPNum, P, depth), that is to say,
        it is the same as running again the procedure over the generated string in the previous example.

        This script also accepts more than one rule. Let's see an example if we had 2 rules.
            >>> W = 'F+X-FF'
            >>> P = [[100, 'F', 'ff'], [100, 'X', 'xx']]
            >>> depth = 1
            >>> string = writeLS(W, pPNum, P, depth)
            >>> print string
            ff+xx-ffff
            >>>

        The way I worked out the probabilities is quite odd. We know a rule is specified X --> YY,
        so what I did is I appended in a list the right hand side of the rule TIMED by the
        percentage number the user wrote. For instance if we had [70, 'X', 'YY'] (70% chance for X
        to be replaced with YY) and [30, 'X', 'ZZ'] (30% chance for X to be replaced with ZZ),
        I collect in the "choiceList" a bunch of 'ZZ' items and 'YY' items. In this particular case I
        would have seventy 'YY's and thirty 'ZZ's. Now If I pick an random value between 0-100 I
        can access randomly an element in this list. So as we have many more 'YY's we will have
        more possibility to pick one. The bad things of this method are two:

            - Performancewise it takes quite a lot of memory.
            - I cannot work with floating point values given that array index must be integers. I
            could get more precise results if I make the list instead of being 100 items long, 1000.
    '''

    if pDepth == 0:
        return pW

    else:
        tempList = ''
        for i in range(0, len(pW)): # Search for coincidences in the string
            coincidence = []
            for j in range(0, len(pP)):
                if pW[i] == pP[j][1]: # IF the current letter matches any of the rule cases...
                    coincidence.append([i,j]) # Appends the index of the string in which the rule
                                              # satisfies and the rule index

            if len(coincidence) == 0: # IF coincidence is empty
                tempList += pW[i] # Just add the current character
            elif len(coincidence) == 1: # ELSE IF it finds just one coincidence
                tempList += pP[coincidence[0][1]][2] # Add the right hand side content of the rule.
            else:
            #--- Working out the probabilities ---#
                choiceList = []
                for item in coincidence:
                    choiceList.append(int(pP[item[j]][0]) * [pP[item[j]][2]])
                flattenedList = [] # As we get a multidimensional array I must flatten it to 1D in
                                   # order to pick an item just using one single index
                for item in choiceList:
                    flattenedList.extend(item)
                randomIndex = random.randint(0, len(flattenedList))
                tempList += flattenedList[randomIndex]
        pW = tempList
        return writeLS(pW, pP, pDepth-1) # Recursive call