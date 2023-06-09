import datetime
from loguru import logger
import pyautogui as pag
import keyboard
import threading
from datetime import datetime as time, timedelta as delta

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!


class Macros:
    def __init__(self, fb):
        # Установка переменных
        self.key_work, self.key_exit, self.key_cycle, self.key_stop = 'q', 'w', 'e', 'r'  # Клавиши управления

        self.delay = 0.2  # Базовая задержка в секундах
        self.click_delay = 0.1  # Задержка перед кликом в секундах
        self.confidence = 0.8  # Точность поиска

        self.count = 0

        self.full_buy = fb
        self.event_stop = False
        logger.debug("Базовые переменные объявлены.")

        # Объявление горячей клавиши
        keyboard.add_hotkey(self.key_cycle,
                            lambda: (logger.debug(f"Сработка горячей клавиши {self.key_cycle}."),
                                     self.cycle(pag.prompt("Введите количество успешных покупок, ед.: "),
                                                pag.prompt("Введите продолжительность работы макроса, мин.: ")),
                                     logger.debug("Цикл запущен по горячей клавише.")))

        keyboard.add_hotkey(self.key_stop, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_stop}."), self.stop(f"Горячая клавиша {self.key_stop}"),
            logger.debug("Запуск одной покупки по горячей клавише.")))

        keyboard.add_hotkey(self.key_work, lambda: (
            logger.debug(f"Сработка горячей клавиши {self.key_work}."), self.work(),
            logger.debug("Запуск одной покупки по горячей клавише.")))
        logger.debug("Горячие клавиши обозначены.")

    # TODO: Сделать решение капчи
    # TODO: Сделать адаптацию для работы на разном разрешении
    # TODO: Сделать возможность автоввода параметров сортировки

    def stop(self, reason='stop'):
        self.event_stop = True
        logger.info(f'СТОП. Причина: {reason}')

    def validate(self, var: any) -> int:
        try:
            var_int = int(var)
            logger.debug(f"Значение {var} преобразовано в целочисленное.")
            return var_int
        except ValueError:
            logger.error(f"Значение '{var}' не может быть преобразовано в целочисленное.")
            pag.alert("Задан неверный формат чисел!")
            return 0

    def update(self):  # Метод обновления
        cost_up = pag.locateCenterOnScreen('Images/Buttons/button_cost_up.png', confidence=self.confidence)
        cost_down = pag.locateCenterOnScreen('Images/Buttons/button_cost_down.png', confidence=self.confidence)
        if cost_up:
            pag.click(cost_up, duration=self.click_delay)
            logger.debug("Обновлено по cost_up.")
        elif cost_down:
            pag.click(cost_down, duration=self.click_delay)
            logger.debug("Обновлено по cost_down.")
        else:
            logger.debug("Кнопка обновления не найдена.")

        # try:
        #     logger.debug("Обновление по cost_up.")
        #     pag.click(pag.locateCenterOnScreen('Images/Buttons/button_cost_up.png', confidence=self.confidence),
        #               duration=self.click_delay)
        #     logger.info("Обновлено по cost_up.")
        # except Exception as e:
        #     logger.debug(e)
        #     try:
        #         logger.debug("Обновление по cost_down.")
        #         pag.click(pag.locateCenterOnScreen('Images/Buttons/button_cost_down.png', confidence=self.confidence),
        #                   duration=self.click_delay)
        #         logger.info("Обновлено по cost_down.")
        #     except Exception as e:
        #         logger.error(e)
        #         logger.info("Кнопка обновления не найдена.")

    def buy(self, button_center: tuple):  # Метод покупки
        logger.debug(f"Кнопка по координатам: {button_center}.")
        pag.click(button_center, duration=self.click_delay)  # Нажатие на кнопку
        logger.info("Кнопка покупки нажата.")

        if self.full_buy:
            logger.debug(f"Покупка всех предметов в лоте. full_buy={self.full_buy}")
            pag.sleep(self.delay)
            pag.click(pag.locateCenterOnScreen('Images/Buttons/button_full.png', confidence=self.confidence),
                      duration=self.click_delay)
            logger.info("Выбраны все предметы в лоте.")

        pag.sleep(self.delay)  # Задержка перед нажатием клавиши "y"
        keyboard.press_and_release('y')  # Нажать на клавишу "y"
        logger.info("Кнопка 'Y' была нажата.")

    def error_catch(self):
        pag.sleep(self.delay)

        error_out_of = pag.locateCenterOnScreen('Images/Errors/error_out_of_place.png', confidence=self.confidence)
        error_not_all = pag.locateCenterOnScreen('Images/Errors/error_not_all.png', confidence=self.confidence)
        error_not_enough = pag.locateCenterOnScreen('Images/Errors/error_not_enough.png', confidence=self.confidence)

        if error_out_of:
            logger.error("НЕДОСТАТОЧНО МЕСТА.")
            self.stop("НЕДОСТАТОЧНО МЕСТА.")
            pag.click(pag.locateCenterOnScreen('Images/Buttons/button_ok.png'))
            logger.debug("Нажата ОК.")
        elif error_not_enough:
            logger.error("НЕДОСТАТОЧНО СРЕДСТВ.")
            self.stop("НЕДОСТАТОЧНО СРЕДСТВ.")
            pag.click(pag.locateCenterOnScreen('Images/Buttons/button_ok.png'))
            logger.debug("Нажата ОК.")
        elif error_not_all:
            logger.info("Куплено СТОЛЬКО-ТО ед.")  # TODO: доделать обработку покупки не полной пачки предметов
            pag.click(pag.locateCenterOnScreen('Images/Buttons/button_ok.png'))
            logger.debug("Нажата ОК.")
        else:
            logger.debug("Ошибок не обнаружено.")

        # try:
        #     pag.locateCenterOnScreen('Images/Errors/error_out_of_place.png', confidence=self.confidence)
        #     logger.error("НЕДОСТАТОЧНО МЕСТА.")
        #     self.stop("НЕДОСТАТОЧНО МЕСТА.")
        # except:
        #     try:
        #         pag.locateCenterOnScreen('Images/Errors/error_not_all.png', confidence=self.confidence)
        #         logger.info("Куплено СТОЛЬКО-ТО ед.")  # TODO: доделать обработку покупки не полной пачки предметов
        #     except:
        #         try:
        #             pag.locateCenterOnScreen('Images/Errors/error_not_enough.png', confidence=self.confidence)
        #             logger.error("НЕДОСТАТОЧНО СРЕДСТВ.")
        #             self.stop("НЕДОСТАТОЧНО СРЕДСТВ.")
        #         except:
        #             pass  # TODO: Сделать отслеживание капчи
        # finally:
        #     try:
        #         pag.click(pag.locateCenterOnScreen('Images/Buttons/button_ok.png'))
        #         logger.debug("Нажата ОК.")
        #     except:
        #         logger.debug("Ошибок не обнаружено.")

    # TODO: Добавить возможность выбора в GUI продолжительности проверки на появление уведомления о покупке
    def check_purchase(self, check_time: datetime.datetime, pause: int = 2):  # Метод проверки покупки
        def check(delay=pause):  # Функция, которая проверяет, появилось ли уведомление о покупке
            target_time = delta(seconds=delay)
            while (time.now() - check_time) < target_time:  # TODO: переделать обработчик на покупку множества
                if pag.locateCenterOnScreen('Images/Notices/notice_purchase.png'):  # Поиск уведомления
                    logger.info(f"Покупка от {check_time} подтверждена.")
                    self.count += 1
                    self._hook()
                    return

        checker = threading.Thread(target=check)
        logger.debug("Поток с циклом проверки на наличе уведомления Объявлен.")
        checker.start()  # Запуск нового потока
        logger.debug("Поток с циклом проверки на наличе уведомления Запущен.")
        checker.join()  # Ожидание результата потока и его завершение
        logger.debug("Поток с циклом проверки на наличе уведомления Завершён.")

    @logger.catch
    def work(self):

        logger.debug("Поиск кнопки 'Купить'.")
        pag.sleep(self.delay * 2)
        button_center = pag.locateCenterOnScreen('Images/Buttons/button_buy2.png', confidence=self.confidence)
        logger.debug(f"Полученные координаты: {button_center}")

        if button_center:  # Проверка на наличие лота
            logger.debug("Начинается покупка.")
            self.buy(button_center)  # Покупается лот из списка
            logger.info(f"Совершена покупка в {time.now()}.")
            logger.debug("Начинается проверка на ошибки.")
            self.error_catch()  # Проверка на ошибки
            logger.debug(f"Начинается проверка покупки от {time.now()}.")
            self.check_purchase(time.now())  # Проверяется, случилась ли удачная покупка
        else:
            logger.debug("Кнопка 'Купить' не найдена.")

    @logger.catch
    def cycle(self, target_count, duration):
        self.event_stop = False
        validated_target_count = self.validate(target_count)
        validated_duration = self.validate(duration)
        if not (validated_duration and validated_target_count):
            logger.error(f"Параметры заданы неверно, либо равны нулю.")
            return self.stop("Неверно заданы стартовые параметры")
        logger.debug(f"Целевое количество успешных покупок: {validated_target_count}")
        logger.debug(f"Продолжительность работы: {validated_duration}.")
        self.count = 0
        self._hook()
        target_time = time.now() + delta(minutes=validated_duration)  # Создаётся время окончания работы макроса
        logger.info(f"Время окончания работы макроса {target_time}")
        while not self.event_stop:
            logger.debug(f"Подтверждённых покупок на начало выполнения цикла: {self.count}")

            pag.sleep(self.delay)

            logger.debug("Запуск метода 'work'.")
            self.work()

            logger.debug("Запуск метода 'update'.")
            self.update()

            if self.count >= validated_target_count:  # Остановка цикла при достижении заданного кол-ва успешных покупок
                pag.alert('Цикл остановлен.\nДостигнут лимит по покупкам.\n' + str(time.now()))
                self.stop("Цикл остановлен. Достигнут лимит по покупкам. " + str(time.now()))

            if time.now() >= target_time:  # Остановка макроса при истечении заданной продолжительности работы
                pag.alert('Цикл остановлен.\nВремя вышло.' + str(time.now()))
                self.stop("Цикл остановлен. Время вышло. " + str(time.now()))

        pag.alert('Цикл остановлен.')
        logger.info("Цикл остановлен. " + str(time.now()))

    def _hook(self, *args):
        pass


if __name__ == "__main__":
    macros = Macros(pag.confirm("Покупать все единицы товара в лоте?"))
    keyboard.wait(macros.key_exit)  # Ожидание нажатия кнопки остановки
    pag.alert('Выход из макроса.')
