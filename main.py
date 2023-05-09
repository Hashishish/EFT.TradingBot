import threading
import pyautogui as pag
import keyboard
import sys
import tkinter as tk
from macros import Macros
from loguru import logger


class Window(Macros):
    def __init__(self, master):
        super().__init__(True)
        self.master = master
        master.title("Настройки")
        keyboard.clear_all_hotkeys()
        logger.debug("Горячие клавиши сброшены.")

        # Горячая клавиша на начало работы цикла
        keyboard.add_hotkey(self.key_cycle, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_cycle}."), self.start(),
            logger.debug("Цикл ЗАПУЩЕН по горячей клавише.")))

        # Горячая клавиша на завершение работы цикла
        keyboard.add_hotkey(self.key_stop, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_stop}."), self.stop(f"Горячая клавиша {self.key_stop}"),
            logger.debug("Цикл ОСТАНОВЛЕН по горячей клавише.")))

        # Горячая клавиша на единовременный запуск итерации
        keyboard.add_hotkey(self.key_work, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_work}."), self.work(),
            logger.debug("Запуск одной покупки по горячей клавише.")))

        # Горячая клавиша на единовременный запуск итерации
        keyboard.add_hotkey(self.key_exit, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_exit}."), self.close(),
            logger.debug("Запуск одной покупки по горячей клавише.")))
        logger.debug("Горячие клавиши обозначены для графического интерфейса.")

        # Задаём новый тип данных для переменных для их отслеживания и передачи в GUI
        self.sv_confidence = tk.StringVar(value=str(self.confidence)[2:])
        self.sv_confidence.trace("w", self.confidence_change)

        self.sv_count = tk.StringVar(value=str(self.count))

        self.b_full_buy = tk.BooleanVar(value=self.full_buy)

        # Создаём названия
        self.label_check_full_buy = tk.Label(master, text="Покупка всех предметов в лоте:")
        self.label_quantity = tk.Label(master, text="Нужное количество успешных покупок, ед.:")
        self.label_duration = tk.Label(master, text="Длительность работы цикла, мин.:")
        self.label_confidence = tk.Label(master, text="Точность поиска кнопок, д.ед.: \t\t0.")
        self.label_count_text = tk.Label(master, text="Текущее количество успешных покупок, ед.: ")

        # Создаём показатели
        self.check_full_buy = tk.Checkbutton(master, text="Покупать всё", onvalue=True, offvalue=False,
                                             variable=self.b_full_buy,
                                             command=lambda: (logger.debug(f"Покупать всё = {self.b_full_buy.get()}"),
                                                              self.full_buy_change()))

        self.entry_quantity = tk.Entry(self.master)
        self.entry_quantity.insert(0, str(5))

        self.entry_duration = tk.Entry(self.master)
        self.entry_duration.insert(0, str(5))

        self.entry_confidence = tk.Entry(self.master, textvariable=self.sv_confidence)

        self.label_count_variable = tk.Label(master, textvariable=self.sv_count)

        # Создаём кнопки
        self.button_stop = tk.Button(master, text="Остановить цикл", command=lambda: self.stop("Графическая кнопка"))
        self.button_stop.grid(row=5, column=0, sticky="E")
        self.button_stop.config(state="disabled")  # По умолчанию кнопка выключена
        self.button_start = tk.Button(master, text="Запустить цикл", command=lambda: self.start())
        self.button_start.grid(row=5, column=1, sticky="E")

        # Располагаем элементы по сетке
        self.label_check_full_buy.grid(row=0, column=0, sticky="W")
        self.label_quantity.grid(row=1, column=0, sticky="W")
        self.label_duration.grid(row=2, column=0, sticky="W")
        self.label_confidence.grid(row=3, column=0, sticky="W")
        self.label_count_text.grid(row=4, column=0, sticky="E")

        self.check_full_buy.grid(row=0, column=1)
        self.entry_quantity.grid(row=1, column=1)
        self.entry_duration.grid(row=2, column=1)
        self.entry_confidence.grid(row=3, column=1)
        self.label_count_variable.grid(row=4, column=1)

    def confidence_change(self, *args):
        now = self.sv_confidence.get()
        if now:
            try:
                self.confidence = float("0." + now)
                logger.debug(f"Confidence: {self.confidence}")
            except ValueError:
                logger.error(f"Получено неверное значение для точности! {self.sv_confidence.get()}")
                self.sv_confidence.set("8")
                self.confidence = 0.8
                logger.debug(f"Confidence: {self.confidence}")
        else:
            pass

    def full_buy_change(self, *args):
        self.full_buy = self.b_full_buy.get()

    def start(self):
        logger.debug("Цикл запущен по графической кнопке.")
        target_count, duration = self.entry_quantity.get(), self.entry_duration.get()
        trader = threading.Thread(target=self.cycle, args=(target_count, duration))
        logger.debug("Поток с циклом МАКРОСА Объявлен.")
        trader.start()  # Запуск нового потока
        logger.debug("Поток с циклом МАКРОСА Запущен.")

        # Переключаем положения кнопок при запуске
        self.button_stop.config(state="normal")
        self.button_start.config(state="disabled")

    def stop(self, reason='stop'):
        super().stop(reason)
        pag.sleep(self.delay * 2)

        # Переключаем положения кнопок при остановке
        self.button_stop.config(state="disabled")
        self.button_start.config(state="normal")

    # def cycle(self, target_count, duration):  # Переопределение для недопущения запуска при остановленном положении
    #     if not self.event_stop:
    #         return self.stop()
    #     super().cycle(target_count, duration)

    def close(self):
        logger.debug("Завершение цикла и закрытие окна.")
        self.stop("Закрытие окна")
        root.destroy()
        sys.exit(0)

    def _hook(self):
        self.sv_count.set(self.count)  # Хук на macros:check_purchase:check:while:if


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)
    my_window = Window(root)
    root.protocol("WM_DELETE_WINDOW", lambda: my_window.close())
    root.mainloop()
