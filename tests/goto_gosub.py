import unittest
from pyc64.basic import BasicInterpreter, BasicError, GotoLineException
from pyc64.memory import ScreenAndMemory

class BasicEmulatorTest(unittest.TestCase):
    
    def setUp(self):
        self.b = BasicInterpreter(ScreenAndMemory())

    def tearDown(self):
        self.b=None

    def test_ok(self):
        self.assertEqual(True,True)
    def test_on_goto0(self):
        try:
            self.b.execute_on_goto_gosub("on 1 goto 1,2")
            self.fail("unde'd statement error expected")
        except BasicError as e:
            pass
    
    def test_on_goto1(self):
        try:
            # LOADED:{0: 'rem Tester', 20: 'on 2 goto 30,40', 30: 'print "failure"', 40: 'print "success"'}
            self.b.execute_load("load \"ongoto1\" ")
            self.b.execute_run("run 20")
            #b.execute_line("run 20")
            self.fail("No error?")
        except GotoLineException as gx:
            self.b.implementGoto(gx)
            self.assertTrue(self.b.running_program)
            self.b.program_step()
            #print("CURRENT LINE:"+str(self.b.next_run_line_idx))
            self.assertEqual(3,self.b.next_run_line_idx)
            #b.execute_run("run")
            # print("***"+str(b.))
    # TODO Implement a silly test program to test the on expr syntax

    def test_gosub1(self):
        try:
            print("TESTING")
            self.b.execute_load("load \"gosubtest1\" ")
            self.b.execute_run("run")
        except GotoLineException as gx:
            self.b.implementGoto(gx)
            self.b.program_step()
            self.b.program_step()
            print("Stack: %s -- %s " %( self.b.basic_stack , self.b.data_line))
            self.b.program_step()
            print("Stack: %s -- %s " %( self.b.basic_stack , self.b.data_line))
            self.b.program_step()
            print("Stack: %s -- %s " %( self.b.basic_stack , self.b.data_line))


if __name__ == '__main__':
    unittest.main()
