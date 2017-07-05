import time
import threading
from threading import Timer
from queue import Queue
from paho.mqtt.client import topic_matches_sub

STEPS_FUN_KEY = "steps_fun"
SECONDS_KEY = "seconds"
START_TIME_KEY = "start"

queues_dictionary = {}


def emit_event(event_name):

    for event_pattern in list(queues_dictionary):
        if topic_matches_sub(event_pattern, event_name):
            queues_dictionary[event_pattern].put(event_name)


class ConditionalTimer(threading.Timer):
    def __init__(self, interval, function_arg, condition, args=None, kwargs=None):
        threading.Timer.__init__(self, interval=interval, function=function_arg, args=args, kwargs=kwargs)
        self.condition = condition

    def run(self):
        with self.condition:
            self.condition.wait()
        threading.Timer.run(self)


class Executor:
    def __init__(self):
        self.cond = threading.Condition()
        self.start_time = time.time()

    def start(self):
        with self.cond:
            self.cond.notifyAll()

    def get_time(self):
        return time.time() - self.start_time


executor = Executor()


def parametrized(decorator):
    def layer(*args, **kwargs):
        def wrapper(f):
            return decorator(f, *args, **kwargs)

        return wrapper

    return layer


@parametrized
def after(steps_fun, **kwargs):
    ConditionalTimer(kwargs[SECONDS_KEY], steps_fun, executor.cond).start()
    return steps_fun


@parametrized
def every(steps_fun, *args, **kwargs):
    def execute_repeatedly(steps_fun, *args, **kwargs):
        try:
            steps_fun()
        except StopIteration:
            print("Not enough data to continue data generation")
            return
        kwargs[STEPS_FUN_KEY] = steps_fun
        Timer(kwargs[SECONDS_KEY], execute_repeatedly, args, kwargs).start()

    start_time = 0
    if "start" in kwargs.keys():
        start_time = kwargs[START_TIME_KEY]
    kwargs[STEPS_FUN_KEY] = steps_fun
    ConditionalTimer(start_time, execute_repeatedly, executor.cond, args, kwargs).start()
    return steps_fun


@parametrized
def every_event(steps_fun, *args, **kwargs):
    def execute():
        while True:
            event_name = queues_dictionary[event_pattern].get(block=True)
            steps_fun(event_name)

    event_pattern = kwargs["event"]
    if event_pattern not in queues_dictionary.keys():
        queues_dictionary[event_pattern] = Queue()
    threading.Thread(target=execute, args=()).start()
    return steps_fun


@parametrized
def on_event(steps_fun, **kwargs):
    def execute():
        event_name = queues_dictionary[event_pattern].get(block=True)
        steps_fun(event_name)

    event_pattern = kwargs["event"]
    if event_pattern not in queues_dictionary.keys():
        queues_dictionary[event_pattern] = Queue()
    threading.Thread(target=execute, args=()).start()
    return steps_fun


def start_executing():
    executor.start()
