# Sid chip Unusable emulator
from psonic import play,sample,AMBI_LUNAR_LAND, PULSE
from .memory import ScreenAndMemory
"""
Sid emulator class based on psonic

"""
class SidEmulator:
    def __init__(self,screenAndMemory : ScreenAndMemory ):
        #play (60, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5)
        #play (70, attack=0.5, decay=1, sustain_level=0.4, sustain=2, release=0.5)
        # sample(AMBI_LUNAR_LAND, amp=0.5)        
        self.screen=screenAndMemory
        self.start=0xd400
        # Wipe sid chip set
        self.screen.memory[self.start:(self.start+0x1c)]=bytearray(0x1c)
        # Enable some interceptor on write
        def sid_action(address, old,newvalue):
            #print("Volume changed")
            return newvalue
        self.screen.memory.intercept_write(self.start+0x18,sid_action)
        print("Sid_Unusable_Emulator READY")
        # TODO: Implement PULSE for voice 1

