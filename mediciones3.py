import pyfirmata2
import time

def conexion():
    
    board = pyfirmata2.Arduino('COM3')  # Reemplaza 'COM3' con el puerto del Arduino
    board.samplingOn(100)

    # Configurar pines analógicos A0 y A1
    board.analog[0].enable_reporting()
    board.analog[1].enable_reporting()

    # Leer los valores analógicos
    while True:
        valor_analogico_0 = board.analog[0].read()
        valor_analogico_1 = board.analog[1].read()
        if (valor_analogico_0 == None) or (valor_analogico_1 == None):
            time.sleep(1)
            continue
        else:
            #print(f'{valor_analogico_0*5*100}, {valor_analogico_1*5*100}')
            board.samplingOff()
            board.exit()
            return valor_analogico_0*5*100, valor_analogico_1*5*100
        
    

        

# Ejemplo de uso
if __name__ == "__main__":
    for i in range(10):
        print(conexion())