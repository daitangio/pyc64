from psonic import *
play(70) #play MIDI note 70
sleep(1)
play (60, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5)
sleep(2)
# Play some sample
sample(AMBI_LUNAR_LAND, amp=0.5)