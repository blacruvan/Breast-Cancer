from pyspark.sql import SparkSession
# import requests
from datetime import datetime
import os
# import json
# import urllib3
import pandas as pd

class HandlerBranchCode:

    # Create a SparkSession
    @staticmethod
    def newSession(name):
        spark = SparkSession.builder \
            .appName(name) \
            .getOrCreate()
        return spark

    # Crear carpetas por año, mes y día
    @staticmethod
    def partition_folder(RUTA):
        # Comprobamos que existan las particiones
        path = os.path.join(str(RUTA))
        os.makedirs(path, exist_ok=True)
        return path

    # Guardamos el fichero en su carpeta correspondiente
    @staticmethod
    def clean_data(RUTA_OG, RUTA_DEST):
        spark = HandlerBranchCode.newSession('New Session')

        date = datetime.now()
        horas = date.hour
        minutos = date.minute
        segundos = date.second

        data = spark.read.csv(RUTA_OG, header=True, inferSchema=True)
        ruta_destino = os.path.join(RUTA_DEST, f'cardio_{horas}-{minutos}-{segundos}')
        data.write.json(ruta_destino)

        spark.stop()


path_staging = HandlerBranchCode.partition_folder('.\\staging')
HandlerBranchCode.clean_data('.\\raw\\cardio.csv', path_staging)