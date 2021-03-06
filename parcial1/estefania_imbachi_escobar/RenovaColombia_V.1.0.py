﻿#RenovaColombia v1.0
#programa que mide las enegias renovales de los departamentos de Colombia, y genera un un archivo llamado invertir.txt 
#con los departamentos con deficit de generacion por cada tipo, para que se haga una inversion.

#Desarrollado por Estefania Imbachi Escobar
#Septiembre 18 de 2015

# Importar libreria sys para manejo de argumentos de linea de comandos
import os
import sys

# ------------------ Inicio de definicion de constantes y parametros ------------------ #

# Nombre archivo de errores
nombre_archivo_errores = "errores.txt"

# Nombre archivo de registro de operacion del programa
nombre_archivo_registro = "log.txt"

# Nombre archivo que contendra los departamentos con tipo de energia para invertir
nombre_archivo_invertir = "invertir.txt"

# Nombre de archivo que contendra el informe con todos los totales y npromedios de energia
nombre_archivo_informe = "informe.txt"

# Numero minimo de lineas para archivo energias y sostenible
numero_minimo_lineas = 4

# ------------------ Fin de definicion de constantes y parametros ------------------ #

# ------------------ Inicio de definicion de funciones empleadas ------------------ #

# Funcion para leer el directorio y las extensiones de sus archivos 
def directory(path,extension):
  list_dir = []
  list_dir = os.listdir(path)
  archiv = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
      archiv += 1
  return archiv


# Funcion para crear un archivo con el nombre especificado. Devuelve True si fue exitoso o False en caso de error.
def crear_archivo(nombre_archivo):
	try:
		archivo = open(nombre_archivo, 'w')
		archivo.close()
	except:
		guardar_error("Error creando archivo " + nombre_archivo + "!");
		return False
		
	return True


# Funcion que guarda un mensaje de error en el archivo errores.txt
def guardar_error(mensaje_error):
	escribir_linea_archivo(nombre_archivo_errores, "\n" + mensaje_error + "\n")
	
# Funcion que guarda un registro de operacion en el archivo log.txt
def guardar_log(mensaje_registro):
	escribir_linea_archivo(nombre_archivo_registro, "\n" + mensaje_registro + "\n")

# Funcion que finaliza el programa y guarda el respectivo mensaje de terminacion en el archivo errores.txt
def terminar_programa(mensaje_terminacion):
	guardar_error(mensaje_terminacion)
	guardar_log("Programa terminado por error... Verificar archivo errores.txt para mas detalles.")
	
	# Terminar el programa
	sys.exit()

# Funcion que guarda al final del archivo definido la linea especificada. Devuelve True si fue exitoso o False en caso de error.	
def escribir_linea_archivo(nombre_archivo, linea_a_escribir):	
	try:
		archivo = open(nombre_archivo, 'a')
		archivo.write(linea_a_escribir)
		archivo.close()
	except IOError:
		guardar_error("Error escribiendo linea " + linea_a_escribir + " en archivo " + nombre_archivo + "!")
		return False
		
	return True

	
# Funcion que lee las lineas de un archivo de texto y las devuelve en una lista.
def leer_lineas_archivo(nombre_archivo):
	lineas = ()
	try:
		archivo = open(nombre_archivo, 'r')
		lineas = archivo.readlines()
		archivo.close()
	except IOError:
		guardar_error("Error leyendo archivo " + nombre_archivo + "!")
		
	return lineas 

	
# Funcion para validar la lineas de los archivos
def validar_linea(linea_por_validar, numero_linea):	
	array_respuesta = [0 for x in range(2)]
	
	# Separar la linea por el simbolo (space) 
	arreglo_campos = linea_por_validar.split(" ")	
	array_respuesta[0]=arreglo_campos[0]
	# Validar que el campo sea de tipo numerico
	try:
		tipo_sostenible = int(arreglo_campos[1])								
		array_respuesta[1] = tipo_sostenible
	except ValueError:	
		guardar_error(arreglo_campos[1] + " no puede convertirse a entero!")
		return array_respuesta
	return array_respuesta
	
# ------------------ Fin de definicion de funciones empleadas ------------------ #

# Inicializacion de archivos

# Crear el archivo errores.txt para almacenar los errores que se presenten.
crear_archivo("errores.txt")

# Crear el archivo log.txt para almacenar el registro de operacion del programa.
crear_archivo("log.txt")

guardar_log("Creados archivos errores.txt y log.txt")


program_path = os.getcwd()

# Argumentos
ruta = sys.argv[1]
energias = sys.argv[2]
sostenible = sys.argv[3]

# Validaciones
if (sys.argv[2].endswith(".txt") == False):
	terminar_programa("El archivo energias no tiene extension .txt!")
else:
	guardar_log("Extension de archivo de energias OK")
	
if (sys.argv[3].endswith(".txt") == False):
	terminar_programa("El archivo sostenible no tiene extension .txt!")
else:
	guardar_log("Extension de archivo de sostenible OK")

leido_energias=tuple(leer_lineas_archivo(energias))
numero_energias=len(leido_energias)

guardar_log("archivo energias leido OK")

leido_sostenible=tuple(leer_lineas_archivo(sostenible))
numero_sostenible=len(leido_sostenible)

guardar_log("archivo sostenible leido OK")

if(numero_sostenible!=numero_energias and numero_sostenible==numero_minimo_lineas):
	terminar_programa("Los archivos sostenible y energias no tienen igual numero de lineas o igual al numero de tipo")
else:
	guardar_log("archivos con igual numero de lineas e igual al numero de tipo")
	
	
# ------------------ Inicio de logica de programa ------------------ #

array_sostenible = [[columnas for columnas in range(2)] for filas in range(numero_sostenible)]

guardar_log("Cargando sostenible en memoria...");
for x in range(0, numero_sostenible):
	linea_validada = validar_linea(leido_sostenible[x], x+1)
	guardar_log("Procesando linea " + str(x+1));
	array_sostenible[x][0] = linea_validada[0]
	array_sostenible[x][1] = linea_validada[1]

guardar_log("sostenible cargada en memoria!");

# Validando la extension de los archivos del directorio
archiv=directory(sys.argv[1],'.txt')
if(archiv==0):
	terminar_programa("no hay archivos validos en el directorio")
i=0
no_format=[[columnas for columnas in range(1)] for filas in range(100)]
array_depart = [[columnas for columnas in range(1)] for filas in range(archiv)]
rootDir = ruta
for dirName, subdirList, fileList in os.walk(rootDir):
   
    for fname in fileList:
		if(fname.endswith('.txt')):
			array_depart[i][0] = fname
		else:
			no_format[i][0]=fname
			i=i-1
		if(i!=(archiv-1)):
			i=i+1
guardar_log("directorio encontrado");
 

guardar_log("contanto archivos con extension '.txt' en el directorio")
guardar_log("archivos OK contados y listados")
guardar_log("procesando informacion del directorio")
guardar_log("si no se continua el texto leer archivo errores.txt y log.txt en directorio dado")
os.chdir(ruta)

array_array = [[columnas for columnas in range(6)] for filas in range(archiv)]
for x in range(0,archiv):
	array_array[x]=tuple(leer_lineas_archivo(array_depart[x][0]))


array_validado = [[columnas for columnas in range(4)] for filas in range(archiv+1)]

i=0
j=1
while (j<archiv+1):
	for x in range(0, 4):
		linea_validada = validar_linea(array_array[i][x+2], x+3)
		array_validado[0][x] = linea_validada[0]
		array_validado[j][x] = linea_validada[1]
	i=i+1
	j=j+1

os.chdir(program_path)
guardar_log("informacion del directorio procesada");
guardar_log("creando array array_suma");

array_suma = [[columnas for columnas in range(1)] for filas in range(4)]

guardar_log("sumando tipo")
k=0	
while (k<4):
	for x in range(1,archiv+1):
		array_suma[k][0]+=int(array_validado[x][k])
	k=k+1

guardar_log("tipo sumados y guardados")

array_promedio = [[columnas for columnas in range(1)] for filas in range(4)]

for x in range (0,4):
	array_promedio[x][0]=array_suma[x][0]/archiv
	
guardar_log("tipo promediados y guardados")


# Arreglo para comprar los datos obtenidos con los minimos en sostenible
array_comparacion = [[columnas for columnas in range(4)] for filas in range(archiv)]

guardar_log("comparando datos de tipo de los archivos con la sostenible")
k=1
i=0
while (k<archiv+1):
	for x in range (0,4):
		array_comparacion[i][x]=array_validado[k][x]-array_sostenible[x][1]
	k=k+1
	i=i+1
guardar_log("datos comparados y guardados")


# Creando el archivo invertir 
guardar_log("archivo invertir.txt creado y en ejecucion")
crear_archivo("invertir.txt")
i=0
while (i<archiv-1):
	for x in range(0, 1):
		if(array_comparacion[i][x]<0 or array_comparacion[i][x+1]<0 or array_comparacion[i][x+2]<0 or array_comparacion[i][x+3]):
			
			escribir_linea_archivo(nombre_archivo_invertir, "\n" + array_depart[i][0] + "\n\n")
		if(array_comparacion[i][x]<0):
			escribir_linea_archivo(nombre_archivo_invertir, "\t-" + array_sostenible[x][0] + "\n")
		if(array_comparacion[i][x+1]<0):
			escribir_linea_archivo(nombre_archivo_invertir, "\t-" + array_sostenible[x+1][0] + "\n")	
		if(array_comparacion[i][x+2]<0):
			escribir_linea_archivo(nombre_archivo_invertir, "\t-" + array_sostenible[x+2][0] + "\n")	
		if(array_comparacion[i][x+3]<0):
			escribir_linea_archivo(nombre_archivo_invertir, "\t-" + array_sostenible[x+3][0] + "\n")		
		i=i+1
guardar_log("archivo invertir.txt cerrado")

#Creando archivo informe
crear_archivo("informe.txt")
guardar_log("archivo informe.txt creado y en ejecucion")
totales=str('TOTALES')
fortotales="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, fortotales % (totales))
for x in range (0,4):
	contenido_linea1 = ( 
		array_sostenible[x][0], array_suma[x][0],
	)
	formato_linea1 = "\t-%s %d\n"
	escribir_linea_archivo(nombre_archivo_informe, formato_linea1 % (contenido_linea1))

promedio=str('\nPROMEDIO'),
forprom="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, forprom % (promedio))		
for x in range (0,4):
	contenido_linea1 = (	
		array_sostenible[x][0], array_promedio[x][0],
	)
	formato_linea1 = "\t-%s %d\n"
	escribir_linea_archivo(nombre_archivo_informe, formato_linea1 % (contenido_linea1))
	
datlun=str('\nDATOS DEPARTAMENTOS'),
fordatlun="%s\n\n"
escribir_linea_archivo(nombre_archivo_informe, fordatlun % (datlun))
for x in range(0, archiv):
	contenido_linea2 = (
		array_depart[x][0],array_array[x][0],array_array[x][1],	
	)
	formato_linea2 = "\t-%s %s \t %s\n "
	escribir_linea_archivo(nombre_archivo_informe, formato_linea2 % (contenido_linea2))

guardar_log("archivo informe.txt cerrado")
guardar_log("programa terminado, abrir archivo informe.txt y invertir.txt")


