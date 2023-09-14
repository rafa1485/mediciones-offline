#from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#import openpyxl
from openpyxl import Workbook
from datetime import datetime

import pyfirmata
import time

def leer_valores_analogicos(analog_pin_0, analog_pin_1):

    contador_nones = 0

    while True:
        # Leer los valores analógicos
        valor_analogico_0 = analog_pin_0.read()
        valor_analogico_1 = analog_pin_1.read()

        if (valor_analogico_0 == None) or (valor_analogico_1 == None):
            contador_nones += 1
            print(contador_nones)
            time.sleep(1)
            continue
        else:

            return valor_analogico_0*5*100, valor_analogico_1*5*100

board = pyfirmata.Arduino('COM3')  # Reemplaza 'COM3' con el puerto del Arduino

# Inicializar el protocolo Firmata
it = pyfirmata.util.Iterator(board)
it.start()

# Configurar pines analógicos A0 y A1
analog_pin_0 = board.get_pin('a:0:i')
analog_pin_1 = board.get_pin('a:1:i')



# Función para añadir valores a la lista
def agregar_valores():
    time.sleep(1)
    valor_a0, valor_a1 = leer_valores_analogicos(analog_pin_0, analog_pin_1)
    temperatura1 = valor_a0
    entrada_temp1.config(text= str(temperatura1))
    #entrada_temp1.get()
    temperatura2 = valor_a1
    entrada_temp2.config(text= str(temperatura2))
    #entrada_temp2.get()
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
#entrada_temp1 = ttk.Entry(frame)
entrada_temp1 = ttk.Label(frame, text='0')
entrada_temp1.grid(column=1, row=0, padx=5, pady=5)

ttk.Label(frame, text="Temperatura 2:").grid(column=0, row=1, padx=5, pady=5)
entrada_temp2 = ttk.Label(frame, text='0') #ttk.Entry(frame)
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
