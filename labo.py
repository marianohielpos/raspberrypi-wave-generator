#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Generador de funciones para RPi

import RPi.GPIO as GPIO
import math
import time

GPIO.cleanup()

pins = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16] #Pins físicos que se utilizan.
pins = pins[::-1]
CANT_DIV_PERIODO = 64.0

def PrenderPin(pin):
#'''Enciende el pin dado'''
    return GPIO.output(pins[pin],GPIO.HIGH)
    
def ApagarPin(pin):
#'''Apaga el pin dado'''
    return GPIO.output(pins[pin],GPIO.LOW)
    
def GenerarTablaSenoidal( cantidadDePins, cantidadDivisionesPeriodo ):

    tabla = []    
    amplitudMaxima = ( 2 ** cantidadDePins - 1 )/2
    
    for division in xrange(int( cantidadDivisionesPeriodo) ):
        valorDeLaFuncion = int( round (amplitudMaxima * math.sin( division * 2 * math.pi/(cantidadDivisionesPeriodo)) + amplitudMaxima ))
        #print(str(valorDeLaFuncion) + " " + str(amplitudMaxima) + " " + str(division))
        valorDeLaFuncionEnBinario = bin( valorDeLaFuncion )[2::]
        valorDeLaFuncionEnBinario = (cantidadDePins - len(valorDeLaFuncionEnBinario)) * "0" + valorDeLaFuncionEnBinario
        tabla.append( valorDeLaFuncionEnBinario )
       
    return tabla
    

def GenerarTablaTriangular( cantidadDePins, cantidadDivisionesPeriodo ):

    tabla = []    
    amplitudMaxima = ( 2 ** cantidadDePins - 1)/2
    
    for division in xrange(int (cantidadDivisionesPeriodo/2) ):
        valorDeLaFuncion = int( 2 * amplitudMaxima * (division * 2/cantidadDivisionesPeriodo) )
        valorDeLaFuncionEnBinario = bin( valorDeLaFuncion )[2::]
        valorDeLaFuncionEnBinario = (cantidadDePins - len(valorDeLaFuncionEnBinario)) * "0" + valorDeLaFuncionEnBinario
        tabla.append( valorDeLaFuncionEnBinario )
    
    for valor in tabla[::-1]:
        tabla.append(valor)
    
    #tabla = tabla[0:len(tabla)-1:]
    
    return tabla

def setearPins(numeroBinario):
#'''Recibe un numero binario indicando las posiciones que necesita prender'''
    posicion = 0
    for numero in numeroBinario:
        if numero == "1":
            PrenderPin(posicion)        # settea los pins desde el most significant bit.
        else:
            ApagarPin(posicion)        # apaga los pins restantes
        posicion = posicion + 1
    return


# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)




#Inicio del programa

cantidadDePins = input('Introduzca cantidad de pins a utilizar: ')
while ((cantidadDePins>10) or (cantidadDePins<1)):
    cantidadDePins = input('Introduzca cantidad de pins a utilizar (1-10): ')

frecuencia = input('Introduzca frecuencia deseada (en Hz): ')
frecuencia = frecuencia
t = 10.0/(frecuencia*CANT_DIV_PERIODO)
cicloDeTrabajo = -1.0

onda = raw_input('Opciones posibles: "senoidal" "triangular" "cuadrada"\nIntroduzca onda deseada: ')

tablaSenoidal = GenerarTablaSenoidal(cantidadDePins, CANT_DIV_PERIODO)
tablaTriangular = GenerarTablaTriangular(cantidadDePins, CANT_DIV_PERIODO)

try:
    if onda == 's' or onda == 'senoidal':
        while True:
            for valor in tablaSenoidal:
                setearPins(valor)
                time.sleep(t)
    elif onda == 't' or onda == 'triangular':
        while True:    
            for valor in tablaTriangular:
                setearPins(valor)
                time.sleep(t)
    elif onda == 'c' or onda == 'cuadrada':
        while ((cicloDeTrabajo < 0) or (cicloDeTrabajo > 100)):
            cicloDeTrabajo = input('Introduzca ciclo de trabajo deseado (0-100): ')
        cicloDeTrabajo = float( cicloDeTrabajo )
        up = cantidadDePins*'1'
        down = cantidadDePins*'0'
        timeUp = cicloDeTrabajo/(100.0*frecuencia)
        timeDown = (100 - cicloDeTrabajo)/(100.0 * frecuencia)
        while True:
            #a = time.time()
            setearPins( up )
            time.sleep( timeUp )
            setearPins( down )
            time.sleep( timeDown )
            #print time.time() - a
    else:
        up = cantidadDePins * '1'
        setearPins( up )
        time.sleep(600)

except KeyboardInterrupt:
    pass
    
 

GPIO.cleanup()


