# Main application code

import tkinter as tk

from widgets import FiguresList, Interface


class MainWindow(tk.Tk):
    """Class for main application window"""

    def __init__(self):
        super().__init__()
        self.title("Application")
        self.geometry("+10+10")
        self.resizable(False, False)
        self.figures_list = FiguresList(self)
        self.interface = Interface(self,
                                   self.figures_list.get_selected_num,
                                   self.figures_list.remove_selection)

        self.bind("<Delete>", lambda x: self.interface.drawing_field.del_selected())

    def run(self):
        self.figures_list.draw()
        self.interface.draw()
        self.mainloop()  # Start application


window = MainWindow()  # Init main window
window.run()  # Run application
