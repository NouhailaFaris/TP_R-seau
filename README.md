# TP_R-seau

BMP280 Sensor Data Compensation
This section explains how to calculate the compensated temperature and pressure from the raw data provided by the BMP280 sensor, using its calibration coefficients.

Temperature Compensation
To calculate the compensated temperature, use the following procedure, which relies on the calibration coefficients dig_T1, dig_T2, and dig_T3 provided by the sensor. The formula computes the temperature in degrees Celsius (°C), multiplied by 100 for integer-based precision.

Code Example (C):
c
Copy code
int32_t t_fine;
int32_t var1, var2, T;

// raw_temp is the raw temperature reading from the sensor
var1 = ((((raw_temp >> 3) - ((int32_t)dig_T1 << 1))) * ((int32_t)dig_T2)) >> 11;
var2 = (((((raw_temp >> 4) - ((int32_t)dig_T1)) * ((raw_temp >> 4) - ((int32_t)dig_T1))) >> 12) * ((int32_t)dig_T3)) >> 14;
t_fine = var1 + var2;

T = (t_fine * 5 + 128) >> 8;
raw_temp: The raw temperature data read from the sensor.
t_fine: An intermediate variable used for both temperature and pressure compensation.
T: The compensated temperature in °C, multiplied by 100.
Result:
The compensated temperature T is returned as an integer representing the temperature in degrees Celsius multiplied by 100 (i.e., a result of 2015 means 20.15°C).

Pressure Compensation
To calculate the compensated pressure, use the variable t_fine (from the temperature calculation) and the calibration coefficients dig_P1, dig_P2, ..., dig_P9. The result is the pressure in Pascals (Pa).

Code Example (C):
c
Copy code
int64_t var1, var2, p;

// raw_press is the raw pressure reading from the sensor
var1 = ((int64_t)t_fine) - 128000;
var2 = var1 * var1 * (int64_t)dig_P6;
var2 = var2 + ((var1 * (int64_t)dig_P5) << 17);
var2 = var2 + (((int64_t)dig_P4) << 35);
var1 = ((var1 * var1 * (int64_t)dig_P3) >> 8) + ((var1 * (int64_t)dig_P2) << 12);
var1 = (((((int64_t)1) << 47) + var1)) * ((int64_t)dig_P1) >> 33;

if (var1 == 0) {
    return 0;  // Avoid division by zero
}

p = 1048576 - raw_press;
p = (((p << 31) - var2) * 3125) / var1;
var1 = (((int64_t)dig_P9) * (p >> 13) * (p >> 13)) >> 25;
var2 = (((int64_t)dig_P8) * p) >> 19;

p = ((p + var1 + var2) >> 8) + (((int64_t)dig_P7) << 4);
raw_press: The raw pressure data read from the sensor.
p: The compensated pressure in Pascals (Pa).
Result:
The pressure p is calculated in Pascals. To convert it to hectopascals (hPa), divide the result by 100 (i.e., 101325 Pa equals 1013.25 hPa).

This README section explains the procedure for reading and compensating the raw temperature and pressure data from the BMP280 sensor, ensuring accurate environmental measurements. For more details, consult the BMP280 datasheet.







You said:
non en laugague de readme 
ChatGPT said:
ChatGPT
Voici le texte structuré pour un fichier README dans le format attendu sur GitHub :

BMP280 Sensor Data Compensation
This section describes how to compute the compensated temperature and pressure from the raw data provided by the BMP280 sensor using the sensor's calibration coefficients.

Temperature Compensation
To calculate the compensated temperature, use the following formula which utilizes the calibration coefficients dig_T1, dig_T2, and dig_T3. The result gives the temperature in degrees Celsius, multiplied by 100 for precision.

Example (C):
c
Copy code
int32_t t_fine;
int32_t var1, var2, T;

// raw_temp is the raw temperature reading from the sensor
var1 = ((((raw_temp >> 3) - ((int32_t)dig_T1 << 1))) * ((int32_t)dig_T2)) >> 11;
var2 = (((((raw_temp >> 4) - ((int32_t)dig_T1)) * ((raw_temp >> 4) - ((int32_t)dig_T1))) >> 12) * ((int32_t)dig_T3)) >> 14;
t_fine = var1 + var2;

T = (t_fine * 5 + 128) >> 8;
raw_temp: Raw temperature data from the sensor.
t_fine: Intermediate variable used for both temperature and pressure calculations.
T: Compensated temperature in °C multiplied by 100.
Result:
The temperature T is in °C multiplied by 100 (e.g., a value of 2015 means 20.15°C).

Pressure Compensation
To compute the compensated pressure, use the t_fine value from the temperature calculation and the pressure calibration coefficients (dig_P1, dig_P2, etc.). The result is the pressure in Pascals (Pa).

Example (C):
c
Copy code
int64_t var1, var2, p;

// raw_press is the raw pressure reading from the sensor
var1 = ((int64_t)t_fine) - 128000;
var2 = var1 * var1 * (int64_t)dig_P6;
var2 = var2 + ((var1 * (int64_t)dig_P5) << 17);
var2 = var2 + (((int64_t)dig_P4) << 35);
var1 = ((var1 * var1 * (int64_t)dig_P3) >> 8) + ((var1 * (int64_t)dig_P2) << 12);
var1 = (((((int64_t)1) << 47) + var1)) * ((int64_t)dig_P1) >> 33;

if (var1 == 0) {
    return 0;  // Avoid division by zero
}

p = 1048576 - raw_press;
p = (((p << 31) - var2) * 3125) / var1;
var1 = (((int64_t)dig_P9) * (p >> 13) * (p >> 13)) >> 25;
var2 = (((int64_t)dig_P8) * p) >> 19;

p = ((p + var1 + var2) >> 8) + (((int64_t)dig_P7) << 4);
raw_press: Raw pressure data from the sensor.
p: Compensated pressure in Pascals (Pa).
Result:
The pressure p is in Pascals (Pa). To convert it to hectopascals (hPa), divide the result by 100 (e.g., 101325 Pa is 1013.25 hPa).

This section provides the method to read, compensate, and output accurate temperature and pressure values from the BMP280 sensor using the raw data and calibration coefficients. For more information, please refer to the BMP280 datasheet.







