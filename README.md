# psyCore
A study on CPUs and their internal machinery.

## The Why
> _Sometimes, the best way to truly grasp the essence of a thing is to build your own from scratch with some Python scripts._
<p align="right">Someone very clearly underestimating a gargantuan task.</p>

## The Goal
This project about designing a **homemade CPU** and a detailed **emulator** for it.<br>
Ultimately, it would run on real hardware once the architecture is settled, the performances assessed and potential bottlenecks identified.

PsyCore is a sort of _meta-CPU_ in the sense that it's a framework to build, emulate and evaluate the CPU before commiting to a real hardware.

## The Specifications
The main requirements I have in mind for this project:
- **Flexible instruction set**: the psyCore has its own customizable instruction set. Adding a new instruction must be super easy so that the focus can be on evaluating the benefits of an instruction rather than the way to implement it on actual hardware
- **Full hardware emulator**: simulate every single register and peripheral at clock cycle level. It provides a reference for later HDL design
- **Latency definition**: define the latency for the peripherals, the cycles needed for each instruction and see immediatly how it impacts the performances 
- **Pipeline display**: show the instruction pipeline in action, the branching, the bubbles and cache misses etc.
- **UI peripherals emulation**: built-in emulation for a tiny screen display, mouse and keyboard if you want to develop video hardware accelerators
- **Debug**: integrate means to debug properly, follow exactly what the CPU does, add breakpoints etc.
- **Performance assessment**: monitor the efficiency, see the impact on instruction latency, pipeline, cache etc. on the lost clock cycles
- **Multiple core capable**: the core is thought to collaborate with other instances of itself from the beginning 
- **_Hardware aware_**: integrate parameters in the peripheral emulation to make them as close as possible to the real hardware constraints
