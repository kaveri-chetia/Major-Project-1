from function import *

variation_path = "df_final_experiment_clients.csv"
web_data_path = "merged_df_final_web_data.csv"
demo_path = "df_final_demo.csv"


merged_df2 = data_load(variation_path, web_data_path, demo_path)
merged_df2.to_csv('merged_df2.csv', index=False)              

control_df = process_control_data(merged_df2)
control_df.to_csv('control_df.csv', index=False) 

test_df = process_control_data(merged_df2)
test_df.to_csv('test_df.csv', index=False) 