import pandas as pd
from functions import processor

# vars
client = "out"
file_name = 'Noviembre.xlsx'

# doc
xls = pd.ExcelFile(f'in/{file_name}')

# debug
#df_mask = pd.read_excel(xls, "Enero")
#clmns = ["Monto","Descripcion1", "Descripcion2", "Detalle", "Fecha", "Numero", "Sucursal1", "Sucursal2", "Cargo/Abono"]
#df_mask.columns = clmns

#exe
processor(xls, client)


    