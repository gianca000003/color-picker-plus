from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import pyperclip

# Lista estesa di colori con nomi italiani/descriptive (semplificata qui per esempio, ma può essere espansa)
colori_nomi = {
    (255, 0, 0): "Rosso",
    (200, 0, 0): "Rosso scuro",
    (255, 100, 100): "Rosa acceso",
    (255, 192, 203): "Rosa",
    (255, 165, 0): "Arancione",
    (255, 215, 0): "Oro",
    (255, 255, 0): "Giallo",
    (240, 230, 140): "Kaki chiaro",
    (189, 183, 107): "Kaki",
    (0, 255, 0): "Verde",
    (34, 139, 34): "Verde foresta",
    (0, 128, 0): "Verde scuro",
    (173, 255, 47): "Verde giallastro",
    (0, 255, 255): "Ciano",
    (0, 128, 128): "Verde acqua",
    (0, 0, 255): "Blu",
    (100, 149, 237): "Blu fiordaliso",
    (65, 105, 225): "Blu reale",
    (0, 0, 139): "Blu scuro",
    (138, 43, 226): "Indaco",
    (75, 0, 130): "Indaco scuro",
    (255, 0, 255): "Magenta",
    (128, 0, 128): "Viola",
    (148, 0, 211): "Viola intenso",
    (255, 255, 255): "Bianco",
    (211, 211, 211): "Grigio chiaro",
    (169, 169, 169): "Grigio",
    (128, 128, 128): "Grigio scuro",
    (0, 0, 0): "Nero",
    (139, 69, 19): "Marrone",
    (160, 82, 45): "Marrone rossiccio",
    (245, 222, 179): "Beige",
    (210, 180, 140): "Marrone chiaro"
}

def nome_colore(rgb):
    def distanza(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))

    più_vicino = min(colori_nomi.keys(), key=lambda c: distanza(rgb, c))
    return colori_nomi[più_vicino]

class ColorPickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Picker Avanzato")

        self.img = None
        self.tk_img = None
        self.zoom = 10
        self.zoom_size = 100

        self.canvas = tk.Canvas(root, cursor="crosshair")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mostra_colore)
        self.canvas.bind("<Motion>", self.aggiorna_lente)

        self.btn = tk.Button(root, text="Carica Immagine", command=self.carica_immagine)
        self.btn.pack(pady=5)

        self.info = tk.Label(root, text="Clicca sull'immagine per ottenere il colore", font=("Arial", 14))
        self.info.pack(pady=5)

        self.lente_canvas = tk.Canvas(root, width=self.zoom_size, height=self.zoom_size)
        self.lente_canvas.pack(pady=10)

    def carica_immagine(self):
        path = filedialog.askopenfilename(filetypes=[("Immagini", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.img = Image.open(path).convert("RGB")
            self.tk_img = ImageTk.PhotoImage(self.img)
            self.canvas.config(width=self.img.width, height=self.img.height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def mostra_colore(self, event):
        if self.img:
            x, y = event.x, event.y
            if 0 <= x < self.img.width and 0 <= y < self.img.height:
                rgb = self.img.getpixel((x, y))
                hex_color = '#%02x%02x%02x' % rgb
                colore_nome = nome_colore(rgb)

                self.info.config(
                    text=f"{colore_nome} | RGB: {rgb} | HEX: {hex_color}",
                    bg=hex_color,
                    fg="white" if sum(rgb) < 400 else "black"
                )
                pyperclip.copy(hex_color)

                self.canvas.delete("marker")
                r = 5
                self.canvas.create_oval(x - r, y - r, x + r, y + r, outline="red", width=2, tags="marker")

    def aggiorna_lente(self, event):
        if self.img:
            x, y = event.x, event.y
            box = (x - 5, y - 5, x + 5, y + 5)
            zoom_area = self.img.crop(box).resize((self.zoom_size, self.zoom_size), Image.NEAREST)
            draw = ImageDraw.Draw(zoom_area)

            cx, cy = self.zoom_size // 2, self.zoom_size // 2
            draw.line((cx - 5, cy, cx + 5, cy), fill="red")
            draw.line((cx, cy - 5, cx, cy + 5), fill="red")

            tk_zoom = ImageTk.PhotoImage(zoom_area)
            self.lente_canvas.image = tk_zoom
            self.lente_canvas.create_image(0, 0, anchor="nw", image=tk_zoom)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorPickerApp(root)
    root.mainloop()
