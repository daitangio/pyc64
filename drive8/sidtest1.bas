  0 rem *** c64-wiki sound-demo ***
 10 rem edited to be pyc64 compatible
100 s = 54272: w = 17: on int(rnd(ti)*4)+1 goto 120,130,140,150
120 w = 33: goto 150
130 w = 65: goto 150
140 w = 129
150 poke s+24,15: poke s+5,97: poke s+6,200: poke s+4,w
160 for x = 0 to 255 step (rnd(ti)*15)+1
170 poke s,x :poke s+1,255-x
180 for y = 0 to 33
185 next y
187 next x
190 for x = 0 to 200: 
195 next x: poke s+24,0
200 for x = 0 to 100: 
210 next x: goto 100
220 rem *** abort only with run/stop ! ***