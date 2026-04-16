import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
from datetime import datetime
import time
import pyfirmata2

valores = []

board = None
analog_pin_0 = None
analog_pin_1 = None

ultimo_a0 = None
ultimo_a1 = None


def callback_a0(valor):
    global ultimo_a0
    ultimo_a0 = valor * 5 * 100   # mismo cálculo que usabas


def callback_a1(valor):
    global ultimo_a1
    ultimo_a1 = valor * 5 * 100   # mismo cálculo que usabas


def inicializar_arduino():
    global board, analog_pin_0, analog_pin_1

    try:
        board = pyfirmata2.Arduino('COM11')

        analog_pin_0 = board.get_pin('a:0:i')
        analog_pin_1 = board.get_pin('a:1:i')

        analog_pin_0.register_callback(callback_a0)
        analog_pin_1.register_callback(callback_a1)

        analog_pin_0.enable_reporting()
        analog_pin_1.enable_reporting()

        board.samplingOn(100)

        estado_label.config(text="Arduino conectado en COM11")
        return True

    except Exception as e:
        estado_label.config(text="Error al conectar Arduino")
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo inicializar Arduino en COM11:\n{e}"
        )
        return False


def actualizar_pantalla():
    if ultimo_a0 is not None:
        entrada_temp1.config(text=f"{ultimo_a0:.2f}")
    if ultimo_a1 is not None:
        entrada_temp2.config(text=f"{ultimo_a1:.2f}")

    root.after(200, actualizar_pantalla)


def agregar_valores():
    if board is None:
        messagebox.showerror("Error", "Arduino no inicializado.")
        return

    if ultimo_a0 is None or ultimo_a1 is None:
        messagebox.showwarning(
            "Sin datos",
            "Todavía no llegaron lecturas del Arduino. Esperá un instante."
        )
        return

    temperatura1 = round(ultimo_a0, 2)
    temperatura2 = round(ultimo_a1, 2)

    hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    texto = f'{hora_actual}: Temp1={temperatura1}, Temp2={temperatura2}'
    valores_listbox.insert(tk.END, texto)
    valores.append((hora_actual, temperatura1, temperatura2))


def guardar_valores():
    if not valores:
        messagebox.showinfo("Error", "La lista de valores está vacía.")
        return

    archivo_excel = "Valores Temperatura.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Mediciones"

    sheet.append(["Fecha y hora", "Temperatura 1", "Temperatura 2"])

    for fila in valores:
        sheet.append(fila)

    try:
        workbook.save(archivo_excel)
        messagebox.showinfo(
            "Éxito",
            f"Los valores se han guardado en el archivo '{archivo_excel}'."
        )
        valores_listbox.delete(0, tk.END)
        valores.clear()
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar los valores: {str(e)}")


def cerrar_aplicacion():
    global board
    try:
        if board is not None:
            board.exit()
    except Exception:
        pass
    root.destroy()


# =========================
# GUI
# =========================
root = tk.Tk()
root.title("Visualizador de Temperaturas")
root.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Temperatura 1:").grid(column=0, row=0, padx=5, pady=5)
entrada_temp1 = ttk.Label(frame, text='0')
entrada_temp1.grid(column=1, row=0, padx=5, pady=5)

ttk.Label(frame, text="Temperatura 2:").grid(column=0, row=1, padx=5, pady=5)
entrada_temp2 = ttk.Label(frame, text='0')
entrada_temp2.grid(column=1, row=1, padx=5, pady=5)

agregar_btn = ttk.Button(frame, text="Añadir Valores", command=agregar_valores)
agregar_btn.grid(column=0, row=2, columnspan=2, padx=5, pady=10)

guardar_btn = ttk.Button(frame, text="Guardar Valores", command=guardar_valores)
guardar_btn.grid(column=0, row=3, columnspan=2, padx=5, pady=10)

estado_label = ttk.Label(frame, text="Inicializando...")
estado_label.grid(column=0, row=4, columnspan=2, padx=5, pady=5)

valores_listbox = tk.Listbox(frame, height=10, width=50)
valores_listbox.grid(column=2, row=0, rowspan=5, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

root.after(100, inicializar_arduino)
root.after(200, actualizar_pantalla)

root.mainloop()