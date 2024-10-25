# TP_R-seau

## Objectif de TP:
 mettre en place l'ensemble des composants suivant:
 ![image](https://github.com/user-attachments/assets/7d0f6780-9d64-4791-b3f1-35c563478f4d)



 ## TP 1:
**mettre en place la communication entre le microcontrôleur et les capteurs (température, pression, accéléromètre...) via  le bus I²C.**

### Capteur BMP280 :

1. les adresses I²C possibles pour ce composant:

2. le registre et la valeur permettant d'identifier ce composant: l'adresse 0xD0 , la valeur est 0x58.

3. le registre et la valeur permettant de placer le composant en mode normal:Le registre ctrl_meas à l'adresse 0xF4. Les bits doivent être à (11) ==>Mode normale.

4. les registres contenant l'étalonnage du composant:Les données d'étalonnage se trouvent dans les registres calib00 à calib25, de l'adresse 0x88 à 0xA1.

5. les registres contenant la température (ainsi que le format):
- temp_msb à l'adresse 0xFA (bits 15-8)
- temp_lsb à l'adresse 0xFB (bits 7-0)
- temp_xlsb à l'adresse 0xFC (bits 7-4)

6. les registres contenant la pression (ainsi que le format):
- press_msb à l'adresse 0xF7 (bits 15-8)
- press_lsb à l'adresse 0xF8 (bits 7-0)
- press_xlsb à l'adresse 0xF9 (bits 7-4)

7. les fonctions permettant le calcul de la température et de la pression compensées, en format entier 32 bits:



 ## TP 3:
 **Développement d'une interface REST sur le Raspberry**
 
### Installation :
1. Création d'un utilisateur avec droits d'administration et accès au port série
   
```c
sudo adduser nouhfari  # Remplacez XXX par le nom de votre utilisateur
sudo usermod -aG sudo nouhfari  # Ajoutez l'utilisateur au groupe sudo
sudo usermod -aG dialout nouhfari  # Donnez l'accès au port série (dialout)
```

2. Délogguez vous, puis relogguez vous en tant que nouhfari
   
```c
logout
ssh nouhfari@192.168.88.228
```

**fichier requirement.txt**

![image](https://github.com/user-attachments/assets/0e661ee0-9e57-47f6-a517-9a58d3ce1fb1)


### Premier fichier Web:

![image](https://github.com/user-attachments/assets/e88737cb-7fa9-4cff-96d1-d3b345701e84)

![image](https://github.com/user-attachments/assets/608c2056-3cbd-4b61-8d35-c533d10f2a03)

### Première route

**Rôle du décorateur @app.route**

Le décorateur @app.route est utilisé dans Flask pour associer une URL à une fonction. Chaque fois qu'un utilisateur accède à une URL correspondant à celle spécifiée par le décorateur, la fonction Python associée est exécutée.

**Rôle du fragment <int:index>**

Le fragment <int:index> dans l'URL permet à Flask de capturer un paramètre de type entier dans l'URL et de le passer à la fonction associée.

![image](https://github.com/user-attachments/assets/f4b414c0-6e15-47b0-83ca-4202d69a1bc6)

![image](https://github.com/user-attachments/assets/ad501736-66cf-45b2-9a8f-d851b8dcc8dd)

On determinant l'index on peut visualiser le caractére qui correspondant dans le tableau welcome  

**Definition JSON:**

En Python, json (JavaScript Object Notation) est un module standard utilisé pour encoder et décoder des données au format JSON, un format de texte léger pour l'échange de données. JSON est couramment utilisé pour transmettre des données entre un serveur et un client (par exemple, dans des APIs web) grâce à sa simplicité et à sa compatibilité avec de nombreux langages de programmation.

```py
from flask import Flask
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!\n'

welcome = "Welcome to 3ESE API!\n"

@app.route('/api/welcome/')
def api_welcome():
    return welcome

@app.route('/api/welcome/<int:index>')
def api_welcome_index(index):
    return json.dumps({"index": index, "val": welcome[index]})

```

![image](https://github.com/user-attachments/assets/e78eabd7-24c0-4d10-9f62-f0874ecf9f83)


On peut bien remarquer que le type n'est pas du JSON c'est du html

![image](https://github.com/user-attachments/assets/e0ae9f05-016d-420f-a792-6975e0b60355)

Ici on a du Json mais c'est nous qui ont forcer ce type avec cette solution

**2éme solution**

![image](https://github.com/user-attachments/assets/807e1bbe-2fc0-4a34-a5d6-55079b35b375)

![image](https://github.com/user-attachments/assets/3f0a2248-1beb-4af9-9b46-cc1bd0b2e30d)

cette solution est meilleure puiqu'on Jsonify le python donc on retrouve que notre python est convertit on json 





