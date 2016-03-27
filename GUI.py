#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from multiprocessing import *
from generadorDeOnda import *

class App(object):

    def __init__(self, master = Tk()):
        
        self.thread = None
        
        self.master = master
        master.title("Generador de ondas")

        """Agrupa todo"""
        self.opciones = Frame(self.master)
        self.opciones.pack()

        """Botones en el frame"""
        self.botonSalir = Button(
            self.opciones, text="Salir", fg="red", command=self.salir
            )
        self.botonSalir.grid(row = 0, column = 0)
        
        self.botonEjecutar = Button(
            self.opciones, text="Ejecutar", fg="blue", command=self.ejecutarOnda
            )
        self.botonEjecutar.grid(row = 0, column = 1)
        
        self.botonDetener = Button(
            self.opciones, text="Detener", fg="blue", command=self.pararOnda
            )
        self.botonDetener.grid(row = 0, column = 2)


        """Listas mas etiquetas en el frame"""
        #Columna 1
        self.nombreColumnaUno = Label(self.opciones, text = "Lista de ondas")
        self.nombreColumnaUno.grid(row = 1, column = 0)
        self.listaOndas = Listbox(self.opciones, selectmode=SINGLE, height = 11, exportselection = 0)
        for onda in ["Cuadrada", "Senoidal", "Triangular"]:
            self.listaOndas.insert(END, onda)
        self.listaOndas.grid(row = 2, column = 0)
        
        #Columna 2
        self.nombreColumnaDos = Label(self.opciones, text = "Ciclo de trabajo (%)")
        self.nombreColumnaDos.grid(row = 1, column = 1)
        self.listaCicloDeTrabajo = Listbox(self.opciones, selectmode=SINGLE, height = 11, exportselection = 0)
        for cicloDeTrabajo in xrange(0,101,10):
            self.listaCicloDeTrabajo.insert(END, cicloDeTrabajo)
        self.listaCicloDeTrabajo.grid(row = 2, column = 1)
        
        #Columna 3
        self.nombreColumnaTres = Label(self.opciones, text = "Cantidad de pines")
        self.nombreColumnaTres.grid(row = 1, column = 2)
        self.listaCantidadDePines = Listbox(self.opciones, selectmode=SINGLE, height = 11, exportselection = 0)
        for pin in xrange(1,11):
            self.listaCantidadDePines.insert(END, pin)
        self.listaCantidadDePines.grid(row = 2, column = 2)
        
        #Columna 4
        self.nombreColumnaCuatro = Label(self.opciones, text = "Número de muestreo")
        self.nombreColumnaCuatro.grid(row = 1, column = 3)
        self.listaNumeroDeMuestreo = Listbox(self.opciones, selectmode=SINGLE, height = 11, exportselection = 0)
        for numeroDeMuestreo in xrange(11):
            self.listaNumeroDeMuestreo.insert(END, 2**numeroDeMuestreo)
        self.listaNumeroDeMuestreo.grid(row = 2, column = 3)
        
        #Columna 5
        self.nombreColumnaCinco = Label(self.opciones, text = "Frecuencia (Hz)")
        self.nombreColumnaCinco.grid(row = 1, column = 4)
        self.listaNumeroFrecuencia = Listbox(self.opciones, selectmode=SINGLE, height = 11, exportselection = 0)
        valor = 5
        for onda in xrange(11):
            self.listaNumeroFrecuencia.insert(END, valor)
            valor = valor * 2
        self.listaNumeroFrecuencia.grid(row = 2, column = 4)
        
    def mainloop(self):
        self.master.mainloop()
        
    def salir(self):
        self.pararOnda()
        self.opciones.quit()
        
    def pararOnda(self):
        if self.thread != None :
            self.thread.terminate()
            GPIO.cleanup()
            self.thread = None
    
    
    def ejecutarOnda(self):
    
        self.pararOnda()
    
        tipoDeOnda = self.listaOndas.curselection()
        tipoDeOnda = self.listaOndas.get(tipoDeOnda[0])
        
        cicloDeTrabajo = self.listaCicloDeTrabajo.curselection()
        cicloDeTrabajo = self.listaCicloDeTrabajo.get(cicloDeTrabajo[0])
        
        cantidadDePines = self.listaCantidadDePines.curselection()
        cantidadDePines = self.listaCantidadDePines.get(cantidadDePines[0])
        
        numeroDeMuestreo = self.listaNumeroDeMuestreo.curselection()
        numeroDeMuestreo = self.listaNumeroDeMuestreo.get(numeroDeMuestreo[0])
        
        numeroFrecuencia = self.listaNumeroFrecuencia.curselection()
        numeroFrecuencia = self.listaNumeroFrecuencia.get(numeroFrecuencia[0])
        
        argumentos = (cantidadDePines, numeroFrecuencia, cicloDeTrabajo, tipoDeOnda, numeroDeMuestreo)
        

        
        self.thread = Process(target = generarOnda, args = argumentos)
        self.thread.start()
        
        
        return
    
        
"""Comienzo del programa"""   
app = App()

app.mainloop()

