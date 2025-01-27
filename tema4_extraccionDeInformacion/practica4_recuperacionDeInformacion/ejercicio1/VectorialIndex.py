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


class VectorialIndex(object):


    #******************************************************************************
    #FUNCION init
    #******************************************************************************
    def __init__(self, directorio):
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
                    "normal":0
                }
                fileReference+=1;


        #PASO 2: Analisis de los dicheros
        numFilesIndex=0;
        print("Analizando el contenido de los ficheros", end="", file=sys.stderr);
        for document in self.URLfiles:
            file = open(self.URLfiles[document]["url"], mode="r", encoding="iso-8859-1");
            lines= file.readlines()
           
            vecWordsByFile={};
            for line in lines:
                words=extrae_palabras(line);
                for word in words:
                    if word not in vecWordsByFile:
                        vecWordsByFile[word]={"n":1}
                    else:
                        vecWordsByFile[word]["n"]+=1;

            for word in vecWordsByFile:
                if word not in self.vecIndex:
                    self.vecIndex[word]={
                        "weights":[(document, vecWordsByFile[word]["n"])]
                    }
                else:
                    self.vecIndex[word]["weights"].append((document, vecWordsByFile[word]["n"]));

            file.close();
            numFilesIndex+=1;
            print("\rAnalizando el contenido de los ficheros: ",numFilesIndex, "/",len(self.URLfiles), end="", file=sys.stderr);


        #PASO 3: Cálculo de pesos
        print("\nCalculando Pesos", file=sys.stderr);
        for word in self.vecIndex:
            dfi=math.log(len(self.URLfiles)/len(self.vecIndex[word]["weights"]) ,2);
            i=0;
            for weight in self.vecIndex[word]["weights"]:
                tf=1+math.log(weight[1], 2);
                self.vecIndex[word]["weights"].insert(i+1, (weight[0], tf*dfi));
                self.vecIndex[word]["weights"].pop(i);
                i+=1;
                self.URLfiles[weight[0]]["normal"]+=pow( (tf*dfi), 2);

        #PASO4: Calculo de normales
        print("\nCalculando Normales", file=sys.stderr);
        for document in self.URLfiles:
            self.URLfiles[document]["normal"]=math.sqrt(self.URLfiles[document]["normal"]);

        tFinal = time.time();  
        print("INDICE CREADO CON EXITO - Tiempo de procesamiento:", tFinal-tInicio,"\n", file=sys.stderr);
        return;


    #******************************************************************************
    #FUNCION consulta_vectorial
    #******************************************************************************
    def consulta_vectorial(self, consulta, n=3):
        
        wordList=consulta.lower().split(" ");
        scores={};
        topScores=[-1]*n;
        topScoresID=[-1]*n;
        for word in wordList:
            for document in self.vecIndex[word]["weights"]:
                if document[0] not in scores:
                    scores[document[0]]={
                        "relevant": document[1]
                    }
                else:
                    scores[document[0]]["relevant"]+=document[1];

        for score in scores:
            if self.URLfiles[score]["normal"]>0:
                scores[score]["relevant"] = scores[score]["relevant"]/ self.URLfiles[score]["normal"];
                if scores[score]["relevant"] > topScores[-1]:
                    tempScore=scores[score]["relevant"];
                    tempScore2=0;
                    tempID=score;
                    tempID2=0;
                    for i in range(n):
                        if tempScore>topScores[i]:
                            tempScore2=topScores[i];
                            topScores[i]=tempScore;
                            tempScore=tempScore2;

                            tempID2=topScoresID[i];
                            topScoresID[i]=tempID;
                            tempID=tempID2
                        else:
                            break;
                          
        topScoresID=self.getURLbyID(topScoresID);
        result=[];
        i=0;
        for url in topScoresID:
            result.append((url, topScores[i]));
            i+=1;

        return result;




    #******************************************************************************
    #FUNCION consulta_conjuncion
    #******************************************************************************
    def consulta_conjuncion(self, consulta):

        result=[];

        #PASO 1:Verificamos que existan ficheros que contengan todas las palabras
        wordList=consulta.lower().split(" ")
        for word in wordList:
            if word not in self.vecIndex:
                print("No se ha encontrado ningún fichero que contenga todas las palabras indicadas.");
                return result;

        #PASO 2: Buscamo la palabra que aparece en menos ficheros y la tomamos como referencia.
        minFiles=len(self.vecIndex[wordList[0]]["weights"]);
        minPos=0;
        minWord=wordList[0];
        i=0
        for word in wordList:           
            if len(self.vecIndex[word]["weights"])<minFiles:
                minFiles=len(self.vecIndex[word]["weights"]);
                minPos=i;
                minWord=word;
            i+=1;
        wordList.pop(minPos);

        #PASO 3: Avanzamos en todas las listas buscando las coincidencias con los ficheros de la palabra de referencia.
        indexList=[0]*len(wordList);
        for elementReference in self.vecIndex[minWord]["weights"]:
            flagEndOfFIle=False;
            flagFileFounded=False;
            flagIntersect=True;   
            i=0;
            for word in wordList:
                j=indexList[i];
                if j<len(self.vecIndex[word]["weights"]):
                    while self.vecIndex[word]["weights"][j][0]<=elementReference[0]:

                        if self.vecIndex[word]["weights"][j][0]==elementReference[0]:
                            flagFileFounded=True;
                        j+=1;
                        if j==len(self.vecIndex[word]["weights"]):
                            break;

                indexList[i]=j
                if flagFileFounded==True:
                    flagFileFounded=False;
                else:
                    flagIntersect=False;
                i+=1

                if j>=len(self.vecIndex[word]["weights"]):
                    flagEndOfFIle=True;
            
            if flagIntersect==True:
                result.append(elementReference[0]);
            if flagEndOfFIle==True:
                break;

        if len(result)==0:
            print("No se ha encontrado ningún fichero que contenga todas las palabras indicadas.");
            return result;
        else:
            result=self.getURLbyID(result);
        
        return result;



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
    index = VectorialIndex(urlFolder);
    printDictionaty(index.vecIndex);
    
    print("Comenzando petición consulta_conjuncion", file=sys.stderr);    
    consulta="I am happy city";
    tInicio = time.time();
    listResult=index.consulta_conjuncion(consulta);
    tFinal = time.time();  
    print("consulta_conjuncion finalizada - Tiempo de procesamiento:", tFinal-tInicio, file=sys.stderr);    
    print("*** Resultado consulta_conjuncion: ", consulta, "***");
    if len(listResult)!=0:
        for element in listResult:
            print(element);

    print("\nComenzando petición consulta_vectorial", file=sys.stderr);    
    consulta="I am happy city";
    tInicio = time.time();
    listResult=index.consulta_vectorial(consulta, n=5);
    tFinal = time.time();  
    print("consulta_vectorial finalizada - Tiempo de procesamiento:", tFinal-tInicio, file=sys.stderr);    
    print("*** Resultado consulta_vectorial: ", consulta, "***");
    if len(listResult)!=0:
        for element in listResult:
            print(element);
