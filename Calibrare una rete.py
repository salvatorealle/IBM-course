#importar dependencias
import os
from  epanettools.epanettools import EPANetSimulation, Node, Link, Network
from epanettools.examples import simple
import numpy as np
import scipy
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt
import setPROPERTY


#leer la red
file = os.path.join(os.path.dirname(simple.__file__),'test.inp') 
es=EPANetSimulation(file)

#instanciar clases y metodos
cond=es.network.links
nod=es.network.nodes

#obtener la cantidad de conductos
ret,num_links=es.ENgetcount(es.EN_LINKCOUNT)  #numero de links

#leer propiedades de la red
diametros=Link.value_type['EN_DIAMETER']
scabrezze=Link.value_type['EN_ROUGHNESS']
presiones=Node.value_type['EN_PRESSURE']
flow=Link.value_type['EN_FLOW']
elevations=Node.value_type['EN_ELEVATION']
velocities=Link.value_type['EN_VELOCITY']


#Raccogliere ixs condotte in Cast Iron e listare le loro scabrezze
lista_IX_CI_PIPES=[]
for i in range(num_links):
      C=es.ENgetlinkvalue(i, scabrezze)
      if C[1] != 0 and 70<C[1]<101:
            lista_IX_CI_PIPES.append(i)
lista_RUG=[]
for i in lista_IX_CI_PIPES:
      C=es.ENgetlinkvalue(i, scabrezze)
      if C[1] != 0:
            lista_RUG.append(C[1])

#Ottenere l'indice del nodo da calibrare
es.run()
nodo_12_index=nod['5'].index
p12=nod[nodo_12_index].results[presiones][:24]
obj=[69.59861755371094, 69.14949798583984, 68.551025390625, 67.80951690673828, 66.9296875, 64.7691879272461, 58.91615676879883, 51.11674118041992, 54.2637825012207, 55.253944396972656, 58.91615676879883, 58.91615676879883, 58.91615676879883, 60.56578063964844, 62.09236145019531, 62.09236145019531, 62.09236145019531, 55.253944396972656, 51.11674118041992, 53.24409866333008, 55.253944396972656, 60.56578063964844, 64.7691879272461, 69.14949798583984]
rms = sqrt(mean_squared_error(obj, p12))

RMS=[]
if rms < 1 and (abs(min(obj)-min(p12)))<1:
      print("network calibrated")
      plt.plot(obj)
      plt.plot(p12)
      plt.ylabel('Pressure(m)')
      plt.show()
    
elif len(lista_IX_CI_PIPES)!= 0:
      plt.plot(obj)
      plt.plot(p12)
      plt.ylabel('Pressure(m)')
      plt.show()
      RMS =[]
      while (abs(min(obj)-min(p12)))>1:
            #modifica las rugosidades de los tubos en la red
            for i in range(int(min(lista_RUG)), 60, -1):
                  for j in lista_IX_CI_PIPES:
                      es.ENsetlinkvalue(j,scabrezze,i)
                      #import tempfile
                      #f=os.path.join(tempfile.gettempdir(),'new.inp')#NON FUNZIONA
                      #es.ENsaveinpfile(f)
                      #es2=EPANetSimulation(f)5
                  print (i)
                  es.run()    
                  p12=nod[nodo_12_index].results[presiones][:len(obj)]
                  rms = sqrt(mean_squared_error(obj, p12))
                  RMS.append(rms)
                  if rms<1 and (abs(min(obj)-min(p12)))<1:
                        print('Rugosidad aceptable=',i, ' rms=', rms)
                        import tempfile
                        f=os.path.join(tempfile.gettempdir(),'new.inp')
                        es.ENsaveinpfile(f)
                        es2=EPANetSimulation(f)
                        plt.plot(obj,  label="observed")
                        plt.plot(p12,  label="simulated")
                        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.) 
                        plt.ylabel('Pressure(m)')
                        plt.show()
                        break
            break
else:
      print("no pipes to calibrate") #verifica THV
if min(RMS)>1 or (abs(min(obj)-min(p12)))<1:
      print("min RMS ", min(RMS))
      plt.plot(obj,  label="observed")
      plt.plot(p12,  label="simulated")
      plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2, mode="expand", borderaxespad=0.) 
      plt.ylabel('Pressure(m)')
      plt.show()
      
      

      



        








