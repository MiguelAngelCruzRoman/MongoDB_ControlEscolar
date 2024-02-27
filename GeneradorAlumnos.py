from faker import Faker
from pymongo import MongoClient
from datetime import datetime
import random

# Conexión a la base de datos
client = MongoClient('localhost', 27017)
db = client['controlEscolar']
collection = db['estudiantes']

# Crear instancia Faker
fake = Faker('es_MX')

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


collection_materias = db['materias']  # Nueva colección para materias
materias = list(collection_materias.find())



# Generar datos de prueba
data = []


for _ in range(100):  # Cambia esto al número deseado de registros
    materias_objetos = []
    materias_seleccionadas = random.sample(materias, k=random.randint(1, 5))

    for materia in materias_seleccionadas:
        materia_objeto = {
            'id': materia['_id'],
            'nombre': materia['nombre'],
            # Puedes agregar más detalles si los tienes en tus documentos de materias
        }
        materias_objetos.append(materia_objeto)

    estudiante = {
        'primerNombre': fake.first_name(),
        'segundoNombre': fake.first_name(),
        'apellidoPaterno': fake.last_name(),
        'apellidoMaterno': fake.last_name(),
        'sexo': fake.random_element(elements=('M', 'F')),
        'fechaNacimiento': fake.date_time_between(start_date='-70y', end_date='-30y'),
        'CURP': generar_curp(),
        'NSS': fake.unique.random_number(digits=11),
        'correoInstitucional': fake.unique.email(),
        'correoPersonal': fake.email(),
        'numeroContacto': fake.phone_number(),
        'fechaIngreso': fake.date_time_between(start_date='-4y', end_date='-1y'),
        'fechaEgreso': fake.date_time_between(start_date='now', end_date='+1y'),
        'estatus': fake.random_element(elements=('Regular', 'Irregular')),
        'materias': materias_objetos,
        'promedioGeneral': random.uniform(6.0, 10),
        'direccion': {
            'calle': fake.street_name(),
            'numero': fake.building_number(),
            'colonia': fake.word(),
            'ciudad': fake.city(),
            'estado': fake.state(),
            'codigoPostal': random.randint(10000, 99999),
            'pais': fake.country()
        }
    }
    data.append(estudiante)

# Insertar datos en la base de datos
collection.insert_many(data)

print("Datos insertados exitosamente.")
