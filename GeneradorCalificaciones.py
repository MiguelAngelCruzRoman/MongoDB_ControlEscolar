from pymongo import MongoClient
from faker import Faker
from datetime import datetime
import random

# Conexión a la base de datos
client = MongoClient('localhost', 27017)
db = client['controlEscolar']  # Reemplaza 'tu_base_de_datos' con el nombre de tu base de datos

# Colecciones
collection_estudiantes = db['estudiantes']
collection_materias = db['materias']
collection_calificaciones = db['calificaciones']

# Crear instancia Faker
fake = Faker('es_MX')

def generar_calificaciones(num_calificaciones):
    calificaciones = []
    estudiantes = list(collection_estudiantes.find())  # Convertir a lista
    materias = list(collection_materias.find())  # Convertir a lista

    for _ in range(num_calificaciones):
        estudiante = random.choice(estudiantes)  # Seleccionar un estudiante aleatorio
        materia = random.choice(materias)  # Seleccionar una materia aleatoria
        calificacion = round(random.uniform(5, 10), 1)  # Generar una calificación aleatoria entre 5 y 10
        fecha = fake.date_time_between(start_date='-1y', end_date='now')  # Generar una fecha aleatoria en el último año

        # Crear objeto de calificación
        nueva_calificacion = {
            'estudiante': estudiante,
            'materia': materia,
            'calificacion': calificacion,
            'fecha': fecha
        }
        calificaciones.append(nueva_calificacion)

    return calificaciones

# Generar datos de calificaciones
num_calificaciones_a_generar = 100  # Puedes ajustar este número según sea necesario
calificaciones_generadas = generar_calificaciones(num_calificaciones_a_generar)

# Insertar datos en la colección de calificaciones
collection_calificaciones.insert_many(calificaciones_generadas)

print("Datos de calificaciones insertados exitosamente.")
