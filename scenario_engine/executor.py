import time
import threading
from threading import Timer
from queue import Queue
from paho.mqtt.client import topic_matches_sub

STEPS_FUN_KEY = "steps_fun"
SECONDS_KEY = "seconds"
START_TIME_KEY = "start"
EVENT_KEY = "event"

queues_dictionary = {}


def emit_event(event_name):
    """
    Puts event to all queues in queues_dictionary with matching regular expression.

    :param event_name: string representing the name of event to be matched with queues.
    """
    for event_pattern in list(queues_dictionary):
        if topic_matches_sub(event_pattern, event_name):
            queues_dictionary[event_pattern].put(event_name)


class ConditionalTimer(threading.Timer):
    """
    Timer class which waits for release of condition variable before running.
    """
    def __init__(self, interval, function_arg, condition, args=None, kwargs=None):
        """
        :param interval: interval after which function will be run
        :param function_arg: function to execute
        :param condition: condition variable to wait for before starting timer
        """
        threading.Timer.__init__(self, interval=interval, function=function_arg, args=args, kwargs=kwargs)
        self.condition = condition

    def run(self):
        """
        Wait until condition variable is released, then start timer.
        """
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
        """
        Get time of scenario execution.

        :return: current execution time in seconds
        """
        return time.time() - self.start_time


executor = Executor()


def parametrized(decorator):
    """
    Decorator for other decorators, which enables them to be parametrized like functions. Parameters on resulting
    decorator by *kwargs dictionary.

    :param decorator: decorator which will be parametrized
    """
    def layer(*args, **kwargs):
        def wrapper(f):
            return decorator(f, *args, **kwargs)
        return wrapper
    return layer


@parametrized
def after(steps_fun, **kwargs):
    """
    Decorator which executes function after given time.
    Recognized kwargs:
        - seconds: seconds after which function will be executed.

    :param steps_fun: function to be executed
    """
    ConditionalTimer(kwargs[SECONDS_KEY], steps_fun, executor.cond).start()
    return steps_fun


@parametrized
def every(steps_fun, *args, **kwargs):
    """
    Decorator which executes function periodically in time domain.
    Recognized kwargs:
        - seconds: interval in seconds between function executions
        - start: time in seconds of first execution

    :param steps_fun: function to be executed
    """
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
    """
    Decorator which executes function on each occurrence of event.
    Recognized kwargs:
        - event: name of event triggering function execution

    :param steps_fun: function to be executed
    """
    def execute():
        while True:
            event_name = queues_dictionary[event_pattern].get(block=True)
            steps_fun(event_name)

    event_pattern = kwargs[EVENT_KEY]
    if event_pattern not in queues_dictionary.keys():
        queues_dictionary[event_pattern] = Queue()
    threading.Thread(target=execute, args=()).start()
    return steps_fun


@parametrized
def on_event(steps_fun, **kwargs):
    """
   Decorator which executes function on first occurrence of event.
   Recognized kwargs:
       - event: name of event triggering function execution

   :param steps_fun: function to be executed
   """
    def execute():
        event_name = queues_dictionary[event_pattern].get(block=True)
        steps_fun(event_name)

    event_pattern = kwargs[EVENT_KEY]
    if event_pattern not in queues_dictionary.keys():
        queues_dictionary[event_pattern] = Queue()
    threading.Thread(target=execute, args=()).start()
    return steps_fun


def start_executing():
    executor.start()
