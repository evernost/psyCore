# -*- coding: utf-8 -*-
# =============================================================================
# Project         : psyCore
# Module name     : instruction
# File name       : instruction.py
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
# None.



# =============================================================================
# CONSTANTS POOL
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================

class instruction : 

  """
  INSTRUCTION object.
  
  The Instruction object is an abstraction for an actual CPU instruction.
  It describes the actual task carried out by the instruction and provides 
  some useful information like:
  - number of clock cycles needed
  - registers 
  """

  def __init__(self) :
    
    
    # Clock cycles needed before the result is available
    self.latency = 1  

    # Reference to the CPU instance.
    # An instruction has full control over the internal attributes of the CPU.
    self.cpu = None

    # Internal parameters
    self._cyclesRemaining = self.latency
    self._normalisedCode = ""   # Normalised string version of the instruction (all caps, proper spacing etc.)


  # ---------------------------------------------------------------------------
  # METHOD instruction.read()
  # ---------------------------------------------------------------------------
  def read(self, text: str) -> None :
    """
    Reads a line of code (as string) check the syntax and initialises the 
    object's attributes based on the decoded instruction
    """
    
    pass





  # ---------------------------------------------------------------------------
  # METHOD instruction.call()
  # ---------------------------------------------------------------------------
  def call(self) :
    """
    Actual definition of the instruction
    The task done may depend on the current cycle count (especially for 
    pipelined instructions)
    """
    
    pass




# ---------------------------------------------------------------------------
# FUNCTION fromTxt()
# ---------------------------------------------------------------------------
def fromTxt(input : str) :
  """
  Creates and initialises an instruction object from a string

  It parses the string, checks if the instruction exists, check if the syntax
  is valid, retrieves the parameters.

  Example: 
  > instruction.fromTxt("NOP")
  """

  return instruction()





# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'instruction' called as main: running unit tests...")

  I = fromTxt("MEET 1")
