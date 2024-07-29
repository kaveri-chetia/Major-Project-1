import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats.contingency import association
from scipy.stats import ttest_ind
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest





def data_load(df1, df2, df3 ):
   
    # Reading variation table and web_data table
    df1 = pd.read_csv("df_final_experiment_clients.csv")
    df2 = pd.read_csv('merged_df_final_web_data.csv')
    df3 = pd.read_csv("df_final_demo.csv")

    #Merging to merged_df_final
    merged_df1 = pd.merge(df1, df2, on='client_id', how='inner')

    # Merging customer_info with merged_df_final
    merged_df2 = pd.merge(merged_df1, df3, on='client_id', how='inner')
    merged_df2=merged_df2.dropna()
    return merged_df2


# def data_demo(merged_df2):

#     # Creating a dataframe for the numerical variables for further analysing correlation with Tenure year.
#     numeric_df = merged_df2.select_dtypes(include=[np.number])

#     # We have used spearman correlation and the result gives a vivid idea how Tenure year is deeply connected with client's  age, balance and number of accounts. here we are ignoring clnt_tenure_mnth, as it dose not make any sense of. 
#     spearman_correlations= numeric_df.corrwith(merged_df2['clnt_tenure_yr'], method= 'spearman')
#     spearman_correlation_sorted= spearman_correlations.sort_values(ascending= False)
#     spearman_correlations_sorted_top = spearman_correlation_sorted[abs(spearman_correlation_sorted) > 0.1]
#     print("Spearman Correlations:")
#     print(spearman_correlations_sorted_top)


#     # A heatmap is used to depict the same.
#     correlation_matrix = numeric_df[spearman_correlations_sorted_top.index].corr()
#     plt.figure(figsize=(6, 6))

#     # Drawing the heatmap for the numerical columns
#     sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")

#     plt.title("Correlation Heatmap for Selected Numerical Variables")

#     # Created a crosstab between gender and clinet tenure, and result has been shown using stacked bar.
#     crosstab_result = pd.crosstab(merged_df2['clnt_tenure_yr'], merged_df2['gendr'])
#     print("Crosstab Result:")
#     print(crosstab_result)

#     crosstab_result.plot(kind="bar", stacked=True)

#     variables = ['clnt_tenure_yr', 'clnt_age', 'num_accts']
#     control_group = merged_df2[merged_df2['Variation'] == 'Control'][variables].mean()
#     test_group = merged_df2[merged_df2['Variation'] == 'Test'][variables].mean()

#     # Create the plot
#     fig, ax = plt.subplots(figsize=(10, 6))

#     # Define the position of bars
#     y = np.arange(len(variables))

#     # Define bar width
#     bar_width = 0.4

#     # Plot bars
#     ax.barh(y - bar_width/2, control_group, bar_width, color='b', label='Control')
#     ax.barh(y + bar_width/2, test_group, bar_width, color='g', label='Test')

#     # Set labels
#     ax.set_yticks(y)
#     ax.set_yticklabels(variables)
#     ax.set_xlabel('Value')
#     ax.set_title('Grouped Bar Chart for Multiple Variables by Group')

#     # Add a legend
#     ax.legend()
#     plt.show()

# data_demo(merged_df2)


# def visualize_data(merged_df2):
#     merged_df2['date_time'] = pd.to_datetime(merged_df2['date_time'])

#     # Sort the DataFrame by 'client_id', 'visit_id', and 'date_time'
#     merged_df2 = merged_df2.sort_values(by=['client_id', 'visit_id', 'date_time'])

#     # Calculate the duration for each step for each 'client_id' and 'visit_id'
#     merged_df2['duration'] = merged_df2.groupby(['client_id', 'visit_id'])['date_time'].diff().dt.total_seconds()

#     # Set the style

#     # Set the style
#     sns.set(style="whitegrid")

#     # Plot for Client Age
#     plt.figure(figsize=(10, 6))
#     sns.histplot(data=merged_df2, x='clnt_age', kde=True)
#     plt.title('Distribution of Client Age')
#     plt.xlabel('Age')
#     plt.ylabel('Frequency')
#     plt.show()

#     # Plot for Gender
#     plt.figure(figsize=(10, 6))
#     sns.countplot(data=merged_df2, x='gendr', order=merged_df2['gendr'].value_counts().index)
#     plt.title('Count Plot for Gender')
#     plt.xlabel('Gender')
#     plt.ylabel('Count')
#     plt.show()

#     # Plot for Number of Accounts
#     plt.figure(figsize=(10, 6))
#     sns.countplot(data=merged_df2, x='num_accts')
#     plt.title('Count Plot for Number of Accounts')
#     plt.xlabel('Number of Accounts')
#     plt.ylabel('Count')
#     plt.show()

#     # Plot for Balance
#     plt.figure(figsize=(10, 6))
#     sns.histplot(data=merged_df2, x='bal', kde=True)
#     plt.title('Distribution of Balance')
#     plt.xlabel('Balance')
#     plt.ylabel('Frequency')
#     plt.show()

#     # Plot for Calls in Last 6 Months
#     plt.figure(figsize=(10, 6))
#     sns.histplot(data=merged_df2, x='calls_6_mnth', kde=True)
#     plt.title('Distribution of Calls in Last 6 Months')
#     plt.xlabel('Number of Calls')
#     plt.ylabel('Frequency')
#     plt.show()

#     # Plot for Logons in Last 6 Months
#     plt.figure(figsize=(10, 6))
#     sns.histplot(data=merged_df2, x='logons_6_mnth', kde=True)
#     plt.title('Distribution of Logons in Last 6 Months')
#     plt.xlabel('Number of Logons')
#     plt.ylabel('Frequency')
#     plt.show()

#     # Box Plot for Duration of Steps
#     plt.figure(figsize=(10, 6))
#     sns.boxplot(data=merged_df2, x='duration')
#     plt.title('Box Plot for Duration of Steps')
#     plt.xlabel('Duration')
#     plt.show()


# visualize_data(merged_df2)


# def process_control_data(merged_df2):
#     # Filter the dataframe for control group
#     df_control = merged_df2[merged_df2['Variation'] == 'Control'].copy()
#     df_control['date_time'] = pd.to_datetime(df_control['date_time'])

#     # Sort the DataFrame by client_id, visitor_id, and date_time
#     df_control = df_control.sort_values(by=['client_id', 'visitor_id', 'date_time'])

#     # Initialize lists to store new dataframe data
#     new_data = []

#     # Dictionary to store start times, end times, and last step
#     client_data = {}

#     # Iterate over rows to collect start and confirm times, last step, and calculate other needed data
#     for index, row in df_control.iterrows():
#         client_id = row['client_id']
#         visitor_id = row['visitor_id']

#         if (client_id, visitor_id) not in client_data:
#             client_data[(client_id, visitor_id)] = {
#                 'start_time': None,
#                 'confirm_time': None,
#                 'last_step': None,
#                 'steps': [],
#                 'age': row['clnt_age'],
#                 'clnt_tenure': f"{int(row['clnt_tenure_yr'])} years "
#             }

#         step = row['process_step']
#         timestamp = row['date_time']

#         if step == 'start':
#             client_data[(client_id, visitor_id)]['start_time'] = timestamp
#         elif step == 'confirm':
#             client_data[(client_id, visitor_id)]['confirm_time'] = timestamp
#         else:
#             client_data[(client_id, visitor_id)]['steps'].append((step, timestamp))

#         if step != 'start':
#             client_data[(client_id, visitor_id)]['last_step'] = step

#     # Process the collected data
#     for (client_id, visitor_id), data in client_data.items():
#         start_time = data['start_time']
#         confirm_time = data['confirm_time']
#         last_step = data['last_step']
#         steps = data['steps']

#         if start_time is not None and confirm_time is not None:
#             completed = 'yes'
#             duration = round((confirm_time - start_time).total_seconds() / 60.0, 2)
#             last_step = 'confirm'
#         else:
#             completed = 'no'
#             if steps:
#                 duration = round((steps[-1][1] - start_time).total_seconds() / 60.0, 2) if start_time else None
#             else:
#                 duration = None

#         new_data.append([client_id, visitor_id, completed, duration, data['age'], data['clnt_tenure'], last_step])

#     # Create new DataFrame
#     control_df = pd.DataFrame(new_data, columns=['client_id', 'visitor_id', 'completed', 'duration', 'age', 'clnt_tenure', 'last_step'])

#     # Add the extra column for completed
#     control_df['completed_numeric'] = control_df['completed'].map({'yes': 1, 'no': 0})

#     return control_df

# # Use the function with your merged_df2 DataFrame
# control_df = process_control_data(merged_df2)




def process_test_dataframe(merged_df2, variation='Test'):
    """
    Process the test DataFrame to create a new DataFrame with completion status, duration, age, client tenure, and last step.
    
    Args:
        merged_df2 (pd.DataFrame): The original DataFrame.
        variation (str): The variation to filter by (default is 'Test').
    
    Returns:
        pd.DataFrame: The processed DataFrame with additional columns.
    """
    # Filter by variation
    df_filtered = merged_df2[merged_df2['Variation'] == variation]

    # Convert 'date_time' to datetime
    df_filtered['date_time'] = pd.to_datetime(df_filtered['date_time'])

    # Sort the DataFrame by client_id, visitor_id, and date_time
    df_filtered = df_filtered.sort_values(by=['client_id', 'visitor_id', 'date_time'])

    # Initialize lists to store new dataframe data
    new_data = []

    # Dictionary to store start times, end times, and last step
    client_data = {}

    # Iterate over rows to collect start and confirm times, last step, and calculate other needed data
    for index, row in df_filtered.iterrows():
        client_id = row['client_id']
        visitor_id = row['visitor_id']

        if (client_id, visitor_id) not in client_data:
            client_data[(client_id, visitor_id)] = {
                'start_time': None,
                'confirm_time': None,
                'last_step': None,
                'steps': [],
                'age': row['clnt_age'],
                'clnt_tenure': f"{int(row['clnt_tenure_yr'])} years "
            }

        step = row['process_step']
        timestamp = row['date_time']

        if step == 'start':
            client_data[(client_id, visitor_id)]['start_time'] = timestamp
        elif step == 'confirm':
            client_data[(client_id, visitor_id)]['confirm_time'] = timestamp
        else:
            client_data[(client_id, visitor_id)]['steps'].append((step, timestamp))

        if step != 'start':
            client_data[(client_id, visitor_id)]['last_step'] = step

    # Process the collected data
    for (client_id, visitor_id), data in client_data.items():
        start_time = data['start_time']
        confirm_time = data['confirm_time']
        last_step = data['last_step']
        steps = data['steps']

        if start_time is not None and confirm_time is not None:
            completed = 'yes'
            duration = round((confirm_time - start_time).total_seconds() / 60.0, 2)
            last_step = 'confirm'
        else:
            completed = 'no'
            if steps:
                duration = round((steps[-1][1] - start_time).total_seconds() / 60.0, 2) if start_time else None
            else:
                duration = None

        new_data.append([client_id, visitor_id, completed, duration, data['age'], data['clnt_tenure'], last_step])

    # Create new DataFrame
    test_df = pd.DataFrame(new_data, columns=['client_id', 'visitor_id', 'completed', 'duration', 'age', 'clnt_tenure', 'last_step'])
    # Add the extra column for completed
    test_df['completed_numeric'] = test_df['completed'].map({'yes': 1, 'no': 0})

    return test_df

# Usage example
# Assuming merged_df2 is already defined and loaded with appropriate data
test_df = process_test_dataframe(merged_df2)
    
     

    
