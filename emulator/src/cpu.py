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
# EXTERNALS
# =============================================================================
import instruction



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

  """
  CPU object.
  
  The CPU object is an abstraction for the CPU internal machinery.
  """

  def __init__(self) :
    
    # Program counter init
    self.PC = 0 

    # Instruction/data memory init
    self.iMem = ["NOP" for _ in range(INSTRUCTION_MEM_SIZE)]
    self.dMem = [0 for _ in range(DATA_MEM_SIZE)]

    # Instruction pipeline init
    #self.pipeline = []

    # Work registers init
    self.W = [0 for _ in range(N_WORK_REG)]

    # Stack 
    # TODO: create a stack object?
    self.stack = []

    # Internal tools
    self.nCyclesLost = 0



  # ---------------------------------------------------------------------------
  # METHOD cpu.step()
  # ---------------------------------------------------------------------------
  def step(self) :
    """
    Makes the CPU progress of 1 clock cycle.
    """

    # 1. For each instruction: do the task of the current cycle
    # 2. Read the new instruction, check its syntax and convert it to an 
    #    Instruction object
    # 3. Call its execution function

    instr = instruction.fromTxt("NOP")


    pass



  # ---------------------------------------------------------------------------
  # METHOD cpu.setPC()
  # ---------------------------------------------------------------------------
  def setPC(self) :
    """
    Sets the PC (program counter) to a specific spot.
    Out of range values will call a hardware trap.
    """

    pass




# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'cpu' called as main: running unit tests...")

  # Example code for the instruction memory
  cpu0 = cpu()
  cpu0.IMem = [
    "NOP",
    "NOP",
    "NOP",
    "MOV 1,[0]",
    "BSET W0,1",
    "NOP",
    "MEET 1",
    "JE W0, W1",
  ]

