""" 
    Asignatura: Gestión de Datos y de Información
    Práctica: Recuperación de información
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

import math
import os
import string
import sys
import time

# Dada una linea de texto, devuelve una lista de palabras no vacias 
# convirtiendo a minusculas y eliminando signos de puntuacion por los extremos
# Ejemplo:
#   > extrae_palabras("Hi! What is your name? John.")
#   ['hi', 'what', 'is', 'your', 'name', 'john']
def extrae_palabras(linea):
  return filter(lambda x: len(x) > 0, 
    map(lambda x: x.lower().strip(string.punctuation), linea.split()))

def printDictionaty(dic):
    for x in dic:
        print (x,"{")
        for y in dic[x]:
            print ("\t",y,':', dic[x][y])
        print("}\n")  
    return;  


class CompleteIndex(object):


    #******************************************************************************
    #FUNCION init
    #******************************************************************************
    def __init__(self, directorio, compresion=None):
        self.vecIndex={};       #Diccionario donde se guardará el índice inevrtido
        self.URLfiles={};       #Duccionario donde se guardará la referencia a las URL de los ficheros
        tInicio = time.time();


        #PASO 1: Creación Del diccionario con las URL de los ficheros
        print("Creando el diccionario de referencia a los ficheros.", file=sys.stderr);
        fileReference=0;
        for osElement in os.walk(directorio):
            for idFile in osElement[2]:
                self.URLfiles[fileReference]={
                    "url": osElement[0]+"/"+idFile,
                }
                fileReference+=1;


        #PASO 2: Analisis de los dicheros
        numFilesIndex=0;
        print("Analizando el contenido de los ficheros", end="", file=sys.stderr);
        for document in self.URLfiles:
            file = open(self.URLfiles[document]["url"], mode="r", encoding="iso-8859-1");
            lines= file.readlines()
           
            numWordsByFile=0;
            vecWordsByFile={};
            for line in lines:
                words=extrae_palabras(line);
                for word in words:
                    numWordsByFile+=1;
                    if word not in vecWordsByFile:
                        vecWordsByFile[word]={
                            "n":[numWordsByFile]
                            }
                    else:
                        vecWordsByFile[word]["n"].append(numWordsByFile);

            for word in vecWordsByFile:
                if word not in self.vecIndex:
                    self.vecIndex[word]={
                        "aparitions":[(document, vecWordsByFile[word]["n"])]
                    }
                else:
                    self.vecIndex[word]["aparitions"].append((document, vecWordsByFile[word]["n"]));

            file.close();
            numFilesIndex+=1;
            print("\rAnalizando el contenido de los ficheros: ",numFilesIndex, "/",len(self.URLfiles), end="", file=sys.stderr);


        tFinal = time.time();  
        print("\nINDICE CREADO CON EXITO - Tiempo de procesamiento:", tFinal-tInicio,"\n", file=sys.stderr);
        return;



    #******************************************************************************
    #FUNCION consulta_frase
    #******************************************************************************
    def consulta_frase(self, frase):
        
        result=[];

        #PASO 1:Verificamos que existan ficheros que contengan todas las palabras
        wordList=frase.lower().split(" ")
        for word in wordList:
            if word not in self.vecIndex:
                print("No se ha encontrado ningún fichero que contenga todas las palabras indicadas.");
                return result;  

        #PASO 2: Tomamos la primera palabra como referencia
        minWord=wordList[0];
        wordList.pop(0); 

        #PASO 3: Avanzamos por las listas buscando las cadenas
        positionList=[-1]*len(wordList);
        for elementReference in self.vecIndex[minWord]["aparitions"]:
            i=0;
            for word in wordList:
                positionList[i]=self.checkDocumentAparitions( elementReference[0], self.vecIndex[word]["aparitions"]);
                i+=1;                

            if not -1 in positionList:
                for positionReference in elementReference[1]:
                    flagExist=True;
                    j=1;
                    for word in wordList:
                        if not self.checkWordPosition( positionReference+j, self.vecIndex[word]["aparitions"][ positionList[j-1] ][1] ):
                            flagExist=False;
                            break;
                        j+=1;

                    if flagExist==True:
                        result.append(elementReference[0]);
                        break;
        if len(result)==0:
            print("No se ha encontrado ningún fichero que contenga todas las palabras indicadas.");
            return;
        else:
            result=self.getURLbyID(result);
        return result;


    def checkDocumentAparitions(self, IDsearch, listID):
        i=0;
        for element in listID:
            if element[0]==IDsearch:
                return i;
            if element[0]>IDsearch:
                break;
            i+=1;
        return -1;

    def checkWordPosition(self, position, listPos):
        for element in listPos:
            if element==position:
                return True;
            if element>position:
                break;
        return False;


    #******************************************************************************
    #FUNCION getURLbyID
    #******************************************************************************
    def getURLbyID(self, IDlist):
        result=[];
        for id in IDlist:
            if id in self.URLfiles:
                result.append( self.URLfiles[id]["url"] );

        return result;


#******************************************************************************
#FUNCION MAIN
#******************************************************************************
if __name__=="__main__":
    if len(sys.argv) == 2:
        urlFolder = sys.argv[1]
    else:
        print("ERROR: Faltan parámetros de entrada.", file=sys.stderr);
        print("\n>> VectorialIndex \"nombreDirectorio\"", file=sys.stderr);
        exit;
    index = CompleteIndex(urlFolder);
    #printDictionaty(index.vecIndex);

    
    print("Comenzando petición consulta_frase", file=sys.stderr);    
    consulta="it sounds to";
    tInicio = time.time();
    listResult=index.consulta_frase(consulta);
    tFinal = time.time();  
    print("consulta_conjuncion finalizada - Tiempo de procesamiento:", tFinal-tInicio, file=sys.stderr);    
    print("*** Resultado consulta_frase: ", consulta, "***");
    if len(listResult)!=0:
        for element in listResult:
            print(element);
