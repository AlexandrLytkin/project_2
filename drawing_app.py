import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.pen_color = 'black'
        self.current_color = None
        self.draw_label()
        self.wight, self.height = 1000, 600
        self.image = Image.new("RGB", (self.wight, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=self.wight, height=self.height, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None

        self.window_color_of_brush()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)
        self.canvas.bind('<Button-1>', self.get_canvas_click_position)

        self.background = 'white'
        self.size_text = 12
        self.x_pos = int(self.wight // 2)
        self.y_pos = int(self.height // 2)

    def setup_ui(self) -> None:
        """Метод рисует прямоугольник, добавляет на него кнопки управления"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        self.make_button(control_frame, "Очистить", self.clear_canvas)
        self.make_button(control_frame, "Выбрать цвет", self.choose_color)
        self.make_button(control_frame, "Сохранить", self.save_image)
        self.make_button(control_frame, "Размера холста", self.resizing_the_canvas)
        self.make_button(control_frame, "Текст", self.add_text)
        self.make_button(control_frame, "Изменить фон", self.change_canvas_color)
        self.make_button(control_frame, "Ластик", self.rubber)

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
        """Метод пишет лейбл 'цвет кисти'"""
        text_color = 'black' if self.pen_color == 'white' else 'white'
        self.lbl = tk.Label(master=self.root, text="Цвет кисти", bg=self.pen_color, fg=text_color)
        self.lbl.pack()

    def window_color_of_brush(self) -> None:
        """Метод показывает текущий цвет кисти в отдельном окне"""
        self.canvas1 = tk.Canvas(self.root, width=50, height=20, bg=self.pen_color, )
        self.canvas1.configure(bg=self.pen_color)
        self.canvas1.pack()

    def show_current_color(self) -> None:
        """Метод показывает текущий цвет кисти"""
        self.canvas1.configure(bg=self.pen_color)
        self.lbl.configure(bg=self.pen_color)

    def pick_color(self, event: tk.Event) -> None:
        """Метод пипетка для выбора цвета с холста
        Выбор цвета кисти нажатием на среднюю (3-button) мыши
        Перевод RGB цвета в HEX код цвета"""
        color = self.image.getpixel((event.x, event.y))
        self.pen_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        self.show_current_color()

    def make_button(self, control_frame: tk.Frame, text: str, command) -> None:
        """Метод создает кнопку.
        Сохраняем ссылку на последнюю созданную кнопку"""
        clear_button = tk.Button(master=control_frame, text=text, command=command)
        clear_button.pack(side=tk.LEFT)
        self.last_button = clear_button

    def rubber(self) -> None:
        """Метод ластик.
        Стирает нарисованные объекты и переключается на последний цвет"""
        if self.current_color:
            self.pen_color = self.current_color
            self.current_color = None
            self.last_button.configure(text='Ластик')
        else:
            self.current_color = self.pen_color
            # self.pen_color = 'white'
            self.pen_color = self.background
            self.last_button.configure(text='Кисть')
        self.show_current_color()

    def brush(self, control_frame: tk.Frame) -> None:
        """Метод создания открывающегося меню выбора толщины кисти.
        Не явно переводит *sizes в строку из чисел для метода command="""
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
        self.image = Image.new("RGB", (self.wight, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event: tk.Event = None) -> None:
        """Метод вывода экрана выбора цвета"""
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.show_current_color()

    def resizing_the_canvas(self, event: tk.Event = None) -> None:
        """Метод изменения размера экрана.
        Проверяем согласие и только потом меняем размеры ширины и высоты"""
        agree = simpledialog.askstring(f'Вы уверены текущий рисунок пропадет',
                                       prompt='Напишите Согласен',
                                       initialvalue='Согласен')
        if agree == 'Согласен':
            wight = simpledialog.askinteger(f'Текущий размер холста {self.wight}x{self.height}',
                                            prompt='Введите ширину холста', minvalue=50, maxvalue=1500,
                                            initialvalue=self.wight)
            if wight:
                self.wight = wight
            self.canvas.config(width=self.wight, height=self.height)

            height = simpledialog.askinteger(f'Текущий размер холста {self.wight}x{self.height}',
                                             prompt='Введите высоту холста', minvalue=50, maxvalue=700,
                                             initialvalue=self.height)
            if height:
                self.height = height
            self.canvas.config(width=self.wight, height=self.height)

            self.clear_canvas()

    def get_canvas_click_position(self, event: tk.Event = None):
        self.x_pos = event.x
        self.y_pos = event.y

    def add_text(self):
        """Метод добавления текста на изображение"""
        some_text = tk.simpledialog.askstring(f'Цвет текста в цвет кисти: {self.pen_color}',
                                              f'Координаты текста {self.x_pos}x{self.y_pos}\nВведите текст:')
        size_text = tk.simpledialog.askinteger('Выбери размер шрифта',
                                               prompt=f'Текущий размер шрифта {self.size_text}\nВведи число:')
        if some_text and size_text:
            x, y = self.x_pos, self.y_pos
            self.draw.text((x, y), some_text, fill=self.pen_color)
            self.canvas.create_text(x, y, text=some_text, font=("Arial", size_text), fill=self.pen_color)

    def change_canvas_color(self) -> None:
        """Метод изменения цвета фона холста"""
        self.background = colorchooser.askcolor()[1]
        self.canvas.config(background=self.background)

    def save_image(self, event: tk.Event = None) -> None:
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
