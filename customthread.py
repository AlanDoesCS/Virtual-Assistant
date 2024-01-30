# Custom threading class for returning values
from threading import Thread


class CustomThread(Thread):  # Custom Thread by CodersLegacy on YouTube
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):  # Override existing run method
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):  # Override existing join method
        Thread.join(self)
        return self._return


def CustomThreadTest():
    def add(n1, n2):
        result = n1 + n2
        return result

    try:
        thread = CustomThread(target=add, args=(5, 4))
        thread.start()
        print("Custom Thread Test Success!:", thread.join())
    except:
        print("Custom Thread Test Failed!")