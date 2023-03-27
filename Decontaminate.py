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
# Although the units of the standards table were given in mg/L, almost every measurement was in ug/L or both ug/L 
# and mg/L - converting everything to ug/L and then converting back for those that only use mg/L

def Decontaminate_Rows(df_list):
    for n in range(len(df_list)):
        df_list[n].dropna(subset=['State_MCL'], how='all', inplace=True)
        df_list[n] = df_list[n].loc[df_list[n].State_MCL != 'MCL']
        df_list[n] = df_list[n].loc[df_list[n].State_MCL != 'mrem/yr']
        df_list[n]['Units'] = 'ug/L'
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


##################
# Before changing the individual row values, I need to multiply the State_MCL, State_DLR, State_PGH, Federal_MCL, and Federal_MCLG by 1000 using
# df['Quantity'] = df['Quantity'].apply(lambda x: x*1000)

# Then I have to go back and convert the values that are incorrect with the following function
# The values that should definitely be only mg/L: Cyanide, Dissolved Fluoride


##################



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
            df_list[n].loc[3, ["Contaminant", "State_MCL", "State_DLR", "State_PHG", "PHG_Date", "Federal_MCL", "Federal_MCLG", 'Units']] = ['Mercury', 2, 1, 1.2, 2005, 2, 2, 'ug/L']
            df_list[n].loc[5, ["Contaminant", "State_MCL", "State_PHG", "Units"]] = [
                'Nitrate', 1, 4.5, 'mg/L as N']
            df_list[n].loc[6, ["Contaminant", "State_MCL", "State_PHG", "Units"]] = [
                'Nitrite', 1, 1, 'mg/L as N']
            df_list[n].loc[7, ["Contaminant", "State_MCL", "State_PHG", "Units"]] = [
                'Nitrate + Nitrite', 1, 1, 'mg/L as N']
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
            df_list[n].loc[0, ["State_MCL", "State_DLR", "State_PHG"]] = [4.0, 1.0, 0.175]
            df_list[n].loc[1, ["State_MCL", "State_DLR", "State_PHG", "Units"]] = [20000, 1000, 400, 'pCi/L']
            df_list[n].loc[2, ["State_MCL", "State_DLR", "State_PHG", "Federal_MCL", "Federal_MCLG", 'Units']] = [30.0, 1.5, 0.64, 30, 0.0, 'ug/L']
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
            df_list[n].loc[7, ["Contaminant", "Federal_MCLG"]] = ['Di(2-ethylhexyl)phthalate (DEHP)', 0.0]
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
                '1,2,3-Trichloropropane', 0.005, 0.005]
            df_list[n].loc[5, ["Contaminant", "State_MCL", "State_DLR", "State_PHG", "Federal_MCL",
                               "Federal_MCLG", 'Units']] = ['2,3,7,8-TCDD (dioxin)', 30.0, 5.0, .05, 30.0, 0.0, 'pg/L']
        elif n == 13:
            df_list[n].loc[2, ["Contaminant"]] = [
                'Haloacetic Acids (five) (HAA5)']
            df_list[n].loc[8, ["State_DLR", "Federal_MCLG"]] = [5.0, 0.0]
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


# Adjust the names to match the naming conventions on the measured data
def Decontaminate_Names(df):
    df.loc[0, ['Contaminant']] = ['Dissolved Aluminum']
    df.loc[1, ['Contaminant']] = ['Dissolved Antimony']
    df.loc[2, ['Contaminant']] = ['Dissolved Arsenic']
    df.loc[3, ['Contaminant']] = ['Asbestos, Chrysotile']
    df.loc[4, ['Contaminant']] = ['Dissolved Barium']
    df.loc[5, ['Contaminant']] = ['Dissolved Beryllium']
    df.loc[6, ['Contaminant']] = ['Dissolved Cadmium']
    df.loc[7, ['Contaminant']] = ['Total Chromium']
    df.loc[8, ['Contaminant']] = ['Cyanide']
    df.loc[9, ['Contaminant']] = ['Dissolved Fluoride']
    df.loc[10, ['Contaminant']] = ['Dissolved Mercury']
    df.loc[11, ['Contaminant']] = ['Dissolved Nickel']
    df.loc[12, ['Contaminant']] = ['Dissolved Nitrate']
    df.loc[13, ['Contaminant']] = ['Dissolved Nitrite']
    df.loc[14, ['Contaminant']] = ['Dissolved Nitrate + Nitrite']
    df.loc[16, ['Contaminant']] = ['Dissolved Selenium']
    df.loc[17, ['Contaminant']] = ['Dissolved Thallium']
    df.loc[18, ['Contaminant']] = ['Dissolved Copper']
    df.loc[19, ['Contaminant']] = ['Dissolved Lead']
    df.loc[23, ['Contaminant']] = ['Dissolved Strontium']
    df.loc[25, ['Contaminant']] = ['Dissolved Uranium']
    df.loc[27, ['Contaminant']] = ['Carbon tetrachloride']
    df.loc[28, ['Contaminant']] = ['1,2-Dichlorobenzene']
    df.loc[29, ['Contaminant']] = ['1,4-Dichlorobenzene']
    df.loc[30, ['Contaminant']] = ['1,1-Dichloroethane']
    df.loc[31, ['Contaminant']] = ['1,2-Dichloroethane']
    # Note that Dichloroethylene and Dichloroethene are the same chemical compound
    df.loc[32, ['Contaminant']] = ['1,1-Dichloroethene']
    df.loc[33, ['Contaminant']] = ['cis-1,2-Dichloroethene']
    df.loc[34, ['Contaminant']] = ['trans-1,2-Dichloroethene']
    # This was listed as Dichloromethane(Metheylene Chloride), the labs use the latter
    df.loc[35, ['Contaminant']] = ['Methylene chloride']
    df.loc[36, ['Contaminant']] = ['1,2-Dichloropropane']
    # There is an issue here where the labs collected cis and trans separately, but the state only regulates the mixture
    df.loc[37, ['Contaminant']] = ['cis-1,3-Dichloropropene']
    # tert is an abbreviation for tertiary
    df.loc[39, ['Contaminant']] = ['Methyl tert-butyl ether (MTBE)']
    # Chlorobenzene is a specific and simplest of the monochlorobenzenes
    df.loc[40, ['Contaminant']] = ['Chlorobenzene']
    # There is a problem with the lab data here; they have both tetrachloroethylene and tetrachloroethene, which are the same thing
    df.loc[43, ['Contaminant']] = ['Tetrachloroethene']
    df.loc[46, ['Contaminant']] = ['1,1,1-Trichloroethane']
    df.loc[47, ['Contaminant']] = ['1,1,2-Trichloroethane']
    df.loc[48, ['Contaminant']] = ['Trichloroethene']
    df.loc[49, ['Contaminant']] = ['Trichlorofluoromethane']
    df.loc[50, ['Contaminant']] = ['1,1,2-Trichlorotrifluoroethane']
    df.loc[52, ['Contaminant']] = ['Total Xylene, (total)']
    df.loc[60, ['Contaminant']] = ['1,2-Dibromo-3-chloropropane (DBCP)']
    df.loc[61, ['Contaminant']] = ['2,4-D']
    # this is the same compound as Di(2-ethylhexyl)adipate
    df.loc[62, ['Contaminant']] = ['Bis(2-ethylhexyl) adipate']
    # This is the same compound as Di(2-ethylhexyl)phthalate
    df.loc[63, ['Contaminant']] = ['bis(2-Ethylhexyl) phthalate']
    df.loc[64, ['Contaminant']] = ['Dinoseb (DNPB)']
    df.loc[68, ['Contaminant']] = ['Ethylene Dibromide']
    df.loc[74, ['Contaminant']] = ['BHC-gamma (Lindane)']
    df.loc[78, ['Contaminant']] = ['Pentachlorophenol (PCP)']
    df.loc[79, ['Contaminant']] = ["PCB's"]
    df.loc[84, ['Contaminant']] = ['1,2,3-Trichloropropane']
    df.loc[85, ['Contaminant']] = ['2,3,7,8-Tetrachlorodibenzo-p-dioxin']
    df.loc[86, ['Contaminant']] = ['2,4,5-TP (Silvex)']
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
    Decontaminate_Names(df)
    return df