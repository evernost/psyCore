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

  def __init__(self, text: str) :
    
    # Clock cycles needed before the result is available
    self.cycles = 1  

    # Populated after a Instruction._decode()
    self.handler = None
    self.mnemonic = ""
    self.addr = 0

    # Reference to the CPU instances.
    # An instruction has full control over the internal attributes of the CPU.
    # There can be more than 1 CPU running simultenously.
    self.nCores = 1
    self.cpu = []
    self.cpuID = 0

    # Arguments (populated after the specific instruction method)
    self.nArgs = 0
    self.args = []

    # Internal parameters
    self._cyclesRemaining = self.cycles
    self._normalisedCode = ""   # Normalised string version of the instruction (all caps, proper spacing etc.)

    # Declare the instruction set recognized by the CPU.
    # Instructions must be declared in the dictionary as a pair:
    # - key   : mnemonic (string)
    # - value : pointer to the custom init function 
    # These functions are like extensions of the original __init__() method.
    self._instructionSet = {
      # Data transfer 
      "MOV"   : self.__init_MOV,
      
      # Conditions
      "JZ"    : self.__init_JZ,
      
      # Context save/restore
      "SCTX"  : self.__init_SCTX,
      "RCTX"  : self.__init_RCTX,

      # Synchronisation (multi-CPU context)
      "LOC"   : self.__init_LOC,
      "MEET"  : self.__init_MEET,
      
      # Hardware instructions
      "NOP"   : self.__init_NOP,
      "RESET" : self.__init_RESET
    }

    # Try to decode the instruction
    # (possible now that the instruction has context)
    self._decode(text)



  # ---------------------------------------------------------------------------
  # METHOD instruction._decode()
  # ---------------------------------------------------------------------------
  def _decode(self, text: str) -> None :
    """
    Reads a line of code (as string) check the syntax and initialises the 
    object's attributes based on the decoded instruction

    
    It does the following:
    - normalisation
    - instruction parsing
    - address extraction (if any)
    - argument extraction (if any) 
    - syntax check
    
    It parses the string, checks if the instruction exists, check if the syntax
    is valid, retrieves the parameters.

    Example: 
    > instruction.fromTxt("NOP")
    > instruction.fromTxt("nop ")
    """
    
    pass

    # # Extract the mnemonic
    # #mnemonic = getMnemonic(input)
    # mnemonic = "NOP"

    # # Create the instruction
    # instruction = Instruction()

    # # Initialise the instruction object based on the mnemonic
    # if mnemonic in instructionSet :
    #   instructionSet[mnemonic](instruction)
    # else:
    #   raise ValueError(f"Invalid instruction: {input}")
    
    # return instruction



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



# =============================================================================
# INSTRUCTION SET DEFINITION
# =============================================================================

  # ---------------------------------------------------------------------------
  # INSTRUCTION: "NOP"
  # ---------------------------------------------------------------------------
  def __init_NOP(self) :
    """
    NOP (No OPeration)

    Does nothing for 1 clock cycle.
    Registers are reset.
    """
    
    # Instruction properties
    self.mnemonic = "MOV"
    self.handler = self.__instr_NOP

    self.cycles = 1
    self.nArgs = 0
  
  def __instr_NOP(self) :
    pass
 


  # ---------------------------------------------------------------------------
  # INSTRUCTION: "JZ"
  # ---------------------------------------------------------------------------
  def __init_JZ(self) :
    """
    JZ (Jump if Zero)

    Description is TODO.
    """

    # Instruction properties
    self.mnemonic = "JZ"
    self.handler = self.__instr_JZ

    self.cycles = 2
    self.nArgs = 0

  def __instr_JZ(self) :
    pass



  # ---------------------------------------------------------------------------
  # INSTRUCTION: "MOV"
  # ---------------------------------------------------------------------------
  def __init_MOV(self) :
    
    # Instruction identifier
    # NOTE: the same function processes all variants of the instruction
    # - MOV number, Wx
    # - MOV Wx, Wy
    # etc.
    self.mnemonic = "MOV"
    self.handler = self.__instr_MOV

    self.cycles = 2
    self.nArgs = 0

  def __instr_MOV(self) :
    pass



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'instruction' called as main: running unit tests...")

  I = Instruction("MEET 1")
