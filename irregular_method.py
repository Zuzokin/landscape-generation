from tkinter import ttk, Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import cv2


class IrregularWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Иррегулярная сетка")

        self.label_landscape_size = ttk.Label(self, text="Размер ландшафта (NxN)")
        self.label_landscape_size.grid(column=5, row=0, pady=(3, 3))

        self.text_box_landscape_size = ttk.Entry(self)
        self.text_box_landscape_size.grid(column=5, row=1, pady=(3, 3))
        self.text_box_landscape_size.insert(0, 100)

        self.label_points_quantity = ttk.Label(self, text="Количество вершин")
        self.label_points_quantity.grid(column=5, row=2, pady=(3, 3))

        self.text_box_points_quantity = ttk.Entry(self)
        self.text_box_points_quantity.grid(column=5, row=3, pady=(3, 3))
        self.text_box_points_quantity.insert(0, 100)

        self.label_blur_iterations = ttk.Label(self, text="Повторений сглаживания")
        self.label_blur_iterations.grid(column=5, row=4, pady=(3, 3))

        self.text_box_blur_iterations = ttk.Entry(self)
        self.text_box_blur_iterations.grid(column=5, row=5, pady=(3, 3))
        self.text_box_blur_iterations.insert(0, 5)

        self.label_kernel_size = ttk.Label(self, text="Размер ядра")
        self.label_kernel_size.grid(column=5, row=6, pady=(3, 3))

        self.text_box_kernel_size = ttk.Entry(self)
        self.text_box_kernel_size.grid(column=5, row=7, pady=(3, 3))
        self.text_box_kernel_size.insert(0, 3)

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

        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()

        self.toolbar.grid(column=0, row=21, padx=(30, 30), pady=(10, 10))
        self.canvas.get_tk_widget().grid(
            column=0, row=0, columnspan=5, rowspan=20, padx=(30, 30), pady=(10, 10)
        )

    def window_destroy(self):
        self.destroy()

    def apply_smoothing_filter(self, landscape, iterations, kernel_size):
        smoothed_landscape = landscape.copy()
        for _ in range(iterations):
            smoothed_landscape = cv2.blur(
                cv2.Mat(smoothed_landscape), (kernel_size, kernel_size)
            )
        return smoothed_landscape

    def add_random_points(self, size, points_quantity):
        landscape = np.random.randint(
            0,
            10,
            (size, size),
        )
        for _ in range(points_quantity):
            i = np.random.randint(1, landscape.shape[0] - 1)
            j = np.random.randint(1, landscape.shape[1] - 1)
            landscape[i][j] = np.random.randint(0, 1000)
        return landscape

    def generate_land(self):
        self.fig.clear()
        self.ax = self.fig.add_subplot(projection="3d")

        n = int(self.text_box_landscape_size.get())  # Размер ландшафта
        # Количество повторений сглаживающего фильтра
        num_iterations = int(self.text_box_blur_iterations.get())
        kernel_size = int(self.text_box_kernel_size.get())
        points_quantity = int(self.text_box_points_quantity.get())

        landscape = self.add_random_points(n, points_quantity)

        landscape = self.apply_smoothing_filter(landscape, num_iterations, kernel_size)

        print(landscape)
        x = np.arange(n)
        y = np.arange(n)
        X, Y = np.meshgrid(x, y)
        self.show_landscape(X, Y, landscape)

    def show_landscape(self, X, Y, Z):
        surf = self.ax.plot_surface(X, Y, Z, cmap="terrain")
        self.ax.set_zticks(np.linspace(0, 255, 15))
        self.canvas.draw()
