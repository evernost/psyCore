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
# EXTERNALS
# =============================================================================
import instruction
import os



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
    self.stack = None

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
          
          # Remove leading whitespaces
          # ...

          # Comment: ignore it
          # ...

          # Detect leading address
          # ...
          
          
          I = instruction.fromStr(line.strip())


    except FileNotFoundError:
      print(f"[ERROR] cpu.loadFromFile(): input file could not be found: '{asmFile}'.")




  # ---------------------------------------------------------------------------
  # METHOD cpu._asmReadRemoveSpaces()                                 [PRIVATE]
  # ---------------------------------------------------------------------------
  @staticmethod
  def _asmReadRemoveSpaces(line: str) -> str :
    """
    Removes leading and redundant whitespaces in a line of ASM code. 
    """

    output = ""
    emptyInput = True
    for (i, c) in enumerate(line) :
      if emptyInput :
        if (c != " ") :
          emptyInput = False
          output += c.upper()



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

  assert(cpu._asmReadRemoveSpaces("nop") == "NOP")
  
  # Example code for the instruction memory
  cpu0 = cpu()
  cpu0.reset()
  cpu0.loadFromFile("./demo.asm")

