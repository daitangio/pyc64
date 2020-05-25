"""
Commodore-64 simulator in 100% pure Python 3.x :)

This module is the GUI window logic, handling keyboard input
and screen drawing via tkinter bitmaps.

Written by Irmen de Jong (irmen@razorvine.net)
License: MIT open-source.
"""

import time
from pyc64.emulator import C64EmulatorWindow
from .memory import ScreenAndMemory
from .cputools import CPU
import struct
import os, fnmatch

class DummyEvent():
    def __init__(self,c):
        self.char=c
        self.state=0
        if c=='\r':
            self.keysym="Return"
            self.keycode=36
        else:
            self.keysym=''
            self.keycode=0
        self.x=0
        self.y=0


class RealC64EmulatorWindow(C64EmulatorWindow):
    welcome_message = "Running the Real ROMS!"
    update_rate = 1000/20

    def __init__(self, screen, title, roms_directory,argv):        
        super().__init__(screen, title, roms_directory, True)

        self.last_describe_state=""
        #from .monitor import MonitorWindow
        #self.monitor_window=MonitorWindow(self, self.screen.memory,None)
       
        self.keypresses = [ ]
        if argv!=None and len(argv) >=2:            
            for c in  reversed("lO\"" + argv[1]+ "\"\rlI\rrun\r"):
                 self.keypresses.append( DummyEvent(c))
        # Maps logical kernel files to IORecord
        self.device23={}
        self.TRACE_REF={}
        self.load_trace()
    
    def trace_toggle(self):
        """
         Override trace toggle
        """
        self.trace_mode=not self.trace_mode        
        self.info_label.config(text= ("Reloaded/Trace Mode:"+str(self.trace_mode)))
        self.load_trace()



    def load_trace(self):
        from .xref_loader import load_64disasm
        self.TRACE_REF= load_64disasm()

    def keyrelease(self, event):
        pass

    def keypress(self, event):        
        self.keypresses.append(event)

    def describe_state(self,cpu,mem):
        """ Describe the current state if there is some new message under the hood 
            FIXME: Try also to unwind the stack a bit
        """
        if cpu.pc in self.TRACE_REF:
            category, comment=self.TRACE_REF[cpu.pc]
            msg="{:02X} {:6.6} {:100.100}".format(cpu.pc,category,comment)
            if self.last_describe_state!=msg:
                print(msg+(" - A=${:02x} X=${:02x} Y=${:02x} P=%{:08b} SP={:02X}"
                    .format( cpu.a, cpu.x, cpu.y, cpu.p, cpu.sp)))
                # for i in range(cpu.sp+2, cpu.sp-8, -2):
                #     loc=mem[i] +mem[i-1]*256
                #     if i==cpu.sp:
                #         print("Stack: {:02X} ptr* -> {:04X} ".format(i, loc))
                #     else:
                #         print("Stack: {:02X} ptr  -> {:04X} ".format(i, loc))
                self.last_describe_state=msg         
    

    def run_rom_code(self, reset):
        # Init memory interceptors
        cpu = CPU(memory=self.screen.memory, pc=reset)
        self.real_cpu_running = cpu
        #self.monitor_window.set_cpu(cpu)
        previous_cycles = 0
        mem = self.screen.memory
        old_raster = 0
        while True:
            irq_start_time = time.perf_counter()
            while time.perf_counter() - irq_start_time < 1.0/60.0:
                for _ in range(1000):
                    cpu.step()
                    if self.trace_status():
                        self.describe_state(cpu,mem)
                    if cpu.pc == 0xFFD8:
                        self.breakpointKernelSave(cpu,mem)
                    elif cpu.pc == 0xFFD5:
                        self.breakpointKernelLoad(cpu,mem)                      
                    # FFCF KERNAL CHRIN  Input character from channel    byte -> A  - A=$40 X=$01 Y=$0a P=%10110000                    
                    # LISTEN 8/OPEN 15/"I"/UNLISTEN/LISTEN 8/CLOSE 15/UNLISTEN
                    elif cpu.pc == 0xFFBA:
                        print("** Reading logical, first and second file parameters A = lfn, X = pa, Y = sa")
                        if cpu.x == 23:
                            print("Registering Probe for Device 23 logical file {}".format(cpu.a))
                            self.device23[cpu.a]={}
                        # self.last_kernel_file=IORecord(cpu.a,cpu.x,cpu.y,"")
                        # print("{}".format (self.last_kernel_file))
                    elif cpu.pc == 0xFFBD and cpu.a !=0:                        
                        # A = len, X/Y = name
                        # X low, Y High                        
                        fname=self.get_filename(cpu.x+cpu.y*256,cpu.a,cpu)
                        ## 
                        # FFC0 KERNAL Open a logical file / 0xB8 è  logical filename?!
                        print("** Reading filename (if A=0 ignore it) {}".format(fname))
                        # Then execute FFDB to be sure data is set                                            
                    # FFCF KERNAL CHRIN       Input character from channel    byte -> A       - A=$01 X=$00 Y=$00 P=%00110010 SP=F0
                    # F157 KERNAL Input a byte              - A=$01 X=$00 Y=$00 P=%00110010 SP=F0                        
                    # Traps 
                    # +KERNAL Send LISTEN Command on Serial Bus
                    # +KERNAL Send LISTEN Secondary Addres
                    # +KERNAL Send Data On Serial Bus 
                    # and avoid stalling the emulator                    
                    elif cpu.pc in [ 0xED0C, 0xEDB9, 0xED40 ]:
                        # RTS on Listen
                        # print("LISTEN / SEND Low level Kernal TRAPPED")
                        cpu.pc=0xE1C6

                    # -------
                    # set the raster line based off the number of CPU cycles processed
                    raster = (cpu.processorCycles//63) % 312
                    if raster != old_raster:
                        mem[53266] = raster and 255
                        high = mem[53265] & 0b01111111
                        if raster > 255:
                            high |= 0b10000000
                        mem[53265] = high
                        old_raster = raster
                # skip sleep if trace active: we are too slow to take care of this sleep                        
                if not self.trace_status():
                    time.sleep(0.001)
            self.irq(cpu)
            duration = time.perf_counter() - irq_start_time
            speed = (cpu.processorCycles-previous_cycles) / duration / 1e6
            previous_cycles = cpu.processorCycles    
            if self.trace_status()==False:
                print("CPU simulator: PC=${:04x} A=${:02x} X=${:02x} Y=${:02x} P=%{:08b} -  clockspeed = {:.1f} MHz   "
                .format(cpu.pc, cpu.a, cpu.x, cpu.y, cpu.p, speed), end="\r")


    def breakpointKernelSave(self,cpu,mem):        
        """ Ref https://github.com/irmen/ksim65/blob/d1d433c3a640e1429f8fe2755afa96ca39c4dfbb/src/main/kotlin/razorvine/c64emu/c64Main.kt#L82
        """
        print("Kernal Save Intercept....")        
        fnlen = mem[0xb7]   # file name length
        fa = mem[0xba]      # device number
        sa = mem[0xb9]      # secondary address
        fnaddr = cpu.WordAt(0xbb)  # memory[0xbb]+256*memory[0xbc]  # file name address
        if fnlen >0:            
            fname=self.get_filename(fnaddr,fnlen,cpu)
            startAddr= mem[cpu.a]+256*mem[cpu.a+1]
            endAddr=cpu.x+256*cpu.y
            print("\nSaving... {} Start Addr:{:02X} End: {:02X} Size:{}".format(fname,startAddr,endAddr, endAddr-startAddr))
            # Write fromAddr high and low
            with open("drive{}/{}".format(fa,fname), "wb") as file:
                file.write(startAddr.to_bytes(2, byteorder='little'))
                print("Header ok")
                for i in range(startAddr,endAddr):
                    data= mem[i].to_bytes(1, byteorder='little')
                    file.write( data )
                    print("{}".format(data))
                file.close()                
            # write data
            mem[0x90]=0 # OK
            print("Save completed\n")
            #success!
            cpu.pc=0xf5a9
        else:
            print("?missing file name")
            cpu.pc=0xf710 

    def breakpointKernelLoad(self,cpu,mem):
        """ Ported from kim65
        https://github.com/irmen/ksim65/blob/d1d433c3a640e1429f8fe2755afa96ca39c4dfbb/src/main/kotlin/razorvine/c64emu/c64Main.kt#L82
        """
        if cpu.a ==0:
            fnlen = mem[0xb7]   # file name length
            fa = mem[0xba]      # device number (i.e 8)
            sa = mem[0xb9]      # secondary address (i.e 15 for disk commands)
            # Redirect TAP to disk8
            if fa==1:
                fa=8
            destinationAddress=mem[0x2b]+256*mem[0x2c]
            fnaddr = cpu.WordAt(0xbb)             
            fname=self.get_filename(fnaddr,fnlen,cpu)
            if fnlen ==0:
                print("?missing file name")
                cpu.pc=0xf710 
                return
            if fname=="$":
                # Make magic dir listing
                print("Generating dir listing")
                prog=self.make_dir_listing(fa,destinationAddress)
                self.load(destinationAddress,prog)  
                cpu.pc=0xf5a9
                return            
            else:
                final_path="drive{}/{}".format(fa, fname)
                try:
                    with open(final_path, "rb") as file:
                        startAddr = struct.unpack("<H", file.read(2))[0]                                            
                        prog=file.read()
                        endAddress=self.load(startAddr,prog)
                        print("\nLoading {:02X}:{:02X} {} Start Addr: {:02X} ... up to: $ {:02X}\n".format(
                                       fa,sa,final_path, startAddr, endAddress))                        
                        file.close()                
                    # success
                    cpu.pc=0xf5a9
                except FileNotFoundError:
                    print("ERR FILE NOT FOUND:", final_path)
                    cpu.pc=0xf704 # 'file not found'           
        else:
            print("device not present (VERIFY command not supported)")
            cpu.pc=0xf707

    def load(self,startAddr,prog):
        """
         Load a program into memory.
         Emulate Kernal code for prg loads
        """
        ram = self.screen.memory
        cpu = self.real_cpu_running
        endAddress= startAddr + len(prog)
        ram[startAddr: endAddress] = prog
        ram[0x90] = 0  # status OK                
        ram[0xae]= endAddress & 0x00ff
        high=(endAddress & 0xff00) >>8                    
        ram[0xaf]= high
        return endAddress        

    def get_filename(self,fnaddr,fnlen,cpu):
        fname=""
        for i in range(0,fnlen):
            fname=fname + chr(cpu.ByteAt(fnaddr+i)).lower()
        if fname!="$" and ("." not in fname):
            fname=fname+".prg"
        return fname         

    def make_dir_listing(self,deviceNumber,basicLoadAddress):
        listing=[]
        address = basicLoadAddress
        def add_line(lineNumber:int, line: str):
            nonlocal address
            address = address + len(line)+3
            listing.append(address & 0xff)
            listing.append( (address & 0xff00) >>8 )
            listing.append( lineNumber & 0xff)
            listing.append( (lineNumber & 0xff00) >>8 )
            data=bytearray(line,"utf-8")
            for d in data:
                listing.append(d)
            listing.append(0)        
        # For formatting see https://pyformat.info/#string_pad_align
        add_line(0, "\u0012\"{:16.16}\" 00 2A".format("DRIVE"+str(deviceNumber)))
        # scan directory and find out files.
        # Then produce a "floppy disk drive"-like directory
        total_blocks=0
        for root, dirs, filenames in os.walk("./drive{}".format(deviceNumber)):
            for fname in fnmatch.filter(filenames,"*"):
                st=os.stat(os.path.join(root,fname))
                block_size=int(st.st_size/256)+1
                total_blocks += block_size
                if "." in fname:
                    splitted_filename=fname.upper().split(".")
                    base_filename=splitted_filename[0]
                    extension=splitted_filename[1]
                else:
                    base_filename=fname.upper()
                    extension=""
                # Create an aligned line
                pad1="   "[0: 3-len(str(block_size))] 
                add_line(block_size,"{} {:18.18} {:3.3}".format(pad1,"\""+base_filename+"\"",extension))                
        add_line(644-total_blocks , "BLOCKS FREE.")
        # Basic program termination
        listing.append(0);listing.append(0)
        return listing


    def irq(self, cpu):
        self.simulate_keystrokes()
        if hasattr(cpu, "irq"):
            cpu.irq()
        else:
            self.cpu_irq(cpu)

    def cpu_irq(self, cpu):
        # fallback for py65 library that doesn't yet have the irq() and nmi() methods
        if cpu.p & cpu.INTERRUPT:
            return
        cpu.stPushWord(cpu.pc)
        cpu.p &= ~cpu.BREAK
        cpu.stPush(cpu.p | cpu.UNUSED)
        cpu.p |= cpu.INTERRUPT
        cpu.pc = cpu.WordAt(cpu.IRQ)
        cpu.processorCycles += 7

    control_color_chars = {
        '0': 0x92,
        '1': 0x90,
        '2': 0x05,
        '3': 0x1c,
        '4': 0x9f,
        '5': 0x9c,
        '6': 0x1e,
        '7': 0x1f,
        '8': 0x9e,
        '9': 0x12,
    }

    commodore_color_chars = {
        '0': 0x00,
        '1': 0x81,
        '2': 0x95,
        '3': 0x96,
        '4': 0x97,
        '5': 0x98,
        '6': 0x99,
        '7': 0x9a,
        '8': 0x9b,
        '9': 0x00,
    }

    def simulate_keystrokes(self):
        if not self.keypresses:
            return
        num_keys = self.screen.memory[0xc6]
        while self.keypresses and num_keys < self.screen.memory[0x289]:
            event = self.keypresses.pop()
            #print(repr(event))
            char = event.char
            if not char or ord(char) > 255:
                char = event.keysym
            with_shift = event.state & 1
            with_control = event.state & 4
            with_alt = event.state & 8
            if (with_control or with_alt) and event.keysym in "0123456789":
                # control+number or alt+number
                if with_control:
                    petscii = self.control_color_chars[event.keysym]
                else:
                    petscii = self.commodore_color_chars[event.keysym]
            elif char == '\b':
                petscii = 0x14    # backspace ('delete')
            elif char == '\x1b':
                petscii = 0x83 if with_shift else 0x03
            elif event.keysym == "Home":
                petscii = 0x93 if with_shift else 0x13      # clear/home
            elif event.keysym == "Up":
                petscii = 0x91
            elif event.keysym == "Down":
                petscii = 0x11
            elif event.keysym == "Left":
                petscii = 0x9d
            elif event.keysym == "Right":
                petscii = 0x1d
            elif event.keysym == "Insert":
                petscii = 0x94
            elif event.keysym == "F1":
                petscii = 0x85
            elif event.keysym == "F2":
                petscii = 0x86
            elif event.keysym == "F3":
                petscii = 0x87
            elif event.keysym == "F4":
                petscii = 0x88
            elif event.keysym == "F5":
                petscii = 0x89
            elif event.keysym == "F6":
                petscii = 0x8a
            elif event.keysym == "F7":
                petscii = 0x8b
            elif event.keysym == "F8":
                petscii = 0x8c
            elif (event.keycode == 50 and with_alt) or (event.keycode == 64 and with_shift):
                charset = self.screen.memory[0xd018] & 0b00000010
                petscii = 0x8e if charset else 0x0e
            else:
                try:
                    encoded = self.screen.encode_petscii(event.char)
                    if encoded:
                        petscii = encoded[0]
                    else:
                        return
                except UnicodeEncodeError:
                    return      # not mapped
            self.screen.memory[0x277 + num_keys] = petscii
            num_keys += 1
        self.screen.memory[0xc6] = num_keys




def start(args=None):
    rom_directory = "roms"
    screen = ScreenAndMemory(columns=C64EmulatorWindow.columns,
                             rows=C64EmulatorWindow.rows,
                             sprites=C64EmulatorWindow.sprites,
                             rom_directory=rom_directory,
                             run_real_roms=True)
    emu = RealC64EmulatorWindow(screen, "Commodore-64 emulator in pure Python! - running actual roms", rom_directory,args)
    emu.start()
    emu.mainloop()


if __name__ == "__main__":
    start()
