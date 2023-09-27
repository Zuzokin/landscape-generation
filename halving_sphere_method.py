from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class SphereWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Сферический ландшафт")

        self.label_dots = ttk.Label(self, text="Плотность точек")
        self.label_dots.grid(column=5, row=0, pady=(3, 3))

        self.text_box_dots = ttk.Entry(self)
        self.text_box_dots.grid(column=5, row=1, pady=(3, 3))
        self.text_box_dots.insert(0, 100)

        self.label_iterations = ttk.Label(self, text="Количество итераций")
        self.label_iterations.grid(column=5, row=2, pady=(3, 3))

        self.text_box_iterations = ttk.Entry(self)
        self.text_box_iterations.grid(column=5, row=3, pady=(3, 3))
        self.text_box_iterations.insert(0, 100)

        self.label_hemispherical_magnification_factor = ttk.Label(
            self, text="Коэф. увеличения"
        )
        self.label_hemispherical_magnification_factor.grid(column=5, row=4, pady=(3, 3))

        self.text_box_hemispherical_magnification_factor = ttk.Entry(self)
        self.text_box_hemispherical_magnification_factor.grid(
            column=5, row=5, pady=(3, 3)
        )
        self.text_box_hemispherical_magnification_factor.insert(0, 1.01)

        self.label_hemispherical_reduction_factor = ttk.Label(
            self, text="Коэф. уменьшения"
        )
        self.label_hemispherical_reduction_factor.grid(column=5, row=6, pady=(3, 3))

        self.text_box_hemispherical_reduction_factor = ttk.Entry(self)
        self.text_box_hemispherical_reduction_factor.grid(column=5, row=7, pady=(3, 3))
        self.text_box_hemispherical_reduction_factor.insert(0, 0.99)

        self.button_start = ttk.Button(self, text="Сгенерировать")
        self.button_start["command"] = self.generate_land
        self.button_start.grid(column=5, row=8, padx=(30, 30), pady=(10, 10))

        self.button_exit = ttk.Button(self, text="Закрыть окно")
        self.button_exit["command"] = self.window_destroy
        self.button_exit.grid(column=5, row=9, padx=(30, 30), pady=(10, 10))

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(projection="3d")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(
            column=0, row=0, columnspan=5, rowspan=20, padx=(30, 30), pady=(10, 10)
        )

    def window_destroy(self):
        self.destroy()

    def generate_terrain(self, iterations, magnification_factor, reduction_factor):
        # Создание сферы
        u = np.linspace(0, 2 * np.pi, int(self.text_box_dots.get()))
        v = np.linspace(0, np.pi, int(self.text_box_dots.get()))
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        for _ in range(iterations):
            # Выбор случайной плоскости для разделения полусферы
            plane = np.random.normal(size=4)
            plane /= np.linalg.norm(plane)

            plane[3] = 0

            first_couple, second_couple = magnification_factor, reduction_factor

            # Разделение полусферы на две части
            mask = (x * plane[0] + y * plane[1] + z * plane[2] + plane[3]) > 0
            x1, y1, z1 = x.copy(), y.copy(), z.copy()
            x2, y2, z2 = x.copy(), y.copy(), z.copy()
            x1[mask], y1[mask], z1[mask] = (
                first_couple * x[mask],
                first_couple * y[mask],
                first_couple * z[mask],
            )
            x2[~mask], y2[~mask], z2[~mask] = (
                second_couple * x[~mask],
                second_couple * y[~mask],
                second_couple * z[~mask],
            )

            # Обновление сферы
            x = x1 + x2
            y = y1 + y2
            z = z1 + z2

        return x, y, z

    def generate_land(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(projection="3d")

        iterations = int(self.text_box_iterations.get())
        magnification_factor = float(
            self.text_box_hemispherical_magnification_factor.get()
        )
        reduction_factor = float(self.text_box_hemispherical_reduction_factor.get())

        X, Y, Z = self.generate_terrain(
            iterations, magnification_factor, reduction_factor
        )
        surf = self.ax.scatter(X, Y, Z, s=0.1)
        self.canvas.draw()
