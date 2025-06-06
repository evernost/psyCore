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

    # Reference to the CPU instance.
    # An instruction has full control over the internal attributes of the CPU.
    self.cpu = None

    # Arguments (populated )
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



  # ---------------------------------------------------------------------------
  # DECORATOR instruction.register()
  # ---------------------------------------------------------------------------
  @classmethod
  def register(cls, mnemonic: str) -> None :
    def preProcessor(classInitFunc):
      cls._instructionSet[mnemonic] = classInitFunc
      return classInitFunc
    return preProcessor

  # def execute(self, action_name):
  #   if action_name in self._instructionSet :
  #     return self._registry[action_name](self)
  #   raise ValueError(f"Unknown action '{action_name}'")










# -----------------------------------------------------------------------------
# FUNCTION fromTxt()
# -----------------------------------------------------------------------------
def fromTxt(input : str) :
  """
  Creates and initialises an instruction object from a string (factory function)

  It parses the string, checks if the instruction exists, check if the syntax
  is valid, retrieves the parameters.

  Example: 
  > instruction.fromTxt("NOP")
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

instructionSet = {}

def register(mnemonic: str) :
  def decorateur(mnemoInitFunc) :
    instructionSet[mnemonic] = mnemoInitFunc
    return mnemoInitFunc
  return decorateur


# -----------------------------------------------------------------------------
# INSTRUCTION: "NOP"
# -----------------------------------------------------------------------------
@register("NOP")
def __instr_NOP(instruction) :
  
  # Number of clock cycles required to carry out the instruction
  instruction.cycles = 1
  
  # Past this point, 'Instruction.args' and 'Instruction.nArgs' are 
  # ready to be used by the instruction
  if (instruction._cyclesRemaining > 0) :
    pass



# ---------------------------------------------------------------------------
# INSTRUCTION: "JZ"
# ---------------------------------------------------------------------------
@register("JZ")
def __instr_JZ(instruction) :
  
  pass





# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'instruction' called as main: running unit tests...")

  I = fromTxt("MEET 1")
