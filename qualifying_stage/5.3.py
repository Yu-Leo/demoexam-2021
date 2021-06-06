import tkinter as tk
import tkinter.messagebox as mb
from math import pi, sin, cos


class Figure:
    color = "orange"  # Figure's fill-color

    def __init__(self, field, center_coords, angles):
        self.__field = field
        self.__center = center_coords
        self.__angles = angles  # Number of polygon angles
        self.__big_radius = 40  # Radius of described near the polygon circle
        self.__vertexes = self.__get_vertexes()  # List of vertexes coordinates
        self.__object = field.create_polygon(*self.__vertexes, fill=Figure.color)  # Polygon object
        self.__field.tag_bind(self.__object, '<Button-1>', self.transform)

    def __get_vertexes(self):
        """Return list of vertexes coordinates (x, y)"""
        vertexes = []
        alpha = (2 * pi) / self.__angles  # Vertex angle
        x0, y0 = self.__center  # Zero-coordinates
        r = self.__big_radius
        for i in range(self.__angles):
            vertexes.append((x0 + r * cos(- pi / 2 + alpha * i),
                             y0 + r * sin(- pi / 2 + alpha * i)))
        return vertexes

    def delete(self):
        """Delete figures from the field"""
        self.__field.delete(self.__object)

    def transform(self, event):
        """Redraw figure"""
        global figure_click
        figure_click = True
        self.delete()
        self.__add_vertex()

    def __add_vertex(self):
        """Add angle and draw new figure"""
        self.__angles += 1
        self.__vertexes = self.__get_vertexes()  # List of vertexes coordinates
        self.__object = self.__field.create_polygon(*self.__vertexes, fill=Figure.color)  # Polygon object
        self.__field.tag_bind(self.__object, '<Button-1>', self.transform)


def del_all_figures(field, figures):
    if len(figures_list) == 0:  # If there are no figures on the field
        mb.showerror(title="Error", message="There are no figures on the field")
    else:
        field.delete(tk.ALL)  # Delete all figures from the field
        figures.clear()  # Delete all figures from the list


def check_click(event, field, figures):
    global figure_click
    if not figure_click:
        figures.append(Figure(field, (event.x, event.y), angles=3))
    figure_click = False


root = tk.Tk()  # Main window
root.title("Task 5.3")
root.resizable(False, False)

drawing_field = tk.Canvas(root, bg="white", width=400, height=400)
drawing_field.pack()

figures_list = []  # List of figures, which drawn on the field
figure_click = False  # Was some figure clicked?

drawing_field.bind('<Button-1>', lambda event: check_click(event, drawing_field, figures_list))
root.bind('<Delete>', lambda event: del_all_figures(drawing_field, figures_list))

root.mainloop()
