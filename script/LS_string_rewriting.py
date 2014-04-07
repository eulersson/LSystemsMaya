#!/usr/bin/env python
'''
    L-System String Rewriting Module:            <LS_string_rewriting.py>

    This module will generate a text string which later will  be used by the interpreter module to generate all the geometry
    according to certain conventions.

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

    ''' Iterates through the string. It will create a global string variable called "result" which is a concatenation of
    various additions done when reading the Axiom or Word entered by the user (W).

        pW :      Axiom, the initial state.
        pP:       Number of production rules. Production rules are used to replace letters by another sequence of them. For
                  instance 'F --> F+F-F' means if you find an F, replace it by F+F-F. You don't need to know the meaning of
                  the symbols yet, just get the idea. LSystems on their own are not more than that, a set of rules which
                  iterate recursively. They are set as a 3-item tuple. The first one indicates the probability for this rule
                  to apply. The second one is the letter that must be replaced and the third one, the content to be replaced
                  with. (We can have multiple rules which apply for a same letter, that's why we take into account the
                  percentages --> Stochastic).
        pDepth :  Recursive index or number of iterations over the string.

        On Exit : Will return a result string. Thus it is recommendable binding the call to a variable.

        For example:
            >>> W = 'F'                            # The initial word. It is properly called Axiom
            >>> P = [100, 'F', 'F[+F]F[-F]F']      # Means: ALWAYS when you find 'F', replace it with ~
            >>> depth = 1                          # Depth of the procedure, number of iterations
            >>> string = writeLS(W, P, depth) 
                                                   # Binds the return value to a variable...
            >>> print string                       # ... which now is printed
            F[+F]F[-F]F
            >>>

        As we have seen here above^ we started with an initial axiom F, and it has been replaced following a production rule.

        If the depth increases we carry the recursion one step further:
            >>> W = 'F'
            >>> P = [100, 'F', 'F[+F]F[-F]F']
            >>> depth = 2
            >>> string = writeLS(W, P, depth)
            >>> print string
            F[+F]F[-F]F[+F[+F]F[-F]F]F[+F]F[-F]F[-F[+F]F[-F]F]F[+F]F[-F]F
            >>>

        This last example would be the same as we run writeLS(variable1, pPNum, P, depth), that is to say, it is the same as
        running again the procedure over the generated string in the previous example.

        This script also accepts more than one rule. Let's see an example if we had 2 rules.
            >>> W = 'F+X-FF'
            >>> P = [[100, 'F', 'ff'], [100, 'X', 'xx']]
            >>> depth = 1
            >>> string = writeLS(W, P, depth)
            >>> print string
            ff+xx-ffff
            >>>

        The way I worked out the probabilities is quite odd. We know a rule is specified X --> YY, so what I did is I
        appended in a list the right hand side of the rule TIMED by the percentage number the user wrote. For instance if we
        had [70, 'X', 'YY'] (70% chance for X to be replaced with YY) and [30, 'X', 'ZZ'] (30% chance for X to be replaced
        with ZZ), I collect in the "choiceList" a bunch of 'ZZ' items and 'YY' items. In this particular case I would have
        seventy 'YY's and thirty 'ZZ's. Now If I pick an random value between 0-100 I can access randomly an element in this
        list. So as we have many more 'YY's we will have more possibility to pick one. The bad things of this method are two:

            - Performancewise it takes quite a lot of memory.
            - I cannot work with floating point values given that array index must be integers. I could get more precise
            results if I make the list instead of being 100 items long, 1000.
    '''

    if pDepth == 0:
        return pW

    else:
        tempList = ''
        for i in range(0, len(pW)): # Search for coincidences in the string
            coincidence = []
            for j in range(0, len(pP)):
                if pW[i] == pP[j][1]: # IF the current letter matches any of the rule cases... p[X][1] is the predecessor
                    coincidence.append([i,j]) # Appends the index of the string where rule satisfies and the rule index
            """
            For example:
            >>> word = 'F+FX+FF'
            >>> rules = [ [50, 'F', 'GF'],
                          [50, 'F', 'ff'] ]
            What will happen is that we will go over each character of the word and compare to the rules. Let's do it. We
            start with word[0] which is 'F'. We will compare it to ALL the predecessors to see if they are the same. So, as
            word[0] is the same char as rules[0][1] we will add in the coincidence array the touple [0,0], which can be
            understood as "We have found a coincidence in word[X] matching the rule[Y]".
            """
            if len(coincidence) == 0: # IF coincidence is empty
                tempList += pW[i] # Just add the current character
            elif len(coincidence) == 1: # ELSE IF it finds just one coincidence
                tempList += pP[coincidence[0][1]][2] # Add the right hand side content (sucessor) of the rule.
            else:
                '''
                WORKING OUT THE PROBABILITIES
                This is the most complicated part. To work out the percentages I do it using a rudimentary way. I create a
                a list, called choiceList. Then I iterate over the coincidence list we created before which contains all the
                rule matchings. Refer back to the previous explanation if you don't know what I am talking about. It is
                rudimentary because what I put in the choiceList the successors of the rules multiple times in the array.
                
                Let me explain myself with a simple example:
                >>> word = 'F'
                >>> rules = [ [30, 'F', 'P'],
                              [70, 'F', 'Q'] ]
                
                Imagine we were in this case. choiceList would be an array containing 30 times the item 'P' and 70 times the
                element 'Q'. So it would be huge.

                    choiceList --> [['P','P','P', ...thirty times...],['Q','Q','Q','Q','Q','Q','Q', ...seventy times...]]
                
                Then I flatten the list so that I have a one-dimensional array:

                    flattenedList --> ['P','P','P',...thirty items...,'Q','Q','Q','Q','Q','Q','Q',...seventy times...]

                Now it is so easy because I pick a random number between 0 and the length of the array which will be used to
                select the successor.
                '''
                choiceList = []

                for k in range(0,len(coincidence)):
                    choiceList.append(int(pP[coincidence[k][1]][0]) * [pP[coincidence[k][1]][2]])

                flattenedList = [] # As we get a multidimensional array I must flatten it to 1D in order to pick an item just using one single index
                for item in choiceList:
                    flattenedList.extend(item)
                # We pick one of the possible sucessors and we carry on
                randomIndex = random.randint(0, len(flattenedList))
                tempList += flattenedList[randomIndex]
                
        pW = tempList
        return writeLS(pW, pP, pDepth-1) # Recursive call