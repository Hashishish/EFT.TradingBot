import pyautogui as pag
import keyboard
import sys
import tkinter as tk
from macros import Macros


class Window(Macros):
    def __init__(self, master):
        super().__init__()
        self.master = master
        master.title("Настройки")
        self.full_buy = tk.BooleanVar(value=True)

        # Создаём переключатель для Полной закупки
        self.check_full_buy = tk.Checkbutton(master, text="Покупать всё", onvalue=True, offvalue=False,
                                             variable=self.full_buy)
        self.check_full_buy.pack()

        self.quantity = tk.Entry(self.master)
        self.quantity.insert(5, "Количество успешных покупок, мин")
        self.quantity.pack()

        self.duration = tk.Entry(self.master)
        self.duration.insert(5, "Длительность работы цикла, мин")
        self.duration.pack()

        self.button = tk.Button(self.master, text="Запустить цикл", command=self.start)
        self.button.pack()

    def start(self):
        target_count, duration = self.quantity.get(), self.duration.get()
        try:
            target_count = int(target_count)
            duration = int(duration)
            self.cycle(target_count, duration)
        except ValueError:
            return pag.alert("Задано неверное значение!")


if __name__ == "__main__":
    root = tk.Tk()
    my_window = Window(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), sys.exit(0)))
    root.mainloop()
    keyboard.wait(my_window.key_stop)  # Ожидание нажатия кнопки остановки
    pag.alert('Выход из макроса.')
