import tkinter as tk
import pyautogui


class MousePosition(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mouse Position")
        self.geometry("250x25")
        self.label = tk.Label(self, text="")
        self.label.pack()

        # Запускаем функцию для обновления координат
        self.update_position()

    def update_position(self):
        x, y = pyautogui.position()
        self.label.config(text=f"X: {x}, Y: {y}")
        self.after(100, self.update_position)


if __name__ == "__main__":
    app = MousePosition()
    app.mainloop()
