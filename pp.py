# Pre-proceso: Selecting variables for IDS
import pandas as pd
import numpy          as np
import inform_gain    as ig
import redundancy_svd as rsvd
import csv
import itertools

pd.options.mode.chained_assignment = None  # default='warn'

# Load Parameters
def load_config():
    #cargar parametros de configuracion  del problema
    #param[0] N numero de muestras
    #param[1] top-k de relevancia
    #param[2] nro_svd nummero de vectores singulares
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
def load_data(param):
	#cargar datos de KDDTrain.txt y normalizarlos    
    # parametros de cnf_sv a variables
    N = param[0]
    top_k = param[1]
    nro_svd = param[2]
    clase_normal = param[3]
    clase_dos = param[4]
    clase_probe = param[5]

    dataframe = pd.read_csv('KDDTrain.txt', names=range(1,44))
    dataframe.index = np.arange(1, len(dataframe) + 1)
    idx_samples = pd.read_csv('idx_samples.csv', header=None)
    lst_idx_samples = idx_samples[0].values.tolist()
    dataframe = dataframe.loc[lst_idx_samples]

    # clasifica la columna 42 dependiendo del tipo de trafico en clase 1, 2 o 3
    if clase_normal == 1: #clase normal
        dataframe[42] = dataframe[42].replace('normal', 1)
    if clase_dos == 1: #clase DOS
        dataframe[42] = dataframe[42].replace(['neptune', 'teardrop', 'smurf', 'pod', 'back', 'land', 'apache2', 'processtable', 'mailbomb', 'udpstorm'], 2)
    if clase_probe == 1: #clase probe
        dataframe[42] = dataframe[42].replace(['ipsweep', 'portsweep', 'nmap','satan', 'saint', 'mscan'], 3)
    dataframe[42] = dataframe[42].apply(pd.to_numeric,errors='coerce') # transforma el trafico no perteneciente a ninguna clase a "NaN"
    dataframe= dataframe[dataframe[42].notna()] # se eliminan las clases que no aplican
    dataframe = dataframe.head(N)

    # convierte variables no-numericas a numericas
    dataframe[[2, 3, 4]] = dataframe[[2, 3, 4]].apply(lambda x: pd.factorize(x)[0])

    a = 0.01
    b = 0.99
    # normaliza cada variable de las columnas 1 a la 41
    dataframe.iloc[:, :41] = dataframe.iloc[:, :41].apply(lambda x: ((x-x.min())/(x.max()-x.min())*(b-a))+a)
    dataframe = dataframe.fillna(0)

    # re-ordena aleatoriamente las filas del dataframe
    dataframe = dataframe.sample(frac = 1)

    return dataframe

# selecting variables
def select_vars(df,param):
    N = param[0]
    top_k = param[1]
    nro_svd = param[2]
     
    x = pd.unique(df[42])
    x = x[~pd.isnull(x)].astype(int)
    m = x.size # cantidad de clases
    Y = 0
    for i in x:
        d_i = df[42].value_counts()[i] # numero de muestras de la i-esima clase
        p_i = d_i/N # probabilidad de la i-esima clase
        Y -= p_i*np.log2(p_i) # entropia de shannon

    B = (np.floor(np.sqrt(N))).astype(int) # numero de bins de la variable x en la data X
    #delta = (b-a)/(B-1)
    df2 = df.drop(columns=[42, 43])
    lst_e = []

    for (colname,colval) in df2.items():
        delta = (colval.max() - colval.min())/(B-1)
        e = 0

        for v in range(1, B+1):
            left_bound = (delta*(v-1))+a
            right_bound = (delta*v)+a
            bin = df[df[colname].between(left_bound, right_bound, inclusive="left")]
            x = pd.unique(bin[42])
            x = x[~pd.isnull(x)].astype(int)
            m = x.size # cantidad de clases
            s = 0
            d = 0

        for i in x:
            d_i = bin[42].value_counts()[i] # numero de muestras de la i-esima clase
            p_i = d_i/bin.shape[0] # probabilidad de la i-esima clase
            s -= p_i*np.log2(p_i) # entropia de shannon
            d += d_i
            e += (d/N)*s

        lst_e.append(e)

    xy = []
    for e in lst_e:
        xy.append(Y-e)
    d_xy = dict(enumerate(xy))
    d_xy = dict(sorted(d_xy.items(), key = lambda x: x[1], reverse = True))
    d_top_k = dict(itertools.islice(d_xy.items(), top_k))
    key_list = keysList = list(d_top_k.keys())
    key_list = [x+1 for x in key_list]
    key_list.sort()
    new_df = df[key_list]

    for (colname,colval) in new_df.items():
        x_mean = new_df[colname].mean()
        new_df[colname] = new_df[colname].apply(lambda x : x-x_mean)
    new_df

    # normaliza la data de X
    Y_df = new_df/(np.sqrt(N-1))
    Y_df

    svd_Y = np.linalg.svd(Y_df)
    U, S, V = svd_Y

    top_k_V = np.delete(V, slice(nro_svd, None, None) ,axis=1)
    X=np.matmul(new_df.to_numpy(),top_k_V)
    X_df = pd.DataFrame(X)  
    
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
    X            = load_data(param)   
    [gain, idx,  V]= select_vars(X,param)                 
    save_results(gain,idx,V)
       
if __name__ == '__main__':   
	 main()

#-------------------------------------------------------------------
