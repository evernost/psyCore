# -*- coding: utf-8 -*-
# =============================================================================
# Project         : psyCore
# Module name     : cpu
# File name       : cpu.py
# File type       : Python script (Python 3.10 or higher)
# Purpose         : 
# Author          : QuBi (nitrogenium@outlook.fr)
# Creation date   : May 22nd, 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# Description is TODO.



class cpu:

  def __init__(self) :
    self.pc = 0  # Indicates where the CPU is currently at




# Example code for the instruction memory
cpu0 = cpu()
cpu0.IMem = [
  instruction.txt("MOV 1,[0]"),
  instruction.txt("BSET W0,1"),
  instruction.txt("NOP"),
  instruction.txt("MEET 1")
]

