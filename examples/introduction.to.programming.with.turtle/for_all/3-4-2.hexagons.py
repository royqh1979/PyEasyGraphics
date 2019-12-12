from easygraphics.turtle import *

def main():
    create_world(800, 600)
    
    for i in range(6):
        for j in range(6):
            fd(100)
            rt(60)
        rt(60)
    
    pause()
    close_world()

easy_run(main)