from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class PolyWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Сферический ландшафт")

        self.label_dots = ttk.Label(self, text="Плотность точек")
        self.label_dots.grid(column=5, row=0, pady=(3, 3))

        self.text_box_dots = ttk.Entry(self)
        self.text_box_dots.grid(column=5, row=1, pady=(3, 3))
        self.text_box_dots.insert(0, 20)

        self.label_iterations = ttk.Label(self, text="Количество итераций")
        self.label_iterations.grid(column=5, row=2, pady=(3, 3))

        self.text_box_iterations = ttk.Entry(self)
        self.text_box_iterations.grid(column=5, row=3, pady=(3, 3))
        self.text_box_iterations.insert(0, 7)

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

    @staticmethod
    def random_vector():
        # n = np.random.uniform(-1.0, 1.0, 3)
        n = np.random.rand(3)
        magnitude = np.linalg.norm(n)
        while magnitude >= 1:
            n = np.random.rand(3)
            # n = np.random.uniform(-1.0, 1.0, 3)
            magnitude = np.linalg.norm(n)
        return n

    @staticmethod
    def move_vertex(vertex, n, m):
        d = np.dot(n, vertex)
        x = np.random.choice([-1, 1])
        y = np.random.choice([-1, 1])
        z = np.random.choice([-1, 1])
        vertex[0] += m * x
        vertex[1] += m * y
        vertex[2] += m * z

        return vertex

    @staticmethod
    def create_sphere(num_vertices):
        theta = np.linspace(0, 2 * np.pi, num_vertices)
        phi = np.linspace(0, np.pi, num_vertices)
        theta, phi = np.meshgrid(theta, phi)
        x = np.cos(theta) * np.sin(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(phi)
        vertices = np.vstack((x.flatten(), y.flatten(), z.flatten())).T
        return vertices

    def distort_sphere(self, vertices, num_iterations):
        print(f"start")
        for _ in range(num_iterations):
            if _ % 10 == 0:
                print(f"итерация номер {_}")
            n = self.random_vector()
            m = np.random.choice([-0.05, 0.05])
            for i in range(len(vertices)):
                vertices[i] = self.move_vertex(vertices[i], n, m)
        return vertices

    @staticmethod
    def create_sphere_triangles(vertices):
        triangles = []
        n = int(np.sqrt(len(vertices)))  # Количество вершин вдоль каждой оси

        for i in range(n - 1):
            for j in range(n - 1):
                # Индексы вершин для текущего квадрата
                v0 = i * n + j
                v1 = i * n + j + 1
                v2 = (i + 1) * n + j
                v3 = (i + 1) * n + j + 1

                # Добавление треугольника 1
                triangles.append([v0, v2, v1])

                # Добавление треугольника 2
                triangles.append([v1, v2, v3])

        return np.array(triangles)

    def generate_land(self):
        # Параметры сферы и алгоритма
        iterations = int(self.text_box_iterations.get())
        vertices = int(self.text_box_dots.get())

        # Создание сферы
        sphere = self.create_sphere(vertices)

        # Искажение сферы
        distorted_sphere = self.distort_sphere(sphere.copy(), vertices)

        triangles = self.create_sphere_triangles(distorted_sphere)

        self.fig.clear()
        self.ax = self.fig.add_subplot(projection="3d")

        result = Poly3DCollection(
            distorted_sphere[triangles], alpha=0.25, edgecolor="k", linewidths=0.1
        )
        self.ax.add_collection3d(result)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])
        self.canvas.draw()
