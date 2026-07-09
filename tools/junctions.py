import pandas as pd

def juntar_dataframes_merge(df1, df2, col1, col2, how="inner"):
    """
    Realiza o merge de dois dataframes baseados em colunas chave.
    """
    return pd.merge(df1, df2, left_on=col1, right_on=col2, how=how)

def juntar_dataframes_concat(df_list, axis=0):
    """
    Concatena uma lista de dataframes (empilhar tabelas).
    """
    return pd.concat(df_list, axis=axis, ignore_index=True)