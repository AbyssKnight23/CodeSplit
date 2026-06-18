import tkinter as tk
from tkinter import filedialog, messagebox
from file_detector import file_detector
from pe_analyzer import detectar_bits
from pe_sections import obtener_text_section
from linux_analyzer import detectar_bits_linux
from linux_sections import obtener_text_section_linux
from disassembler32 import desensamblar32
from disassembler64 import desensamblar64
from linux_analyzer import detectar_bits_linux
from linux_sections import obtener_text_section_linux
import os

# ---------- VARIABLES ----------
data = b''
archivo_valido = False
MAX_BYTES = 512

# ---------- COLORES ----------
BG = "#1e1e1e"
PANEL = "#252526"
TEXT = "#d4d4d4"
ACCENT = "#569cd6"

# ---------- MESSAGEBOX PERSONALIZADO ----------
def messagebox_color(titulo, mensaje, bg=BG, fg=TEXT, accent=ACCENT):
    win = tk.Toplevel()
    win.title(titulo)
    win.configure(bg=bg)
    win.resizable(False, False)

    # --- Posicionar a la derecha de la ventana principal ---
    root.update_idletasks()
    x = root.winfo_x() + root.winfo_width() + 10   # 10 px de separación
    y = root.winfo_y()
    win.geometry(f"+{x}+{y}")

    frame = tk.Frame(win, bg=PANEL, padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text=mensaje,
        bg=PANEL,
        fg=fg,
        font=("Consolas", 11),
        justify="left"
    ).pack(pady=(0, 10))

    win.grab_set()


# ---------- FUNCIONES ----------

def desensamblar_auto(data):

    if data[0:4] == b'\x7fELF':

        bits = detectar_bits_linux(data)

    else:

        bits = detectar_bits(data)

    if "64" in bits:
        return desensamblar64(data)

    else:
        return desensamblar32(data)


def dividir_hex_ascii(data):
    hex_result = ""
    ascii_result = ""

    for i in range(0, len(data), 16):
        linea = data[i:i+16]

        hex_line = f"{i:08X}  "
        for byte in linea:
            hex_line += f"{byte:02X} "
        hex_result += hex_line + "\n"

        ascii_line = ""
        for byte in linea:
            if 32 <= byte <= 126:
                ascii_line += chr(byte)
            else:
                ascii_line += "."
        ascii_result += ascii_line + "\n"

    return hex_result, ascii_result


def cargar_archivo():

    global data
    global archivo_valido

    ruta = filedialog.askopenfilename()

    if ruta:

        with open(ruta, "rb") as f:
            data = f.read()
            # Limpiar siempre al cargar un archivo nuevo
            hex_text.delete("1.0", tk.END)
            ascii_text.delete("1.0", tk.END)
            dis_text.delete("1.0", tk.END)

        nombre = os.path.basename(ruta)

        resultado = file_detector(data)

        if data[0:2] == b'MZ':

            bits = detectar_bits(data)
            archivo_valido = True

        elif data[0:4] == b'\x7fELF':

            bits = detectar_bits_linux(data)
            archivo_valido = True

        else:

            bits = "Formato no soportado"
            archivo_valido = False

        status_label.config(
            text=f"{nombre} | {resultado} | {bits}"
        )

        if not archivo_valido:

            hex_text.delete("1.0", tk.END)
            ascii_text.delete("1.0", tk.END)
            dis_text.delete("1.0", tk.END)

            dis_text.insert(
                tk.END,
                "ERROR\n\nFormato no soportado.\n\nSolo se permiten archivos EXE (PE) y ELF."
            )
        return

        fragmento = data[:MAX_BYTES]

        hex_text.delete("1.0", tk.END)
        ascii_text.delete("1.0", tk.END)
        dis_text.delete("1.0", tk.END)

        hex_part, ascii_part = dividir_hex_ascii(fragmento)

        hex_text.insert(tk.END, hex_part)
        ascii_text.insert(tk.END, ascii_part)


def mostrar_texto():

    if not archivo_valido:

        hex_text.delete("1.0", tk.END)
        ascii_text.delete("1.0", tk.END)
        dis_text.delete("1.0", tk.END)

        dis_text.insert(
            tk.END,
            "Error: archivo no válido. Solo se permiten EXE y ELF."
        )
        return

    if data[0:2] == b'MZ':

        texto = obtener_text_section(data)

    elif data[0:4] == b'\x7fELF':

        texto = obtener_text_section_linux(data)

    else:

        texto = None

    hex_text.delete("1.0", tk.END)
    ascii_text.delete("1.0", tk.END)
    dis_text.delete("1.0", tk.END)

    if texto:

        fragmento = texto[:MAX_BYTES]

        hex_part, ascii_part = dividir_hex_ascii(
            fragmento
        )

        hex_text.insert(tk.END, hex_part)
        ascii_text.insert(tk.END, ascii_part)

        dis_text.insert(
            tk.END,
            desensamblar_auto(fragmento)
        )

    else:

        dis_text.insert(
            tk.END,
            "No se encontró la sección .text"
        )


def mostrar_header():

    if not archivo_valido:

        hex_text.delete("1.0", tk.END)
        ascii_text.delete("1.0", tk.END)
        dis_text.delete("1.0", tk.END)

        dis_text.insert(
            tk.END,
            "Error: archivo no válido. Solo se permiten EXE y ELF."
        )
        return

    fragmento = data[:MAX_BYTES]

    hex_text.delete("1.0", tk.END)
    ascii_text.delete("1.0", tk.END)
    dis_text.delete("1.0", tk.END)

    hex_part, ascii_part = dividir_hex_ascii(fragmento)

    hex_text.insert(tk.END, hex_part)
    ascii_text.insert(tk.END, ascii_part)

    dis_text.insert(
        tk.END,
        desensamblar_auto(fragmento)
    )


def mostrar_footer():

    if not archivo_valido:

        hex_text.delete("1.0", tk.END)
        ascii_text.delete("1.0", tk.END)
        dis_text.delete("1.0", tk.END)

        dis_text.insert(
            tk.END,
            "Error: archivo no válido. Solo se permiten EXE y ELF."
        )
        return

    fragmento = data[-MAX_BYTES:]

    hex_text.delete("1.0", tk.END)
    ascii_text.delete("1.0", tk.END)
    dis_text.delete("1.0", tk.END)

    hex_part, ascii_part = dividir_hex_ascii(fragmento)

    hex_text.insert(tk.END, hex_part)
    ascii_text.insert(tk.END, ascii_part)

    dis_text.insert(
        tk.END,
        desensamblar_auto(fragmento)
    )

def mostrar_info():
    messagebox_color(
        "Información",
        "Desensamblador\n\n"
        "Versión 1.0\n\n"
        "Desarrollado por:\n"
        "- José Antonio Rodríguez Ballesteros\n"
        "- Pablo José Feu Chamorro\n"
    )

# ---------- VENTANA ----------

root = tk.Tk()
root.title("Desensamblador")
root.geometry("1100x600")
root.configure(bg=BG)

# ---------- TOOLBAR ----------

toolbar = tk.Frame(root, bg=PANEL)
toolbar.pack(fill="x")

def crear_boton(texto, comando):
    return tk.Button(
        toolbar,
        text=texto,
        command=comando,
        bg=PANEL,
        fg=TEXT,
        activebackground=ACCENT,
        activeforeground="white",
        relief="flat",
        padx=10,
        pady=5
    )

crear_boton("📂 Abrir", cargar_archivo).pack(side="left", padx=5, pady=5)
crear_boton("📄 Header", mostrar_header).pack(side="left", padx=5)
crear_boton("💻 .text", mostrar_texto).pack(side="left", padx=5)
crear_boton("📦 Footer", mostrar_footer).pack(side="left", padx=5)
crear_boton("ℹ Info", mostrar_info).pack(side="right", padx=5)

# ---------- STATUS ----------
status_label = tk.Label(root, text="Sin archivo cargado",
                        bg=BG, fg="#aaaaaa", anchor="w")
status_label.pack(fill="x")

# ---------- PANEL PRINCIPAL ----------

main_paned = tk.PanedWindow(root, orient="vertical", bg=BG)
main_paned.pack(fill="both", expand=True)

# ---------- HEX PARTIDO ----------

top_paned = tk.PanedWindow(main_paned, orient="horizontal", bg=BG)

hex_frame = tk.Frame(top_paned, bg=BG)
tk.Label(hex_frame, text="HEX", bg=PANEL, fg=TEXT).pack(fill="x")
hex_text = tk.Text(hex_frame, bg=BG, fg="#9cdcfe", font=("Consolas", 10))
hex_text.pack(fill="both", expand=True)

ascii_frame = tk.Frame(top_paned, bg=BG)
tk.Label(ascii_frame, text="ASCII", bg=PANEL, fg=TEXT).pack(fill="x")
ascii_text = tk.Text(ascii_frame, bg=BG, fg="#dcdcaa", font=("Consolas", 10))
ascii_text.pack(fill="both", expand=True)

top_paned.add(hex_frame)
top_paned.add(ascii_frame)

# ---------- DESENSAMBLADO ----------

dis_frame = tk.Frame(main_paned, bg=BG)
tk.Label(dis_frame, text="DESENSAMBLADO", bg=PANEL, fg=TEXT).pack(fill="x")

dis_text = tk.Text(dis_frame, bg=BG, fg="#dcdcaa", font=("Consolas", 10))
dis_text.pack(fill="both", expand=True)

main_paned.add(top_paned)
main_paned.add(dis_frame)

# ---------- AJUSTE ----------
def ajustar():
    root.update_idletasks()
    main_paned.sash_place(0, 0, root.winfo_height() // 2)

root.after(100, ajustar)

# ---------- INICIO ----------
root.mainloop()
