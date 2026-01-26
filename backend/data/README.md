# Directorio de Datos

Coloca aquí tu archivo `car_prediction_data.csv` para entrenar el modelo.

## Formato Requerido

El archivo CSV debe contener las siguientes columnas:

| Columna       | Tipo   | Descripción                            | Ejemplo           |
| ------------- | ------ | -------------------------------------- | ----------------- |
| Year          | int    | Año de fabricación                     | 2015              |
| Present_Price | float  | Precio del modelo nuevo actual (miles) | 9.85              |
| Kms_Driven    | int    | Kilometraje del vehículo               | 6900              |
| Fuel_Type     | string | Tipo de combustible                    | Petrol/Diesel/CNG |
| Seller_Type   | string | Tipo de vendedor                       | Dealer/Individual |
| Transmission  | string | Tipo de transmisión                    | Manual/Automatic  |
| Owner         | int    | Número de dueños previos               | 0-3               |
| Selling_Price | float  | Precio de venta (objetivo)             | 8.5               |

## Ejemplo de CSV

```csv
Year,Present_Price,Kms_Driven,Fuel_Type,Seller_Type,Transmission,Owner,Selling_Price
2015,9.85,6900,Petrol,Dealer,Manual,0,8.50
2014,8.00,15000,Diesel,Individual,Manual,1,6.25
2016,12.50,8000,Petrol,Dealer,Automatic,0,11.00
```

## Notas

- Los precios están en miles de unidades monetarias
- El archivo debe estar codificado en UTF-8
- No debe contener valores nulos
- Los nombres de las columnas deben coincidir exactamente
