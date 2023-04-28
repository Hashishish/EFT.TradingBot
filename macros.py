import pyautogui as pag
import keyboard
from colorama import init, Fore, Style

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!
init()


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

    def update(self):
        print(Fore.YELLOW + "Обновление..." + Style.RESET_ALL)
        pag.click(pag.locateCenterOnScreen('Images/Buttons/cost_button.png', confidence=0.8), duration=self.delay / 2)
        print(Fore.GREEN + "Обновление...Done" + Style.RESET_ALL)

    def buy(self, button_center, full=False):
        pag.click(button_center, duration=self.delay / 2)  # Нажатие на кнопку

        pag.sleep(self.delay * 2)

        if full:
            print(Fore.YELLOW + "ВСЕ..." + Style.RESET_ALL)
            pag.click(pag.locateCenterOnScreen('Images/Buttons/full_button.png', confidence=0.8), duration=self.delay)
            print(Fore.GREEN + "ВСЕ...Done" + Style.RESET_ALL)

        pag.sleep(self.delay)  # Задержка перед нажатием клавиши "y"
        pag.press('y')  # Нажать на клавишу "y"
        print("Нажата кнопка Y")

    def work(self):
        while True:

            self.update()  # Обновим список лотов

            pag.sleep(self.delay * 5)

            print(Fore.YELLOW + "Ищем кнопку 'Купить'..." + Style.RESET_ALL)
            button_center = pag.locateCenterOnScreen('Images/Buttons/buy_button.png', confidence=0.6)
            print(Fore.CYAN + f"Полученные координаты: {button_center}" + Style.RESET_ALL)

            if button_center:  # Проверка на наличие лота
                print(Fore.GREEN + "Начинается покупка" + Style.RESET_ALL)
                self.buy(button_center)  # Покупается лот из списка
            else:
                print(Fore.RED + "Кнопка 'Купить' не найдена" + Style.RESET_ALL)

            if keyboard.is_pressed(self.work_key):
                print(Fore.CYAN + "Зажата рабочая кнопка" + Style.RESET_ALL)
                pag.sleep(0.1)  # Ожидание зажатия
                print(Fore.GREEN + "Зажата рабочая кнопка" + Style.RESET_ALL)

                if keyboard.is_pressed(self.work_key):
                    pag.alert('Цикл остановлен.')
                    print(Fore.RED + "Цикл остановлен." + Style.RESET_ALL)
                    return


if __name__ == "__main__":
    macros = Macros()
