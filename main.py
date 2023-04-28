import time
import pyautogui as pag
import keyboard

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


class Macros:
    def __init__(self):
        # установка начальных координат
        self.position_1 = 1870, 165
        self.position_2 = 2350, 240

        self.delay = 0.4  # задержка в секундах между действиями

        self.work_key, self.stop_key = 'q', 'w'  # клавиши управления

        self.click_delay = 0.1  # задержка перед кликом в секундах

        self.hold_time = 0.03  # время удержания в секундах

        keyboard.add_hotkey(self.work_key, lambda: self.buy())  # объявление горячей клавиши

        self.work()  # запуск основного метода

    def buy(self):
        while keyboard.is_pressed(self.work_key):
            # print(f"Кнопка {self.work_key} зажата")
            pag.moveTo(self.position_1[0], self.position_1[1], duration=self.delay / 2)  # переместить мышь на позицию 1
            # print("Курсор перемещён в 1 позицию")
            pag.mouseDown(button='left')  # нажать на левую кнопку мыши
            # print("Левая кнопка мыши нажата")
            pag.PAUSE = self.hold_time  # задержка в отжатии
            pag.mouseUp(button='left')  # отпустить левую кнопку мыши
            # print("Левая кнопка мыши отпущена")
            pag.PAUSE = self.click_delay  # задержка в нажатии
            pag.moveTo(self.position_2[0], self.position_2[1], duration=self.delay)  # переместить мышь на позицию 2
            # print("Курсор перемещён во 2 позицию")
            pag.PAUSE = self.click_delay  # задержка в нажатии
            pag.mouseDown(button='left')  # нажать на левую кнопку мыши
            # print("Левая кнопка мыши нажата")
            pag.PAUSE = self.hold_time  # задержка в отжатии
            pag.mouseUp(button='left')  # отпустить левую кнопку мыши
            # print("Левая кнопка мыши отпущена")
            time.sleep(self.delay)  # задержка перед нажатием клавиши "y"
            pag.press('y')  # нажать на клавишу "y"
            # print("Нажата кнопка Y")

    def work(self):
        keyboard.wait(self.stop_key)
        pag.alert('Выход из макроса.')
        exit()


if __name__ == "__main__":
    macros = Macros()
