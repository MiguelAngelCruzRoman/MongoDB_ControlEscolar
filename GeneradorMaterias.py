from faker import Faker
from pymongo import MongoClient
import random

# Conexión a la base de datos
client = MongoClient('localhost', 27017)
db = client['controlEscolar']
collection_maestros = db['maestros']
collection_materias = db['materias']  # Nueva colección para materias

# Crear instancia Faker
fake = Faker('es_MX')

# Obtener IDs de maestros existentes
maestros_ids = [maestro['_id'] for maestro in collection_maestros.find({}, {'_id': 1})]
maestros_primerNombre = [maestro['primerNombre'] for maestro in collection_maestros.find({}, {'primerNombre':1})]
maestros_segundoNombre = [maestro['segundoNombre'] for maestro in collection_maestros.find({}, {'segundoNombre':1})]
maestros_apellidoPaterno = [maestro['apellidoPaterno'] for maestro in collection_maestros.find({}, {'apellidoPaterno':1})]
maestros_apellidoMaterno = [maestro['apellidoMaterno'] for maestro in collection_maestros.find({}, {'apellidoMaterno':1})]

def generar_codigo_materia():
    return fake.unique.random_number(digits=6)

# Generar datos de prueba para materias
materias_data = []
for _ in range(100):  # Cambia esto al número deseado de registros
    materia = {
        'nombre': fake.job(),
        'maestro': {'_id':random.choice(maestros_ids), 'primerNombre':random.choice(maestros_primerNombre),'segundoNombre':random.choice(maestros_segundoNombre),'apellidoPaterno':random.choice(maestros_apellidoPaterno),'apellidoMaterno':random.choice(maestros_apellidoMaterno)}, # Seleccionar aleatoriamente un maestro existente
        'horasPracticas': random.randint(1, 5) * 10,
        'horasTeoricas': random.randint(1, 5) * 10,
        'creditos': random.randint(1, 10)
    }
    materias_data.append(materia)

# Insertar datos de materias en la base de datos
collection_materias.insert_many(materias_data)

print("Datos de materias insertados exitosamente.")
