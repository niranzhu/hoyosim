import logging


# 单例模式
def singleton(cls):
    instance = {}

    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return wrapper


@singleton
class Event:
    def __init__(self):
        self.observers = []
        self.state = {}
        self.previous_states = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def change_event(self, state={}):
        # 记录事件前的状态。
        self.previous_states.append(self.state)
        self.state = state  # 更新状态

        self.notify_observers()

        # 所有观察者都完成响应后，回退事件状态。
        if self.previous_states:
            self.state = self.previous_states.pop()

    def modify_event(self, state):
        new_state = dict(self.state)
        new_state.update(state)
        self.change_event(new_state)

    def modify_last_event(self, state):
        self.previous_states[-1].update(state)

    def notify_observers(self):
        # 优先级考虑
        sorted_observers = sorted(self.observers, key=lambda x: x.priority, reverse=True)
        for observer in sorted_observers:
            observer.response_event()
