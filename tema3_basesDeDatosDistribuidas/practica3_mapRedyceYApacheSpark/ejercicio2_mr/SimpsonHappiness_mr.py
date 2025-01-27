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
        12º word_count              (int) Número de palabras que conforman la lína de diálogo
"""

import csv
from io import StringIO
from mrjob.job import MRJob


class SimpsonHappiness(MRJob):

    """  
        Entrada: Línea del fichero space.json
        Salida: ( id episodio, felicidad parcial )
    """
    def mapper(self, key, line):
        urlFile=("/home/mario/Documentos/masterIngenieriaInformatica/sistemaDeGestionDeDatosYDeInformacion/tema3_basesDeDatosDistribuidas/practica3_mapRedyceYApacheSpark/ejercicio2/happiness.txt")
        lines = line.splitlines()
        reader = csv.reader(lines, delimiter=',')
        wordDict={}

        for row in reader:
            if len(row)!=13 or row[0]=="id":
                return
            words = row[11].split(" ")
            for word in words:
                if word.isalpha():
                    wordDict[word]=0;
                    
        file = open(urlFile, 'r')
        lines = file.readlines()
        for line in lines:
            chunksFile = line.split("\t")
            if chunksFile[0] in wordDict:
                wordDict[chunksFile[0]]=float(chunksFile[2]);

        yield ("uniqueReducer", (row[1], sum(wordDict.values()) ) )



    """  
        Entrada: ( id episodio, [felicidad parcial] )
        Salida: ( id episodio, felicidad parcial )
    """ 
    def combiner(self, key, values):
        result={}
        for value in values:
            if value[0] in result:
                result[value[0]]+=float(value[1])
            else:
                result[value[0]]=float(value[1])

        for key in result:
            yield ("uniqueReducer", (key, result[key]))     


    """  
        Entrada: ( id episodio, [felicidad parcial] )
        Salida: ( id episodio, felicidad media )
    """
    def reducer(self, key, values):
        result={}
        for value in values:
            if value[0] in result:
                result[value[0]]+=float(value[1])
            else:
                result[value[0]]=float(value[1])

        result = sorted(result.items(), key=lambda item: item[1], reverse=True)
        for value in result:
            yield (value[0], value[1])




if __name__ == '__main__':
    SimpsonHappiness.run()

