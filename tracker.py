import tkinter as tk
import pyautogui


class MousePosition(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mouse Position")
        self.geometry("250x40")
        self.label = tk.Label(self, text="")
        self.label.pack()
        self.color_label = tk.Label(self, text="")
        self.color_label.pack()

        # Запускаем функцию для обновления координат и цвета
        self.update_position()

    def update_position(self):
        x, y = pyautogui.position()
        self.label.config(text=f"X: {x}, Y: {y}")

        # Получаем цвет пикселя под курсором
        color = pyautogui.screenshot().getpixel((x, y))
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        self.color_label.config(text=f"Color: {hex_color}")

        self.after(100, self.update_position)


if __name__ == "__main__":
    app = MousePosition()
    app.mainloop()
