import cv2
import os
import numpy as np

dataPath = 'C:/Master/SGDI/ML/Data/'
peopleList = os.listdir(dataPath)

print('Persons List: ', len(peopleList))

labels = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    print('Reading images')
    for fileName in os.listdir(personPath):
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName,0))
    label = label + 1


face_recognizer = cv2.face.EigenFaceRecognizer_create()

print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))

# Almacenando el modelo obtenido
face_recognizer.write('modeloEigenFace.xml')

print("Modelo almacenado...")