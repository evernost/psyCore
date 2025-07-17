# -*- coding: utf-8 -*-
# =============================================================================
# Project         : psyCore
# Module name     : cpu
# File name       : cpu.py
# File type       : Python script (Python 3.10 or higher)
# Purpose         : abstraction class for a single core custom CPU
# Author          : QuBi (nitrogenium@outlook.fr)
# Creation date   : May 22nd, 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
import instruction
import stack

# Standard libraries
import os               # For path manipulations
from enum import Enum   # For enumerated types in FSM


# =============================================================================
# CONSTANTS POOL
# =============================================================================
INSTRUCTION_MEM_SIZE  = 1024    # Size of the instruction memory (in words)
DATA_MEM_SIZE         = 1024    # Size of the data memory (in words)

PIPELINE_SIZE = 5

N_WORK_REGS = 16                # Number of Work registers (W)



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class cpu :

  """
  CPU object.
  
  The CPU object is an abstraction for the machinery of a single core CPU.
  """

  def __init__(self) :
    
    # Program counter init
    self.PC = 0 

    # Instruction/data memory init
    self.iMem = ["NOP" for _ in range(INSTRUCTION_MEM_SIZE)]
    self.dMem = [0 for _ in range(DATA_MEM_SIZE)]

    # Code structure
    # - cpu.resetAddr : address of the first instruction read after CPU reset
    # - cpu.itAddr    : address of the interrupt handler
    self.resetAddr = 0
    self.itAddr = 1000 

    # Work registers init
    self.W = [0 for _ in range(N_WORK_REGS)]

    # Status
    self.statReg = 0
    self.isTrapped = False

    # Stack 
    # TODO: create a stack object?
    self.stack = stack.Stack()

    # CPU execution statistics
    self.nCyclesLost = 0



  # ---------------------------------------------------------------------------
  # METHOD cpu.loadFromFile()
  # ---------------------------------------------------------------------------
  def loadFromFile(self, asmFile: str) :
    """
    Initialises the program memory with assembly code from a text file.
    
    By default, the first instruction in the file is written at 'cpu.startAddr'.
    Consecutive instructions are stored at contiguous addresses in program
    memory.
    
    Instructions can be prefixed with the address of their location in program
    memory. 

    Uninitialised addresses are set to "NOP".

    The loading operation generates an intermediate file where the address of
    each instruction is explicited.
    This is necessary since:
    - in the input code, not all instructions have their address explicited
    - labels are read once, but they impact the address of all the instructions
      coming after.
    - instruction address depends on the memory alignment, which is a setting 
      known by the CPU only.
    Therefore, the code must be treated as a whole before being actually decoded.

    'asmFile' must be the full path to the text file.
    """

    asmFileIn       = asmFile
    asmFileOutFull  = os.path.basename(asmFileIn)
    (asmFileOut, _) = os.path.splitext(asmFileOutFull)
    asmFileOut      = f"{asmFileIn}__processed.asm"

    try :
      
      # PREPROCESSING: generate an intermediate assembly file with all addresses
      # explicited
      addr = self.resetAddr
      with open(asmFileIn, "r") as fileHandleIn, open(asmFileOut, "w") as fileHandleOut :
        for line in fileHandleIn :
          
          # Normalise the line of code
          line = self._asmReaderFormatLine(line)

          # Comment: ignore it
          # ...

          # Detect leading address
          # ...
          
          
          I = instruction.fromStr(line.strip())


    except FileNotFoundError:
      print(f"[ERROR] cpu.loadFromFile(): input file could not be found: '{asmFile}'.")



  # ---------------------------------------------------------------------------
  # METHOD cpu._asmReaderFormatLine()                        [STATIC] [PRIVATE]
  # ---------------------------------------------------------------------------
  @staticmethod
  def _asmReaderFormatLine(line: str) -> str :
    """
    Normalises the line of instruction:
    - removes useless/redundant whitespaces in a line of assembly code.
    - enforce capital letters.

    EXAMPLES
    "   nop"        -> "NOP"
    " noP   "       -> "NOP"
    "MOV W1,   W2"  -> "MOV W1, W2"
    See unit tests in main() for more examples.

    Function is declared as static so that unit tests can be run on it.
    """

    # Void input case
    if (line == "") :
      return ""
  
    class fsmState(Enum) :
      INIT      = 0
      MNEMONIC  = 1
      ARG       = 2
      END       = 3
  
    state     = fsmState.INIT
    stateNext = fsmState.INIT
  
    output = ""
    spaceQuota = 0
    for (i, c) in enumerate(line) :
      isLast = (i == (len(line)-1))
      
      # State INIT
      if (state == fsmState.INIT) :
        if (c != " ") :
          output += c
          stateNext = fsmState.MNEMONIC


      # State MNEMONIC
      elif (state == fsmState.MNEMONIC) :
        output += c
        if (c == " ") : stateNext = fsmState.ARG


      # State ARG
      elif (state == fsmState.ARG) :
        if (c == ",") :
          spaceQuota = 1
          output += c
          if not(isLast) :
            if (line[i+1] != " ") :
              output += " "
        elif (c == " ") :
          if (spaceQuota > 0) : 
            output += c
            spaceQuota -= 1
        else :
          output += c

      state = stateNext

    # Remove excessive trailing white spaces
    for (i,c) in enumerate(output[::-1]) :
      if (c != " ") :
        iMax = len(output) - 1 - i
        output = output[:(iMax+1)]
        break



    print()

    output = output.upper()
    return output



  # ---------------------------------------------------------------------------
  # METHOD cpu._asmReaderConsumeSpace()                      [STATIC] [PRIVATE]
  # ---------------------------------------------------------------------------
  @staticmethod
  def _asmReaderConsumeSpace(line: str) -> str :
    """
    Consumes the leading whitespace in a string (utility function)
    Only the beginning of the string is affected.
    The rest of the string remains untouched.

    EXAMPLES
    " 123 "   -> "123 "
    "   nop"  -> "nop"
    "  "      -> ""
    See unit tests in main() for more examples.

    Function is declared as static so that unit tests can be run on it.
    """

    # Empty input: empty output
    if (line == "") : return line

    # If it doesn't start with a space, there is nothing to trim
    if (line[0] != " ") : return line

    output = ""
    isStillBlank = True
    for c in line :
      if isStillBlank :
        if (c != " ") :
          output += c
          isStillBlank = False
        else :
          pass
      else :
        output += c

    return output



  # ---------------------------------------------------------------------------
  # METHOD cpu.reset()
  # ---------------------------------------------------------------------------
  def reset(self) :
    """
    Emulates a hardware reset on the CPU.
    """

    self.PC         = self.startAddr
    self.W          = [0 for _ in range(N_WORK_REGS)]
    self.stack      = []
    self.isTrapped  = False



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

    instr = instruction.fromStr("NOP")

    pass



  # ---------------------------------------------------------------------------
  # METHOD cpu._setPC()                                               [PRIVATE]
  # ---------------------------------------------------------------------------
  def _setPC(self, newPC) :
    """
    Sets the PC (program counter) to a specific spot.
    Out of range values will call a hardware trap.
    """

    if not(self.isTrapped) :
      if ((newPC < 0) or (newPC >= DATA_MEM_SIZE)) :
        self.__trap_pcOutOfRange()

      else :
        self.PC = newPC



  # ---------------------------------------------------------------------------
  # METHOD cpu._pcJump()                                              [PRIVATE]
  # ---------------------------------------------------------------------------
  def _pcJump(self, delta) :
    """
    Does a relative jump on the PC (positive or negative)
    Out of range values will call a hardware trap.
    """

    self._setPC(self.PC + delta)



  # ---------------------------------------------------------------------------
  # METHOD cpu.__trap_pcOutOfRange()                                  [PRIVATE]
  # ---------------------------------------------------------------------------
  def __trap_pcOutOfRange(self) :
    """
    CPU trap: PC out of range.
    This function is called when the PC is requested to go beyond the program
    memory.
    """

    self.isTrapped = True
    print("[ERROR] Reached hardware trap: PC is out of range. Simulation halted")



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'cpu' called as main: running unit tests...")

  assert(cpu._asmReaderConsumeSpace("nop")      == "nop")
  assert(cpu._asmReaderConsumeSpace(" nop")     == "nop")
  assert(cpu._asmReaderConsumeSpace(" nop  ")   == "nop  ")
  assert(cpu._asmReaderConsumeSpace(" ,123 ")   == ",123 ")
  assert(cpu._asmReaderConsumeSpace("  ;456  ") == ";456  ")
  print("- Unit test passed: 'cpu._asmReaderConsumeSpace()'")

  assert(cpu._asmReaderFormatLine("nop")                == "NOP")               # Outputs are in capital letters (except for labels)
  assert(cpu._asmReaderFormatLine("   nop")             == "NOP")               # Leading whitespaces are ignored
  assert(cpu._asmReaderFormatLine(" noP   ")            == "NOP")               # Trailing whitespaces are ignored
  assert(cpu._asmReaderFormatLine("MoV w1,   w2")       == "MOV W1, W2")        # Whitespaces in separators are normalised
  assert(cpu._asmReaderFormatLine("MoV w4,w6")          == "MOV W4, W6")        # Ditto
  assert(cpu._asmReaderFormatLine("moV w1,[ 0x240]")    == "MOV w1, [0x240]")   # Ditto
  assert(cpu._asmReaderFormatLine("moV w9, ( 0x240 )")  == "MOV w9, (0x240)")   # Same with parenthesis
  assert(cpu._asmReaderFormatLine("mov w1,,; w2")       == "MOV W1,,; W2")      # Note that the function does minimal syntax check.
  assert(cpu._asmReaderFormatLine("")                   == "")                  # Odd input
  assert(cpu._asmReaderFormatLine(" ")                  == "")                  # Odd input
  assert(cpu._asmReaderFormatLine("   ")                == "")                  # Odd input
  print("- Unit test passed: 'cpu._asmReaderFormatLine()'")
  
  # Example code for the instruction memory
  cpu0 = cpu()
  cpu0.reset()
  cpu0.loadFromFile("./demo.asm")

