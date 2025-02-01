import serial

try:
    ser = serial.Serial("COM3", baudrate=115200, timeout=5)
    print("Connexion série établie sur COM4 !")

    ser.write(b'Hello?\n')  # Envoi d'un message test
    response = ser.read(100)  # Lecture de la réponse

    print(f"Réponse reçue : {response}")

    ser.close()
except Exception as e:
    print(f"Erreur : {e}")
