# simple_coin_machine.py

from my_states import LockedState
import logging
logging.basicConfig(level=logging.DEBUG)

class SimpleCoinMachine(object):
    """ 
    A simple state machine that mimics the functionality of a coin machine from a 
    high level.
    """

    def __init__(self):
        """ Initialize the components. """
        logging.debug("Initialised a coin machine, please change states by on_event() function call")
        # Start with a default state.
        self.state = LockedState()

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)