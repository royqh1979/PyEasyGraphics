"""
Message Dialogs
most code from EasyGUI_Qt(https://github.com/aroberge/easygui_qt/)
"""
import os
import sys
import traceback
import webbrowser
from collections import OrderedDict

if sys.version_info < (3,):
    raise RuntimeError("We don't support Python < 3")

from PyQt5 import QtGui, QtCore, QtWidgets

from . import calendar_widget
from . import multichoice
from . import multifields
from . import show_text_window
from ._invoke_in_app_thread import *


# ========== Message Boxes ====================#
@invoid_in_thread()
def show_message(message="Message",
                 title="Title"):
    """Simple message box.

       :param message: message string
       :param title: window title

       >>> import easygui_qt as easy
       >>> easy.show_message()

       .. image:: ../docs/images/show_message.png
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


@invoid_in_thread()
def get_yes_or_no(message="Answer this question", title="Title"):
    """Simple yes or no question.

       :param question: Question (string) asked
       :param title: Window title (string)

       :return: ``True`` for "Yes", ``False`` for "No",
               and ``None`` for "Cancel".

       >>> import easygui_qt as easy
       >>> choice = easy.get_yes_or_no()

       .. image:: ../docs/images/yes_no_question.png
    """
    flags = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    flags |= QtWidgets.QMessageBox.Cancel

    dialog = QtWidgets.QMessageBox()
    _send_to_front(dialog)
    reply = dialog.question(None, title, message, flags)
    if reply == QtWidgets.QMessageBox.Cancel:
        return None
    return reply == QtWidgets.QMessageBox.Yes


@invoid_in_thread()
def get_continue_or_cancel(message="Processed will be cancelled!",
                           title="Title",
                           continue_button_text="Continue",
                           cancel_button_text="Cancel"):
    """Continue or cancel question, shown as a warning (i.e. more urgent than
       simple message)

       :param question: Question (string) asked
       :param title: Window title (string)
       :param continue_button_text: text to display on button
       :param cancel_button_text: text to display on button

       :return: True for "Continue", False for "Cancel"

       >>> import easygui_qt as easy
       >>> choice = easy.get_continue_or_cancel()

       .. image:: ../docs/images/get_continue_or_cancel.png
    """
    dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, title, message,
                                   QtWidgets.QMessageBox.NoButton)
    dialog.addButton(continue_button_text, QtWidgets.QMessageBox.AcceptRole)
    dialog.addButton(cancel_button_text, QtWidgets.QMessageBox.RejectRole)
    _send_to_front(dialog)
    reply = dialog.exec()
    return reply == QtWidgets.QMessageBox.AcceptRole


# ============= Color dialogs =================
@invoid_in_thread()
def get_color_hex():
    """Using a color _dialog, returns a color in hexadecimal notation
       i.e. a string '#RRGGBB' or "None" if color _dialog is dismissed.

       >>> import easygui_qt as easy
       >>> color = easy.get_color_hex()

       .. image:: ../docs/images/select_color.png
       """
    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.white, None)
    if color.isValid():
        return color.name()


@invoid_in_thread()
def get_color_rgb(app=None):
    """Using a color _dialog, returns a color in rgb notation
       i.e. a tuple (r, g, b)  or "None" if color _dialog is dismissed.

       >>> import easygui_qt as easy
       >>> easy.set_language('fr')
       >>> color = easy.get_color_rgb()

       .. image:: ../docs/images/select_color_fr.png
       """
    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.white, None)
    if color.isValid():
        return (color.red(), color.green(), color.blue())


# ================ Date ===================
@invoid_in_thread()
def get_date(title="Select Date"):
    """Calendar widget

       :param title: window title
       :return: the selected date as a ``datetime.date`` instance

       >>> import easygui_qt as easy
       >>> date = easy.get_date()

       .. image:: ../docs/images/get_date.png
    """
    cal = calendar_widget.CalendarWidget(title=title)
    date = cal.date.toPyDate()
    return date


# =========== InputDialogs ========================
def get_common_input_flags():
    '''avoiding copying same flags in all functions'''
    flags = QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
    flags |= QtCore.Qt.WindowStaysOnTopHint
    return flags


class VisibleInputDialog(QtWidgets.QInputDialog):
    '''A simple InputDialog class that attempts to make itself automatically
       on all platforms
    '''

    def __init__(self):
        super(VisibleInputDialog, self).__init__()


@invoid_in_thread()
def get_int(message="Choose a number", title="Title",
            default_value=1, min_=0, max_=100, step=1):
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

       >>> import easygui_qt as easy
       >>> number = easy.get_int()

       .. image:: ../docs/images/get_int.png


       If ``default_value`` is larger than ``max_``, it is set to ``max_``;
       if it is smaller than ``min_``, it is set to ``min_``.

       >>> number = easy.get_integer("Enter a number", default_value=125)

       .. image:: ../docs/images/get_int2.png

    """
    # converting values to int for launcher demo set_font_size which
    # first queries the user for a value; the initial values are passed
    # as strings by the subprocess module and need to be converted here

    default_value = int(default_value)
    min_ = int(min_)
    max_ = int(max_)

    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    number, ok = dialog.getInt(None, title, message,
                               default_value, min_, max_, step,
                               flags)
    dialog.destroy()
    if ok:
        return number


get_integer = get_int


@invoid_in_thread()
def get_float(message="Choose a number", title="Title", default_value=0.0,
              min_=-10000, max_=10000, decimals=3):
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

       >>> import easygui_qt as easy
       >>> number = easy.get_float()

       .. image:: ../docs/images/get_float.png

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
    flags = get_common_input_flags()
    number, ok = dialog.getDouble(None, title, message,
                                  default_value, min_, max_, decimals,
                                  flags)
    if ok:
        return number


@invoid_in_thread()
def get_string(message="Enter your response", title="Title",
               default_response=""):
    """Simple text input box.  Used to query the user and get a string back.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param default_response: default response appearing in the text box

       :return: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> reply = easy.get_string()

       .. image:: ../docs/images/get_string.png

       >>> reply = easy.get_string("new message", default_response="ready")

       .. image:: ../docs/images/get_string2.png
    """
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    text, ok = dialog.getText(None, title, message, QtWidgets.QLineEdit.Normal,
                              default_response, flags)
    if ok:
        return text


@invoid_in_thread()
def get_password(message="Enter your password", title="Title"):
    """Simple password input box.  Used to query the user and get a string back.

       :param message: Message displayed to the user, inviting a response
       :param title: Window title


       :return: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> password = easy.get_password()

       .. image:: ../docs/images/get_password.png
    """
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    text, ok = dialog.getText(None, title, message, QtWidgets.QLineEdit.Password,
                              '', flags)
    if ok:
        return text


@invoid_in_thread()
def get_choice(message="Select one item", title="Title", choices=None):
    """Simple _dialog to ask a user to select an item within a drop-down list

       :param message: Message displayed to the user, inviting a response
       :param title: Window title
       :param choices: iterable (list or tuple) containing the names of
                       the items that can be selected.

       :returns: a string, or ``None`` if "cancel" is clicked or window
                is closed.

       >>> import easygui_qt as easy
       >>> choices = ["CPython", "Pypy", "Jython", "IronPython"]
       >>> reply = easy.get_choice("What is the best Python implementation",
       ...                         choices=choices)

       .. image:: ../docs/images/get_choice.png
    """
    if choices is None:
        choices = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    dialog = VisibleInputDialog()
    flags = get_common_input_flags()
    choice, ok = dialog.getItem(None, title, message, choices, 0, False, flags)
    if ok:
        return choice


@invoid_in_thread()
def get_username_password(title="Title", labels=None):
    """User name and password input box.

       :param title: Window title
       :param labels: an iterable containing the labels for "user name"
                      and "password"; if the value not specified, the
                      default values will be used.

       :return: An ordered dict containing the fields item as keys, and
                the input from the user (empty string by default) as value

       Note: this function is a special case of ``get_many_strings`` where
       the required masks are provided automatically..

       >>> import easygui_qt as easy
       >>> reply = easy.get_username_password()
       >>> reply
       OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

       .. image:: ../docs/images/get_username_password.png
    """
    if labels is None:
        labels = ["User name", "Password"]
    if len(labels) != 2:
        _title = "Error found"
        message = "labels should have 2 elements; {} were found".format(len(labels))
        get_abort(title=_title, message=message)
    masks = [False, True]
    return get_many_strings(title=title, labels=labels, masks=masks)


@invoid_in_thread()
def get_new_password(title="Title", labels=None):
    """Change password input box.

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

       >>> import easygui_qt as easy
       >>> reply = easy.get_new_password()

       .. image:: ../docs/images/get_new_password.png
    """

    if not labels:  # empty list acceptable for test
        labels = ["Old password:", "New password:", "Confirm new password:"]
    if len(labels) != 3:
        _title = "Error found"
        message = "labels should have 3 elements; {} were found".format(len(labels))
        get_abort(title=_title, message=message)
    masks = [True, True, True]

    class Parent:
        pass

    parent = Parent()
    dialog = multifields.MultipleFieldsDialog(labels=labels, masks=masks,
                                              parent=parent, title=title)
    _send_to_front(dialog)
    dialog.exec_()
    return parent.o_dict


@invoid_in_thread()
def get_many_strings(title="Title", labels=None, masks=None):
    """Multiple strings input

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

       >>> import easygui_qt as easy
       >>> labels = ["User name", 'Password']
       >>> masks = [False, True]
       >>> reply = easy.get_many_strings(labels=labels, masks=masks)
       >>> reply
       OrderedDict([('User name', 'aroberge'), ('Password', 'not a good password')])

       .. image:: ../docs/images/get_many_strings.png
    """

    class Parent:
        pass

    parent = Parent()
    dialog = multifields.MultipleFieldsDialog(labels=labels, masks=masks,
                                              parent=parent, title=title)
    _send_to_front(dialog)
    dialog.exec_()

    class IndexedOrderedDict(OrderedDict):
        def __getitem__(self, key):
            if isinstance(key, int):
                i = 0
                for v in self.values():
                    if i == key:
                        return v
                    i = i + 1
            return super().__getitem__(key)

    return IndexedOrderedDict(parent.o_dict)


@invoid_in_thread()
def get_list_of_choices(title="Title", choices=None):
    """Show a list of possible choices to be selected.

       :param title: Window title
       :param choices: iterable (list, tuple, ...) containing the choices as
                       strings

       :returns: a list of selected items, otherwise an empty list.

       >>> import easygui_qt as easy
       >>> choices = easy.get_list_of_choices()

       .. image:: ../docs/images/get_list_of_choices.png
    """
    dialog = multichoice.MultipleChoicesDialog(title=title, choices=choices)
    _send_to_front(dialog)
    dialog.exec_()
    return dialog.selection


# ========== Files & directory dialogs

@invoid_in_thread()
def get_directory_name(title="Get directory"):
    '''Gets the name (full path) of an existing directory

       :param title: Window title
       :return: the name of a directory or an empty string if cancelled.

       >>> import easygui_qt as easy
       >>> easy.get_directory_name()

       .. image:: ../docs/images/get_directory_name.png

       By default, this _dialog initially displays the content of the current
       working directory.
    '''
    options = QtWidgets.QFileDialog.Options()
    # Without the following option (i.e. using native dialogs),
    # calling this function twice in a row made Python crash.
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    options |= QtWidgets.QFileDialog.DontResolveSymlinks
    options |= QtWidgets.QFileDialog.ShowDirsOnly
    directory = QtWidgets.QFileDialog.getExistingDirectory(None,
                                                           title, os.getcwd(), options)
    return directory


@invoid_in_thread()
def get_file_names(title="Get existing file names"):
    '''Gets the names (full path) of existing files

       :param title: Window title
       :return: the list of names (paths) of files selected.
               (It can be an empty list.)

       >>> import easygui_qt as easy
       >>> easy.get_file_names()

       .. image:: ../docs/images/get_file_names.png

       By default, this _dialog initially displays the content of the current
       working directory.
    '''
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    files = QtWidgets.QFileDialog.getOpenFileNames(None, title, os.getcwd(),
                                                   "All Files (*.*)", options)
    return files


@invoid_in_thread()
def get_save_file_name(title="File name to save"):
    '''Gets the name (full path) of of a file to be saved.

       :param title: Window title
       :return: the name (path) of file selected

       The user is warned if the file already exists and can choose to
       cancel.  However, this _dialog actually does NOT save any file: it
       only return a string containing the full path of the chosen file.

       >>> import easygui_qt as easy
       >>> easy.get_save_file_name()

       .. image:: ../docs/images/get_save_file_name.png

       By default, this _dialog initially displays the content of the current
       working directory.
    '''
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog  # see get_directory_name
    file_name = QtWidgets.QFileDialog.getSaveFileName(None, title, os.getcwd(),
                                                      "All Files (*.*)", options)
    return file_name


@invoid_in_thread()
def show_file(file_name=None, title="Title", file_type="text"):
    '''Displays a file in a window.  While it looks as though the file
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

       >>> import easygui_qt as easy
       >>> easy.show_file()

       .. image:: ../docs/images/show_file.png
    '''
    editor = show_text_window.TextWindow(file_name=file_name,
                                         title=title,
                                         text_type=file_type)
    editor.show()


@invoid_in_thread()
def show_text(title="Title", text=""):
    '''Displays some text in a window.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_code()

       .. image:: ../docs/images/show_text.png
    '''
    editor = show_text_window.TextWindow(title=title, text_type='text', text=text)
    editor.resize(720, 450)
    editor.show()


@invoid_in_thread()
def show_code(title="Title", text=""):
    '''Displays some text in a window, in a monospace font.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_code()

       .. image:: ../docs/images/show_code.png
    '''
    editor = show_text_window.TextWindow(title=title, text_type='code', text=text)
    editor.resize(720, 450)
    editor.show()


@invoid_in_thread()
def show_html(title="Title", text=""):
    '''Displays some html text in a window.

       :param title: the window title
       :param code: a string to display in the window.

       >>> import easygui_qt as easy
       >>> easy.show_html()

       .. image:: ../docs/images/show_html.png
    '''
    editor = show_text_window.TextWindow(title=title, text_type='html', text=text)
    editor.resize(720, 450)
    editor.show()


@invoid_in_thread()
def get_abort(message="Major problem - or at least we think there is one...",
              title="Major problem encountered!"):
    '''Displays a message about a problem.
       If the user clicks on "abort", sys.exit() is called and the
       program ends.  If the user clicks on "ignore", the program
       resumes its execution.

       :param title: the window title
       :param message: the message to display

       >>> import easygui_qt as easy
       >>> easy.get_abort()

       .. image:: ../docs/images/get_abort.png
    '''

    reply = QtWidgets.QMessageBox.critical(None, title, message,
                                           QtWidgets.QMessageBox.Abort | QtWidgets.QMessageBox.Ignore)
    if reply == QtWidgets.QMessageBox.Abort:
        try:
            os._exit(0)
        except:
            sys.exit()
    else:
        pass


def handle_exception(title="Exception raised!"):
    '''Displays a traceback in a window if an exception is raised.
       If the user clicks on "abort", sys.exit() is called and the
       program ends.  If the user clicks on "ignore", the program
       resumes its execution.

       :param title: the window title

       .. image:: ../docs/images/handle_exception.png
    '''
    try:
        message = "\n".join(traceback.format_exception(sys.exc_info()[0],
                                                       sys.exc_info()[1], sys.exc_info()[2]))
    except AttributeError:
        return "No exception was raised"

    get_abort(title=title, message=message)


@invoid_in_thread()
def find_help():
    '''Opens a web browser, pointing at the documention about EasyGUI_Qt
       available on the web.
    '''
    webbrowser.open('http://easygui-qt.readthedocs.org/en/latest/api.html')


if __name__ == '__main__':
    try:
        from demos import guessing_game

        guessing_game.guessing_game()
    except ImportError:
        print("Could not find demo.")
