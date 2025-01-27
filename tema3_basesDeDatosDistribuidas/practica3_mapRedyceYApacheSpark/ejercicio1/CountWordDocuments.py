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

import json
from mrjob.job import MRJob


class CountWordDocuments(MRJob):

    """  
        Entrada: Línea del fichero space.json
        Salida: ( palabra, { filname: "nombreFichero", repetitions:" 1 } )
    """
    def mapper(self, key, line):
        document=json.loads(line)
        chunks=document["content"].split(" ");
        for word in chunks:
            if word.isalpha():
                word=word.lower()
                result={
                    "filname": document["filename"],
                    "repetitions": 1
                }
                yield(word, result)



    """  
        Entrada: ( palabra, [{ filname: "nombreFichero", repetitions:" 1 }] )
        Salida: ( palabra, { filname: "nombreFichero", repetitions:" X } )
    """ 
    def combiner(self, key, values):
        repetitionsFiles={}
        for value in values:
            if value["filname"] in repetitionsFiles:
                repetitionsFiles[value["filname"]]+=value["repetitions"]
            else:
                repetitionsFiles[value["filname"]]=value["repetitions"]

        result={}
        for value in repetitionsFiles:
            result={
                "filname": value,
                "repetitions": repetitionsFiles[value],
            }
            yield (key, result)



    """  
        Entrada: ( palabra, [{ filname: "nombreFichero", repetitions:" X }] )
        Salida: ( palabra, (fichero, repeticiones) )
    """
    def reducer(self, key, values):
        repetitionsFiles={}
        for value in values:
            if value["filname"] in repetitionsFiles:
                repetitionsFiles[value["filname"]]+=value["repetitions"]
            else:
                repetitionsFiles[value["filname"]]=value["repetitions"]

        maxFiles=[]
        maxRepetitions=0
        maxFileResult=""
        for dicKey in repetitionsFiles:
            if repetitionsFiles[dicKey]> maxRepetitions:
                maxRepetitions = repetitionsFiles[dicKey]
                maxFiles.clear()
                maxFiles.append(dicKey)

            elif repetitionsFiles[dicKey]==maxRepetitions:
                maxFiles.append(dicKey)

        maxFileResult=maxFiles[0]
        for file in maxFiles:
            if file<maxFileResult:
                maxFileResult=file

        yield (key, (maxFileResult, maxRepetitions))



if __name__ == '__main__':
    CountWordDocuments.run()

