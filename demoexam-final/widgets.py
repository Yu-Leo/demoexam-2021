# File with code for widgets, which used in interface

import tkinter as tk
from math import pi, sin, cos
import tkinter.messagebox as mb

from constants import *


class Figure:
    """Class of figure"""

    color = "orange"  # Main figure color
    border_color = "black"  # Color of border (indicate, that figure is selected)
    size = 80  # Default size

    def __init__(self, field, figure_type, center, size=None, move_mode=False, selected=False):
        """
        Init figure object
        :param field: field for drawing figure
        :param center: coordinates of center of figure
        :param size: size of figure
        :param move_mode: is figure moving
        :param selected: is figure is selected
        """
        self.__field = field
        self.__type = figure_type
        if figure_type == FIRST_FIGURE:
            self.__angles = FIRST_FIGURE_ANGLES
        elif figure_type == SECOND_FIGURE:
            self.__angles = SECOND_FIGURE_ANGLES
        elif figure_type == THIRD_FIGURE:
            self.__angles = THIRD_FIGURE_ANGLES
        else:
            raise ValueError("Incorrect figure type")

        self.__radius = Figure.size if size is None else size
        self.__center = center  # Coordinates of center (x, y)
        self.__vertexes = self.__generate_vertexes()
        self.__object = self.__field.create_polygon(*self.__vertexes, fill=Figure.color)

        self.__is_selected = selected
        if selected:
            self.select()
        self.move_mode = move_mode

    @property
    def center(self):
        return self.__center

    @property
    def type(self):
        return self.__type

    @property
    def radius(self):
        return self.__radius

    @property
    def fig_object(self):
        return self.__object

    def delete(self):
        """Delete figure object from field"""
        self.__field.delete(self.__object)

    def select(self):
        """Select this figure"""
        self.__is_selected = True
        self.__field.delete(self.__object)
        self.__object = self.__field.create_polygon(*self.__vertexes,
                                                    fill=Figure.color,
                                                    outline=Figure.border_color,
                                                    width=3)
        self.__field.tag_bind(self.__object, "<Button-1>", lambda x: self.__start_tracking())

    def hide_selection(self):
        """Hide selection"""
        self.__is_selected = False
        self.__field.delete(self.__object)
        self.__object = self.__field.create_polygon(*self.__vertexes,
                                                    fill=Figure.color)

    def finish_tracking(self):
        self.move_mode = False

    def __start_tracking(self):
        self.move_mode = not self.move_mode

    def __generate_vertexes(self):
        """
        :return: list of coordinates of figure vertexes
        """
        vertexes = []
        a = (2 * pi / self.__angles)
        x0, y0 = self.__center
        for i in range(self.__angles):
            vertexes.append((x0 + cos(-pi / 2 + a * i) * self.__radius,
                             y0 + sin(-pi / 2 + a * i) * self.__radius))
        return vertexes


class FigureListItem(tk.Canvas):
    """Class for figure item in left figures list"""

    def __init__(self, window, i, change_act_func):
        """
        :param window: window (or frame), on which item will drawing
        :param i: index of figure
        :param change_act_func: function, which need call to change selected figure
        """
        super().__init__(window,
                         width=FIGURE_ITEM_SIZE,
                         height=FIGURE_ITEM_SIZE,
                         bg="white")

        self.index = i
        self.change_act_func = change_act_func
        self.figure = Figure(self, i,
                             (FIGURE_ITEM_SIZE / 2, FIGURE_ITEM_SIZE / 2 + 5),
                             FIGURE_ITEM_SIZE / 2 - 10)

        self.bind("<Button-1>", lambda x: self.select())

    def select(self):
        """Select figure item in list"""
        self.change_act_func(self.index)
        self.create_rectangle(3, 3, FIGURE_ITEM_SIZE,
                              FIGURE_ITEM_SIZE,
                              width=2,
                              outline="black")

    def hide_selection(self):
        """Hide selection"""
        self.create_rectangle(3, 3, FIGURE_ITEM_SIZE,
                              FIGURE_ITEM_SIZE,
                              width=2,
                              outline="white")


class FiguresList(tk.Frame):
    """Class for list of figures"""

    def __init__(self, window):
        """Init object of figures list"""
        super().__init__(window)
        self.__figures = self.__generate_figures_list()  # Figures items list
        self.__selected_figure = NONE_FIGURE  # Number of selected figure

    def __change_selection(self, new_index):
        """
        Change type of selected figure
        :param new_index: index of new selected figure
        """
        self.__selected_figure = new_index
        # Hide all selections
        for figure in self.__figures:
            figure.hide_selection()

    def __generate_figures_list(self):
        """Generate list with figures items"""
        figures = [FigureListItem(self, FIRST_FIGURE, self.__change_selection),
                   FigureListItem(self, SECOND_FIGURE, self.__change_selection),
                   FigureListItem(self, THIRD_FIGURE, self.__change_selection)]
        return figures

    def draw(self):
        """Draw figures list on main window"""
        for figure in self.__figures:
            figure.pack(padx=10, pady=10)
        self.pack(side=tk.LEFT)

    def get_selected_num(self):
        """Get num of selected figure"""
        return self.__selected_figure

    def remove_selection(self):
        """Remove selection from all figures"""
        self.__selected_figure = NONE_FIGURE
        for figure in self.__figures:
            figure.hide_selection()


class Interface(tk.Frame):
    def __init__(self, window, get_selected_num, remove_selection):
        """
        :param window: window, on which interface will be drawing
        :param get_selected_num: function, which needs call to get num of selected figure
        :param remove_selection: function, which needs call to remove selection from all items in list
        """
        super().__init__(window)
        self.drawing_field = DrawingField(self,
                                          get_selected_num,
                                          remove_selection)
        self.buttons = Buttons(self,
                               self.drawing_field.del_selected)

    def draw(self):
        self.drawing_field.pack(padx=(10, 15), pady=10)
        self.buttons.draw()
        self.pack(side=tk.RIGHT)


class DrawingField(tk.Canvas):
    """Class of main drawing field"""

    @staticmethod
    def distance(point1, point2):
        """
        :param point1: coordinates of first point (x, y)
        :param point2: coordinates of second point (x, y)
        :return: distance between this points
        """
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    def __init__(self, window, get_selected_num, remove_selection):
        """

        :param window: window, on which field will drawing
        :param get_selected_num: function, which needs call to get num of selected figure
        :param remove_selection:
        """
        super().__init__(window,
                         width=DRAWING_FIELD_SIZE,
                         height=DRAWING_FIELD_SIZE,
                         bg="white")
        self.__figures_list = []  # List of figures, which place on field
        self.__selected_figure_index = None

        self.bind("<Button-1>", lambda x: self.__check_click(x, get_selected_num))
        self.bind("<Button-3>", lambda x: remove_selection())
        self.bind("<Motion>", self.__check_motion)
        self.bind("<ButtonRelease-1>", lambda x: self.__check_release())

    def __check_release(self):
        """Check button-1 release"""
        if self.__selected_figure_index is not None:
            self.__figures_list[self.__selected_figure_index].finish_tracking()

    def del_selected(self):
        """Delete selected figure if any figure is selected"""
        if self.__selected_figure_index is not None:
            figure_object = self.__figures_list[self.__selected_figure_index].fig_object
            self.delete(figure_object)
            self.__figures_list.pop(self.__selected_figure_index)
            self.__selected_figure_index = None
        else:
            mb.showerror(title="Error", message="There are no selected figure")

    def __check_motion(self, event):
        """Check mouse motion"""
        if self.__selected_figure_index is not None:
            index = self.__selected_figure_index
            fig = self.__figures_list[index]
            if fig.move_mode:
                self.__figures_list[index].delete()
                self.__figures_list[index] = Figure(self,
                                                    fig.type,
                                                    (event.x, event.y),
                                                    size=fig.size,
                                                    move_mode=True,
                                                    selected=True)

    def __check_click(self, event, get_selected_num):
        """Check click on button-1"""
        x, y = event.x, event.y
        sel_num = get_selected_num()
        if sel_num == NONE_FIGURE:  # If there are no selected figure
            self.__select_figure((x, y))
        else:  # Creating new figure
            if len(self.__figures_list) < MAX_NUMBER_OF_FIGURES_ON_FIELD:
                self.__figures_list.append(Figure(self, sel_num, (x, y)))
            else:
                msg_text = f"There are also {MAX_NUMBER_OF_FIGURES_ON_FIELD} figures on the field"
                mb.showerror(title="Error",
                             message=msg_text)

    def __select_figure(self, coordinates):
        """Select figure after click"""
        self.__hide_all_selections()
        index = self.__find_min_dist_figure_index(coordinates)
        if index is not None:
            self.__figures_list[index].select()
        self.__selected_figure_index = index

    def __hide_all_selections(self):

        for figure in self.__figures_list:
            figure.hide_selection()

    def __find_min_dist_figure_index(self, coordinates):
        """Find index of figure with min distance to click's coordinates"""
        min_d = None
        min_d_fig_id = None
        for i in range(len(self.__figures_list)):
            figure = self.__figures_list[i]
            d = DrawingField.distance(coordinates, figure.center)
            if (min_d is None or d < min_d) and d < figure.radius:
                min_d = d
                min_d_fig_id = i

        return min_d_fig_id


class Buttons(tk.Frame):
    """Class for menu with buttons"""

    def __init__(self, window, del_func):
        """
        :param window: window, on which buttons will be drawing
        :param del_func: function, which needs call to del selected figure
        """
        super().__init__(window)
        self.del_btn = tk.Button(self,
                                 width=BTN_WIDTH,
                                 height=BTN_HEIGHT,
                                 text="Delete",
                                 font=("Arial", 18),
                                 command=del_func)

        self.exit_btn = tk.Button(self,
                                  width=BTN_WIDTH,
                                  height=BTN_HEIGHT,
                                  text="Exit",
                                  font=("Arial", 18),
                                  bg="orange",
                                  command=lambda: exit())

    def draw(self):
        """Draw buttons"""
        self.del_btn.pack(side=tk.LEFT, padx=10)
        self.exit_btn.pack(side=tk.LEFT)
        self.pack(side=tk.RIGHT, padx=15, pady=15)
