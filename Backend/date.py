from datetime import datetime

# Lista de fechas formateadas en "Y/m/d H:M:S"
fechas_formateadas = [
    "2023/03/15 10:30:00",
    "2023/02/22 08:45:00",
    "2023/04/10 14:15:00"
]

# Ordena las fechas
fechas_formateadas.sort()

# Resultado
for fecha in fechas_formateadas:
    print(fecha)