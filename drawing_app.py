import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.draw_label()

        self.image = Image.new("RGB", (1000, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=1000, height=600, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self) -> None:
        """Метод рисует прямоугольник, добавляет на него кнопки управления"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        self.make_button(control_frame, "Очистить", self.clear_canvas)
        self.make_button(control_frame, "Выбрать цвет", self.choose_color)
        self.make_button(control_frame, "Сохранить", self.save_image)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.RIGHT)

        self.brush(control_frame)

    def paint(self, event: tk.Event) -> None:
        """Метод получения координат нажатой кнопки из event и рисования"""
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def draw_label(self) -> None:
        self.lbl = tk.Label(master=self.root, text="Hello").pack()

    def make_button(self, control_frame: tk.Frame, text: str, command) -> None:
        """Метод создает кнопку"""
        print(type(command))
        clear_button = tk.Button(master=control_frame, text=text, command=command)
        clear_button.pack(side=tk.LEFT)

    def brush(self, control_frame: tk.Frame) -> None:
        """Метод создания открывающегося меню выбора толщины кисти.
        не явно переводит *sizes в строку из чисел для метода command="""
        sizes = [br for br in range(1, 11)]
        self.brush_size = tk.StringVar(self.root)
        self.brush_size.set(f'Размер кисти-{self.brush_size_scale.get()}')
        brush_size_menu = tk.OptionMenu(control_frame,
                                        self.brush_size,
                                        *sizes,
                                        command=self.change_size_brush)
        brush_size_menu.pack(side=tk.RIGHT)

    def change_size_brush(self, size) -> None:
        """Метод выбора размера кисти, принимает size: int"""
        self.brush_size_scale.set(size)
        self.brush_size.set(f'Размер кисти-{size}')

    def reset(self, event) -> None:
        """Метод отпускания кнопки снимает статус координат 'event' не используется"""
        self.last_x, self.last_y = None, None

    def clear_canvas(self) -> None:
        """Метод очистки экрана"""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (1000, 600), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self) -> None:
        """Метод вывода экрана выбора цвета"""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self) -> None:
        """Метод сохранения рисунка в файл.png"""
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
