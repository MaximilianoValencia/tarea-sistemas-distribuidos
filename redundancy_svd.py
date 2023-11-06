# My Utility : 

import numpy  as np   

# normalization of the data
def norm_data():
    x = pd.unique(dataframe[42])
    x = x[~pd.isnull(x)].astype(int)
    m = x.size # cantidad de clases
    Y = 0
    for i in x:
        d_i = dataframe[42].value_counts()[i] # numero de muestras de la i-esima clase
        p_i = d_i/N # probabilidad de la i-esima clase
        Y -= p_i*np.log2(p_i) # entropia de shannon
    
    return()

# SVD of the data
def svd_data():
    #...    
    return()



#-----------------------------------------------------------------------
