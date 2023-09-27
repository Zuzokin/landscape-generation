from tkinter import ttk, Tk
from irregular_method import IrregularWindow
from halving_sphere_method import SphereWindow
from regular_method import RegWindow


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Выбор метода")

        # Определение 3-x кнопок для каждого метода
        self.button_reg_net = ttk.Button(self, text="Регулярная сетка")
        self.button_reg_net["command"] = RegWindow
        self.button_reg_net.grid(
            column=0, row=1, columnspan=3, padx=(50, 50), pady=(10, 10)
        )

        self.button_ireg_net = ttk.Button(self, text="Иррегулярная сетка")
        self.button_ireg_net["command"] = IrregularWindow
        self.button_ireg_net.grid(
            column=0, row=2, columnspan=3, padx=(50, 50), pady=(10, 10)
        )

        self.button_sphere = ttk.Button(self, text="Сферические ландшафты")
        self.button_sphere["command"] = SphereWindow
        self.button_sphere.grid(
            column=0, row=3, columnspan=3, padx=(50, 50), pady=(10, 10)
        )
