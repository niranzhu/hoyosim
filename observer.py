import logging
from event import Event

# logging.basicConfig(level=logging.DEBUG)


class Observer:
    def __init__(self, priority=0):
        self.event = Event()
        self.event.add_observer(self)
        self.priority = priority  # 响应优先级

    def response_event(self):
        logging.debug(self.event.state)
        '''if 'say' in self.event.state and self.event.state['say'] == 'hello':
            self.change_event({'say': 'world'})'''

    def change_event(self, state):
        self.event.change_event(state)

    def modify_event(self, state):
        self.event.modify_event(state)

    def modify_last_event(self, state):
        self.event.modify_last_event(state)

    def remove_observer(self, observer):
        self.event.remove_observer(observer)

    def add_observer(self, observer):
        self.event.add_observer(observer)

    def get_state(self, key, data_type=int):
        zero_value = None
        if self.event.state and key in self.event.state:
            return self.event.state[key]
        elif data_type == int:
            zero_value = 0
        elif data_type == float:
            zero_value = 0.0
        elif data_type == bool:
            zero_value = False
        elif data_type == str:
            zero_value = ''
        elif data_type == list:
            zero_value = []
        elif data_type == tuple:
            zero_value = ()
        elif data_type == dict:
            zero_value = {}
        elif data_type == set:
            zero_value = set()
        return zero_value

