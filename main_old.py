import time
import pyautogui as pag
import keyboard

pag.FAILSAFE = False  # НЕ ТРОГАТЬ!

# установить начальные координаты
x1, y1 = 1870, 165
x2, y2 = 2350, 240

# задержка в секундах между действиями
delay = 0.25

# клавиши управления
work_key, stop_key = 'q', 'w'

# задержка перед кликом в секундах
click_delay = 0.15

# время удержания в секундах
hold_time = 0.03

# ждём, пока пользователь нажмёт нужную кнопку
while not keyboard.is_pressed(work_key):
    if keyboard.is_pressed(stop_key):
        pag.alert('Выход из макроса')
        break
    pass

# основной цикл
while keyboard.is_pressed('q'):
    print(f"Кнопка {work_key} зажата")
    pag.moveTo(x1, y1, duration=delay)  # переместить мышь на позицию 1
    print("Курсор перемещён в 1 позицию")
    pag.mouseDown(button='left')  # нажать на левую кнопку мыши
    print("Левая кнопка мыши нажата")
    pag.PAUSE = hold_time  # задержка в отжатии
    pag.mouseUp(button='left')  # отпустить левую кнопку мыши
    print("Левая кнопка мыши отпущена")
    pag.PAUSE = click_delay  # задержка в нажатии
    pag.moveTo(x2, y2, duration=delay)  # переместить мышь на позицию 2
    print("Курсор перемещён во 2 позицию")
    pag.PAUSE = click_delay  # задержка в нажатии
    pag.mouseDown(button='left')  # нажать на левую кнопку мыши
    print("Левая кнопка мыши нажата")
    pag.PAUSE = hold_time  # задержка в отжатии
    pag.mouseUp(button='left')  # отпустить левую кнопку мыши
    print("Левая кнопка мыши отпущена")
    pag.PAUSE = click_delay  # задержка в нажатии
    time.sleep(delay)  # задержка перед нажатием клавиши "y"
    pag.press('y')  # нажать на клавишу "y"
    print("Нажата кнопка Y")
    time.sleep(delay)  # задержка после нажатия клавиши "y"
