import random
import uuid
import pandas as pd
from faker import Faker

# 1. Escoger el pais y lenguaje para simular los datos
fake = Faker("es_CO")

# 2. Sembrar semillas (para que el archivo sea reproducible)
Faker.seed(42)
random.seed(42)

# 3. Definir el dato y su tipo a simular
# id (texto (UUID)),
# fecha_registro (fecha y hora),
# observacion (texto),
# estado (texto),
# id_usuario (texto (UUID)),
# id_reto (texto (UUID)).

# 4. Definir el numero de datos simulados (DATASET) y las constantes
FILAS = 800

ESTADOS = ["inscrito", "en proceso", "finalizado"]
IDS_USUARIO = [str(uuid.uuid4()) for _ in range(400)]
IDS_RETO = [str(uuid.uuid4()) for _ in range(120)]


# 5. Ensuciar los datos

# 5.1 Funcion que devuelve una muestra (los indices).
#     Cada porcentaje se calcula sobre las filas base, asi es exacto.
def generar_muestra(datos, porcentaje, excluir=None):
    cantidad = int(len(datos) * porcentaje)
    candidatos = datos if excluir is None else datos.drop(excluir)
    return candidatos.sample(n=cantidad, random_state=random.randint(0, 9999)).index


# 5.2 Funcion que ensucia los datos
def ensuciar(datos_df, n=FILAS):
    datos_df = datos_df.copy()

    # --- fecha_registro: dos formatos mezclados ---------------
    # "2026-03-15 14:30:00" (ISO) y "15/03/2026 14:30" (latino)
    datos_df["fecha_registro"] = datos_df["fecha_registro"].astype(str)

    subconjunto_datos = generar_muestra(datos_df, 0.12)
    datos_df.loc[subconjunto_datos, "fecha_registro"] = (
        pd.to_datetime(datos_df.loc[subconjunto_datos, "fecha_registro"])
        .dt.strftime("%d/%m/%Y %H:%M")
    )

    # --- observacion: 20% en None -----------------------------
    subconjunto_datos = generar_muestra(datos_df, 0.20)
    datos_df.loc[subconjunto_datos, "observacion"] = None

    # --- estado: variantes de escritura (sin solaparse) -------
    # 10% en MAYUSCULAS ('EN PROCESO')
    mayusculas = generar_muestra(datos_df, 0.10)
    datos_df.loc[mayusculas, "estado"] = datos_df.loc[mayusculas, "estado"].str.upper()

    # 8% con espacios sobrantes (' inscrito ')
    espacios = generar_muestra(datos_df, 0.08, excluir=mayusculas)
    datos_df.loc[espacios, "estado"] = " " + datos_df.loc[espacios, "estado"] + " "

    # 5% capitalizado y con espacios (' Finalizado ')
    usados = mayusculas.union(espacios)
    capital = generar_muestra(datos_df, 0.05, excluir=usados)
    datos_df.loc[capital, "estado"] = (
        " " + datos_df.loc[capital, "estado"].str.capitalize() + " "
    )

    # --- Repetidos y duplicados (filas finales = 800) ---------
    # Se eligen filas destino distintas entre si, asi cada % es exacto.
    pares = int(n * 0.10)        # 10% pares id_usuario + id_reto repetidos
    duplicados = int(n * 0.05)   # 5% filas duplicadas exactas

    destinos = datos_df.sample(n=pares + duplicados, random_state=random.randint(0, 9999)).index
    destinos_pares = destinos[:pares]
    destinos_duplicados = destinos[pares:]
    origenes = datos_df.index.difference(destinos)

    # 10%: el mismo usuario inscrito dos veces en el mismo reto
    for destino in destinos_pares:
        origen = random.choice(origenes)
        datos_df.loc[destino, "id_usuario"] = datos_df.loc[origen, "id_usuario"]
        datos_df.loc[destino, "id_reto"] = datos_df.loc[origen, "id_reto"]

    # 5%: filas repetidas tal cual (mismo id y todos los campos)
    for destino in destinos_duplicados:
        origen = random.choice(origenes)
        datos_df.loc[destino] = datos_df.loc[origen]

    return datos_df


# 6. Construir la funcion generadora de datos
def generar_registros(n=FILAS):
    filas = []
    for _ in range(n):
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })

    df = pd.DataFrame(filas)
    df = ensuciar(df, n)
    return df


# 7. Ejecucion principal
if __name__ == "__main__":
    df = generar_registros()
    print(df.shape)
    print(df.head())
    print(df.isna().sum())