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
  It describes the task carried out by the instruction and keeps track of some 
  useful information like:
  - address of the instruction
  - number of clock cycles needed
  - modified registers

  It keeps track of the context for instructions that need more than one 
  clock cycle to be done.

  Usually, the instruction object is destroyed once its execution is done.
  """

  def __init__(self, text: str) :
    
    # Clock cycles needed before the result is available
    self.cycles = 1  

    # Populated after a Instruction._decode()
    self.mnemonic = ""      # Normalised mnemonic of the instruction
    self.handler  = None    # Pointer to the function carrying out the instruction task
    self.addr     = 0       # Address of the instruction in program memory

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
    self.size = 32  # Size of the instruction (bits)
    self._cyclesRemaining = self.cycles
    
    # Declare the instruction set supported by the CPU.
    # Instructions must be declared in the dictionary as a pair:
    # - key   : mnemonic (string)
    # - value : pointer to the custom init function 
    # These functions extend the __init__() method.
    self._instructionSet = {
      # Data transfer 
      "MOV"     : self.__init_MOV,
      
      # Branch
      "JZ"      : self.__init_JZ,
      "JE"      : self.__init_JE,
      "REPEAT"  : self.__init_REPEAT,
      
      # Math
      "ADD"     : self.__init_ADD,
      "SUB"     : self.__init_SUB,

      # Context save/restore
      "SCTX"    : self.__init_SCTX,
      "RCTX"    : self.__init_RCTX,

      # Synchronisation (multi-CPU context)
      "LOC"     : self.__init_LOC,
      "MEET"    : self.__init_MEET,
      
      # Hardware instructions
      "NOP"     : self.__init_NOP,
      "RESET"   : self.__init_RESET
    }

    # Normalised string version of the instruction (all caps, proper spacing etc.)
    # Populated after 'Instruction._decode()'.
    self._normalisedCode = ""

    # Try to decode the instruction
    self._decode(text)



  # ---------------------------------------------------------------------------
  # METHOD instruction._decode()
  # ---------------------------------------------------------------------------
  def _decode(self, text: str) -> bool :
    """
    Reads a line of code (as string) checks the syntax and initialises the 
    object's attributes based on the decoded content.

    It does the following:
    - normalisation (uniform caps, remove useless whitespaces etc.)
    - instruction parsing
    - syntax check
    - address extraction (if any)
    - argument extraction (if any) 
    
    If the parsing fails, the object's attributes are left to their default 
    state (empty) so that the CPU can detect an exception.

    Valid characters in the text file:
    - alphanumeric    : a-z, A-Z, 0-9
    - comma           : ,
    - round brackets  : ()
    - square brackets : []
    - underscore      : _
    - whitespace
    - carriage return / line feed

    Capitalisation is ignored.
    Multiple whitespaces are ignored

    Returns True if parsing succeeded.
    """
    
    # Detect invalid characters
    for (loc, char) in enumerate(self.input) :
      isAlpha       = self._decodeIsAlpha(char)
      isDigit       = self._decodeIsDigit(char)
      isOthers      = (char in ["[", "]", "(", ")", "_", ","])
      
      if not(isAlpha or isDigit or isOthers) :
        print("[ERROR] This character is not supported by the parser.")
        return False
    
    
    
 

  # ---------------------------------------------------------------------------
  # METHOD instruction._decodeIsAlpha()
  # ---------------------------------------------------------------------------
  def _decodeIsAlpha(self, s: str) -> bool :
    """
    Returns True if the first char of 's' is a letter.
    Capitalisation is ignored.
    """

    # Keep the first char, ignore the rest.
    char = s[0]

    isAlpha = False
    isAlpha = isAlpha or ((ord(char) >= ord("A")) and (ord(char) <= ord("Z")))
    isAlpha = isAlpha or ((ord(char) >= ord("a")) and (ord(char) <= ord("z")))

    return isAlpha



  # ---------------------------------------------------------------------------
  # METHOD instruction._decodeIsDigit()
  # ---------------------------------------------------------------------------
  def _decodeIsDigit(self, s: str) -> bool :
    """
    Returns True if the first char of 's' is a digit.
    """

    # Keep the first char, ignore the rest.
    char = s[0]

    return (ord(char) >= ord("0")) and (ord(char) <= ord("9"))



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

    Arguments: none

    Behaviour:
    - STAT reg  : reset
    - W_XX regs : unchanged
    - PC        : +1
    """
    
    # Instruction properties
    self.mnemonic = "MOV"
    self.handler = self.__instr_NOP

    self.cycles = 1
    self.nArgs = 0
  
  def __instr_NOP(self) :
    self.cpu[self.cpuID]._setPC()
 


  # ---------------------------------------------------------------------------
  # INSTRUCTION: "JZ"
  # ---------------------------------------------------------------------------
  def __init_JZ(self) :
    """
    JZ (Jump if Zero)
    Description is TODO

    Arguments: TODO

    Behaviour:
    - STAT reg  : TODO
    - W_XX regs : TODO
    - PC        : TODO
    """

    # Instruction properties
    self.mnemonic = "JZ"
    self.handler = self.__instr_JZ

    self.cycles = 2
    self.nArgs = 0

  def __instr_JZ(self) :
    pass



  # ---------------------------------------------------------------------------
  # INSTRUCTION: "JE"
  # ---------------------------------------------------------------------------
  def __init_JE(self) :
    """
    JE (Jump if Equal)
    Skips the next instruction if the content of 2 work registers is 
    identical.

    Arguments: TODO

    Behaviour:
    - STAT reg  : TODO
    - W_XX regs : TODO
    - PC        : TODO
    """

    # Instruction properties
    self.mnemonic = "JE"
    self.handler = self.__instr_JE

    self.cycles = 2
    self.nArgs = 0

  def __instr_JE(self) :
    pass


  # ---------------------------------------------------------------------------
  # INSTRUCTION: "REPEAT"
  # ---------------------------------------------------------------------------
  def __init_REPEAT(self) :
    """
    REPEAT #N
    Repeats the next instruction N times.

    Arguments: none

    Behaviour:
    - STAT reg  : TODO
    - W_XX regs : TODO
    - PC        : TODO
    """
    
    # Instruction properties
    self.mnemonic = "REPEAT"
    self.handler = self.__instr_REPEAT

    self.cycles = 1
    self.nArgs = 0
  
  def __instr_REPEAT(self) :
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



# -----------------------------------------------------------------------------
# FUNCTION fromStr
# -----------------------------------------------------------------------------
def fromStr(self, text: str) :
  """
  Factory function

  Creates an instruction object from a string containing the mnemonic and 
  the arguments.

  It is essentially a shorthand notation to avoid doing things like 
  instruction.Instruction(...) which are not very handy.
  """
  
  # Try to decode
  I = Instruction(text)

  if (I.mnemonic == "") :
    return None
  else :
    return Instruction(text)



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'instruction' called as main: running unit tests...")

  I = Instruction("MEET 1")
