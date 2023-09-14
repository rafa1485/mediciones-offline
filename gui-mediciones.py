import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#import openpyxl
from openpyxl import Workbook
from datetime import datetime

# Función para añadir valores a la lista
def agregar_valores():
    temperatura1 = entrada_temp1.get()
    temperatura2 = entrada_temp2.get()
    hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    valores_listbox.insert(tk.END, f'{hora_actual}: Temp1={temperatura1}, Temp2={temperatura2}')
    valores.append((hora_actual, temperatura1, temperatura2))

# Función para guardar los valores en un archivo Excel
def guardar_valores():
    if not valores:
        messagebox.showinfo("Error", "La lista de valores está vacía.")
        return

    archivo_excel = "Valores Temperatura.xlsx"
    workbook = Workbook()
    sheet = workbook.active

    for fila in valores:
        sheet.append(fila)

    try:
        workbook.save(archivo_excel)
        messagebox.showinfo("Éxito", "Los valores se han guardado en el archivo 'Valores Temperatura.xlsx'.")
        valores_listbox.delete(0, tk.END)  # Limpiar la lista
        valores.clear()  # Vaciar la lista de valores
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar los valores: {str(e)}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Visualizador de Temperaturas")

frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiquetas y entradas para las temperaturas
ttk.Label(frame, text="Temperatura 1:").grid(column=0, row=0, padx=5, pady=5)
entrada_temp1 = ttk.Entry(frame)
entrada_temp1.grid(column=1, row=0, padx=5, pady=5)

ttk.Label(frame, text="Temperatura 2:").grid(column=0, row=1, padx=5, pady=5)
entrada_temp2 = ttk.Entry(frame)
entrada_temp2.grid(column=1, row=1, padx=5, pady=5)

# Botones para añadir y guardar valores
agregar_btn = ttk.Button(frame, text="Añadir Valores", command=agregar_valores)
agregar_btn.grid(column=0, row=2, columnspan=2, padx=5, pady=10)

guardar_btn = ttk.Button(frame, text="Guardar Valores", command=guardar_valores)
guardar_btn.grid(column=0, row=3, columnspan=2, padx=5, pady=10)

# Lista de valores
valores_listbox = tk.Listbox(frame, height=10, width=50)
valores_listbox.grid(column=2, row=0, rowspan=4, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))

valores = []

root.mainloop()
