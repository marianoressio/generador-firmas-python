# Generador de Firmas Corporativas - Disei & Conelci

> Una herramienta interna diseñada para estandarizar y unificar las firmas de correo electrónico de los empleados de **Disei SRL** y **Conelci SRL**.

## Propósito del Proyecto

Este software fue creado con el objetivo de **unificar la imagen de marca** en todas las comunicaciones por correo electrónico. Al utilizar esta herramienta, aseguramos que todos los empleados presenten una firma profesional, consistente y alineada con la identidad visual de nuestras empresas.

## ✨ Características Principales

- **Interfaz Sencilla y Moderna:** Un diseño intuitivo para que cualquier usuario pueda generar su firma en segundos.
- **Logos Predefinidos:** Incluye los logos oficiales de **Disei SRL** y **Conelci SRL** para una selección rápida, además de la opción de subir un logo personalizado si es necesario.
- **Vista Previa en Tiempo Real:** Visualiza exactamente cómo quedará tu firma mientras completas tus datos.
- **Consistencia Garantizada:** Utiliza las fuentes, colores y formatos corporativos aprobados.
- **Fácil Exportación:** Guarda la firma final como una imagen (PNG/JPG) lista para ser usada en tu cliente de correo.

## 🚀 Instrucciones de Uso para Empleados

Sigue estos tres sencillos pasos para generar e instalar tu nueva firma de correo.

### 1. Descargar el Programa

- Ve a la sección de **[Releases]https://github.com/marianoressio/generador-firmas-python/releases/tag/v1.0** de este repositorio.
- Descarga el archivo `GeneradorDeFirmas.zip` que corresponde a la última versión.

### 2. Generar tu Firma

- Descomprime el archivo `.zip` en un lugar de tu computadora (como el Escritorio).
- Haz doble clic para ejecutar el programa `GeneradorDeFirmas.exe`. No necesita instalación.
- En la aplicación:
  1.  **Selecciona el logo** de tu empresa (Disei o Conelci) en el menú desplegable.
  2.  **Completa tus datos** en los campos correspondientes (Nombre, Puesto, etc.).
  3.  Verás cómo la **vista previa** se actualiza al instante.
  4.  Cuando estés conforme, haz clic en el botón **"Generar y Guardar Firma Final"**.
  5.  Guarda la imagen en un lugar que recuerdes fácilmente.

### 3. Configurar la Firma en tu Correo

Ahora que tienes la imagen, solo falta añadirla a tu programa de correo.

**Para Microsoft Outlook:**

1.  En Outlook, ve a `Archivo` > `Opciones` > `Correo` > `Firmas...`.
2.  Crea una `Nueva` firma o edita una existente.
3.  En el cuadro de edición, haz clic en el icono de **"Insertar imagen"** (parece un cuadro con montañas).
4.  Selecciona el archivo de imagen de la firma que acabas de guardar.
5.  ¡Listo! Asegúrate de asignarla para "Mensajes nuevos" y/o "Respuestas/reenvíos".

**Para Gmail:**

1.  En Gmail, ve a `Configuración` (el icono del engranaje) > `Ver todos los ajustes`.
2.  En la pestaña `General`, baja hasta la sección de `Firma`.
3.  Crea una `Nueva` firma o edita una existente.
4.  En la barra de herramientas, haz clic en el icono de **"Insertar imagen"**.
5.  Sube el archivo de imagen de la firma que guardaste.
6.  Guarda los cambios al final de la página.

---

## 🔧 Para Desarrollo y Mantenimiento

Esta sección está destinada a los desarrolladores que necesiten modificar o mantener el código fuente.

### Ejecutar el Código Fuente

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/marianoressio/generador-firmas-python
    cd nombre-del-repositorio
    ```
2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecuta la aplicación:**
    ```bash
    python generador_firmas.py
    ```

### Compilar el Ejecutable (.exe)

Para empaquetar la aplicación en un único archivo ejecutable, utiliza el siguiente comando de PyInstaller desde la raíz del proyecto:

```bash
pyinstaller --onefile --windowed --name "GeneradorDeFirmas" --add-data "Montserrat-Bold.ttf;." --add-data "Montserrat-Medium.ttf;." --add-data "Montserrat-Regular.ttf;." --add-data "phone_icon.png;." --add-data "email_icon.png;." --add-data "web_icon.png;." --add-data "location_icon.png;." --add-data "logo_empresa1.png;." --add-data "logo_empresa2.png;." --add-data "logo_empresa3.png;." generador_firmas.py
```
