import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.eraser_color = 'white' 
        self.brush_size = 1

        self.canvas.bind('<Button-3>', lambda event: self.pick_color(event))

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        self.root.bind('<Control-s>', lambda event: self.save_image())
        self.root.bind('<Control-c>', lambda event: self.choose_color())

        resize_button = tk.Button(self.root, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.BOTTOM)


    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.choose_eraser_color)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_var = tk.StringVar()
        self.brush_size_var.set('1')
        sizes = ['1', '2', '5', '10']
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        self.brush_size_menu.config(width=len(max(sizes, key=len)))
        self.brush_size_menu.pack(side=tk.LEFT)

     def resize_canvas(self):
        new_width = simpledialog.askinteger(title="Изменение размера холста", prompt="Введите новую ширину:")
        new_height = simpledialog.askinteger(title="Изменение размера холста", prompt="Введите новую высоту:")

        if new_width and new_height:
            self.image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
            self.draw = ImageDraw.Draw(self.image)
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.delete('all')

     def choose_eraser_color(self):
        self.eraser_color = colorchooser.askcolor()[1] or self.eraser_color  # Используйте текущий цвет, если выбор не был сделан
        self.pen_color = self.eraser_color
        self.update_color_display()


    def update_brush_size(self, size):
        self.brush_size = int(size)
        print(f"Новый размер кисти: {self.brush_size}")

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.delete('all')

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.image.save(filename)

     def choose_color(self):
        new_color = colorchooser.askcolor()[1]
        if new_color:
            self.pen_color = new_color
            self.update_color_display()

    def update_color_display(self):
        self.color_display_label.configure(bg=self.pen_color)

    def pick_color(self, event):
        x, y = event.x, event.y
        pixel_color = self.image.getpixel((x, y))
        self.pen_color = pixel_color
        print(f"Выбранный цвет: {pixel_color}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
