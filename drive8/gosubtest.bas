10 print chr$(147)
20 sp = 20: ze = 3: a$ = "good morning!": gosub 1000: gosub 2000
30 sp = 10: ze = 3: a$ = "i'm the commodore 64": gosub 1000: gosub 2000
40 sp = 12: ze = 6: a$ = "and what is your name ?": gosub 1000
100 end
1000 rem cursor positioning and printing
1010 poke 211,sp :poke 214, ze: sys 58640 : print a$
1020 return
2000 rem delay-loop
2010 for x=0 to 3000: next x
2020 return