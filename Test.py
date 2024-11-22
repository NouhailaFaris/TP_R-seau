from flask import Flask, jsonify
import serial
import time

# Configuration de l'interface série
SERIAL_PORT = '/dev/ttyAMA0'  # Port série (à adapter si nécessaire)
BAUD_RATE = 115200

# Initialisation de Flask
app = Flask(__name__)

# Fonction pour initialiser la connexion série
def init_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        if ser.is_open:
            print(f"Connexion série établie sur {SERIAL_PORT} à {BAUD_RATE} bps")
            return ser
        else:
            print("La connexion série n'a pas pu être établie.")
            return None
    except serial.SerialException as e:
        print(f"Erreur lors de la connexion série : {e}")
        return None

# Fonction pour envoyer une commande et récupérer la réponse
def send_command(ser, command):
    if ser and ser.is_open:
        ser.write((command + '\r\n').encode())  # Envoi de la commande avec un retour à la ligne
        time.sleep(0.1)  # Pause pour laisser la STM32 répondre
        response = ser.readline()  # Lecture de la réponse brute
        print(f"Données brutes reçues : {response}")
        try:
            decoded_response = response.decode().strip()  # Décodage de la réponse
            return decoded_response
        except UnicodeDecodeError:
            print(f"Erreur de décodage : {response}")
            return None
    else:
        print("Le port série n'est pas ouvert.")
        return None

# Route API pour obtenir la température
@app.route('/temperature', methods=['GET'])
def get_temperature():
    # Initialiser la connexion série
    ser = init_serial()
    if ser is None:
        return jsonify({'error': 'Impossible d\'établir une connexion série'}), 500

    # Envoyer la commande "GET_T" à la STM32
    temperature = send_command(ser, "GET_T")

    # Fermer la connexion série
    ser.close()

    # Vérifier si la température a été reçue
    if temperature:
        return jsonify({'temperature': temperature}), 200
    else:
        return jsonify({'error': 'Impossible de lire la température depuis la STM32'}), 500

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)