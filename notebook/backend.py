

def data_load(variation_path, web_data_path, demo_path):
   
    # Reading variation table and web_data table
    df1 = pd.read_csv(variation_path)
    df2 = pd.read_csv(web_data_path)
    df3 = pd.read_csv(demo_path)

    #Merging to merged_df_final
    merged_df1 = pd.merge(df1, df2, on='client_id', how='inner')

    # Merging customer_info with merged_df_final
    merged_df2 = pd.merge(merged_df1, df3, on='client_id', how='inner')
    merged_df2=merged_df2.dropna()
    return merged_df2

def get_summary(merged_df2):