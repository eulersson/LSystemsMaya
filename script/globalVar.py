#!/usr/bin/env python
"""
    Global Variables Module:    <globalVar.py>

    I hate working with global variables in Python, maybe it's because I lack in knowledge, but I had a lot of problems
    declaring them. I wanted to have variables which are GLOBAL TO ALL THE MODULES, but as Python always passes by value,
    it creates kind of a copy of them, and the "global" word loses its meaning. I don't really know what I did in here, but
    IT WORKS, and I will keep it as it is until I realize why I am doing this or when I notice a quicker or better way.
"""
import pydoc

global plantNumber
global pathVar