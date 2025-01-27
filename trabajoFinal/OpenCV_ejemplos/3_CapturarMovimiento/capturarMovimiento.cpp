#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include <opencv2/videoio/videoio.hpp>


using namespace std;
using namespace cv;

int main() {

	VideoCapture cap("laser.avi");
	if (!cap.isOpened()){
		return 1;
	}
	Mat imagen;
	int indice = 0;
	int tiempoDeEspera = 100;
	namedWindow("1. Video Original");
	namedWindow("2. Video Captura Movimiento");


	//Reproducción del vídeo original
	printf("Video preparado para la reproducción de prueba, pulse ESPACIO para continuar\n");
	waitKey(0);
	while(1){
		if (!cap.read(imagen)){
			break;
		}
		imshow("1. Video Original", imagen);
		indice++;
		char c = waitKey(tiempoDeEspera);
		if (c == 27)
			break;
	}
	indice=0;
	VideoCapture cap2("laser.avi");
	if (!cap.isOpened()){
		return 1;
	}


	//Reproducción del vídeo en seguimiento
	printf("pulse ESPACIO para realziar el seguimiento\n");
	waitKey(0);
	while(1){
		if (!cap2.read(imagen)){
			break;
		}
		imshow("1. Video Original", imagen);

		Mat imagenR;
		vector<Mat> canales;
		split(imagen,canales);
		threshold(canales[2], imagenR, 220, 255, THRESH_BINARY_INV);
		imshow("2. Video Captura Movimiento", imagenR);

		indice++;
		char c = waitKey(tiempoDeEspera);
		if (c == 27)
			break;
	}


	return 0;
}
