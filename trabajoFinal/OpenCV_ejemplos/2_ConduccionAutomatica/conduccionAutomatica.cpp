#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>

using namespace std;
using namespace cv;

int main() {
	
	Mat imagen, imagenCanny, imagenCannyInv;
	Mat imagenGauss, imagenGaussCanny, imagenGaussCannyInv;

	//Paso 1: Lectura d ela imagen original
	imagen = imread("carretera.jpg", IMREAD_GRAYSCALE);
	if (!imagen.data){
		cout << "IMAGEN NO LEIDA" << endl;
		return 1;
	}
	namedWindow("1. Imagen Original",WINDOW_NORMAL);
	imshow("1. Imagen Original", imagen);
	printf("Pulse SPACIO para continuar\n");
	waitKey(0);

	//Paso 2: Detección de líneas de la imagen original
	Canny(imagen, imagenCanny, 125, 350);
	threshold(imagenCanny, imagenCannyInv, 128, 255, THRESH_BINARY_INV);
	namedWindow("2. Deteccion de lineas origianl", WINDOW_NORMAL);
	imshow("2. Deteccion de lineas origianl", imagenCannyInv);
	printf("Pulse SPACIO para continuar\n");
	waitKey(0);

	//Paso3: Aplicamos el filtro Gauss para evitar ruido en la imagen 
	GaussianBlur(imagen, imagenGauss, Size(5,5), 0.7);
	namedWindow("3. Imagen Gauss", WINDOW_NORMAL);
	imshow("3. Imagen Gauss", imagenGauss);
	printf("Pulse SPACIO para continuar\n");
	waitKey(0);

	//Paso 4: Detectamos las líneas en la imagen sin ruido
	Canny(imagenGauss, imagenGaussCanny, 125, 350);
	threshold(imagenGaussCanny, imagenGaussCannyInv, 128, 255, THRESH_BINARY_INV);
	namedWindow("4. Deteccion de lineas Gauss", WINDOW_NORMAL);
	imshow("4. Deteccion de lineas Gauss", imagenGaussCannyInv);
	printf("Pulse SPACIO para finalizar\n");
	waitKey(0);

	return 0;
}
