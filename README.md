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

![image](https://github.com/user-attachments/assets/1762f883-cabb-47ad-8956-99a91d7de897)

### Test de la chaîne de compilation et communication UART sur USB

 ![image](https://github.com/user-attachments/assets/2d6e6b36-20b6-44f5-a11b-88a4bfdd816c)

### Identification du BMP280

```c

 /* USER CODE BEGIN PD */ 

#define BMP280_I2C_ADDRESS 0x77 << 1 

#define BMP280_ID_REG 0xD0 

/* USER CODE END PD */ 

 

int main(void) 

{ 

 

/* USER CODE BEGIN 2 */ 

printf("=======demarage Systeme=======\r\n"); 

uint8_t reg = BMP280_ID_REG; 

uint8_t bmp280_id = 0; 

HAL_I2C_Master_Transmit(&hi2c1, BMP280_I2C_ADDRESS, &reg, 1, HAL_MAX_DELAY); //envoyer l'adresse du registre ID

HAL_I2C_Master_Receive(&hi2c1, BMP280_I2C_ADDRESS, &bmp280_id, 1, HAL_MAX_DELAY); //recevoir 1 octet correspondant au contenu du registre

printf("Id: 0x%x...", buf[0]);
	if (buf[0] == BMP280_ID_VAL) {
		printf("Ok\r\n");
		return 0;
	} else {
		printf("not Ok!\r\n");
		return 1;
	}

 

/* USER CODE END 2 */ 

}

```
** le contenu du registre correspond bien à la datasheet:

![image](https://github.com/user-attachments/assets/8f9a9f1e-26c8-4432-89ab-7fab195d8874)

** Vérifiez à l'oscilloscope que la formes des trames I²C est conforme:

### Configuration du BMP280

```c

/* USER CODE BEGIN PD */ 

#define BMP280_CTRL_MES_REG 0xF4 

/* USER CODE END PD */ 

 

int main(void) 

{ 

/* USER CODE BEGIN 2 */ 

printf("=======demarage Systeme=======\r\n"); 

uint8_t reg1 = BMP280_CTRL_MES_REG; 

uint8_t buf[2]; 

buf[1]=reg1; 

buf[2]=0x57; 

HAL_I2C_Master_Transmit(&hi2c1, BMP280_I2C_ADDRESS, buf, 2, HAL_MAX_DELAY); 

HAL_I2C_Master_Transmit(&hi2c1, BMP280_I2C_ADDRESS, &reg1, 1, HAL_MAX_DELAY); 

HAL_I2C_Master_Receive(&hi2c1, BMP280_I2C_ADDRESS, &bmp280_ctrl, 1, HAL_MAX_DELAY); 

printf("Valeur du registre de contrôle (0xF4) : 0x%02X\r\n", bmp280_ctrl);

```

 ![image](https://github.com/user-attachments/assets/f8de9a36-e626-463b-8ec6-9aaa9afbc1b2)

 # Récupération de l'étalonnage, de la température et de la pression

 ![image](https://github.com/user-attachments/assets/136f1959-bfd9-4d44-8567-f35044e979a9)
 
**Interfaçage de l'accléromètre**

![image](https://github.com/user-attachments/assets/bf406e71-3157-4ac5-8568-c7c07a1db3f0)


**BMP280_simple.h**
```c
/*
 * BMP280.h
 *
 *  Created on: Oct 3, 2020
 *      Author: cbares
 */

#ifndef SRC_BMP280_SIMPLE_H_
#define SRC_BMP280_SIMPLE_H_
#ifndef MPU9250_H
#define MPU9250_H

#define MPU9250_ADDR         0x68  // Adresse I2C par défaut du MPU-9250
#define MPU9250_WHO_AM_I     0x75  // Registre ID pour le MPU-9250
#define MPU9250_WHO_AM_I_VAL 0x71  // Valeur d'ID pour le MPU-9250
#define MPU9250_PWR_MGMT_1   0x6B  // Registre de gestion d'alimentation
#define MPU9250_ACCEL_XOUT_H 0x3B  // Premier registre de données pour les axes X, Y, Z de l'accéléromètre

typedef uint32_t BMP280_U32_t;
typedef int32_t BMP280_S32_t;
typedef int64_t BMP280_S64_t;

static const uint8_t BMP280_ADDR = 0x77 << 1; // Use 8-bit address
// static const uint8_t BMP280_ADDR = 0x76 << 1; // Use 8-bit address

static const uint8_t BMP280_ID_REG = 0xD0;
static const uint8_t BMP280_ID_LEN = 1;
static const uint8_t BMP280_ID_VAL = 0x58;

static const uint8_t BMP280_CTRL_MEAS_REG = 0xF4;

static const uint8_t BMP280_PRES_REG_MSB = 0xF7;
static const uint8_t BMP280_PRES_LEN = 3;

static const uint8_t BMP280_TEMP_REG_MSB = 0xFA;
static const uint8_t BMP280_TEMP_LEN = 3;

static const uint8_t BMP280_TRIM_REG_MSB = 0x88;
static const uint8_t BMP280_TRIM_LEN = 12 * 2;

//uint8_t temp_calib[3];
//uint8_t pres_calib[3];

int BMP280_check();
int BMP280_init();
BMP280_S32_t BMP280_get_temperature();
int BMP280_get_pressure();
uint8_t* BMP280_Read_Reg(uint8_t reg, uint8_t value);
int BMP280_Write_Reg(uint8_t reg, uint8_t value);
int MPU9250_check();
int MPU9250_init();
void MPU9250_read_acceleration(int16_t *x, int16_t *y, int16_t *z);

#endif // MPU9250_H

#endif /* SRC_BMP280_H_ */
```
**BMP280_simple.c**
```c
/*
 * BMP280.c
 *
 *  Created on: Oct 3, 2020
 *      Author: cbares
 */

#include "stdio.h"
#include "stdlib.h"

#include "main.h"
#include "BMP280_simple.h"

extern I2C_HandleTypeDef hi2c1;

uint16_t dig_T1;
int16_t dig_T2;
int16_t dig_T3;
uint16_t dig_P1;
int16_t dig_P2;
int16_t dig_P3;
int16_t dig_P4;
int16_t dig_P5;
int16_t dig_P6;
int16_t dig_P7;
int16_t dig_P8;
int16_t dig_P9;


BMP280_S32_t t_fine;


int MPU9250_check() {
    uint8_t buf[1];
    HAL_StatusTypeDef ret;

    buf[0] = MPU9250_WHO_AM_I;
    ret = HAL_I2C_Master_Transmit(&hi2c1, MPU9250_ADDR << 1, buf, 1, HAL_MAX_DELAY);
    if (ret != HAL_OK) {
        printf("Erreur I2C Transmit pour MPU-9250 Check\r\n");
        return 1;
    }

    ret = HAL_I2C_Master_Receive(&hi2c1, MPU9250_ADDR << 1, buf, 1, HAL_MAX_DELAY);
    if (ret != HAL_OK) {
        printf("Erreur I2C Receive pour MPU-9250 Check\r\n");
        return 1;
    }

    printf("MPU-9250 ID: 0x%x...", buf[0]);
    return (buf[0] == MPU9250_WHO_AM_I_VAL) ? 0 : 1;
}


int MPU9250_init() {
    uint8_t buf[2];
    HAL_StatusTypeDef ret;

    // Sortir de l'état de veille
    buf[0] = MPU9250_PWR_MGMT_1;
    buf[1] = 0x00;  // Clear sleep bit
    ret = HAL_I2C_Master_Transmit(&hi2c1, MPU9250_ADDR << 1, buf, 2, HAL_MAX_DELAY);
    if (ret != HAL_OK) {
        printf("Erreur configuration Power Management pour MPU-9250\r\n");
        return 1;
    }

    printf("Configuration MPU-9250 réussie\r\n");
    return 0;
}

void MPU9250_read_acceleration(int16_t *x, int16_t *y, int16_t *z) {
    uint8_t buf[6];
    HAL_StatusTypeDef ret;

    // Lecture des données d'accélération
    ret = HAL_I2C_Master_Transmit(&hi2c1, MPU9250_ADDR << 1, (uint8_t *)MPU9250_ACCEL_XOUT_H, 1, HAL_MAX_DELAY);
    if (ret != HAL_OK) {
        printf("Erreur I2C Transmit pour MPU-9250\r\n");
        return;
    }

    ret = HAL_I2C_Master_Receive(&hi2c1, MPU9250_ADDR << 1, buf, 6, HAL_MAX_DELAY);
    if (ret != HAL_OK) {
        printf("Erreur I2C Receive pour MPU-9250\r\n");
        return;
    }

    *x = (int16_t)((buf[0] << 8) | buf[1]);
    *y = (int16_t)((buf[2] << 8) | buf[3]);
    *z = (int16_t)((buf[4] << 8) | buf[5]);

    printf("Acceleration - X: %d, Y: %d, Z: %d\r\n", *x, *y, *z);
}

```
**main.c**
```c
// main.c
#include "main.h"
#include "MPU9250.h"
#include "stdio.h"

// Redirection du printf pour UART (si nécessaire)
int __io_putchar(int ch) {
    HAL_UART_Transmit(&huart2, (uint8_t*)&ch, 1, HAL_MAX_DELAY);
    return ch;
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_I2C1_Init();

    printf("Vérification du MPU-9250...\r\n");
    if (MPU9250_check() == 0) {
        printf("MPU-9250 détecté avec succès!\r\n");
    } else {
        printf("Erreur: MPU-9250 non détecté.\r\n");
        while (1);
    }

    if (MPU9250_init() == 0) {
        printf("Initialisation du MPU-9250 réussie.\r\n");
    } else {
        printf("Erreur d'initialisation du MPU-9250.\r\n");
        while (1);
    }

    int16_t accel_x, accel_y, accel_z;

    while (1) {
        MPU9250_read_acceleration(&accel_x, &accel_y, &accel_z);
        HAL_Delay(1000);
    }
}
```

 ## TP 2:
 
**Préparation du Raspberry**

 ![image](https://github.com/user-attachments/assets/94f776dd-35a3-4498-9f7a-2e10c8755ed6)

 ![image](https://github.com/user-attachments/assets/2697a3e5-2ef1-443b-a6ca-087e84e0d57e)

**Connexion SSH :**
![image](https://github.com/user-attachments/assets/06dd0bb4-5c9b-4916-a870-c02d4f86b695)

**installation minicom**
```
sudo apt update
sudo apt install minicom
```
**configuration minicom**
![image](https://github.com/user-attachments/assets/7440a819-35a6-43c9-8d32-0b3d0156ebb5)

**Test minicom**
![image](https://github.com/user-attachments/assets/f2a962d3-000d-4299-931e-9e45f2eff4c5)

## Communication avec la STM32:

```c
/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2024 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include <stdio.h>
#include <string.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/*#define BMP280_I2C_ADDRESS  0x77 << 1

#define BMP280_ID_REG       0xD0
#define BMP280_CTRL_MES_REG       0xF4
#define BMP280_calib25_REG       0xA1
#define BMP280_temp_msb_REG      0xFA
#define BMP280_temp_lsb_REG      0xFB
#define BMP280_temp_xlsb_REG     0xFC
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
CAN_HandleTypeDef hcan1;

UART_HandleTypeDef huart4;
UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
float temperature = 25.75;
int pression = 101325;
float coefficient_k = 1.234;
float angle = 125.7;
#define RX_BUFFER_SIZE 50
char rxBuffer[RX_BUFFER_SIZE];
char txBuffer[50];
int K_value = 1234;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_UART4_Init(void);
static void MX_CAN1_Init(void);
static void MX_USART2_UART_Init(void);
void handleCommand(char *command);

/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
    if (huart->Instance == USART2) { // Si le message vient du Raspberry Pi
    	 printf("commande recue");
    	handleCommand(rxBuffer); // Traite la commande reçue

        // Vide le buffer pour éviter des lectures résiduelles
        memset(rxBuffer, 0, RX_BUFFER_SIZE);

        // Relance la réception
        HAL_UART_Receive_IT(&huart2, (uint8_t *)rxBuffer, RX_BUFFER_SIZE);
    }
}

void handleCommand(char *command) {
    if (strncmp(command, "GET_T", 5) == 0) {
        snprintf(txBuffer, sizeof(txBuffer), "T=+%.2f_C\r\n", temperature);
    } else if (strncmp(command, "GET_P", 5) == 0) {
        snprintf(txBuffer, sizeof(txBuffer), "P=%dPa\r\n", pression);
    } else if (strncmp(command, "SET_K=", 6) == 0) {
        sscanf(command + 6, "%d", &K_value);
        snprintf(txBuffer, sizeof(txBuffer), "SET_K=OK\r\n");
    } else if (strncmp(command, "GET_K", 5) == 0) {
        snprintf(txBuffer, sizeof(txBuffer), "K=%d.%04d\r\n", K_value / 100, K_value % 100);
    } else if (strncmp(command, "GET_A", 5) == 0) {
        snprintf(txBuffer, sizeof(txBuffer), "A=%.4f\r\n", angle);
    } else {
        snprintf(txBuffer, sizeof(txBuffer), "Unknown Command\r\n");
    }
    HAL_UART_Transmit(&huart2, (uint8_t *)txBuffer, strlen(txBuffer), HAL_MAX_DELAY);
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */


  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_UART4_Init();
  MX_CAN1_Init();
  MX_USART2_UART_Init();
  /* USER CODE BEGIN 2 */
	printf("=======demarage Systeme=======\r\n");

	//uint8_t reg1 =BMP280_CTRL_MES_REG;
	//uint8_t reg1 =BMP280_calib25_REG;
	//uint8_t reg2[] = {BMP280_temp_msb_REG,BMP280_temp_lsb_REG,BMP280_temp_xlsb_REG};
	//uint8_t temp_data[3];  // Tableau pour stocker les 3 octets de température
	//uint32_t temp_raw = 0;
	//uint8_t buf[10];
	//buf[1]=reg1;
	//buf[2]=0x57;
	//HAL_I2C_Master_Transmit(&hi2c1, BMP280_I2C_ADDRESS, buf, 2, HAL_MAX_DELAY);
	//HAL_I2C_Master_Transmit(&hi2c1, BMP280_I2C_ADDRESS, &reg1, 1, HAL_MAX_DELAY);
	//HAL_I2C_Master_Receive(&hi2c1, BMP280_I2C_ADDRESS, &bmp280_ctrl, 1, HAL_MAX_DELAY);
	//Buffer de réception et transmission


	//printf("Valeur du registre de contrôle (0xF4) : 0x%02X\r\n", bmp280_ctrl);

	HAL_UART_Receive_IT(&huart2, (uint8_t *)rxBuffer, RX_BUFFER_SIZE);


  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	while (1)
	{
        // Réception des commandes

        HAL_UART_Receive_IT(&huart2, (uint8_t *)rxBuffer, RX_BUFFER_SIZE);
        // Traiter la commande reçue
        handleCommand(rxBuffer);

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */

	}
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief CAN1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_CAN1_Init(void)
{

  /* USER CODE BEGIN CAN1_Init 0 */

  /* USER CODE END CAN1_Init 0 */

  /* USER CODE BEGIN CAN1_Init 1 */

  /* USER CODE END CAN1_Init 1 */
  hcan1.Instance = CAN1;
  hcan1.Init.Prescaler = 6;
  hcan1.Init.Mode = CAN_MODE_NORMAL;
  hcan1.Init.SyncJumpWidth = CAN_SJW_1TQ;
  hcan1.Init.TimeSeg1 = CAN_BS1_11TQ;
  hcan1.Init.TimeSeg2 = CAN_BS2_2TQ;
  hcan1.Init.TimeTriggeredMode = DISABLE;
  hcan1.Init.AutoBusOff = DISABLE;
  hcan1.Init.AutoWakeUp = DISABLE;
  hcan1.Init.AutoRetransmission = DISABLE;
  hcan1.Init.ReceiveFifoLocked = DISABLE;
  hcan1.Init.TransmitFifoPriority = DISABLE;
  if (HAL_CAN_Init(&hcan1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN CAN1_Init 2 */

  /* USER CODE END CAN1_Init 2 */

}

/**
  * @brief UART4 Initialization Function
  * @param None
  * @retval None
  */
static void MX_UART4_Init(void)
{

  /* USER CODE BEGIN UART4_Init 0 */

  /* USER CODE END UART4_Init 0 */

  /* USER CODE BEGIN UART4_Init 1 */

  /* USER CODE END UART4_Init 1 */
  huart4.Instance = UART4;
  huart4.Init.BaudRate = 115200;
  huart4.Init.WordLength = UART_WORDLENGTH_8B;
  huart4.Init.StopBits = UART_STOPBITS_1;
  huart4.Init.Parity = UART_PARITY_NONE;
  huart4.Init.Mode = UART_MODE_TX_RX;
  huart4.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart4.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart4) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN UART4_Init 2 */

  /* USER CODE END UART4_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : PB6 PB7 */
  GPIO_InitStruct.Pin = GPIO_PIN_6|GPIO_PIN_7;
  GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  GPIO_InitStruct.Alternate = GPIO_AF4_I2C1;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */
	__disable_irq();
	while (1)
	{
	}
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
	/* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
```


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
**teste jsonify** 
![image](https://github.com/user-attachments/assets/807e1bbe-2fc0-4a34-a5d6-55079b35b375)

![image](https://github.com/user-attachments/assets/3f0a2248-1beb-4af9-9b46-cc1bd0b2e30d)

cette solution est meilleure puiqu'on Jsonify le python donc on retrouve que notre python est convertit on json 

### Erreur 404

```py
from flask import Flask, jsonify, abort

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
    if 0 <= index < len(welcome):
        return jsonify({"index": index, "val": welcome[index]})
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404
```

![image](https://github.com/user-attachments/assets/7e51c079-0691-45fa-8c86-e70f57b1fb7e)




***Méthode POST***
![WhatsApp Image 2024-10-25 at 11 46 03](https://github.com/user-attachments/assets/a661c525-4e84-4cdb-949f-746ede889136)

# Tp4
##  Configuration CAN


![image](https://github.com/user-attachments/assets/77538c80-8f19-4b30-8ace-854c0075aa64)
![image](https://github.com/user-attachments/assets/2e20b4c8-96e1-456b-a587-8ff39b89f5c7)
```c
/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * Copyright (c) 2024 STMicroelectronics.
 * All rights reserved.
 *
 * This software is licensed under terms that can be found in the LICENSE file
 * in the root directory of this software component.
 * If no LICENSE file comes with this software, it is provided AS-IS.
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
CAN_HandleTypeDef hcan1;

UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_CAN1_Init(void);
/* USER CODE BEGIN PFP */
void rotate_motor_90_degrees(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
int __io_putchar(int ch) {
	HAL_UART_Transmit(&huart2, (uint8_t *)&ch, 1, HAL_MAX_DELAY);
	return ch;
}

void rotate_motor_90_degrees(void) {
	CAN_TxHeaderTypeDef pHeader;
	uint8_t data[2];
	uint32_t pTxMailbox;

	// Configure CAN header for angle control
	pHeader.StdId = 0x61;
	pHeader.IDE = CAN_ID_STD;
	pHeader.RTR = CAN_RTR_DATA;
	pHeader.DLC = 2;  // Set to 2 because only 2 bytes are used

	// Rotate 90° clockwise
	data[0] = 90;  // D0: Angle
	data[1] = 0x00;  // D1: Direction (0 for clockwise)

	if (HAL_CAN_AddTxMessage(&hcan1, &pHeader, data, &pTxMailbox) != HAL_OK) {
		Error_Handler();
	}
	HAL_Delay(1000);  // Wait for motor to reach position

	// Rotate 90° counterclockwise
	data[1] = 0x01;  // D1: Direction (1 for counterclockwise)
	if (HAL_CAN_AddTxMessage(&hcan1, &pHeader, data, &pTxMailbox) != HAL_OK) {
		Error_Handler();
	}
	HAL_Delay(1000);  // Wait for motor to reach position
}
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_CAN1_Init();
  /* USER CODE BEGIN 2 */
	HAL_CAN_Start(&hcan1);
	printf("Starting motor control\r\n");
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	while (1) {
		printf("Rotating motor 90 degrees\r\n");
		rotate_motor_90_degrees();
		printf("Motor rotation complete.\r\n");
		HAL_Delay(1000);  // Add a delay between rotations
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	}
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 2;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief CAN1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_CAN1_Init(void)
{

  /* USER CODE BEGIN CAN1_Init 0 */

  /* USER CODE END CAN1_Init 0 */

  /* USER CODE BEGIN CAN1_Init 1 */

  /* USER CODE END CAN1_Init 1 */
  hcan1.Instance = CAN1;
  hcan1.Init.Prescaler = 6;
  hcan1.Init.Mode = CAN_MODE_NORMAL;
  hcan1.Init.SyncJumpWidth = CAN_SJW_1TQ;
  hcan1.Init.TimeSeg1 = CAN_BS1_11TQ;
  hcan1.Init.TimeSeg2 = CAN_BS2_2TQ;
  hcan1.Init.TimeTriggeredMode = DISABLE;
  hcan1.Init.AutoBusOff = DISABLE;
  hcan1.Init.AutoWakeUp = DISABLE;
  hcan1.Init.AutoRetransmission = DISABLE;
  hcan1.Init.ReceiveFifoLocked = DISABLE;
  hcan1.Init.TransmitFifoPriority = DISABLE;
  if (HAL_CAN_Init(&hcan1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN CAN1_Init 2 */

  /* USER CODE END CAN1_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pin : LD2_Pin */
  GPIO_InitStruct.Pin = LD2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LD2_GPIO_Port, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
	/* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
```
![image](https://github.com/user-attachments/assets/3296caf0-9704-4a29-a0b3-8d420b9e9e24)

