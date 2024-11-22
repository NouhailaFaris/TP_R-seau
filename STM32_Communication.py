import serial
import time

# Initialisation de la connexion série
def init_serial(port='/dev/ttyAMA0', baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        if ser.is_open:
            print(f"Connexion série établie sur {port} à {baudrate} bps")
            return ser
        else:
            print("La connexion série n'a pas pu être établie.")
            return None
    except serial.SerialException as e:
        print(f"Erreur lors de la connexion série : {e}")
        return None

# Fonction pour envoyer une commande et lire la réponse
def send_command(ser, command):
    if ser and ser.is_open:
        ser.write((command + '\r\n').encode())  # Envoi de la commande avec un retour à la ligne
        time.sleep(0.1)  # Pause pour laisser le STM32 répondre
        try:
            response = ser.readline()  # Lire la réponse brute
            print(f"Données brutes reçues : {response}")
            decoded_response = response.decode().strip()  # Décodage de la réponse
            if decoded_response:
                print(f"Envoyé : {command} | Reçu : {decoded_response}")
            else:
                print(f"Envoyé : {command} | Aucune réponse reçue.")
            return decoded_response
        except UnicodeDecodeError:
            print(f"Envoyé : {command} | Erreur de décodage. Réponse brute : {response}")
            return None
    else:
        print("Le port série n'est pas ouvert.")
        return None

# Fonction pour obtenir la température
def get_temperature(ser):
    return send_command(ser, "GET_T")

# Fonction pour obtenir la pression
def get_pressure(ser):
    return send_command(ser, "GET_P")

# Fonction pour fermer la connexion série
def close_serial(ser):
    if ser and ser.is_open:
        ser.close()
        print("Connexion série fermée.")

# Exemple d'utilisation
if __name__ == "__main__":
    # Modifier le port selon votre configuration
    serial_port = init_serial(port='/dev/ttyAMA0', baudrate=115200)

    if serial_port:
        print("La connexion avec la STM32 est prête. Envoi des commandes...")
        
        # Lecture de la température
        print("Lecture de la température...")
        temperature = get_temperature(serial_port)
        
        # Lecture de la pression
        print("Lecture de la pression...")
        pressure = get_pressure(serial_port)

        # Fermer la connexion série
        close_serial(serial_port)
    else:
        print("Impossible d'établir une connexion avec la STM32.")
