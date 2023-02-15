####################################################
# Decontaminate.py                                ##
# To use, import Decontaminate from Decontaminate ##
####################################################

# Decontaminate takes a pdf filename containing tables of values and returns a single dataframe 

# The function utilizes the following subroutines: 
## Decontaminate_Labels - makes meaningful headers
## Decontaminate_Nulls - converts missing values to nulls
## Decontaminate_Rows - adds units and removes rows without data
## Decontaminate_Lists - fixes the dfs where the columns were incorrectly shifted
## Decontaminate_Values - fixes the erroneous formats and values within each df
## Decontaminate_Datatypes - changes datatypes from string to numeric where appropriate

#####################################################
################### Subroutines #####################
# The input to these functions is a list of dataframes
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
        
# Fix the cases where '--' was used instead of a Null
def Decontaminate_Nulls(df_list): 
    import numpy as np
    for df in df_list:
        df.replace('--', np.nan, inplace=True)
    return df_list

# Drop the rows that are subheaders in the individual tables or with Null Required levels
def Decontaminate_Rows(df_list):
    for n in range(len(df_list)):
        df_list[n].dropna(subset=['State_MCL'], how='all', inplace=True)
        df_list[n] = df_list[n].loc[df_list[n].State_MCL != 'MCL']
        df_list[n] = df_list[n].loc[df_list[n].State_MCL != 'mrem/yr']
        df_list[n]['Units'] = 'mg/L'
    return df_list

# Adjust the column shifts in dfs 4, 7, and 11 so values are aligned properly
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
            df_list[n].rename(
                columns={'Federal\rMCLG': 'Federal_MCLG'}, inplace=True)
    return df_list

# Fix the individual dfs based on the issuers with inputs, missing values, and strings in numerical entries
def Decontaminate_Values(df_list):
    import numpy as np
    for n in range(len(df_list)):
        if n == 0:
            # Fixes the string zero to numerical
            df_list[n].loc[4, ["Federal_MCLG"]] = [0]
            df_list[n].loc[5, ["Contaminant", "State_MCL", "State_DLR", "State_PHG", "PHG_Date", "Federal_MCL", "Federal_MCLG", "Units"]] = [
                'Asbestos', 7.0, 0.2, 7.0, 2003, 7.0, 7.0, 'MFL']  # Removes the units from every value to numerical values
            # Changes long text to just chromium, total - changes 'witdrawn' to Null
            df_list[n].loc[12, ["Contaminant", "State_PHG"]] = ['Chromium, Total', np.nan]
        elif n == 1:
            df_list[n].loc[0, ["Contaminant"]] = ['Chromium, Hexavalent']
            df_list[n].loc[3, ["Contaminant", "PHG_Date"]] = ['Mercury', 2005]
            df_list[n].loc[5, ["Contaminant", "State_MCL", "State_PHG", "Units"]] = [
                'Nitrate', 10, 45, '10 as N mg/L']
            df_list[n].loc[6, ["Contaminant", "State_MCL", "State_PHG", "Units"]] = [
                'Nitrite', 1, 1, '1 as N mg/L']
            df_list[n].loc[7, ["Contaminant", "State_MCL", "State_PHG", "Units"]] = [
                'Nitrate + Nitrite', 10, 10, '10 as N mg/L']
            df_list[n].loc[10, ["PHG_Date"]] = [2004]
        elif n == 2:
            df_list[n].loc[3, ["Federal_MCLG"]] = [0.0]
        elif n == 3:
            df_list[n].loc[2, ["Contaminant", "State_PHG", "PHG_Date", "Federal_MCLG", "Units"]] = [
                "Gross Alpha Particle", np.nan, np.nan, 0.0, 'pCi/L']
            df_list[n].loc[7, ["Contaminant", "State_PHG", "PHG_Date", "Federal_MCLG", "Units"]] = [
                "Gross Beta Particle", np.nan, np.nan, 0.0, 'pCi/L']
            df_list[n].loc[14, ["Contaminant", "Federal_MCLG", "Units"]] = [
                'Radium-226 + Radium-228', 0.0, 'pCi/L']
        elif n == 4:
            df_list[n].loc[0, ["Units"]] = ['pCi/L']
            df_list[n].loc[1, ["State_MCL", "State_DLR", "State_PHG", "Units"]] = [20000, 1000, 400, 'pCi/L']
            df_list[n].loc[2, ["Federal_MCL", "Federal_MCLG", 'Units']] = [
                30, 0.0, 'pCi/L (ug/L for Federal_MCL)']
        elif n == 5:
            df_list[n].loc[0, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[1, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[2, ["PHG_Date"]] = [2009]
            df_list[n].loc[3, ["Contaminant"]] = ['1,4-Dichlorobenzene(p-DCB)']
            df_list[n].loc[4, ["Contaminant"]] = ['1,1-Dichloroethane (1,1-DCA)']
            df_list[n].loc[5, ["Contaminant", "PHG_Date", "Federal_MCLG"]] = [
                '1,2-Dichloroethane (1,2-DCA)', 2005, 0.0]
            df_list[n].loc[6, ["Contaminant"]] = [
                '1,1-Dichloroethylene (1,1-DCE)']
        elif n == 6:
            df_list[n].loc[1, ["Contaminant"]] = ['trans-1,2-Dichloroethylene']
            df_list[n].loc[2, ["Contaminant", "Federal_MCLG"]] = [
                'Dichloromethane (Methylene chloride)', 0.0]
            df_list[n].loc[3, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[4, ["PHG_Date"]] = [2006]
            df_list[n].loc[6, ["Contaminant"]] = [
                'Methyl tertiary butyl ether (MTBE)']
            df_list[n].loc[9, ["Contaminant"]] = ['1,1,2,2-Tetrachloroethane']
            df_list[n].loc[10, ["Contaminant", "Federal_MCLG"]] = [
                'Tetrachloroethylene (PCE)', 0.0]
        elif n == 7:
            df_list[n].loc[0, ["Contaminant"]] = [
                '1,1,1-Trichloroethane (1,1,1-TCA)']
            df_list[n].loc[1, ["Contaminant"]] = [
                '1,1,2-Trichloroethane (1,1,2-TCA)']
            df_list[n].loc[2, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[3, ["Contaminant"]] = [
                'Trichlorofluoromethane (Freon 11)']
            df_list[n].loc[4, ["Contaminant", "PHG_Date"]] = [
                '1,1,2-Trichloro-1,2,2-Trifluoroethane (Freon 113)', 2011]
            df_list[n].loc[5, ["Federal_MCLG"]] = [0.0]
        elif n == 8:
            df_list[n].loc[0, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[2, ["PHG_Date"]] = [2009]
        elif n == 9:
            df_list[n].loc[0, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[2, ["PHG_Date", "Federal_MCLG"]] = [2006, 0.0]
            df_list[n].loc[3, ["PHG_Date"]] = [2009]
            df_list[n].loc[4, ["Contaminant", "Federal_MCLG"]] = [
                '1,2-Dibromo-3-chloropropane (DBCP)', 0.0]
            df_list[n].loc[5, ["Contaminant"]] = [
                '2,4-Dichlorophenoxyacetic acid (2,4-D)']
            df_list[n].loc[6, ["Contaminant"]] = ['Di(2-ethylhexyl)adipate']
            df_list[n].loc[7, ["Contaminant", "Federal_MCLG"]] = [
                'Di(2-ethylhexyl)phthalate (DEHP)', 0.0]
            df_list[n].loc[8, ["PHG_Date"]] = [2010]
        elif n == 10:
            df_list[n].loc[1, ["Contaminant", "Federal_MCL", "Federal_MCLG"]] = [
                'Ethylene dibromide (EDB)', 0.00005, 0.0]
            df_list[n].loc[3, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[4, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[5, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[6, ["Contaminant"]] = ['Hexachlorocyclopentadiene']
            df_list[n].loc[7, ["PHG_Date"]] = [2005]
            df_list[n].loc[11, ["Federal_MCLG"]] = [0.0]
        elif n == 11:
            df_list[n].loc[0, ["Contaminant", "Federal_MCLG"]] = [
                'Polychlorinated biphenyls (PCBs)', 0.0]
            df_list[n].loc[3, ["Federal_MCLG"]] = [0.0]
            df_list[n].loc[4, ["Contaminant", "State_MCL", "State_DLR"]] = [
                '1,2,3-Trichloropropane', 0.000005, 0.000005]
            df_list[n].loc[5, ["Contaminant", "State_MCL", "State_DLR", "State_PHG", "Federal_MCL",
                               "Federal_MCLG"]] = ['2,3,7,8-TCDD (dioxin)', 3.0e-8, 5.0e-9, 5.0e-11, 3.0e-8, 0.0]
        elif n == 13:
            df_list[n].loc[2, ["Contaminant"]] = [
                'Haloacetic Acids (five) (HAA5)']
            df_list[n].loc[8, ["State_DLR", "Federal_MCLG"]] = [0.0050, 0.0]
    return df_list

# Change the datatypes from string to numeric
def Decontaminate_Datatypes(df):
    import pandas as pd
    df.State_MCL = pd.to_numeric(df.State_MCL)
    df.State_DLR = pd.to_numeric(df.State_DLR)
    df.State_PHG = pd.to_numeric(df.State_PHG)
    df.Federal_MCL = pd.to_numeric(df.Federal_MCL)
    df.Federal_MCLG = pd.to_numeric(df.Federal_MCLG)
    return df 


#####################################################
################### Main Function ###################
def Decontaminate(filename):
    from tabula import read_pdf
    from tabulate import tabulate
    import pandas as pd

    df_list = read_pdf(filename, pages='all')
    Decontaminate_Labels(df_list)
    Decontaminate_Nulls(df_list)
    Decontaminate_Rows(df_list)
    Decontaminate_Lists(df_list)
    Decontaminate_Values(df_list)
    df = pd.concat(df_list, ignore_index=True)
    Decontaminate_Datatypes(df)
    return df