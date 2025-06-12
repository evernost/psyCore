# -*- coding: utf-8 -*-
# =============================================================================
# Project         : psyCore
# Module name     : instruction
# File name       : instruction.py
# File type       : Python script (Python 3.10 or higher)
# Purpose         : class definition for the 'Instruction' object
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


def registerInstructionSet(cls) :
  """
  Registration decorator to declare all the supported instructions.
  Add the code for your custom instructions here.
  """

  # ---------------------------------------------------------------------------
  # INSTRUCTION: "NOP"
  # ---------------------------------------------------------------------------
  def __instr_NOP(self) :
    
    # Number of clock cycles required for the instruction to be completed.
    # Might depend on the instruction's arguments.
    self.cycles = 1

    if (self.__cyclesRemaining > 0) :
      pass

  # Register the instruction
  cls.__instr_NOP = __instr_NOP



  # ---------------------------------------------------------------------------
  # INSTRUCTION: "JZ"
  # ---------------------------------------------------------------------------
  def __instr_JZ(self) :
    
    # Number of clock cycles required for the instruction to be completed.
    # Might depend on the instruction's arguments.
    self.cycles = 1

    if (self.__cyclesRemaining > 0) :
      pass

  # Register the instruction
  cls.__instr_JZ = __instr_JZ



  # ---------------------------------------------------------------------------
  # INSTRUCTION: "MOV"
  # ---------------------------------------------------------------------------
  def __instr_MOV(self) :
    
    # Instruction identifier
    # NOTE: the same function processes all variants of the instruction
    # - MOV number, Wx
    # - MOV Wx, Wy
    # etc.
    self.mnemonic = "MOV"

    # Number of clock cycles required for the instruction to be completed.
    # Might depend on the instruction's arguments.
    self.cycles = 1

    if (self.__cyclesRemaining > 0) :
      pass

  # Register the instruction
  cls.__instr_MOV = __instr_MOV



  return cls







@registerInstructionSet
class Instruction : 

  """
  INSTRUCTION object.
  
  The Instruction object is an abstraction for a CPU instruction.
  It describes the task carried out by the instruction and provides some 
  useful information like:
  - number of clock cycles needed
  - registers 

  It keeps track of the context for instructions that need more than one 
  clock cycle to be done.

  Usually, the instruction object is destroyed once its execution is done.
  """

  def __init__(self) :
    
    # Clock cycles needed before the result is available
    self.cycles = 1  

    # Reference to the CPU instances.
    # An instruction has full control over the internal attributes of the CPU.
    # There can be more than 1 CPU running simultenously.
    self.nCores = 1
    self.cpu = [None for _ in range(self.nCores)]

    # Arguments (populated after the specific instruction method)
    self.nArgs = 0
    self.args = {}

    # Internal parameters
    self._cyclesRemaining = self.cycles
    self._normalisedCode = ""   # Normalised string version of the instruction (all caps, proper spacing etc.)

    self._instructionSet = {}



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








# -----------------------------------------------------------------------------
# FUNCTION fromTxt()
# -----------------------------------------------------------------------------
def fromTxt(input : str) :
  """
  FACTORY FUNCTION (returns an Instruction object)
  
  Creates and initialises an instruction object from a string containing the raw
  line of code.

  It does the following:
  - normalisation
  - instruction parsing
  - argument extraction 
  - syntax check

  It parses the string, checks if the instruction exists, check if the syntax
  is valid, retrieves the parameters.

  Example: 
  > instruction.fromTxt("NOP")
  > instruction.fromTxt("nop ")
  """

  # Extract the mnemonic
  #mnemonic = getMnemonic(input)
  mnemonic = "NOP"

  # Create the instruction
  instruction = Instruction()

  # Initialise the instruction object based on the mnemonic
  if mnemonic in instructionSet :
    instructionSet[mnemonic](instruction)
  else:
    raise ValueError(f"Invalid instruction: {input}")
  
  return instruction
  
  

# =============================================================================
# INSTRUCTION SET DEFINITION
# =============================================================================


# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'instruction' called as main: running unit tests...")

  I = fromTxt("MEET 1")
