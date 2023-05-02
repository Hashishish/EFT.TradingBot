import datetime
from loguru import logger
import pyautogui as pag
import keyboard
import threading
from datetime import datetime as time, timedelta as delta

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


class Macros:
    def __init__(self):
        # Установка переменных
        self.key_work, self.key_stop, self.key_cycle = 'q', 'w', 'e'  # Клавиши управления

        self.delay = 0.2  # Базовая задержка в секундах
        self.click_delay = 0.1  # Задержка перед кликом в секундах
        self.hold_time = 0.03  # Время удержания в секундах

        self.count = 0

        self.full_buy = False
        logger.debug("Базовые переменные объявлены.")

        # Объявление горячей клавиши
        keyboard.add_hotkey(self.key_cycle,
                            lambda: (logger.debug(f"Сработка горячей клавиши {self.key_cycle}."),
                                     self.cycle(pag.prompt("Введите количество успешных покупок, ед.: "),
                                                pag.prompt("Введите продолжительность работы макроса, мин.: "))),
                            logger.debug("Цикл запущен по горячей клавише."))

        keyboard.add_hotkey(self.key_work, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_cycle}."), self.work(),
            logger.debug("Запуск одной покупки по горячей клавише.")))
        logger.debug("Горячие клавиши обозначены.")

    def validate(self):  # TODO: доделать проверку на верность введённых данных, а из гуи убрать.
        pass

    def check_purchase(self, check_time: datetime.datetime, pause: int = 5):  # Метод проверки покупки
        def check(delay=pause):  # Функция, которая проверяет, появилось ли уведомление о покупке
            while not pag.locateCenterOnScreen('Images/Notices/notice_purchase.png') and (
                    time.now() - check_time) < delta(seconds=delay):
                if pag.locateCenterOnScreen('Images/Notices/notice_purchase.png'):  # Поиск уведомления
                    logger.info("Покупка подтверждена.")
                    self.count += 1
                    return
                pag.sleep(self.delay)

        checker = threading.Thread(target=check())
        logger.debug("Поток с циклом проверки на наличе уведомления Объявлен.")
        checker.start()  # Запуск нового потока
        logger.debug("Поток с циклом проверки на наличе уведомления Запущен.")
        checker.join()  # Ожидание результата потока и его завершение
        logger.debug("Поток с циклом проверки на наличе уведомления Завершён.")

    def update(self):  # Метод обновления
        try:
            logger.debug("Обновление по cost_up.")
            pag.click(pag.locateCenterOnScreen('Images/Buttons/button_cost_up.png', confidence=0.8),
                      duration=self.click_delay)
            logger.info("Обновлено по cost_up.")
        except:
            try:
                logger.debug("Обновление по cost_down.")
                pag.click(pag.locateCenterOnScreen('Images/Buttons/button_cost_down.png', confidence=0.8),
                          duration=self.click_delay)
                logger.info("Обновлено по cost_down.")
            except Exception as e:
                logger.debug(e)
                logger.info("Кнопка обновления не найдена.")

    def buy(self, button_center: tuple):  # Метод покупки
        logger.debug(f"Кнопка по координатам: {button_center}.")
        pag.click(button_center, duration=self.click_delay)  # Нажатие на кнопку
        logger.info("Кнопка покупки нажата.")

        if self.full_buy:
            logger.debug("Покупка всех предметов в лоте.")
            pag.sleep(self.delay)
            pag.click(pag.locateCenterOnScreen('Images/Buttons/button_full.png', confidence=0.8),
                      duration=self.click_delay)
            logger.info("Выбраны все предметы в лоте.")

        pag.sleep(self.delay)  # Задержка перед нажатием клавиши "y"
        keyboard.press_and_release('y')  # Нажать на клавишу "y"
        logger.info("Кнопка 'Y' была нажата.")

    @logger.catch
    def work(self):

        logger.debug("Поиск кнопки 'Купить'.")
        button_center = pag.locateCenterOnScreen('Images/Buttons/button_buy.png', confidence=0.6)
        logger.info(f"Полученные координаты: {button_center}")

        if button_center:  # Проверка на наличие лота
            logger.debug("Начинается покупка.")
            self.buy(button_center)  # Покупается лот из списка
            logger.info(f"Совершена покупка в {time.now()}.")
            logger.debug(f"Начинается проверка покупки от {time.now()}.")
            self.check_purchase(time.now())  # Проверяется, случилась ли удачная покупка
            logger.info("Проверка покупки запущена.")
        else:
            logger.info("Кнопка 'Купить' не найдена.")

    @logger.catch
    def cycle(self, target_count: int, duration: int):
        logger.debug(f"Целевое количество успешных покупок: {target_count}, Продолжительность работы: {duration}.")
        if not self.full_buy:
            logger.debug(f"Переменная полного закупа {self.full_buy}.")
            self.full_buy = pag.confirm("Покупать все единицы товара в лоте?")
            logger.info(f"Переменная полного закупа от пользователя {self.full_buy}.")

        self.count = 0
        target_time = time.now() + delta(duration)  # Создаётся время окончания работы макроса
        logger.info(f"Время окончания работы макроса {target_time}")
        while not keyboard.is_pressed(self.key_work):
            logger.debug(f"Подтверждённых покупок на начало выполнения цикла: {self.count}")

            pag.sleep(self.delay * 4)

            logger.debug("Запуск метода 'work'.")
            self.work()

            logger.debug("Запуск метода 'update'.")
            self.update()

            if self.count >= target_count:  # Остановка макроса при достижении заданного количества успешных покупок
                pag.alert('Цикл остановлен.\nДостигнут лимит по покупкам.\n' + str(time.now()))
                logger.info("Цикл остановлен. Достигнут лимит по покупкам. " + str(time.now()))
                return

            if time.now() >= target_time:  # Остановка макроса при истечении заданной продолжительности работы
                pag.alert('Цикл остановлен.\nВремя вышло.' + str(time.now()))
                logger.info("Цикл остановлен. Время вышло. " + str(time.now()))
                return

        pag.alert('Цикл остановлен.')
        logger.info("Цикл остановлен. " + str(time.now()))


if __name__ == "__main__":
    macros = Macros()
    keyboard.wait(macros.key_stop)  # Ожидание нажатия кнопки остановки
    pag.alert('Выход из макроса.')
