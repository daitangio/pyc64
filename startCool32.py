from pyc64 import emulator
from pyc64.emulator import C64EmulatorWindow
from pyc64.memory import ScreenAndMemory

from pyc64.shared import StdoutWrapper, do_load, do_dos, do_sys, FlowcontrolException

# Cool32 is a Retro Dream done by Giovanni Giorgi
def start():
    rom_directory = "roms"
    screen = ScreenAndMemory(columns=C64EmulatorWindow.columns,
                             rows=C64EmulatorWindow.rows,
                             sprites=C64EmulatorWindow.sprites,
                             rom_directory=rom_directory)
    emu = C64EmulatorWindow(screen, "Cool-32 simulator in pure Python!", rom_directory)
    emu.start()
    autoload="load \"c32autorun\",8,1"
    autorun="run"
    #emu.screen.writestr(autoload + "\n")
    emu.execute_direct_line(autoload)
    #emu.screen.writestr(autorun + "\n")
    emu.execute_direct_line(autorun)
    
    #ret=do_load(screen,"\"c32\",8,1")
    #print("Loaded:"+str(ret))
    emu.mainloop()

if __name__ == "__main__":
    start()