import tkinter
import customtkinter
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import sys

# --- Configuración de la Apariencia ---
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# --- Constantes y Rutas ---
try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

LOGOS_PREDEFINIDOS = {
    "Disei SRL": os.path.join(base_path, "logo_empresa1.png"),
    "Conelci SRL": os.path.join(base_path, "logo_empresa2.png"),
    "UT Disei Conelci": os.path.join(base_path, "logo_empresa3.png"),
}

RUTA_FUENTE_BOLD = os.path.join(base_path, "Montserrat-Bold.ttf")
RUTA_FUENTE_MEDIUM = os.path.join(base_path, "Montserrat-Medium.ttf")
RUTA_FUENTE_REGULAR = os.path.join(base_path, "Montserrat-Regular.ttf")
ICONOS = { "telefono": os.path.join(base_path, "phone_icon.png"), "email": os.path.join(base_path, "email_icon.png"), "web": os.path.join(base_path, "web_icon.png"), "direccion": os.path.join(base_path, "location_icon.png") }

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Generador de Firmas")
        self.geometry("1000x550")
        self.resizable(False, False)

        self.ruta_logo_personalizado = ""
        self.preview_update_job = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        controls_frame = customtkinter.CTkFrame(self, corner_radius=10)
        controls_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        preview_frame = customtkinter.CTkFrame(self, corner_radius=10)
        preview_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        preview_frame.grid_propagate(False) # ## CORRECCIÓN 1: FIJAR TAMAÑO DEL PANEL ##
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        customtkinter.CTkLabel(controls_frame, text="Configuración de la Firma", font=("", 16, "bold")).pack(pady=(10, 15))

        logo_options = list(LOGOS_PREDEFINIDOS.keys()) + ["Seleccionar archivo..."]
        self.logo_selector = customtkinter.CTkComboBox(controls_frame, values=logo_options, command=self.on_logo_select)
        self.logo_selector.set(logo_options[0])
        self.logo_selector.pack(fill="x", padx=15, pady=5)
        
        self.entry_nombre = self.create_entry(controls_frame, "Nombre Completo")
        self.entry_puesto = self.create_entry(controls_frame, "Puesto de Trabajo")
        self.entry_telefono = self.create_entry(controls_frame, "Teléfono (ej: 549264...)")
        self.entry_email = self.create_entry(controls_frame, "Correo Electrónico")
        self.entry_web = self.create_entry(controls_frame, "Página Web", "disei.com.ar")
        self.entry_direccion = self.create_entry(controls_frame, "Dirección", "Corrientes 1060 Este...")

        self.btn_generar = customtkinter.CTkButton(controls_frame, text="Generar Firma", command=self.save_final_signature, height=40, font=("", 14, "bold"))
        self.btn_generar.pack(fill="x", padx=15, pady=(20, 10))

        self.preview_label = customtkinter.CTkLabel(preview_frame, text="La vista previa aparecerá aquí", text_color="gray")
        self.preview_label.grid(row=0, column=0, sticky="nsew")
        self.preview_image_object = None

        self.schedule_preview_update()

    def create_entry(self, parent, placeholder, default_text=None):
        entry = customtkinter.CTkEntry(parent, placeholder_text=placeholder)
        if default_text:
            entry.insert(0, default_text)
        entry.pack(fill="x", padx=15, pady=5)
        entry.bind("<KeyRelease>", self.schedule_preview_update)
        return entry

    def on_logo_select(self, choice):
        if choice == "Seleccionar archivo...":
            ruta = filedialog.askopenfilename(title="Selecciona un logo", filetypes=[("Archivos de imagen", "*.png *.jpg")])
            if ruta:
                self.ruta_logo_personalizado = ruta
                nombre_archivo = os.path.basename(ruta)
                self.logo_selector.configure(values=[nombre_archivo] + list(LOGOS_PREDEFINIDOS.keys()) + ["Seleccionar archivo..."])
                self.logo_selector.set(nombre_archivo)
            else:
                self.logo_selector.set(list(LOGOS_PREDEFINIDOS.keys())[0])
        else:
            self.ruta_logo_personalizado = ""
        self.schedule_preview_update()

    def schedule_preview_update(self, event=None):
        if self.preview_update_job:
            self.after_cancel(self.preview_update_job)
        self.preview_update_job = self.after(250, self.update_preview)

    def update_preview(self):
        """Genera la imagen de vista previa y la escala para que quepa perfectamente en su panel."""
        pil_image = self._create_signature_image(preview_mode=True)
        if not pil_image:
            self.preview_label.configure(image=None, text="La vista previa aparecerá aquí")
            return

        # ## CORRECCIÓN 2: LÓGICA DE ESCALADO MEJORADA ##
        container_width = self.preview_label.winfo_width() - 20
        container_height = self.preview_label.winfo_height() - 20

        if container_width <= 0 or container_height <= 0:
            return

        img_width, img_height = pil_image.size
        
        width_ratio = container_width / img_width
        height_ratio = container_height / img_height
        scale_factor = min(width_ratio, height_ratio)

        preview_width = int(img_width * scale_factor)
        preview_height = int(img_height * scale_factor)
        
        ctk_image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(preview_width, preview_height))
        
        self.preview_label.configure(image=ctk_image, text="")
        self.preview_image_object = ctk_image

    def save_final_signature(self):
        final_image = self._create_signature_image(preview_mode=False)
        if not final_image:
            messagebox.showerror("Error", "No se pudo generar la firma.")
            return

        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")], title="Guardar firma como...")
        if ruta_guardado:
            if ruta_guardado.lower().endswith(('.jpg', '.jpeg')):
                final_image = final_image.convert('RGB')
            final_image.save(ruta_guardado)
            messagebox.showinfo("Éxito", f"Firma guardada correctamente en:\n{ruta_guardado}")

    def _create_signature_image(self, preview_mode=False):
        nombre = self.entry_nombre.get()
        puesto = self.entry_puesto.get()
        telefono = self.entry_telefono.get()
        email = self.entry_email.get()
        web = self.entry_web.get()
        direccion = self.entry_direccion.get()

        if not nombre and not puesto:
            return None

        scale = 0.5 if preview_mode else 1.0

        ancho_firma = int(800 * scale)
        alto_firma = int(300 * scale)
        firma = Image.new('RGBA', (ancho_firma, alto_firma), (255, 255, 255, 255))
        draw = ImageDraw.Draw(firma)

        try:
            font_nombre = ImageFont.truetype(RUTA_FUENTE_BOLD, int(30 * scale))
            font_puesto = ImageFont.truetype(RUTA_FUENTE_MEDIUM, int(22 * scale))
            font_contacto = ImageFont.truetype(RUTA_FUENTE_REGULAR, int(17 * scale))
        except IOError:
            return None

        selected_logo_name = self.logo_selector.get()
        if selected_logo_name in LOGOS_PREDEFINIDOS:
            ruta_logo_a_usar = LOGOS_PREDEFINIDOS[selected_logo_name]
        elif self.ruta_logo_personalizado:
            ruta_logo_a_usar = self.ruta_logo_personalizado
        else:
            ruta_logo_a_usar = list(LOGOS_PREDEFINIDOS.values())[0]

        try:
            logo = Image.open(ruta_logo_a_usar)
            logo.thumbnail((int(250 * scale), int(250 * scale)), Image.Resampling.LANCZOS)
            firma.paste(logo, (int(50 * scale), (alto_firma - logo.height) // 2), logo)
        except Exception:
            error_box_size = int(100 * scale)
            draw.rectangle([(int(50*scale), (alto_firma - error_box_size)//2), (int(50*scale)+error_box_size, (alto_firma + error_box_size)//2)], fill="red")
            
        x_linea = int(320 * scale)
        draw.line([(x_linea, int(40*scale)), (x_linea, alto_firma - int(40*scale))], fill=(77,77,77), width=int(2*scale) if scale > 0.5 else 1)
        
        x_texto = x_linea + int(30 * scale)
        y_actual = int(60 * scale)
        
        draw.text((x_texto, y_actual), nombre, font=font_nombre, fill=(77,77,77))
        y_actual += int(40 * scale)
        draw.text((x_texto, y_actual), puesto, font=font_puesto, fill=(102,102,102))
        y_actual += int(45 * scale)

        tamano_icono = (int(20 * scale), int(20 * scale))
        espacio_icono_texto = int(10 * scale)
        interlineado = int(28 * scale)
        
        info_contacto = [(ICONOS["telefono"], f"+{telefono}" if telefono else ""),(ICONOS["email"], email),(ICONOS["web"], web),(ICONOS["direccion"], direccion)]
        
        for ruta_icono, texto in info_contacto:
            if not texto: continue
            icono_original = self.colorear_icono(ruta_icono, (50, 59, 130))
            if icono_original:
                icono_original.thumbnail(tamano_icono, Image.Resampling.LANCZOS)
                line_bbox = font_contacto.getbbox("Ay")
                line_height = line_bbox[3] - line_bbox[1]
                pos_y_icono = y_actual + line_bbox[1] + (line_height - icono_original.height) // 2
                firma.paste(icono_original, (x_texto, pos_y_icono), icono_original)

            draw.text((x_texto + tamano_icono[0] + espacio_icono_texto, y_actual), texto, font=font_contacto, fill=(77,77,77))
            y_actual += interlineado

        bbox = firma.getbbox()
        if bbox:
            firma = firma.crop(bbox)
            firma = ImageOps.expand(firma, border=int(20 * scale), fill=(255, 255, 255, 255))

        return firma

    def colorear_icono(self, ruta_icono, color):
        try:
            icono = Image.open(ruta_icono).convert("RGBA")
            capa_color = Image.new("RGBA", icono.size, color)
            return Image.composite(capa_color, Image.new("RGBA", icono.size, (0,0,0,0)), icono)
        except FileNotFoundError:
            return None

if __name__ == "__main__":
    app = App()
    app.mainloop()