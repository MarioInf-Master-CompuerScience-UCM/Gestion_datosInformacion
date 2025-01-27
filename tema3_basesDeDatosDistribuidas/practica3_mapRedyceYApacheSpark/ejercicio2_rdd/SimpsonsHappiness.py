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

import json
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, IntegerType
from pyspark.sql.functions import corr

def func(x, rddHappy):
    
    sumTemp=0;
    happyRowTemp=[];

    chunks=x[1].split();
    for chunk in chunks:
        happyRowTemp=rddHappy.lookup(chunk);
        if happyRowTemp:
            sumTemp=sumTemp+int(happyRowTemp[0].split("\t")[2]);

    return sumTemp;





def SimpsonsSuccess(filename):
    
    spark = SparkSession.builder.getOrCreate()
    sc = spark.sparkContext

    urlFile_Happiness="happiness.txt";
    fileHappy = open(urlFile_Happiness, 'r');
    linesHappy = fileHappy.readlines();
    arrayHappy=[]
    for line in linesHappy:
        chunks=line.split("\t");
        arrayHappy.append(( chunks[0], chunks[2] ));
    rddHappy = sc.parallelize(arrayHappy);


    urlFile_ScriptLines="simpsons_script_lines_test.csv";
    dfLines = spark.read.options(header=True).csv(urlFile_ScriptLines);
    arrayWords=[];
    for row in dfLines.collect():
        if len(row)==13 and row["normalized_text"]!=None:
            arrayWords.append(( int(row['episode_id']), row["normalized_text"] ))
    rddLines=sc.parallelize(arrayWords);
    rddLines=rddLines.reduceByKey(lambda x, y: x+y);

    resultList=[];
    for row in rddLines.collect():
        numWordsTemp=0;
        sumTemp=0;
        happyRowTemp=[];
        chunks=row[1].split(" ");
        for chunk in chunks:
            happyRowTemp=rddHappy.lookup(chunk); 
            if happyRowTemp:
                sumTemp=sumTemp+float(happyRowTemp[0]);
                numWordsTemp
        resultList.append((row[0], sumTemp))

    rddResult=sc.parallelize(resultList);
    rddResult=rddResult.sortBy(lambda x: x[1], ascending=False);
    for row in rddResult.collect():
        print(row)


if __name__ == "__main__":
    SimpsonsSuccess(sys.argv[0])