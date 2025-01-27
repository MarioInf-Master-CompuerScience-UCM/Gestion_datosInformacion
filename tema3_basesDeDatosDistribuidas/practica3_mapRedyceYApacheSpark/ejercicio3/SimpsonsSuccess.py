""" 
    Asignatura: Gestión de Datos y de Información
    Práctica: MapReduce y Apache Spark
    Autor: Alonso Núñez, Mario

    Ética Académica:
        Declaramos que esta solución es fruto exclusivamente de nuestro
        trabajo personal. No hemos sido ayudados por ninguna otra persona
        ni hemos obtenido la solución de fuentes externas, y tampoco hemos
        compartido nuestra solución con otras personas. Declaramos además
        que no hemos realizado de manera deshonesta ninguna otra actividad
        que pueda mejorar nuestros resultados ni perjudicar los resultados
        de los demás.
        
"""

""" 
    Campos fichero simpsons_characters.csv:
        0º id:                      (int) Número de identificación del personaje.
        1º name:                    (string) Nombre del personaje.
        2º normalized_name:         (sting) Nombre del personaje normalizado para su tratamiento.
        3º gender:                  (char) Genero del personaje [m|f]
"""

""" 
    Campos fichero simpsons_episodes.csv:
        0º id:                      (int) Número de identificación del episodio.
        1º image_url:               (string) URL imagen del episodio.
        2º imdb_rating:             (float) Puntuación en episodio en IMDB.
        3º imdb_votes:              (float) Número de vetos del episodio en IBDM.
        4º number_in_season:        (int) Número del episodio respecto a la temporada a al cual eprtenece.
        5º number_in_series:        (int) Número del episodio.
        6º original_air_date:       (date) Fecha de lanzamiento oficial del episodio.
        7º original_air_year:       (int) Año de lanzamiento oficial del episodio.
        8º production_code:         (string) Código de producción del episodio.
        9º season:                  (int) Temporada a la que pertenece el episodio.
        10º title:                  (string) Título del episodio.
        11º us_viewers_in_millions: (float) Número de visualizacion en EEUU contadas por millones.
        12º video_url:              (string) URL del episodio.
        13º views:                  (float) Número de visualizaciones del episodioa  través de la URL.
"""

""" 
    Campos fichero simpsons_locations.csv:
        0º id:                      (int) Número de identificación del lugar.
        1º name:                    (string) Nombre del lugar.
        2º normalized_name:         (sting) Nombre del lugar normalizado para su tratamiento.
"""

""" 
    Campos fichero simpsons_script_lines.csv:
        0º id:                      (int) Número de identificación de la línea de diálogo.
        1º episode_id:              (int) Número de identificación del episodio en el que aparece la línea de diálogo.
        2º number:                  (int) Número que indica el orden de la línea de diálogo dentro del episodio. 
        3º raw_text:                (string) Texto en bruto de la líena de diálogo.
        4º timestamp_in_ms:         (int) Momento del episodio en el que aparece la línea de diálogo.
        5º speaking_line:           (bool) Flag que indica si se trata de una línea pronunciada o no.
        6º character_id:            (int) Número de identificación del personaje al cual pertenece la línea.
        7º location_id:             (int) Número de identificación del lugar donde se produce la línea.   
        8º raw_character_text:      (string) Nombre del personaje que dice la línea de diálogo.
        9º raw_location_text:       (string) Nombre del lujar donde se produce la línea de diálogo.
        10º spoken_words:           (string) Palabras produnciadas por el personaje en la línea de diálogo.
        11º normalized_text:        (string) Línea de diágolo normalizada para su tratamiento. No se encuentra entre comillas.
        12º word_count              (int) Número de palabras que conforman la lína de diálogo.
"""

import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
from pyspark.sql.functions import corr

def SimpsonsSuccess(filename):
    
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    urlFile_characters="simpsons_characters.csv"
    urlFile_episodes="simpsons_episodes.csv"
    urlFile_locations="simpsons_locations.csv"
    urlFile_ScriptLines="simpsons_script_lines.csv"
    dfCharacters = spark.read.options(header=True).csv(urlFile_characters)
    dfEpisodes = spark.read.options(header=True).csv(urlFile_episodes)
    #dfLocations = spark.read.options(header=True).csv(urlFile_locations)
    dfLines = spark.read.options(header=True).csv(urlFile_ScriptLines)

    dicEpisodesData={}
    for row in dfEpisodes.collect():
        tempScore = str(row["imdb_rating"]).replace('.', '', 1)
        if not row['id'] in dicEpisodesData and tempScore.isnumeric():
            dicEpisodesData[row["id"]]={
                "imdbScore":row["imdb_rating"],
                "locationsList": [],
                "numLocations": 0,
                "femaleCharactersList": [],
                "numFemaleCharacters": 0,
                "numLines":0,
                "numWords":0,
            }



    for row in dfLines.collect():
        if row['episode_id'] in dicEpisodesData and len(row)==13 and row["speaking_line"]:
            dicEpisodesData[row['episode_id']]["numLines"]+=1
            chunks=str(row[11]).split(" ")
            dicEpisodesData[row['episode_id']]["numWords"]+=len(chunks)
            
            if not row["location_id"] in dicEpisodesData[row['episode_id']]["locationsList"] \
            and str(row["location_id"]).isnumeric():
                dicEpisodesData[row['episode_id']]["locationsList"].append(row["location_id"])
            
            if not row["character_id"] in dicEpisodesData[row['episode_id']]["femaleCharactersList"] \
            and str(row["character_id"]).isnumeric():
                dicEpisodesData[row['episode_id']]["femaleCharactersList"].append(row["character_id"])



    femaleList=[]
    for femaleCharacter in dfCharacters.collect():
        if str(femaleCharacter["gender"])=="f":
            femaleList.append(femaleCharacter["id"])

    for row in dicEpisodesData:
        dicEpisodesData[row]["numLocations"] = len(dicEpisodesData[row]["locationsList"])
        for femaleCharacter in dicEpisodesData[row]["femaleCharactersList"]:
            if femaleCharacter in femaleList:
                dicEpisodesData[row]["numFemaleCharacters"]+=1


    locationsData=[]
    charactersData=[]
    scriptData=[]
    for row in dicEpisodesData:
        locationsData.append( (row, dicEpisodesData[row]["imdbScore"], dicEpisodesData[row]["numLocations"]) )
        charactersData.append( (row, dicEpisodesData[row]["imdbScore"], dicEpisodesData[row]["numFemaleCharacters"]) )
        scriptData.append( (row, dicEpisodesData[row]["imdbScore"], dicEpisodesData[row]["numLines"], dicEpisodesData[row]["numWords"]) )

    locationSchema = StructType([ \
        StructField("idEpisode",StringType(),True), \
        StructField("ibdmScore",StringType(),True), \
        StructField("numLocations",IntegerType(),True), \
    ])
    locations = spark.createDataFrame(data=locationsData, schema = locationSchema)

    charactersSchema = StructType([ \
        StructField("idEpisode",StringType(),True), \
        StructField("ibdmScore",StringType(),True), \
        StructField("numFemaleCharacters",IntegerType(),True), \
    ])
    characters = spark.createDataFrame(data=charactersData, schema = charactersSchema)

    scriptSchema = StructType([ \
        StructField("idEpisode",StringType(),True), \
        StructField("ibdmScore",StringType(),True), \
        StructField("numLines",IntegerType(),True), \
        StructField("numWords",IntegerType(),True), \
    ])
    script = spark.createDataFrame(data=scriptData, schema = scriptSchema)


    locations.select(corr("ibdmScore", "numLocations")).show()
    characters.select(corr("ibdmScore", "numFemaleCharacters")).show()
    script.select(corr("ibdmScore", "numLines")).show()
    script.select(corr("ibdmScore", "numWords")).show()

if __name__ == "__main__":
    SimpsonsSuccess(sys.argv[0])