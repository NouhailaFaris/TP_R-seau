# TP_R-seau

## Objectif de TP:
 mettre en place l'ensemble des composants suivant:
 ![image](https://github.com/user-attachments/assets/7d0f6780-9d64-4791-b3f1-35c563478f4d)



 ## TP 1:
**mettre en place la communication entre le microcontrôleur et les capteurs (température, pression, accéléromètre...) via  le bus I²C.**

### Capteur BMP280 :

1.les adresses I²C possibles pour ce composant:

2.le registre et la valeur permettant d'identifier ce composant: l'adresse 0xD0 , la valeur est 0x58.

3.le registre et la valeur permettant de placer le composant en mode normal:Le registre ctrl_meas à l'adresse 0xF4. Les bits doivent être à 11 ==>Mode normale.

4.les registres contenant l'étalonnage du composant:Les données d'étalonnage se trouvent dans les registres calib00 à calib25, de l'adresse 0x88 à 0xA1.

5.les registres contenant la température (ainsi que le format):
- temp_msb à l'adresse 0xFA (bits 15-8)
- temp_lsb à l'adresse 0xFB (bits 7-0)
- temp_xlsb à l'adresse 0xFC (bits 7-4)

6.les registres contenant la pression (ainsi que le format):
-press_msb à l'adresse 0xF7 (bits 15-8)
-press_lsb à l'adresse 0xF8 (bits 7-0)
-press_xlsb à l'adresse 0xF9 (bits 7-4)

7.les fonctions permettant le calcul de la température et de la pression compensées, en format entier 32 bits:













