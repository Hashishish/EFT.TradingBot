import pyautogui as pag
import keyboard

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


class Macros:
    def __init__(self):
        # Установка переменных
        self.work_key, self.stop_key = 'q', 'w'  # Клавиши управления

        self.delay = 0.2  # Базовая задержка в секундах
        self.click_delay = 0.1  # Задержка перед кликом в секундах
        self.hold_time = 0.03  # Время удержания в секундах

        keyboard.add_hotkey(self.work_key, lambda: self.work())  # Объявление горячей клавиши

        keyboard.wait(self.stop_key)  # Ожидание нажатия кнопки остановки
        pag.alert('Выход из макроса.')
        exit()

    def click(self):
        pag.sleep(self.click_delay)  # Задержка в нажатии
        pag.mouseDown(button='left')  # Нажать на левую кнопку мыши
        print("Левая кнопка мыши нажата")
        pag.sleep(self.hold_time)  # Задержка в отжатии
        pag.mouseUp(button='left')  # Отпустить левую кнопку мыши
        print("Левая кнопка мыши отпущена")

    def update(self):
        pag.moveTo(pag.locateCenterOnScreen('Images/Buttons/cost_button.png', confidence=0.8), duration=self.delay)
        print("Курсор перемещён в 1 позицию")
        pag.sleep(self.click_delay * 4)  # Задержка в обновлении
        self.click()
        pag.sleep(self.click_delay * 2)  # Задержка для обработки обновлённой информации

    def buy(self, button_center, full=False):
        pag.moveTo(button_center, duration=self.delay)  # Переместить мышь на позицию 2
        self.click()

        pag.sleep(self.delay * 2)

        if full:
            pag.moveTo(pag.locateCenterOnScreen('Images/Buttons/full_button.png', confidence=0.8), duration=self.delay)
            self.click()

        pag.sleep(self.delay / 2)  # Задержка перед нажатием клавиши "y"
        pag.press('y')  # Нажать на клавишу "y"
        print("Нажата кнопка Y")

    def work(self):
        while True:
            print("НАЧАЛО ЦИКЛА")

            print("Обновление списка")
            self.update()  # Обновим список лотов

            button_center = pag.locateCenterOnScreen('Images/Buttons/buy_button.png', confidence=0.5)

            if button_center:  # Проверка на наличие лота
                print("Начинается покупка")
                self.buy(button_center)  # Покупается лот из списка

            if keyboard.is_pressed(self.work_key):
                print("Зажата рабочая кнопка")
                pag.sleep(0.1)  # Ожидание зажатия
                print("Зажата рабочая кнопка")

                if keyboard.is_pressed(self.work_key):
                    pag.alert('Цикл остановлен.')
                    print("Команда остановки цикла")
                    return


if __name__ == "__main__":
    macros = Macros()
