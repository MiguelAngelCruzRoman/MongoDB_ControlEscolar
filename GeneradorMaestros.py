from faker import Faker
from pymongo import MongoClient
from datetime import datetime
import random

# Conexión a la base de datos
client = MongoClient('localhost', 27017)
db = client['controlEscolar']
collection = db['maestros']

# Crear instancia Faker
fake = Faker('es_mx')

def generar_curp():
    # Letras para generar la CURP
    vocales = "AEIOU"
    consonantes = "BCDFGHJKLMNPQRSTVWXYZ"
    
    # Elegir aleatoriamente una letra de cada conjunto
    curp = random.choice(consonantes)
    curp += random.choice(vocales)
    curp += random.choice(consonantes)
    
    # Generar números aleatorios para la fecha de nacimiento
    curp += str(random.randint(0, 9))  # Año (última cifra)
    curp += str(random.randint(0, 1))  # Mes
    curp += str(random.randint(0, 3))  # Día
    
    # Letras aleatorias para el estado
    curp += random.choice(consonantes)
    curp += random.choice(consonantes)
    
    # Letra aleatoria para el sexo
    curp += random.choice(["H", "M"])
    
    # Últimos 2 dígitos aleatorios
    curp += str(random.randint(0, 9))
    curp += str(random.randint(0, 9))
    
    # Letra aleatoria para homoclave
    curp += random.choice(consonantes)
    
    return curp
# Generar datos de prueba
data = []
for _ in range(100):  # Cambia esto al número deseado de registros
    maestro = {
        'primerNombre': fake.first_name(),
        'segundoNombre': fake.first_name(),
        'apellidoPaterno': fake.last_name(),
        'apellidoMaterno': fake.last_name(),
        'sexo': fake.random_element(elements=('M', 'F')),
        'fechaNacimiento': fake.date_time_between(start_date='-70y', end_date='-30y'),
        'CURP': generar_curp(),
        'NSS': fake.unique.random_number(digits=11),
        'correoInstitucional': fake.unique.email(),
        'fechaInicioContrato': fake.date_time_between(start_date='-5y', end_date='now'),
        'fechaFinContrato': fake.date_time_between(start_date='now', end_date='+5y'),
        'estatus': fake.random_element(elements=('Activo', 'Inactivo')),
        'salario': fake.random_number(digits=5),
        'jornadaLaboral': fake.random_number(digits=2),
        'experiencia': fake.random_number(digits=1),
        'areaConocimiento': fake.random_element(elements=('Informática', 'Matemáticas', 'Física', 'Biología'))
    }
    data.append(maestro)

# Insertar datos en la base de datos
collection.insert_many(data)

print("Datos insertados exitosamente.")
