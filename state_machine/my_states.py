# my_states.py

from state import State
import logging
logging.basicConfig(level=logging.DEBUG)

# Start of our states
class LockedState(State):
    """
    The state which indicates that the coin machine is in locked state.
    """
    
    # constructor takes care of state entry() and exit() functionalities
    # do not need destructor for this specific case
    def __init__(self):
        self.supported_events = ["coin", "failed"]
        self.collected_amount = 0
        logging.debug('Entered LockedState')

    def accumulate(self):
        amount = input('please enter the amount of coins')
        self.collected_amount += int(amount) 

        if self.collected_amount < 20:
            print ('Still need %d coins to unlock' % (20-self.collected_amount))

    def on_event(self, event):
        if event == 'coin':
            print ("current collected_amount is %d" % self.collected_amount)
            self.accumulate()
            if self.collected_amount >= 20:
                return UnlockedState()
            else:
                return self 

        elif event == 'failed':
            print ('Machine is Out of order')
            return BrokenState()
        else:
            print ('This event %s is not supported in this state' % event)
            print ('Supported events are %s' % self.supported_events)
            return self

class UnlockedState(State):
    """
    The state which indicates that the coin machine is in unlocked state.
    """
    def __init__(self):
        self.supported_events = ["pass","coin", "failed"]
        logging.debug('Entered UnlockedState')

    def on_event(self, event):
        if event == 'pass':
            return LockedState()
        elif event == 'coin':
            print ("Thanks!")
            return self
        elif event == 'failed':
            print ('Machine is Out of order')
            return BrokenState()
        else:
            print ('This event %s is not supported in this state' % event)
            print ('Supported events are %s' % self.supported_events)
            return self


class BrokenState(State):
    """
    The state which indicates that the coin machine is in broken state.
    """
    def __init__(self):
        self.supported_events = ["fixed"]
        logging.debug('Entered BrokenState')

    def on_event(self, event):
        if event == 'fixed':
            return LockedState()
        else:
            print ('This event %s is not supported in this state' % event)
            print ('Supported events are %s' % self.supported_events)
            return self
# End of our states.