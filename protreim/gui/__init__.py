
import PySimpleGUI as sg

from protreim.gui.windows.root import RootWindow
sg.theme('DarkGreen')

def main() -> None:
    win = RootWindow()
    win.protreim.load_config(win.config_path)
    win.show()


if __name__ == '__main__':
    main()