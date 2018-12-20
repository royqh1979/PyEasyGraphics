"""
Message Dialogs
most code from EasyGUI_Qt(https://github.com/aroberge/easygui_qt/)
"""
import datetime
import os
import sys
import traceback
import webbrowser
from typing import List, Optional, Union

from PyQt5 import QtCore, QtWidgets

from ._indexed_order_list import IndexedOrderedDict
from . import calendar_widget
from . import multichoice
from . import multifields
from . import show_text_window
from .invoke_in_app_thread import set_app_font, invoke_in_thread

__all__ = [
    'set_dialog_font_size',
    'show_message', 'show_text', 'show_code', 'show_file',
    'get_abort', 'get_choice', 'get_color_hex', 'get_color_rgb', 'get_color_hex',
    'get_continue_or_cancel', 'get_date', 'get_directory_name', 'get_file_names',
    'get_float', 'get_int', 'get_integer', 'get_list_of_choices', 'get_many_strings',
    'get_new_password', 'get_password', 'get_save_file_name', 'get_string',
    'get_username_password', 'get_yes_or_no'
]


# ========== Message Boxes ====================#
@invoke_in_thread()
def show_message(message: str = "Message",
                 title: str = "Title"):
    """
    Simple message box.

    :param message: message string
    :param title: window title

    >>> from easygraphics.dialog import *
    >>> show_message()

    .. image:: ../../docs/images/show_message.png
    """
    dialog = QtWidgets.QMessageBox(None)
    dialog.setWindowTitle(title)
    dialog.setText(message)
    _send_to_front(dialog)
    dialog.exec()


def _send_to_front(dialog):
    dialog.show()
    dialog.raise_()
    dialog.activateWindow()


@invoke_in_thread()
def get_yes_or_no(question: str = "Answer this question", title: str = "Title") -> Optional[bool]:
    """Simple yes or no question.

       :param question: Question (string) asked
       :param title: Window title (string)

       :return: ``True`` for "Yes", ``False`` for "No",
               and ``None`` for "Cancel".

       >>> from easygraphics.dialog import *
       >>> choice = get_yes_or_no()

       .. image:: ../../docs/images/yes_no_question.png
    """
    flags = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    flags |= QtWidgets.QMessageBox.Cancel

    dialog = QtWidgets.QMessageBox()
    # _send_to_front(dialog)
    reply = dialog.question(None, title, question, flags)
    if reply == QtWidgets.QMessageBox.Cancel:
        return None
    return reply == QtWidgets.QMessageBox.Yes


@invoke_in_thread()
def get_continue_or_cancel(question: str = "Processed will be cancelled!",
                           title: str = "Title",
                           continue_button_text: str = "Continue",
                           cancel_button_text: str = "Cancel") -> bool:
    """Continue or cancel question, shown as a warning (i.e. more urgent than
       simple message)

       :param question: Question (string) asked
       :param title: Window title (string)
       :param continue_button_text: text to display on button
       :param cancel_button_text: text to display on button

       :return: True for "Continue", False for "Cancel"

       >>> from easygraphics.dialog import *
       >>> choice = get_continue_or_cancel()

       .. image:: ../../docs/images/get_continue_or_cancel.png
    """
    dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, question,
                                   QtWidgets.QMessageBox.NoButton)
    dialog.addButton(continue_button_text, QtWidgets.QMessageBox.AcceptRole)
    dialog.addButton(cancel_button_text, QtWidgets.QMessageBox.RejectRole)
    _send_to_front(dialog)
    reply = dialog.exec()
    return reply == QtWidgets.QMessageBox.AcceptRole


# ============= Color dialogs =================
@invoke_in_thread()
def get_color_hex() -> Optional[str]:
    """Using a color _dialog, returns a color in hexadecimal notation
       i.e. a string '#RRGGBB' or "None" if color _dialog is dismissed.

       >>> from easygraphics.dialog import *
       >>> color = get_color_hex()

       .. image:: ../../docs/images/select_color.png
       """
    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.white, None)
    if color.isValid():
        return color.name()


@invoke_in_thread()
def get_color_rgb() -> (int, int, int):
    """Using a color _dialog, returns a color in rgb notation
       i.e. a tuple (r, g, b)  or "None" if color _dialog is dismissed.

       >>> from easygraphics.dialog import *
       >>> color = get_color_rgb()

       .. image:: ../../docs/images/select_color_fr.png
       """
    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.white, None)
    if color.isValid():
        return color.red(), color.green(), color.blue()


# ================ Date ===================
@invoke_in_thread()
def get_date(title: str = "Select Date") -> datetime.date:
    """Calendar widget

       :param title: window title
       :return: the selected date as a ``datetime.date`` instance

       >>> from easygraphics.dialog import *
       >>> date = get_date()

       .. image:: ../../docs/images/get_date.png
    """
    cal = calendar_widget.CalendarWidget(title=title)
    date = cal.date.toPyDate()
    return date


# =========== InputDialogs ========================
def _get_common_input_flags():
    """avoiding copying same flags in all functions"""
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    flags |= QtCore.Qt.WindowStaysOnTopHint
    return flags


class VisibleInputDialog(QtWidgets.QInputDialog):
    """A simple InputDialog class that attempts to make itself automatically
       on all platforms
    """

    def __init__(self):
        super(VisibleInputDialog, self).__init__()


@invoke_in_thread()
def get_int(message: str = "Choose a number", title: str = "Title",
            default_value: int = 1, min_: int = 0, max_: int = 100, step: int = 1) -> Optional[int]:
    """Simple _dialog to ask a user to select an integer within a certain range.

       **Note**: **get_int()** and **get_integer()** are identical.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_value: Default value for integer appearing in the text
                             box; set to the closest of ``min_`` or ``max_``
                             if outside of allowed range.
       :param min_: Minimum integer value allowed
       :param max_: Maximum integer value allowed
       :param step: Indicate the change in integer value when clicking on
                    arrows on the right hand side

       :return: an integer, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> from easygraphics.dialog import *
       >>> number = get_int()

       .. image:: ../../docs/images/get_int.png


       If ``default_value`` is larger than ``max_``, it is set to ``max_``;
       if it is smaller than ``min_``, it is set to ``min_``.

       >>> number = easy.get_integer("Enter a number", default_value=125)

       .. image:: ../../docs/images/get_int2.png

    """
    # converting values to int for launcher demo set_font_size which
    # first queries the user for a value; the initial values are passed
    # as strings by the subprocess module and need to be converted here

    default_value = int(default_value)
    min_ = int(min_)
    max_ = int(max_)

    dialog = VisibleInputDialog()
    flags = _get_common_input_flags()
    number, ok = dialog.getInt(None, title, message,
                               default_value, min_, max_, step,
                               flags)
    dialog.destroy()
    if ok:
        return number


get_integer = get_int


@invoke_in_thread()
def get_float(message: str = "Choose a number", title: str = "Title", default_value: float = 0.0,
              min_: float = -10000, max_: float = 10000, decimals: int = 3) -> Optional[float]:
    """Simple _dialog to ask a user to select a floating point number
       within a certain range and a maximum precision.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_value: Default value for value appearing in the text
                             box; set to the closest of ``min_`` or ``max_``
                             if outside of allowed range.
       :param min_: Minimum value allowed
       :param max_: Maximum value allowed
       :param decimals: Indicate the maximum decimal precision allowed

       :return: a floating-point number, or ``None`` if "cancel" is clicked
                or window is closed.

       >>> from easygraphics.dialog import *
       >>> number = get_float()

       .. image:: ../../docs/images/get_float.png

       **Note:** depending on the locale of the operating system where
       this is used, instead of a period being used for indicating the
       decimals, a comma may appear instead; this is the case for
       the French version of Windows for example.  Therefore, entry of
       floating point values in this situation will require the use
       of a comma instead of a period.  However, the internal representation
       will still be the same, and the number passed to Python will be
       using the familar notation.
    """
    dialog = VisibleInputDialog()
    flags = _get_common_input_flags()
    number, ok = dialog.getDouble(None, title, message,
                                  default_value, min_, max_, decimals,
                                  flags)
    if ok:
        return number


@invoke_in_thread()
def get_string(message: str = "Enter your response", title: str = "Title",
               default_response: str = "") -> Optional[str]:
    """Simple text input box.  Used to query the user and get a string back.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_response: default response appearing in the text box

       :return: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> from easygraphics.dialog import *
       >>> reply = get_string()

       .. image:: ../../docs/images/get_string.png

       >>> reply = get_string("new message", default_response="ready")

       .. image:: ../../docs/images/get_string2.png
    """
    dialog = VisibleInputDialog()
    flags = _get_common_input_flags()
    text, ok = dialog.getText(None, title, message, QtWidgets.QLineEdit.Normal,
                              default_response, flags)
    if ok:
        return text


@invoke_in_thread()
def get_password(message: str = "Enter your password", title: str = "Title") -> Optional[str]:
    """Simple password input box.  Used to query the user and get a string back.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title


       :return: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> from easygraphics.dialog import *
       >>> password = get_password()

       .. image:: ../../docs/images/get_password.png
    """
    dialog = VisibleInputDialog()
    flags = _get_common_input_flags()
    text, ok = dialog.getText(None, title, message, QtWidgets.QLineEdit.Password,
                              '', flags)
    if ok:
        return text


@invoke_in_thread()
def get_choice(message: str = "Select one item", title: str = "Title", choices: List[str] = None) -> Optional[str]:
    """Simple _dialog to ask a user to select an item within a drop-down list

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param choices: iterable (list or tuple) containing the names of
                       the items that can be selected.

       :returns: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> from easygraphics.dialog import *
       >>> choices = ["CPython", "Pypy", "Jython", "IronPython"]
       >>> reply = get_choice("What is the best Python implementation", choices=choices)

       .. image:: ../../docs/images/get_choice.png
    """
    if choices is None:
        choices = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    dialog = VisibleInputDialog()
    flags = _get_common_input_flags()
    choice, ok = dialog.getItem(None, title, message, choices, 0, False, flags)
    if ok:
        return choice


@invoke_in_thread()
def get_username_password(title: str = "Title", labels: List[str] = None) -> IndexedOrderedDict:
    """
    User name and password input box.

    :param title: Window title
    :param labels: an iterable containing the labels for "user name"
                  and "password"; if the value not specified, the
                  default values will be used.

    :return: An ordered dict containing the fields item as keys, and
            the input from the user (empty string by default) as value

    Note: this function is a special case of ``get_many_strings`` where
    the required masks are provided automatically..

    >>> from easygraphics.dialog import *
    >>> reply = easy.get_username_password()
    >>> reply
    OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

    .. image:: ../../docs/images/get_username_password.png
    """
    if labels is None:
        labels = ["User name", "Password"]
    if len(labels) != 2:
        _title = "Error found"
        message = "labels should have 2 elements; {} were found".format(len(labels))
        get_abort(title=_title, message=message)
    masks = [False, True]
    return get_many_strings(title=title, labels=labels, masks=masks)


@invoke_in_thread()
def get_new_password(title: str = "Title", labels: List[str] = None) -> IndexedOrderedDict:
    """
    Change password input box.

    :param title: Window title
    :param labels: an iterable containing the labels for "Old password"
                  and "New password" and "Confirm new password". All
                  three labels must be different strings as they are used
                  as keys in a dict - however, they could differ only by
                  a space.

    :return: An ordered dict containing the fields item as keys, and
            the input from the user as values.

    Note: this function is a special case of ``get_many_strings`` where
    the required masks are provided automatically..

    >>> from easygraphics.dialog import *
    >>> reply = easy.get_new_password()

    .. image:: ../../docs/images/get_new_password.png
    """

    if not labels:  # empty list acceptable for test
        labels = ["Old password:", "New password:", "Confirm new password:"]
    if len(labels) != 3:
        _title = "Error found"
        message = "labels should have 3 elements; {} were found".format(len(labels))
        get_abort(title=_title, message=message)
    masks = [True, True, True]

    dialog = multifields.MultipleFieldsDialog(labels=labels, masks=masks, title=title)
    _send_to_front(dialog)
    dialog.exec_()
    return dialog.enters


@invoke_in_thread()
def get_many_strings(title: str = "Title", labels: List[str] = None, masks: List[bool] = None) -> IndexedOrderedDict:
    """
    Multiple strings input

    :param title: Window title
    :param labels: an iterable containing the labels for to use for the entries
    :param masks: optional parameter.


    :return: An ordered dict containing the labels as keys, and
            the input from the user (empty string by default) as value

    The parameter ``masks`` if set must be an iterable of the same
    length as ``choices`` and contain either True or False as entries
    indicating if the entry of the text is masked or not.  For example,
    one could ask for a username and password using get_many_strings
    as follows [note that get_username_password exists and automatically
    takes care of specifying the masks and is a better choice for this
    use case.]

    >>> from easygraphics.dialog import *
    >>> labels = ["User name", 'Password']
    >>> masks = [False, True]
    >>> reply = get_many_strings(labels=labels, masks=masks)
    >>> reply
    OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

    .. image:: ../../docs/images/get_many_strings.png
    """

    dialog = multifields.MultipleFieldsDialog(labels=labels, masks=masks,
                                              title=title)
    _send_to_front(dialog)
    dialog.exec_()

    return dialog.enters


@invoke_in_thread()
def get_list_of_choices(title: str = "Title", choices: List[str] = None) -> IndexedOrderedDict:
    """
    Show a list of possible choices to be selected.

    :param title: Window title
    :param choices: iterable (list, tuple, ...) containing the choices as
                   strings

    :returns: a list of selected items, otherwise an empty list.

    >>> from easygraphics.dialog import *
    >>> choices = get_list_of_choices()

    .. image:: ../../docs/images/get_list_of_choices.png
    """
    dialog = multichoice.MultipleChoicesDialog(title=title, choices=choices)
    _send_to_front(dialog)
    dialog.exec_()
    return dialog.selection


# ========== Files & directory dialogs

@invoke_in_thread()
def get_directory_name(title: str = "Get directory") -> str:
    """
    Gets the name (full path) of an existing directory

    :param title: Window title
    :return: the name of a directory or an empty string if cancelled.

    >>> from easygraphics.dialog import *
    >>> get_directory_name()

    .. image:: ../../docs/images/get_directory_name.png

    By default, this _dialog initially displays the content of the current
    working directory.
    """
    options = QtWidgets.QFileDialog.Options()
    # Without the following option (i.e. using native dialogs),
    # calling this function twice in a row made Python crash.
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    options |= QtWidgets.QFileDialog.DontResolveSymlinks
    options |= QtWidgets.QFileDialog.ShowDirsOnly
    directory = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                           title, os.getcwd(), options)
    return directory


@invoke_in_thread()
def get_file_names(title: str = "Get existing file names") -> str:
    """
    Gets the names (full path) of existing files

    :param title: Window title
    :return: the list of names (paths) of files selected.
           (It can be an empty list.)

    >>> from easygraphics.dialog import *
    >>> easy.get_file_names()

    .. image:: ../../docs/images/get_file_names.png

    By default, this _dialog initially displays the content of the current
    working directory.
    """
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    files = QtWidgets.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                                   "All Files (*.*)", options)
    return files


@invoke_in_thread()
def get_save_file_name(title: str = "File name to save") -> str:
    """
    Gets the name (full path) of of a file to be saved.

    :param title: Window title
    :return: the name (path) of file selected

    The user is warned if the file already exists and can choose to
    cancel.  However, this _dialog actually does NOT save any file: it
    only return a string containing the full path of the chosen file.

    >>> from easygraphics.dialog import *
    >>> easy.get_save_file_name()

    .. image:: ../../docs/images/get_save_file_name.png

    By default, this _dialog initially displays the content of the current
    working directory.
    """
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog  # see get_directory_name
    file_name = QtWidgets.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                                      "All Files (*.*)", options)
    return file_name


@invoke_in_thread()
def show_file(file_name: str = None, title: str = "Title", file_type: str = "text"):
    """
    Displays a file in a window.  While it looks as though the file
    can be edited, the only changes that happened are in the window
    and nothing can be saved.

    :param title: the window title
    :param file_name: the file name, (path) relative to the calling program
    :param file_type: possible values: ``text``, ``code``, ``html``, ``python``.

    By default, file_type is assumed to be ``text``; if set to ``code``,
    the content is displayed with a monospace font and, if
    set to ``python``, some code highlighting is done.
    If the file_type is ``html``, it is processed assuming it follows
    html syntax.

    **Note**: a better Python code hightlighter would be most welcome!

    >>> from easygraphics.dialog import *
    >>> easy.show_file()

    .. image:: ../../docs/images/show_file.png
    """
    editor = show_text_window.TextWindow(file_name=file_name,
                                         title=title,
                                         text_type=file_type)
    editor.show()


@invoke_in_thread()
def show_text(title: str = "Title", text: str = ""):
    """
    Displays some text in a window.

    :param title: the window title
    :param text: a string to display in the window.

    >>> from easygraphics.dialog import *
    >>> easy.show_code()

    .. image:: ../../docs/images/show_text.png
    """
    editor = show_text_window.TextWindow(title=title, text_type='text', text=text)
    editor.resize(720, 450)
    editor.show()


@invoke_in_thread()
def show_code(title: str = "Title", code: str = ""):
    """
    Displays some text in a window, in a monospace font.

    :param title: the window title
    :param code: a string to display in the window.

    >>> from easygraphics.dialog import *
    >>> show_code()

    .. image:: ../../docs/images/show_code.png
    """
    editor = show_text_window.TextWindow(title=title, text_type='code', text=code)
    editor.resize(720, 450)
    editor.show()


@invoke_in_thread()
def show_html(title: str = "Title", text: str = ""):
    """
    Displays some html text in a window.

    :param title: the window title
    :param text: a string to display in the window.

    >>> from easygraphics.dialog import *
    >>> show_html()

    .. image:: ../../docs/images/show_html.png
    """
    editor = show_text_window.TextWindow(title=title, text_type='html', text=text)
    editor.resize(720, 450)
    editor.show()


@invoke_in_thread()
def get_abort(message: str = "Major problem - or at least we think there is one...",
              title: str = "Major problem encountered!"):
    """
    Displays a message about a problem.
    If the user clicks on "abort", sys.exit() is called and the
    program ends.  If the user clicks on "ignore", the program
    resumes its execution.

    :param title: the window title
    :param message: the message to display

    >>> from easygraphics.dialog import *
    >>> get_abort()

    .. image:: ../../docs/images/get_abort.png
    """

    reply = QtWidgets.QMessageBox.critical(None, title, message,
                                           QtWidgets.QMessageBox.Abort | QtWidgets.QMessageBox.Ignore)
    if reply == QtWidgets.QMessageBox.Abort:
        try:
            os._exit(0)
        except:
            sys.exit()
    else:
        pass


def handle_exception(title: str = "Exception raised!"):
    """
    Displays a traceback in a window if an exception is raised.
    If the user clicks on "abort", sys.exit() is called and the
    program ends.  If the user clicks on "ignore", the program
    resumes its execution.

    :param title: the window title

    .. image:: ../../docs/images/handle_exception.png
    """
    try:
        message = "\n".join(traceback.format_exception(sys.exc_info()[0],
                                                       sys.exc_info()[1], sys.exc_info()[2]))
    except AttributeError:
        return "No exception was raised"

    get_abort(title=title, message=message)


@invoke_in_thread()
def find_help():
    """
    Opens a web browser, pointing at the documention about EasyGUI_Qt
    available on the web.
    """
    webbrowser.open('http://easygui-qt.readthedocs.org/en/latest/api.html')


def set_dialog_font_size(size: int):
    """
    set font size of the dialogs
    :param size: font size

    >>> from easygraphics.dialog import *
    >>> set_dialog_font_size(18)
    >>> show_message("font setted!")
    >>> close_graph()
    """
    set_app_font(size)