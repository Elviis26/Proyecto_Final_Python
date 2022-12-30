from datetime import date

def calcular_edad_agnios(fecha_nacimiento):
    fecha_actual = date.today()
    resultado = fecha_actual.year - fecha_nacimiento.year
    resultado -= ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return resultado

fecha_nacimiento_turing = date(2020,6,23)
edad = calcular_edad_agnios(fecha_nacimiento_turing)

print(f'La edad es de {edad} años.')

if (edad>18):
    print("ES MAYOR DE EDAD")

else :
    print("ES MENOR DE EDAD")