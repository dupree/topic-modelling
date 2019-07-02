import unittest
import io
import sys
from contextlib import contextmanager

from simple_coin_machine import SimpleCoinMachine
import my_states

@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig


class TestNotebook(unittest.TestCase):

    def setUp(self):
        self.device = SimpleCoinMachine()

    def test_state_initial(self): # tests machine starts in Locked state with collected_amount = 0
        self.assertEqual(str(self.device.state), "LockedState")
        self.assertEqual(self.device.state.collected_amount, 0)

    # test (a subset of) state transitions which are not allowed

    def test_illegal_moves_LockedState(self):
        self.assertEqual(str(self.device.state), "LockedState")
        self.device.on_event('pass')
        self.assertEqual(str(self.device.state), "LockedState")
        self.device.on_event('fixed')
        self.assertEqual(str(self.device.state), "LockedState")

        with replace_stdin(io.StringIO("10")): # with 10 coins machine stays in LockedState
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "LockedState")
        
    def test_illegal_moves_UnlockedState(self):
        self.assertEqual(str(self.device.state), "LockedState")
        
        with replace_stdin(io.StringIO("20")): # with 20 coins machine moves to UnlockedState
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "UnlockedState")
            
        self.device.on_event('fixed')
        self.assertEqual(str(self.device.state), "UnlockedState")

    def test_illegal_moves_BrokenState(self):
        self.assertEqual(str(self.device.state), "LockedState")
        self.device.on_event('failed')
        self.assertEqual(str(self.device.state), "BrokenState")
    
    def test_accumulate(self):
        with replace_stdin(io.StringIO("10")): # with 10 coins machine stays in LockedState
            self.device.on_event('coin')
            self.assertEqual(self.device.state.collected_amount, 10)
            self.assertEqual(str(self.device.state), "LockedState")
            
        with replace_stdin(io.StringIO("20")): # with 20 coins machine moves to UnlockedState
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "UnlockedState")        

    # test (a subset of) state transitions which are allowed
    
    def test_legal_moves_LockedState(self):
        self.assertEqual(str(self.device.state), "LockedState")
        self.device.on_event('failed')
        self.assertEqual(str(self.device.state), "BrokenState")

        self.device.on_event('fixed') # move back to LockedState
        with replace_stdin(io.StringIO("10")): # with 10 coins machine stays in LockedState
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "LockedState")

        with replace_stdin(io.StringIO("20")): # with 20 coins machine moves to UnlockedState
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "UnlockedState")

    def test_legal_moves_BrokenState(self): 
        self.device.on_event('failed')
        self.assertEqual(str(self.device.state), "BrokenState")

        self.device.on_event('fixed') # move back to LockedState
        self.assertEqual(str(self.device.state), "LockedState")

    def test_legal_moves_UnlockedState(self):
        with replace_stdin(io.StringIO("20")): # with 20 coins machine goes in UnlockedState
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "UnlockedState")
            self.device.on_event('failed')
            self.assertEqual(str(self.device.state), "BrokenState")
            self.device.on_event('fixed') # move back to LockedState

        with replace_stdin(io.StringIO("20")):    
            self.device.on_event('coin')
            self.assertEqual(str(self.device.state), "UnlockedState")
            self.device.on_event('pass')
            self.assertEqual(str(self.device.state), "LockedState")


unittest.main(argv=[''], verbosity=2, exit=False)