import tkinter as tk
import pyautogui
import pyperclip
import keyboard


class MousePosition(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mouse Position")
        self.geometry("250x60")
        self.label = tk.Label(self, text="")
        self.label.pack()
        self.color_label = tk.Label(self, text="")
        self.color_label.pack()
        self.color_square = tk.Canvas(self, width=20, height=20)
        self.color_square.pack()

        # Запускаем функцию для обновления координат и цвета
        self.update_position()

        # Добавляем горячую клавишу для копирования цвета
        keyboard.add_hotkey("ctrl+c", lambda: self.copy_color_to_clipboard())

    def update_position(self):
        x, y = pyautogui.position()
        self.label.config(text=f"X: {x}, Y: {y}")

        # Получаем цвет пикселя под курсором
        if pyautogui.onScreen(x, y):
            color = pyautogui.screenshot().getpixel((x, y))
        else:
            color = (0, 0, 0)  # При выходе за границы экрана возвращаем чёрный цвет

        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        self.color_label.config(text=f"Color: {hex_color}")

        # Заполняем квадратик цветом пикселя
        self.color_square.create_rectangle(0, 0, 20, 20, fill=hex_color, outline="")

        self.after(100, self.update_position)

    def copy_color_to_clipboard(self):
        color = self.color_label.cget("text").split()[-1]
        pyperclip.copy(color)


if __name__ == "__main__":
    app = MousePosition()
    app.mainloop()
