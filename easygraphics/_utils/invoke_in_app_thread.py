#####################################################################
#                                                                   #
# invoke_in_main.py                                                 #
#                                                                   #
# Copyright 2013, Christopher Billington, Philip Starkey            #
#                                                                   #
# This file is part of the qtutils project                          #
# (see https://bitbucket.org/philipstarkey/qtutils )                #
# and is licensed under the 2-clause, or 3-clause, BSD License.     #
# See the license.txt file in the root of the project               #
# for the full license.                                             #
#
#                                                                   #
#####################################################################

import functools
# tailored and modified by roy
import sys
import threading
import time
from queue import Queue

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, QObject, QCoreApplication


def _reraise(exc_info):
    exc_type, value, traceback = exc_info
    raise value.with_traceback(traceback)


class CallEvent(QEvent):
    """An event containing a request for a function call."""
    EVENT_TYPE = QEvent(QEvent.registerEventType())

    def __init__(self, queue, exceptions_in_main, fn, *args, **kwargs):
        QEvent.__init__(self, self.EVENT_TYPE)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self._returnval = queue
        # Whether to raise exceptions in the main thread or store them
        # for raising in the calling thread:
        self._exceptions_in_main = exceptions_in_main


class Caller(QObject):
    """An event handler which calls the function held within a CallEvent."""

    def event(self, event):
        event.accept()
        exception = None
        try:
            result = event.fn(*event.args, **event.kwargs)
        except Exception:
            # Store for re-raising the exception in the calling thread:
            exception = sys.exc_info()
            result = None

            if not event._exceptions_in_main:
                raise
        finally:
            event._returnval.put([result, exception])
        return True


_caller = None


def init_invoke_in_app():
    global _caller
    _caller = Caller()
    _wait_for_quit = False


def destroy_invoke_in_app():
    global _caller, _wait_for_quit
    _caller = None
    _wait_for_quit = False


def _start_app_thread():
    app = QtWidgets.QApplication([])
    font = app.font()
    font.setPixelSize(_font_size)
    app.setFont(font)
    app.setQuitOnLastWindowClosed(False)
    init_invoke_in_app()
    # init finished, can draw now
    return app



_wait_for_quit = False


def wait_for_quit():
    global _wait_for_quit
    _wait_for_quit = True

_app_lock = threading.Lock()
def invoke_in_app_thread(fn, *args, **kwargs):
    """Queue up the executing of a function in the main thread and return immediately.

    This function queues up a custom :code:`QEvent` to the Qt event loop.
    This event executes the specified function :code:`fn` in the Python
    MainThread with the specified arguments and keyword arguments, and returns
    a Python Queue which will eventually hold the result from the executing of
    :code:`fn`. To access the result, use :func:`qtutils.invoke_in_main.get_inmain_result`.

    This function can be used from the MainThread, but such use will just directly call the function, bypassing the Qt event loop.

    Arguments:
        fn: A reference to the function or method to run in the MainThread.

        *args: Any arguments to pass to :code:`fn` when it is called from the
               MainThread.

        **kwargs: Any keyword arguments to pass to :code:`fn` when it is called
                  from the MainThread

    Returns:
       A Python Queue which will eventually hold the result
       :code:`(fn(*args, **kwargs), exception)` where
       :code:`exception=[type,value,traceback]`.
    """
    _app_lock.acquire()
    try:
        if _caller is None:
            app = _start_app_thread()
            result = fn(*args, **kwargs)
            destroy_invoke_in_app()
            app.quit()
            app = None
            return result
        elif _wait_for_quit:  # the app is quitting. don't show the dialog
            return None
        result = get_in_app_thread_result(_in_app_thread_later(fn, True, *args, **kwargs))
        return result
    finally:
        _app_lock.release()


def _in_app_thread_later(fn, exceptions_in_main, *args, **kwargs):
    """Asks the mainloop to call a function when it has time. Immediately
    returns the queue that was sent to the mainloop.  A call to queue.get()
    will return a list of [result,exception] where exception=[type,value,traceback]
    of the exception.  Functions are guaranteed to be called in the order
    they were requested."""
    queue = Queue()
    QCoreApplication.postEvent(_caller, CallEvent(queue, exceptions_in_main, fn, *args, **kwargs))
    return queue


def get_in_app_thread_result(queue):
    """ Processes the result of :func:`qtutils.invoke_in_main.inmain_later`.

    This function takes the queue returned by :code:`inmain_later` and blocks
    until a result is obtained. If an exception occurred when executing the
    function in the MainThread, it is raised again here (it is also raised in the
    MainThread). If no exception was raised, the result from the execution of the
    function is returned.

    Arguments:
        queue: The Python Queue object returned by :code:`inmain_later`

    Returns:
        The result from executing the function specified in the call to
        :code:`inmain_later`

    """
    result, exception = queue.get()
    if exception is not None:
        _reraise(exception)
    return result


_font_size = 18


def set_app_font(size: int):
    global _font_size
    _font_size = size


def invoke_in_thread():
    """ A decorator which enforces the execution of the decorated thread to occur in the MainThread.

    Returns:
        The decorator returns a function that has wrapped the decorated function
        in the appropriate call to :code:`inmain` or :code:`inmain_later` (if
        you are unfamiliar with how decorators work, please see the Python
        documentation).

        When calling the decorated function, the result is either the result of
        the function executed in the MainThread (if :code:`wait_for_return=True`)
        or a Python Queue to be used with
        :func:`qtutils.invoke_in_main.get_inmain_result` at a later time.

    """

    def wrap(fn):
        """A decorator which sets any function to always run in the main thread."""

        @functools.wraps(fn)
        def f(*args, **kwargs):
            return invoke_in_app_thread(fn, *args, **kwargs)

        return f

    return wrap
