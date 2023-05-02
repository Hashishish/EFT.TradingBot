import threading
import pyautogui as pag
import keyboard
import sys
import tkinter as tk
from macros import Macros
from loguru import logger


class Window(Macros):
    def __init__(self, master):
        super().__init__(tk.BooleanVar(value=True))
        self.master = master
        master.title("Настройки")
        self.event_stop = threading.Event()  # Событие для остановки цикла

        # Создаём названия
        self.label_check_full_buy = tk.Label(master, text="Покупать ли все предметы в лоте?")
        self.label_check_full_buy.grid(row=0, column=0)
        self.label_quantity = tk.Label(master, text="Количество успешных покупок, ед.")
        self.label_quantity.grid(row=1, column=0)
        self.label_duration = tk.Label(master, text="Длительность работы цикла, мин.")
        self.label_duration.grid(row=2, column=0)

        # Создаём показатели
        self.check_full_buy = tk.Checkbutton(master, text="Покупать всё", onvalue=True, offvalue=False,
                                             variable=self.full_buy,
                                             command=lambda: logger.debug(f"Покупать все = {self.full_buy.get()}"))
        self.check_full_buy.grid(row=0, column=1)

        self.entry_quantity = tk.Entry(self.master)
        self.entry_quantity.insert(0, str(5))
        self.entry_quantity.grid(row=1, column=1)

        self.entry_duration = tk.Entry(self.master)
        self.entry_duration.insert(0, str(5))
        self.entry_duration.grid(row=2, column=1)

        # Создаём кнопки
        self.button_stop = tk.Button(master, text="Остановить цикл", command=lambda: self.stop())
        self.button_stop.grid(row=3, column=0)
        self.button_stop.config(state="disabled")  # По умолчанию кнопка выключена
        self.button_start = tk.Button(master, text="Запустить цикл", command=lambda: self.start())
        self.button_start.grid(row=3, column=1)

    def start(self):
        logger.debug("Цикл запущен по графической кнопке.")
        target_count, duration = self.entry_quantity.get(), self.entry_duration.get()
        trader = threading.Thread(target=self.cycle, args=(target_count, duration))
        logger.debug("Поток с циклом МАКРОСА Объявлен.")
        trader.start()  # Запуск нового потока
        logger.debug("Поток с циклом МАКРОСА Запущен.")

        # Переключаем положения кнопок
        self.button_stop.config(state="normal")
        self.button_start.config(state="disabled")

    def stop(self):
        logger.debug("Цикл остановлен по графической кнопке.")
        self.event_stop.set()

        # Переключаем положения кнопок
        self.button_stop.config(state="disabled")
        self.button_start.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    my_window = Window(root)
    root.protocol("WM_DELETE_WINDOW",
                  lambda: (logger.debug("Закрытие окна и завершение кода."), root.destroy(), sys.exit(0)))
    root.mainloop()
    keyboard.wait(my_window.key_exit)  # Ожидание нажатия кнопки остановки
    pag.alert('Выход из макроса.')
