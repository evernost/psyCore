# -*- coding: utf-8 -*-
# =============================================================================
# Project       : psyCore
# Module name   : cpu
# File name     : cpu.py
# File type     : Python script (Python 3.10 or higher)
# Purpose       : abstraction class for 1 core of the psyCore CPU
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : May 22nd, 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Projet libraries
import instruction
import stack

# Standard libraries
import os               # For path manipulations



# =============================================================================
# CONSTANTS POOL
# =============================================================================
INSTRUCTION_SIZE      = 32      # Size of an instruction (in bits)
INSTRUCTION_MEM_SIZE  = 1024    # Size of the instruction memory (in number of instructions)
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

    # Instruction memory (initialized with NOP)
    self.iMem = ["NOP" for _ in range(INSTRUCTION_MEM_SIZE)]
    
    # Data memory (initialized with 0)
    self.dMem = [0 for _ in range(DATA_MEM_SIZE)]

    # Work registers (initialized with 0)
    self.W = [0 for _ in range(N_WORK_REGS)]

    # Status registers
    self.status_Z = 0

    # Code organization
    # - cpu.resetAddr : address of the first instruction read after CPU reset
    # - cpu.irqAddr   : address of the interrupt handler
    self.resetAddr  = 0
    self.irqAddr    = 512

    # Faults
    self.isTrapped = False

    # Stack
    self.stack = stack.Stack()

    # Clock cycles counter
    self.clockCount = 0

    # CPU execution statistics
    self.nCyclesLost = 0



  # ---------------------------------------------------------------------------
  # METHOD cpu.loadFromFile()
  # ---------------------------------------------------------------------------
  def loadFromFile(self, asmFile: str) :
    """
    Initialises the program memory with assembly read from a text file.
    
    By default, the first instruction in the file is written at 'cpu.startAddr'.
    Following instructions are stored at contiguous addresses in program
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
          line = instruction.Instruction._asmReaderFormatLine(line)

          # Comment: ignore it
          # ...

          # Detect leading address
          # ...
          
          
          I = instruction.fromStr(line.strip())


    except FileNotFoundError:
      print(f"[ERROR] cpu.loadFromFile(): input file could not be found: '{asmFile}'.")



  # ---------------------------------------------------------------------------
  # METHOD cpu.reset()
  # ---------------------------------------------------------------------------
  def reset(self) -> None :
    """
    Emulates a hardware reset on the CPU.
    """

    self.PC         = self.resetAddr
    self.W          = [0 for _ in range(N_WORK_REGS)]
    self.stack      = []
    self.isTrapped  = False




  # ---------------------------------------------------------------------------
  # METHOD cpu.fireExtIRQ()
  # ---------------------------------------------------------------------------
  def fireExtIRQ(self) :
    """
    Emulates an external IRQ event ('EXT' pin)
    """

    print("[WARNING] cpu.fireExtIRQ() is not available yet.")



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
  def _setPC(self, val) :
    """
    Sets the PC (program counter) to a specific spot.
    Out of range values will call a hardware trap.
    """

    if not(self.isTrapped) :
      if (val < 0) :
        print("[ERROR] cpu._setPC() cannot handle negative values.")
      elif (val >= DATA_MEM_SIZE) :
        self.__trap_pcOutOfRange()
      else :
        self.PC = val



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

  print("[INFO] Library 'cpu.py' called as main: running unit tests...")
  
  # Example code for the instruction memory
  cpu0 = cpu()
  cpu0.reset()
  cpu0.loadFromFile("./demo.asm")

