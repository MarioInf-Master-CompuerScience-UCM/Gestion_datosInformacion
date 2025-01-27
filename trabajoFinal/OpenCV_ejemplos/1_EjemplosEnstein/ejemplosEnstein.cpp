#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs/imgcodecs.hpp>

using namespace std;
using namespace cv;


int main() {

	//EJEMPLOS GUARDADO DE IMAGEN EN CON DISTINTAS CONFIGURACIONE DE ELEMENTOS VEC
	Mat imagen = imread("Enstein.png");
	if (!imagen.data){
		cout << "NO SE HA CARGADO LA IMAGEN" << endl;
		return 1;
	}
	namedWindow("Parte 1 - Original", WINDOW_NORMAL);
	imshow("Parte 1 - Original", imagen);	

	Mat imagenGray;
	cvtColor(imagen, imagenGray, cv::COLOR_BGRA2GRAY);
	namedWindow("Parte 1 - Escala de grises", WINDOW_NORMAL);
	imshow("Parte 1 - Escala de grises", imagenGray);
	imwrite("Enstein1_GreyScale.png", imagenGray);

	Mat imagen2b;
	imagen2b = imagenGray > 128;
	namedWindow("Parte 1 - Blanco y negro", WINDOW_NORMAL);
	imshow("Parte 1 - Blanco y negro", imagen2b);
	imwrite("Enstein1_BackAndWhite.png", imagen2b);


	//EJEMPLOS OPERACIONES A NIVEL DE PIXEL
	Mat imagenThreshold;
	threshold(imagen, imagenThreshold, 150, 255, THRESH_BINARY);
	namedWindow("Parte 2 - Filtro Threshold", WINDOW_NORMAL);
	imshow("Parte 2 - Filtro Threshold", imagenThreshold);
	imwrite("Enstein2_Threshold.png", imagenThreshold);

	Mat imagenRed= imread("Enstein.png");
	Mat imagenBlue= imread("Enstein.png");
	Mat imagenGreen= imread("Enstein.png");
	if (!imagenRed.data || !imagenRed.data || !imagenGreen.data){
		cout << "NO SE HA CARGADO LA IMAGEN" << endl;
		return 1;
	}
	for (int i=0; i<imagen.rows; i++){
		for (int j=0; j<imagen.cols; j++){
			imagenRed.at<Vec3b>(i,j)[0] = 0;
			imagenRed.at<Vec3b>(i,j)[1] = 0;
			imagenBlue.at<Vec3b>(i,j)[1] = 0;
			imagenBlue.at<Vec3b>(i,j)[2] = 0;
			imagenGreen.at<Vec3b>(i,j)[0] = 0;
			imagenGreen.at<Vec3b>(i,j)[2] = 0;
		}
	}
	namedWindow("Parte 2 - División de canales: Red", WINDOW_NORMAL);
	imshow("Parte 2 - División de canales: Red", imagenRed);
	imwrite("Enstein2_split_red.png", imagenRed);
	
	namedWindow("Parte 2 - División de canales: Blue", WINDOW_NORMAL);
	imshow("Parte 2 - División de canales: Blue", imagenBlue);
	imwrite("Enstein2_split_blue.png", imagenBlue);
	
	namedWindow("Parte 2 - División de canales: Green", WINDOW_NORMAL);
	imshow("Parte 2 - División de canales: Green", imagenGreen);
	imwrite("Enstein2_split_green.png", imagenGreen);


	//EJEMPLOS OPERACIONES A NIVEL DE PIXEL
	Mat imagenGauss;
	GaussianBlur(imagen, imagenGauss, Size(25,25), 1.8);
	imshow("Parte 3 - Filtro Gauus", imagenGauss);
	imwrite("Enstein3_filtroGauss.png", imagenGauss);

	Mat imagenCanny;
	Canny(imagen, imagenCanny, 125, 350);
	imshow("Parte 3 - Filtro Canny", imagenCanny);
	imwrite("Enstein3_filtroCanny.png", imagenCanny);


	//EJEMPLOS OPERACIONES A NIVEL DE IMAGEN	
	Mat imagenSobel_Vertical, imagenSobel_Horizontal;
	Sobel(imagen, imagenSobel_Vertical, CV_8U, 1, 0);
	imshow("Parte 4 - Filtro Sobel Vertical", imagenSobel_Vertical);
	imwrite("Enstein4_filtroSobel_vertical .png", imagenSobel_Vertical);
	Sobel(imagen, imagenSobel_Horizontal, CV_8U, 0, 1);
	imshow("Parte 4 - Filtro Sobel Horizontal", imagenSobel_Horizontal);
	imwrite("Enstein4_filtroSobel_horizontal.png", imagenSobel_Horizontal);

	Mat imagenEsquinas;
	Mat imagenGray2;
	cvtColor(imagen, imagenGray2, cv::COLOR_BGRA2GRAY);
	vector<Point2f> esquinas;
	int maxEsquinas = 100;
	double calidad = 0.01;
	double minimaDistancia = 10;
	int tamBloque = 3;
	bool usarHarris = false;
	double k = 0.04;
	goodFeaturesToTrack(imagenGray2, esquinas, maxEsquinas, calidad, minimaDistancia, Mat(), tamBloque, usarHarris, k);
	for (unsigned int i=0; i<esquinas.size();i++){
		Point2f pcirculo(esquinas[i].x, esquinas[i].y);
		circle(imagenGray2, pcirculo, 8, Scalar(0, 0, 255), 3);
	}
	imshow("Parte 4 - Filtro Esquinas", imagenGray2);
	imwrite("Enstein4_filtroEsquinas.png", imagenGray2);




	waitKey(0);
	return 0;
}
