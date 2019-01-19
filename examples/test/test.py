from easygraphics.dialog import *
from easygraphics import *

set_dialog_font_size(20)
y = get_continue_or_cancel()
show_message(str(y))
