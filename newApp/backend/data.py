import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def extractTopData(top_N,new_df,variable):
    colList=list(new_df.columns)
    new_list=[]
    for index,rows in new_df.iterrows():
        if(top_N>0):
            if (rows[colList[0]]==variable):
                    row_val=[rows[colList[1]],rows[colList[2]]]
                    new_list.append(row_val)
                    top_N-=1
    return new_list
def extractSalesData(top_N,new_df,variable):
    new_list=[]
    for index,rows in new_df.iterrows():
        if(top_N>0):
            row_val=[rows.Rank,rows.Name,rows[variable]]
            new_list.append(row_val)
            top_N-=1
    return new_list
def processing(file_path):

    #read csv file
    df=pd.read_csv(file_path,delimiter=',')

    #removing empty rows and columns
    df.dropna(axis = 0, how = 'all', inplace = True)
    df.dropna(axis = 1, how = 'all', inplace = True)

    #replacing null values
    int_cols = df.select_dtypes(include=['int']).columns
    df[int_cols] = df[int_cols].fillna(0)
    float_cols = df.select_dtypes(include=['float']).columns
    df[float_cols] = df[float_cols].fillna(0)
    object_cols = df.select_dtypes(include=['object']).columns
    df[object_cols] = df[object_cols].fillna("Unknown")

    #drop duplicate values
    df.drop_duplicates(subset=['Year','Name','Last_Update'],keep='first')

    cols=list(df.columns)

    #set proper year format
    df['Year'] = df['Year'].astype("int64")

    #display year and name of top N games published by the given publisher
    top_N_p=5    
    publisher_df=df[["Publisher","Year","Name"]]
    publisherVariable="Microsoft Game Studios"   
    str1="Top "+str(top_N_p)+" Publications by "+publisherVariable
    p_list=extractTopData(top_N_p,publisher_df,publisherVariable)

    #display publisher and name of top N games related to given genre
    top_N_g=5
    genre_df=df[["Genre","Publisher","Name"]]
    genreVariable="Action-Adventure"
    str2="Top "+str(top_N_g)+" Games in "+genreVariable+" Genre"
    g_list=extractTopData(top_N_g,genre_df,genreVariable)

    # display top N games based on particular sales score
    top_N_s=3
    sales_df=df[["Rank","Name","Global_Sales","NA_Sales","PAL_Sales","JP_Sales","Other_Sales"]]
    salesVariable="JP_Sales"
    str3="Top "+str(top_N_s)+" games based on "+salesVariable
    sales_df.sort_values(salesVariable,inplace=True,ascending=False)
    s_list=extractSalesData(top_N_s,sales_df,salesVariable)

    result={
        "List of Columns":cols,
        str1:p_list,
        str2:g_list,
        str3:s_list
    }
    return result

    
