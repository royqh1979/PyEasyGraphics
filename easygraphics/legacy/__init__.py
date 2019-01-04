"""
The BGI compatible module.

This module redefines the functions using the same names used in the BGI, for easily porting BGI graphics
programs to python.
"""
from .legacy import *

__all__ = legacy.__all__
