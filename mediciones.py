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



        

# Ejemplo de uso
if __name__ == "__main__":
    board = pyfirmata.Arduino('COM3')  # Reemplaza 'COM3' con el puerto del Arduino

    # Inicializar el protocolo Firmata
    it = pyfirmata.util.Iterator(board)
    it.start()

    # Configurar pines analógicos A0 y A1
    analog_pin_0 = board.get_pin('a:0:i')
    analog_pin_1 = board.get_pin('a:1:i')

    for i in range(4):
        time.sleep(1)
        valor_a0, valor_a1 = leer_valores_analogicos(analog_pin_0, analog_pin_1)
        if valor_a0 is not None and valor_a1 is not None:
            print(f"Valor analógico en A0: {valor_a0}")
            print(f"Valor analógico en A1: {valor_a1}")
        else:
            print("No se han devuelto valores.")
