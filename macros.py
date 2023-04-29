import pyautogui as pag
import keyboard
import threading
from datetime import datetime as time, timedelta as delta

# from colorama import init, Fore, Style

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


# init()


class Macros:
    def __init__(self):
        # Установка переменных
        self.work_key, self.stop_key = 'q', 'w'  # Клавиши управления

        self.delay = 0.2  # Базовая задержка в секундах
        self.click_delay = 0.1  # Задержка перед кликом в секундах
        self.hold_time = 0.03  # Время удержания в секундах

        self.count = 0

        # Объявление горячей клавиши
        keyboard.add_hotkey(self.work_key,
                            lambda: self.work(pag.prompt("Введите количество успешных покупок, ед.: "),
                                              pag.prompt(
                                                  "Введите продолжительность по времени для работы макроса, мин.: ")))

        keyboard.wait(self.stop_key)  # Ожидание нажатия кнопки остановки
        pag.alert('Выход из макроса.')
        exit()

    def check_purchase(self, check_time, pause=5):  # Метод проверки покупки
        def check(delay=pause):  # Функция, которая проверяет, появилось ли уведомление о покупке
            while not pag.locateCenterOnScreen('Images/Notices/purchase_notice.png') and (
                    time.now() - check_time) < delta(seconds=delay):
                if pag.locateCenterOnScreen('Images/Notices/purchase_notice.png'):  # Поиск уведомления
                    self.count += 1
                    return
                pag.sleep(self.delay)

        checker = threading.Thread(target=check())
        checker.start()  # Запуск нового потока
        checker.join()  # Ожидание результата потока и его завершение

    def update(self):  # Метод обновления
        # print(Fore.YELLOW + "Обновление..." + Style.RESET_ALL)
        pag.click(pag.locateCenterOnScreen('Images/Buttons/cost_button.png', confidence=0.8), duration=self.click_delay)
        # print(Fore.GREEN + "Обновление...Done" + Style.RESET_ALL)

    def buy(self, button_center, full=False):  # Метод покупки
        pag.click(button_center, duration=self.click_delay)  # Нажатие на кнопку

        if full:
            pag.sleep(self.delay)
            # print(Fore.YELLOW + "ВСЕ..." + Style.RESET_ALL)
            pag.click(pag.locateCenterOnScreen('Images/Buttons/full_button.png', confidence=0.8),
                      duration=self.click_delay)
            # print(Fore.GREEN + "ВСЕ...Done" + Style.RESET_ALL)

        pag.sleep(self.delay)  # Задержка перед нажатием клавиши "y"
        keyboard.press_and_release('y')  # Нажать на клавишу "y"
        # print("Нажата кнопка Y")

    def work(self, target_count, duration):
        target_time = time.now() + delta(duration)  # Создаётся время окончания работы макроса
        self.count = 0
        while True:

            pag.sleep(self.delay * 4)

            # print(Fore.YELLOW + "Ищем кнопку 'Купить'..." + Style.RESET_ALL)
            button_center = pag.locateCenterOnScreen('Images/Buttons/buy_button.png', confidence=0.6)
            # print(Fore.CYAN + f"Полученные координаты: {button_center}" + Style.RESET_ALL)

            if button_center:  # Проверка на наличие лота
                # print(Fore.GREEN + "Начинается покупка" + Style.RESET_ALL)
                self.buy(button_center)  # Покупается лот из списка
                self.check_purchase(time.now())  # Проверяется, случилась ли удачная покупка
            else:
                pass
                # print(Fore.RED + "Кнопка 'Купить' не найдена" + Style.RESET_ALL)

            self.update()  # Обновление списка лотов

            if self.count != target_count:  # Остановка макроса при достижении заданного количества успешных покупок
                pag.alert('Цикл остановлен.\nДостигнут лимит по покупкам.\n' + str(time.now()))
                return

            if time.now() != target_time:  # Остановка макроса при истечении заданной продолжительности работы
                pag.alert('Цикл остановлен.\nВремя вышло.' + str(time.now()))
                return

            if keyboard.is_pressed(self.work_key):  # Остановка макроса при зажатии пользователем рабочей кнопки
                # print(Fore.CYAN + "Зажата рабочая кнопка" + Style.RESET_ALL)
                pag.sleep(0.5)  # Ожидание зажатия
                # print(Fore.GREEN + "Зажата рабочая кнопка" + Style.RESET_ALL)

                if keyboard.is_pressed(self.work_key):
                    pag.alert('Цикл остановлен.')
                    # print(Fore.RED + "Цикл остановлен." + Style.RESET_ALL)
                    return


if __name__ == "__main__":
    macros = Macros()
