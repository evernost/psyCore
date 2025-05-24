# psyCore
A study on CPUs and their internal machinery.

## The Why
> _Sometimes, the best way to truly grasp the essence of a thing is to build your own from scratch with some Python scripts._
<p align="right">Some wise man.</p>

## The Goal
This project about designing a **homemade CPU** and a detailed **emulator** for it.<br>
Ultimately, the architecture would be transposed to HDL code and have it run on real hardware.

## The Specifications
Some requirements:
- **Full emulator**: simulate every single register and peripheral at clock cycle level
- **Modular instruction set**: define your very own instruction set, focus on the value added before overthinking on how to implement it
- **Latency definition**: define the latency for the peripherals, the cycles needed for each instruction and see immediatly how it impacts the performances 
- **Pipeline display**: show the instruction pipeline in action, the branching, the bubbles and cache misses etc.
- **UI peripherals emulation**: built-in emulation for a tiny screen display, mouse and keyboard if you want to develop video hardware accelerators
- **Debug**: integrate means to debug properly, follow exactly what the CPU does, add breakpoints etc.
- **Performance assessment**: monitor the efficiency, see the impact on instruction latency, pipeline, cache etc. on the lost clock cycles
- **Multiple core capable**: give the possibility to instanciate more than 1 CPU, and make them work together
- **Hardware aware**: integrate parameters in the peripheral emulation to make them as close as possible to the real hardware constraints
