0x000 : NOP
0x004 : NOP
0x008 : NOP
;
0x100 : NOP
0x104 : NOP
0X108 : NOP
;
label1          : MOV 0x55, W0 
label1 + 0x004  : ADD W0, W1, W0
label1 + 0x008  : ADD W0, W1, W0RESET