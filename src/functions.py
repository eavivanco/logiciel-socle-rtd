import pandas as pd

def processor(xls, client):
    months = months_list(xls.sheet_names)
    i = 0
    for month in months:
        
        # se crea la máscara
        df_mask = pd.read_excel(xls, month)
        df_mask = mask(df_mask)

        # se procesa el archivo
        df = pd.read_excel(xls, month)
        df_filt, index = cleaner(df)
        df_filled = filler(df_filt, index)
        df_output = output(df_mask, df_filled, index)

        # se crea el output
        i += 1
        df_output.to_excel(f"{client}/{i}_{month}.xlsx", sheet_name=month)
        #df_output.to_csv(f"{client}/{month}.csv")
    return None


def mask(pre_df):
    clmns = ["Monto","Descripcion1", "Descripcion2", "Detalle", "Fecha", "Numero", "Sucursal1", "Sucursal2", "Cargo/Abono"]
    pre_df.columns = clmns
    return pre_df

def months_list(xls):
    months = []
    for month in xls:
        months.append(month)
    print(months)
    return months

def cleaner(pre_df):
    clmns = ["Monto","Descripcion1", "Descripcion2", "Detalle", "Fecha", "Numero", "Sucursal1", "Sucursal2", "Cargo/Abono"]
    pre_df.columns = clmns

    index = pre_df.index
    condition = pre_df["Monto"] == "MONTO"
    index = index[condition] 

    df_filt = pre_df.iloc[index[0]+1:index[1]-1]
    for i in range(index[0]+1, index[1]-1):
        df_filt["Descripcion1"][i] = df_filt["Descripcion1"][i].replace(' ','').replace('.','').replace('-','').replace('°','')
        df_filt["Descripcion1"][i] = df_filt["Descripcion1"][i].lower()
        df_filt["Detalle"][i] = "na"
    return df_filt, index

def filler(df_filt, index):
    for i in range(index[0]+1, index[1]-1):
        ingresos(df_filt, i)
        egresos(df_filt, i)  
    return df_filt

def output(df, df_filled, index):
    for i in range(index[0]+1, index[1]-1):
        df["Detalle"][i] = df_filled["Detalle"][i]
    return df

def egresos(df_filt, pos):
    honorarios(df_filt, pos)
    pasivo(df_filt, pos)
    remuneracion(df_filt, pos)
    
    fraude(df_filt, pos)
    sii(df_filt, pos)
    previred(df_filt, pos)
    
    proveedores(df_filt, pos)
    
    gastos(df_filt, pos) # gasto como ultimo
    return df_filt

def ingresos(df_filt, pos):
    clientes(df_filt, pos)
    beneficios(df_filt, pos)
    return df_filt

def clientes(df_filt, pos):
    clientes = ["bnppar", "alton", "documentootros", "ubs", "black", "transf"]
    for cli in clientes:
        if (cli in df_filt["Descripcion1"][pos]) and (df_filt["Monto"][pos] > 0) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Cliente"
    return df_filt

def proveedores(df_filt, pos):
    proveedores = ["mantencion", "transf", "entel", "servicios", "77030755", "77030117"]
    for prov in proveedores:
        if (prov in df_filt["Descripcion1"][pos]) and (df_filt["Monto"][pos] < 0) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Pago Proveedores"
    return df_filt

def gastos(df_filt, pos):
    gastos = ["credito", "crédito", "transf"]
    for gas in gastos:
        if (gas in df_filt["Descripcion1"][pos]) and (df_filt["Monto"][pos] < 0) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Rendición de Gastos"
    return df_filt

def remuneracion(df_filt, pos):
    remuneracion = ["14096", "remun"]
    for remu in remuneracion:
        if (remu in df_filt["Descripcion1"][pos]) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Pago Remuneracion"
    return df_filt

def beneficios(df_filt, pos):
    beneficio = "bene"
    if (beneficio in df_filt["Descripcion1"][pos]) and (len(str(df_filt["Detalle"][pos])) < 3):
        df_filt["Detalle"][pos] = "Pago Remuneracion"
    return df_filt

def honorarios(df_filt, pos):
    honorarios = ["19794","19794"]
    for hon in honorarios:
        if (hon in df_filt["Descripcion1"][pos]) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Pago Honorarios"
    return df_filt

def fraude(df_filt, pos):
    fraude = "fraude"
    if (fraude in df_filt["Descripcion1"][pos]) and (len(str(df_filt["Detalle"][pos])) < 3):
        df_filt["Detalle"][pos] = "Seguro fraude"
    return df_filt

def sii(df_filt, pos):
    sii = "sii"
    if (sii in df_filt["Descripcion1"][pos]) and (len(str(df_filt["Detalle"][pos])) < 3):
        df_filt["Detalle"][pos] = "Pago Impuestos"
    return df_filt

def pasivo(df_filt, pos):
    pasivo = ["cuota", "comercial"]
    for pas in pasivo:
        if (pas in df_filt["Descripcion1"][pos]) and (df_filt["Monto"][pos] < 0) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Pasivo (cargo)"
        elif (pas in df_filt["Descripcion1"][pos]) and (df_filt["Monto"][pos] < 0) and (len(str(df_filt["Detalle"][pos])) < 3):
            df_filt["Detalle"][pos] = "Pasivo (abono)"
    return df_filt

def previred(df_filt, pos):
    previred = "previred"
    if (previred in df_filt["Descripcion1"][pos]) and (len(str(df_filt["Detalle"][pos])) < 3):
        df_filt["Detalle"][pos] = "Pago Cotizaciones"
    return df_filt

    