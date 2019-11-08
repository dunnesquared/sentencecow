"""Module to ensure that application modules are successfully found by nose
testing framework.
"""

import os
import sys

# As the first item in the sys.path list, add an entry for legsewoc directory
# os.path.dirname(__file__) == directory where context.py resides
# The last arguemnt in the function call basically says you need to go
# up to the parent directory (../) and then open the legsewoc directory
# (legsewoc/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                '../legsewoc/')))

# Import everything you're going to need for the test modules to run properly.
# Make sure to "from MODULE import .context" in each test file.
import textanalysis
import leguincounter
import app
