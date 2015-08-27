from SimPy.Simulation import *
from random import uniform

class Proceso(Process):

    # Construcctor, se crea el proceso, fijando su nombre y se fija la cantidad de instrucciones que tiene.
    def __init__(self,id):
        Process.__init__(self)
        self.instrucciones=random.randint(1,10)
        self.id=id
        
        # Esta funcion fija la cantidad de memoria RAM en el contenedor.
    def cargar(self,MemoriaRAM): 
        yield put, self, Memoria, MemoriaRAM

    
    # ESta funcion simula el proceso
    def Procesar(self,Velocidad, RAM,Araiving):
        yield hold,self,Araiving # Se espera a que sea el tiempo de llegada
        print "%5.1f %s is New, it has %d instructions and needs %d RAM" %(now(),self.id, self.instrucciones, RAM)
        yield get, self, Memoria, RAM # Se solicita memoria RAM
        print "%5.1f %s is Ready" %(now(),self.id)
                
        while (self.instrucciones > 0): # Este ciclo sigue mientras haya instrucciones
            
             #se solicita espacio en el CPU
            yield request,self,CPU
            print "%5.1f %s is Running " %(now(),self.id)
            
            if(self.instrucciones < Velocidad): # Si hay menos instrucciones de las que se pueden hacer por unidad de tiempo.
                yield hold,self,0.5 # El tiempo de corrida es menor
                self.instrucciones = 0
            else: # Si no, se espera una unidad de tiempo y se reducen la cantidad de instrucciones.
                yield hold,self,1
                self.instrucciones = self.instrucciones - Velocidad
            yield release,self,CPU # Se libera espacio en el CPU
            opcion = random.randint(1,2) # Se elige un numero al azar entre 1 y 2.
            if (self.instrucciones != 0):
                if (opcion == 1): # Si es 1, entonces el proceso debe esperar antes de volver al estado Ready
                    print "%5.1f %s is in Waiting " %(now(),self.id)
                    yield hold,self,3
                    print "%5.1f %s is Ready %d instrucctions left" %(now(),self.id,self.instrucciones)
                else: # Si es 2, puede volver a Ready inmediatamente
                     print "%5.1f %s is Ready %d instrucctions left" %(now(),self.id,self.instrucciones)
                
            
            
           
        yield put, self, Memoria, RAM # Cuando ya no hay instrucciones, se libera la memoria RAM y se termina el proceso.
        print "%5.1f %s is terminated------" %(now(),self.id)
        # Se calcula el tiempo que el proceso tardo en ejectarse.
        tiempoTotal = now() - Araiving
        wt.observe(tiempoTotal) 
        
wt=Monitor()
initialize()
#Variables que definen el funcionamiento del programa.
procesos = 50
Procesadores = 1
MemoriaRAM = 100
interval =10
velocidad = 3 # instrucciones por unidad de tiempo

#Se crean el CPU y la memoria RAM, el primero es una cola y el segundo es un contenedor.
CPU=Resource(capacity=Procesadores,qType=FIFO)
Memoria=Level(capacity=MemoriaRAM)

# Se crea este proceso solo para fijar la cantidad inicial de memoria RAM.
p1=Proceso(id="Process "+ str(0))
activate(p1,p1.cargar(MemoriaRAM))



for i in range(procesos):
    p=Proceso(id="Process "+ str(i+1)) # Se crea el proceso con su nombre
    #al activar cada proceso, se indica tiempo para llegar (Araiving)
    #y la cantidad de memoria que necesita (RAM)
    activate(p,p.Procesar(Velocidad = velocidad,RAM=random.randint(1,10),Araiving = random.expovariate(1.0 / interval)))
simulate(until=1000)

# Se obtiene la media y la varianza
print "Tiempo total en el procesador: \tmean = %5.1f, \n\t\tvariance=%2d"%(wt.mean(),wt.var()) 
