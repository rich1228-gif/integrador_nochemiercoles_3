import random

import uuid

from faker import Faker


#1. Escoger el pais y lenguaje para simulos datos


fake=Faker("es_CO") # Faker para Colombia


#2. Sembrar semillas

Faker.seed(42)

random.seed(42)


#3. Definir el dato y su tipo a simular


#id (texto (UUID)),

#fecha_registro (fecha y hora),

#observacion (texto),

#estado (texto),************a tratar

#id_usuario (texto (UUID)),

#id_reto (texto (UUID)).


#4. Defini el numero de datos simulados (DATASET)

#DEfinir datos de tegistros
FILAS=800

def generar_datos_registros(numero_registros=FILAS):
    
    ESTADOS=["pendiente","enprogreso","completado"]

    filas=[]

    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro":fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario":random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO)
        })

#def generar_datos_usuarios(numero_registros=FILAS):

    #ROLES=["administrador","empresario","profesor"]

   # filas=[]

    #for _ in range(numero_registros):
     #   filas.append({
      #      "id": str(uuid.uuid4()),
       #     "nombre": fake.name(),
        #    "correo": fake.email(),
         #   "contrasena_hash": fake.sha256(),
          #  "rol": random.choice(ROLES),
           # "activo": random.choice([True, False]),
           # "fecha_registro":fake.date_time_between(start_date="-2y", end_date="now")
        #});