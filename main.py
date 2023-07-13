import PySimpleGUI as sg
from gui import create_gui

sg.theme("DefaultNoMoreNagging")
sg.SetOptions(font=("Microsoft YaHei UI", 10))

if __name__ == "__main__":
    create_gui()