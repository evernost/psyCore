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



# =============================================================================
# CONSTANTS POOL
# =============================================================================
INSTRUCTION_MEM_SIZE = 1024
DATA_MEM_SIZE = 1024

PIPELINE_SIZE = 5

N_WORK_REG = 16



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class cpu :

  def __init__(self) :
    
    # Program counter init
    self.pc = 0 

    # Instruction/data memory init
    self.iMem = ["NOP" for _ in range(INSTRUCTION_MEM_SIZE)]
    self.dMem = ["NOP" for _ in range(DATA_MEM_SIZE)]

    # Instruction pipeline init
    self.pipeline = []

    # Work registers init
    self.W = [0 for _ in range(N_WORK_REG)]



  # ---------------------------------------------------------------------------
  # METHOD cpu.step()
  # ---------------------------------------------------------------------------
  def step(self) :
    """
    Reads the next instruction
    """


    # 1. For each instruction: do the task of the current cycle
    # 2. Read the new instruction, check its syntax and convert it to an 
    #    Instruction object
    # 3. Call its execution function


    pass




# Example code for the instruction memory
cpu0 = cpu()
cpu0.IMem = [
  "MOV 1,[0]",
  "BSET W0,1",
  "NOP",
  "MEET 1"
]

