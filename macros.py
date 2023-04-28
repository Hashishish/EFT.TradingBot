import time
import pyautogui as pag
import keyboard

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


class Macros:
    def __init__(self):
        # Установка переменных
        self.position_1 = 1870, 165  # Позиция с фильтром по цене
        self.position_2 = 2350, 240  # Позиция с кнопкой купить
        self.position_3 = 1585, 650  # Позиция с кнопкой "все"
        self.lotPosition = 2307, 242  # Позиция с точкой для проверки лота

        self.work_key, self.stop_key = 'q', 'w'  # Клавиши управления

        self.delay = 0.2  # Базовая задержка в секундах
        self.click_delay = 0.1  # Задержка перед кликом в секундах
        self.hold_time = 0.03  # Время удержания в секундах

        keyboard.add_hotkey(self.work_key, lambda: self.work())  # Объявление горячей клавиши

        keyboard.wait(self.stop_key)  # Ожидание нажатия кнопки остановки
        pag.alert('Выход из макроса.')
        exit()

    def click(self):
        time.sleep(self.click_delay)  # Задержка в нажатии
        pag.mouseDown(button='left')  # Нажать на левую кнопку мыши
        print("Левая кнопка мыши нажата")
        time.sleep(self.hold_time)  # Задержка в отжатии
        pag.mouseUp(button='left')  # Отпустить левую кнопку мыши
        print("Левая кнопка мыши отпущена")

    def update(self):
        pag.moveTo(self.position_1[0], self.position_1[1])  # Переместить мышь на позицию 1
        print("Курсор перемещён в 1 позицию")
        time.sleep(self.click_delay * 5)  # задержка в обновлении
        self.click()

    def buy(self, full=False):
        pag.moveTo(self.position_2[0], self.position_2[1], duration=self.delay)  # Переместить мышь на позицию 2
        self.click()

        if full:
            pag.moveTo(self.position_3[0], self.position_3[1], duration=self.delay)  # Переместить мышь на позицию 3
            self.click()

        time.sleep(self.delay / 2)  # Задержка перед нажатием клавиши "y"
        pag.press('y')  # Нажать на клавишу "y"
        print("Нажата кнопка Y")

    def work(self):
        while True:
            print("НАЧАЛО ЦИКЛА")

            lot_color = pag.screenshot().getpixel(self.lotPosition)

            print("Обновление списка")
            self.update()  # Обновим список лотов

            if pag.screenshot().getpixel(self.lotPosition) != lot_color:  # Проверка на наличие лота
                print("Появился новый лот")
                self.buy()  # Покупается первый лот из списка

            if keyboard.is_pressed(self.work_key):
                print("Зажата рабочая кнопка")
                time.sleep(0.5)  # Ожидание нажатия продолжительностью 0.5 секунд
                print("Зажата рабочая кнопка уже в течение 0.5 секунд")

                if keyboard.is_pressed(self.work_key):
                    pag.alert('Цикл остановлен.')
                    print("Команда остановки цикла")
                    return


if __name__ == "__main__":
    macros = Macros()
