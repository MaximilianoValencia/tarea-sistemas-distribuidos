# Pre-proceso: Selecting variables for IDS


import numpy          as np
import inform_gain    as ig
import redundancy_svd as rsvd
import csv

# Load Parameters
def load_config():
    #cargar parametros de configuracion  del problema
    #param[0] numero de muestras
    #param[1] top-k de relevancia
    #param[2] nummero de vectores singulares
    #param[3] clase normal
    #param[4] clase DOS
    #param[5] clase Probe
    param = []
    with open("cnf_sv.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # checkeo que la fila no esté vacia
                param.append(row[0])  # Agregar primer ( y unico) elemento de la fila a lista
    return(param)
# Load data 
def load_data():
	#cargar datos de KDDTrain.txt y normalizarlos
    X = 0
    #usar rsvd.norm_data() ??
    return(X)

# selecting variables
def select_vars(X,param):
	#...
	return(0,0,0)#gain,idx,V

#save results
def save_results(gain,idx,V):
# Crear archivos de resultados
    #gain_values.csv Mx1
    #gain_idx.csv Mx1
    #filter_v.csv Matriz de vectores singulares izquierdos (?)
    return

#-------------------------------------------------------------------
# Beginning ...
def main():
    param        = load_config()            
    X            = load_data()   
    [gain, idx,  V]= select_vars(X,param)                 
    save_results(gain,idx,V)
       
if __name__ == '__main__':   
	 main()

#-------------------------------------------------------------------
