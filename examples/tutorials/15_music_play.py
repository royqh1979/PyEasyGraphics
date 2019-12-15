from easygraphics import *
from easygraphics.music import *
from easygraphics.dialog import *

# For legal reasons please prepare a music file by yourself
def main():
    load_music("test.mp3")
    play_music()
    show_message("ok!")
    close_music()

easy_run(main)