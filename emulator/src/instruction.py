# -*- coding: utf-8 -*-
# =============================================================================
# Project       : psyCore
# Module name   : instruction
# File name     : instruction.py
# File type     : Python script (Python 3.10 or higher)
# Purpose       : class definition for the 'Instruction' object
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : May 22nd, 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Projet libraries
# None.

# Standard libraries
from enum import Enum   # For enumerated types in FSM



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
    


    # TODO: syntax check
    # isValid = Instruction._asmReaderSyntaxCheck(line)

    # Parse the instruction
    (address, label, mnemonic, args, comment) = Instruction._asmReaderParse(line)
    
    # Normalise it 
    line = Instruction._asmReaderFormatLine(line)



  # ---------------------------------------------------------------------------
  # METHOD Instruction._asmReaderParse()                     [STATIC] [PRIVATE]
  # ---------------------------------------------------------------------------
  @staticmethod
  def _asmReaderParse(line: str) :
    """
    Extracts the components of an assembly line of code.
    The function returns:
    - the label (if any)
    - the address (if any)
    - the mnemonic
    - the comment (if any)
    - the argument(s)

    Note: the function does not check if the mnemonic exists.
    """

    # Void input case
    if (line == "") : return ("", "", [], "")
  
    hasLabel = Instruction._asmReaderHasLabel(line)

    class fsmState(Enum) :
      INIT          = 0
      ADDRESS       = 1
      LABEL         = 2
      MNEMONIC      = 3
      ARG_ALPHANUM  = 4
      ARG_BRACKET   = 5
      COMMENT       = 6
  
    state     = fsmState.INIT
    stateNext = fsmState.INIT

    address   = ""
    label     = ""
    mnemonic  = ""
    args      = []
    comment   = ""
    acc = ""
    for (i, c) in enumerate(line) :
      isLast = (i == (len(line)-1))
      
      # State INIT
      if (state == fsmState.INIT) :
        if (c == " ") :
          pass
        elif (c == ";") :
          stateNext = fsmState.COMMENT
        elif Instruction._asmReaderIsDigit(c) :
          address += c
          stateNext = fsmState.ADDRESS
        elif Instruction._asmReaderIsAlpha(c) :
          mnemonic += c
          stateNext = fsmState.MNEMONIC
        elif (c != " ") :
          mnemonic += c
          stateNext = fsmState.MNEMONIC

      # State ADDRESS
      elif (state == fsmState.ADDRESS) :
        pass

      # State MNEMONIC
      elif (state == fsmState.MNEMONIC) :
        if (c == " ") : 
          firstSpace = True
          stateNext = fsmState.ARG
        else :
          mnemonic += c


      # State ARG
      elif (state == fsmState.ARG) :
        if firstSpace :
          if (c != " ") :
            firstSpace = False
            acc += c
        else :
          if (c != " ") :
            acc += c
          else :
            args.append(acc)
            acc = ""


      # State COMMENT
      elif (state == fsmState.COMMENT) :
        comment += c


      state = stateNext

    return (address, label, mnemonic, args, comment)



  # ---------------------------------------------------------------------------
  # METHOD Instruction._asmReaderFormatLine()                [STATIC] [PRIVATE]
  # ---------------------------------------------------------------------------
  @staticmethod
  def _asmReaderFormatLine(line: str) -> str :
    """
    Normalises an instruction given as a string:
    - removes useless/redundant whitespaces in a line of assembly code
    - enforces capital letters
    - enforces whitespaces for readability

    EXAMPLES
    "   nop"        -> "NOP"
    " noP   "       -> "NOP"
    "MOV W1,   W2"  -> "MOV W1, W2"
    See unit tests in main() for more examples.

    Function is declared as static so that unit tests can be run on it.
    """

    (address, label, mnemonic, args, comment) = Instruction._asmReaderParse(line)

    # TODO
    # output = ...



  # ---------------------------------------------------------------------------
  # METHOD Instruction._asmReaderHasLabel()                  [STATIC] [PRIVATE]
  # ---------------------------------------------------------------------------
  @staticmethod
  def _asmReaderHasLabel(line: str) -> bool :
    """
    Detects if the current line of assembly code contains an address label.
    """

    # Void input case
    if (line == "") : False
  
    class fsmState(Enum) :
      INIT      = 0
      LABEL     = 1
      REMAINDER = 2

    state     = fsmState.INIT
    stateNext = fsmState.INIT

    hasLabel = True
    for c in line :

      # State INIT
      if (state == fsmState.INIT) :
        if Instruction._asmReaderIsDigit(c) :
          pass
        elif ((c == "x") or (c == "X")) :
          pass
        elif (c == " ") :
          pass
        elif (c == ":") :
          stateNext = fsmState.REMAINDER
        else :
          hasLabel = False

    return hasLabel 



  # # ---------------------------------------------------------------------------
  # # METHOD Instruction._asmReaderConsumeSpace()              [STATIC] [PRIVATE]
  # # ---------------------------------------------------------------------------
  # @staticmethod
  # def _asmReaderConsumeSpace(line: str) -> str :
  #   """
  #   Consumes the leading whitespace in a string (utility function)
  #   Only the beginning of the string is affected.
  #   The rest of the string remains untouched.

  #   EXAMPLES
  #   " 123 "   -> "123 "
  #   "   nop"  -> "nop"
  #   "  "      -> ""
  #   See unit tests in main() for more examples.

  #   Function is declared as static so that unit tests can be run on it.
  #   """

  #   # Empty input: empty output
  #   if (line == "") : return line

  #   # If it doesn't start with a space, there is nothing to trim
  #   if (line[0] != " ") : return line

  #   output = ""
  #   isStillBlank = True
  #   for c in line :
  #     if isStillBlank :
  #       if (c != " ") :
  #         output += c
  #         isStillBlank = False
  #       else :
  #         pass
  #     else :
  #       output += c

  #   return output




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



# ---------------------------------------------------------------------------
# FUNCTION _asmReaderIsAlpha()                                      [PRIVATE]
# ---------------------------------------------------------------------------
def _asmReaderIsAlpha(s: str) -> bool :
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



# -----------------------------------------------------------------------------
# FUNCTION _asmReaderIsDigit()                                        [PRIVATE]
# -----------------------------------------------------------------------------
def _asmReaderIsDigit(s: str) -> bool :
  """
  Returns True if the first char of 's' is a digit.
  """

  # Keep the first char, ignore the rest.
  char = s[0]

  return (ord(char) >= ord("0")) and (ord(char) <= ord("9"))



# ---------------------------------------------------------------------------
# FUNCTION _asmReaderSyntaxCheck()                                  [PRIVATE]
# ---------------------------------------------------------------------------
def _asmReaderSyntaxCheck(line: str) -> bool :
  """
  Checks if line of assembly code complies with the syntax rules.
  Returns True if no violation has been detected, false otherwise.
  """

  # An empty string is not considered as a valid expression
  if (line == "") : return False

  for c in line :
    if _asmReaderIsAlpha(c) :
      pass
    elif _asmReaderIsDigit(c) :
      pass
    elif (c == " ") :
      pass
    elif c in [":", ",", ".", "(", ")", "[", "]", "_"] :
      pass
    else :
      return False

  class fsmState(Enum) :
    INIT          = 0
    LABEL         = 1
    LABEL_OR_MNEM = 2
    ADDR          = 3
    ADDR_HEX      = 4
    MNEMONIC      = 5

  state     = fsmState.INIT
  stateNext = fsmState.INIT

  hasColon = False

  for c in line :
    if (state == fsmState.INIT) :
      if (c == "0") :
        stateNext = fsmState.ADDR_HEX
      elif _asmReaderIsDigit(c) :
        stateNext = fsmState.ADDR
      elif (c == "_") :
        stateNext = fsmState.LABEL
      elif _asmReaderIsAlpha(c) :
        stateNext = fsmState.LABEL_OR_MNEM
      elif (c == " ") :
        pass
      else :
        return False

    elif (state == fsmState.LABEL) :
      if _asmReaderIsAlpha(c) :
        pass
      elif _asmReaderIsDigit(c) :
        pass
      elif (c == " ") :
        pass
      elif (c == ":") :
        stateNext = fsmState.MNEMONIC


    state = stateNext





# ---------------------------------------------------------------------------
# FUNCTION _asmReaderInstrParse()                                   [PRIVATE]
# ---------------------------------------------------------------------------
def _asmReaderInstrParse(line: str)  :
  """
  Extracts all the fields in a line of assembly code.

  The function returns (in the following order):
    - the label       (optional)
    - the address     (optional)
    - the mnemonic
    - the comment     (optional)
    - the argument(s)
  All of them as strings.
  
  The function assumes that a syntax check has been done before.
  (see '_asmReaderSyntaxCheck()')
  """

  # An empty string is not considered as a valid expression
  if (line == "") : return False

  # Function is TODO.






# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'instruction' called as main: running unit tests...")

  assert(_asmReaderSyntaxCheck("") == False)

  assert(Instruction._asmReaderParse("")    == ("", "", [], ""))
  assert(Instruction._asmReaderParse("  ")  == ("", "", [], ""))
  print("- Unit test passed: 'cpu._asmReaderParse()'")


  assert(Instruction._asmReaderFormatLine("nop")                == "NOP")               # Outputs are in capital letters (except for labels)
  assert(Instruction._asmReaderFormatLine("   nop")             == "NOP")               # Leading whitespaces are ignored
  assert(Instruction._asmReaderFormatLine(" noP   ")            == "NOP")               # Trailing whitespaces are ignored
  assert(Instruction._asmReaderFormatLine("MoV w1,   w2")       == "MOV W1, W2")        # Whitespaces in separators are normalised
  assert(Instruction._asmReaderFormatLine("MoV w4,w6")          == "MOV W4, W6")        # Ditto
  assert(Instruction._asmReaderFormatLine("moV w1,[ 0x240]")    == "MOV w1, [0x240]")   # Ditto
  assert(Instruction._asmReaderFormatLine("moV w9, ( 0x240 )")  == "MOV w9, (0x240)")   # Same with parenthesis
  assert(Instruction._asmReaderFormatLine("mov w1,,; w2")       == "MOV W1,,; W2")      # Note that the function does minimal syntax check.
  assert(Instruction._asmReaderFormatLine("")                   == "")                  # Odd input
  assert(Instruction._asmReaderFormatLine(" ")                  == "")                  # Odd input
  assert(Instruction._asmReaderFormatLine("   ")                == "")                  # Odd input
  print("- Unit test passed: 'cpu._asmReaderFormatLine()'")
  