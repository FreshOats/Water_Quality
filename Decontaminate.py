def Decontaminate_Labels(df_list):
    for df in df_list:
        df.rename(columns={df.columns[0]: "Contaminant",
                        df.columns[1]: "State_MCL",
                        df.columns[2]: "State_DLR",
                        df.columns[3]: "State_PHG",
                        df.columns[4]: "PHG_Date",
                        df.columns[5]: "Federal_MCL",
                        df.columns[6]: "Federal_MCLG"
                        }, inplace=True)
    return df_list
        

def Decontaminate_Rows(df_list):
    for n in range(len(df_list)):
        df_list[n].dropna(subset=['State_MCL'], how='all', inplace=True)
        df_list[n] = df_list[n].loc[df_list[n].State_MCL != 'MCL']
        df_list[n] = df_list[n].loc[df_list[n].State_MCL != 'mrem/yr']
        df_list[n]['Units'] = 'mg/L'
    return df_list


def Decontaminate_Lists(df_list): 
    for n in range(len(df_list)):
        if n == 4:
            df_list[n].drop(columns='PHG_Date', inplace=True)
            df_list[n].rename(columns={'Federal_MCL': 'PHG_Date',
                            'Federal_MCLG': 'Federal_MCL',
                            'Federal\rMCLG': 'Federal_MCLG'}, inplace=True)
        elif n == 7:
            df_list[n].drop(columns='State_DLR', inplace=True)
            df_list[n].rename(columns={'State_PHG': 'State_DLR',
                            'PHG_Date': 'State_PHG',
                            'Federal_MCL': 'PHG_Date',
                            'Federal_MCLG': 'Federal_MCL',
                            'Federal\rMCLG': 'Federal_MCLG'}, inplace=True)
        elif n == 11:
            df_list[n].drop(columns='Federal_MCLG', inplace=True)
            df_list[n].rename(columns={'Federal\rMCLG': 'Federal_MCLG'}, inplace=True)
    return df_list


def Decontaminate(filename):
    from tabula import read_pdf
    from tabulate import tabulate
    import pandas as pd
    
    df_list = read_pdf(filename, pages='all')
    Decontaminate_Labels(df_list)
    Decontaminate_Rows(df_list)
    Decontaminate_Lists(df_list)
    df_concat = pd.concat(df_list, ignore_index=True)
    return df_concat