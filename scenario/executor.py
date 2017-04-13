import threading
from threading import Timer

STEPS_FUN_KEY = "steps_fun"
SECONDS_KEY = "seconds"
START_TIME_KEY = "start"


class ConditionalTimer(threading.Timer):
    def __init__(self, interval, function, condition, args=None, kwargs=None):
        threading.Timer.__init__(self, interval=interval, function=function, args=args, kwargs=kwargs)
        self.condition = condition

    def run(self):
        with self.condition:
            self.condition.wait()
        threading.Timer.run(self)


class World():
    def __init__(self):
        self.cond = threading.Condition()

    def start(self):
        with self.cond:
            self.cond.notifyAll()


world = World()


def parametrized(decorator):
    def layer(*args, **kwargs):
        def wrapper(f):
            return decorator(f, *args, **kwargs)

        return wrapper

    return layer


@parametrized
def after(steps_fun, **kwargs):
    if steps_fun.__name__ == "steps":
        ConditionalTimer(kwargs[SECONDS_KEY], steps_fun, world.cond).start()
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

    if steps_fun.__name__ == "steps":
        start_time = 0
        if "start" in kwargs.keys():
            start_time = kwargs[START_TIME_KEY]
        kwargs[STEPS_FUN_KEY] = steps_fun
        ConditionalTimer(start_time, execute_repeatedly, world.cond, args, kwargs).start()
        return steps_fun


def start_world():
    world.start()
