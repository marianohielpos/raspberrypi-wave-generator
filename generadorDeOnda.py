#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Generador de funciones para RPi

import RPi.GPIO as GPIO
import math
import time

pins = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16] #Pins físicos que se utilizan.
pins = pins[::-1]

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
    
    return tabla

def setearPins(numeroBinario):
#'''Recibe un numero binario indicando las posiciones que necesita prender'''

    for posicion in range( len( numeroBinario ) ):
        if numeroBinario[posicion] == "1":
            PrenderPin(posicion)        # settea los pins desde el most significant bit.
        else:
            ApagarPin(posicion)        # apaga los pins restantes
    return




def generarOnda( cantidadDePinsEntrada, frecuenciaEntrada, cicloDeTrabajoEntrada, ondaEntrada, cantidadDivisionesPeridoEntrada):

    GPIO.setwarnings(False)
    # to use Raspberry Pi board pin numbers  
    GPIO.setmode(GPIO.BOARD)
    # set up GPIO output channel
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)



    cantidadDivisionesPeriodo = cantidadDivisionesPeridoEntrada
    cantidadDePins = cantidadDePinsEntrada
    frecuencia = frecuenciaEntrada
    t = 1.0/(frecuencia*cantidadDivisionesPeriodo)
    cicloDeTrabajo = cicloDeTrabajoEntrada
    onda = ondaEntrada

    tablaSenoidal = GenerarTablaSenoidal(cantidadDePins, cantidadDivisionesPeriodo)
    tablaTriangular = GenerarTablaTriangular(cantidadDePins, cantidadDivisionesPeriodo)

    try:
        if onda == 'Senoidal':
            while True:
                for valor in tablaSenoidal:
                    setearPins(valor)
                    time.sleep(t)
        elif onda == 'Triangular':
            while True:    
                for valor in tablaTriangular:
                    setearPins(valor)
                    time.sleep(t)
        elif onda == 'Cuadrada':
            cicloDeTrabajo = cicloDeTrabajo
            up = (len(pins)-cantidadDePins)*'0' + cantidadDePins*'1'
            down = len(pins)*'0'
            timeUp = cicloDeTrabajo/(100.0*frecuencia)
            timeDown = (100 - cicloDeTrabajo)/(100.0 * frecuencia)
            while True:
                setearPins( up )
                time.sleep( timeUp )
                setearPins( down )
                time.sleep( timeDown )
    except SystemExit:
        GPIO.cleanup()
