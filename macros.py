import pyautogui as pag
import keyboard

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


class Macros:
    def __init__(self):
        # установка начальных координат
        self.position_1 = 1870, 165
        self.position_2 = 2350, 240
        self.position_3 = 1585, 650

        self.delay = 0.4  # задержка в секундах между действиями

        self.work_key, self.stop_key = 'q', 'w'  # клавиши управления

        self.click_delay = 0.1  # задержка перед кликом в секундах

        self.hold_time = 0.03  # время удержания в секундах

        keyboard.add_hotkey(self.work_key, lambda: self.work())  # объявление горячей клавиши

        keyboard.wait(self.stop_key)  # ожидание нажатия кнопки остановки
        pag.alert('Выход из макроса.')
        exit()

    def click(self):
        pag.PAUSE = self.click_delay  # задержка в нажатии
        pag.mouseDown(button='left')  # нажать на левую кнопку мыши
        print("Левая кнопка мыши нажата")
        pag.PAUSE = self.hold_time  # задержка в отжатии
        pag.mouseUp(button='left')  # отпустить левую кнопку мыши
        print("Левая кнопка мыши отпущена")

    def update(self):
        pag.moveTo(self.position_1[0], self.position_1[1])  # переместить мышь на позицию 1
        print("Курсор перемещён в 1 позицию")
        self.click()

    def buy(self, full=False):
        pag.moveTo(self.position_2[0], self.position_2[1], duration=self.delay)  # переместить мышь на позицию 2
        self.click()

        if full:
            pag.moveTo(self.position_3[0], self.position_3[1], duration=self.delay / 4)  # переместить мышь на позицию 3
            self.click()

        pag.PAUSE = self.delay  # задержка перед нажатием клавиши "y"
        pag.press('y')  # нажать на клавишу "y"
        print("Нажата кнопка Y")

    def work(self):
        while True:
            print("НАЧАЛО ЦИКЛА")

            if pag.screenshot().getpixel((2477, 204)) == (177, 185, 189):  # Проверка на наличие лота в списке
                print("Появился новый лот")
                self.buy()  # Покупается первый лот из списка

            self.update()  # Обновим список лотов
            pag.PAUSE = self.click_delay  # задержка

            if keyboard.is_pressed(self.work_key):
                print("Зажата рабочая кнопка")
                pag.PAUSE = 2
                print("Зажата рабочая кнопка уже в течение 2 секунд")

                if keyboard.is_pressed(self.work_key):
                    pag.alert('Цикл остановлен.')
                    print("Команда остановки цикла")
                    return


if __name__ == "__main__":
    macros = Macros()
