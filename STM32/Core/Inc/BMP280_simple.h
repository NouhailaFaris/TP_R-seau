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

typedef uint32_t BMP280_U32_t;
typedef int32_t BMP280_S32_t;
typedef int64_t BMP280_S64_t;

// Adresse I2C du MPU9250
#define MPU9250_ADDR         0x68  // Adresse I2C par défaut du MPU-9250
#define MPU9250_WHO_AM_I     0x75  // Registre ID pour le MPU-9250
#define MPU9250_WHO_AM_I_VAL 0x71  // Valeur d'ID pour le MPU-9250
#define MPU9250_PWR_MGMT_1   0x6B  // Registre de gestion d'alimentation
#define MPU9250_ACCEL_XOUT_H 0x3B  // Premier registre de données pour les axes X, Y, Z de l'accéléromètre

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
BMP280_S32_t BMP280_get_pressure();
uint8_t* BMP280_Read_Reg(uint8_t reg, uint8_t value);
void BMP280_get_trimming();
int BMP280_Write_Reg(uint8_t reg, uint8_t value);
int MPU9250_check();
int MPU9250_init();
void MPU9250_read_acceleration(int16_t *x, int16_t *y, int16_t *z);
#endif // MPU9250_H
#endif /* SRC_BMP280_H_ */
