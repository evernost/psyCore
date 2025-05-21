# psyCore
A study on CPUs and all their internal machinery.

## The Why
> _Sometimes, the best way to truly grasp the essence of a thing is to build your own from scratch with some Python scripts._
<p align="right">Some wise man.</p>

## The Goal
This project is a simulator for a **homemade CPU**.<br>
Ultimately, the ambition is to develop the VHDL code for it.

## The Specifications
Some requirements:
- **Full emulator**: simulate every single register and peripheral at clock cycle level
- **Custom instruction set**: define your very own instruction set without overthinking on the detailed implementation
- **Latency definition**: define the latency for the peripherals, the cycles needed for each instruction and see immediatly how it impacts in simulation 
- **Pipeline display**: show the instruction pipeline in action, the branching, the bubbles and cache misses etc.
- **UI peripherals emulation**: integrated emulation for a tiny screen display, mouse and keyboard if you want to develop video hardware accelerators  
