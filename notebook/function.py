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


def data_demo(merged_df2):

    # Creating a dataframe for the numerical variables for further analysing correlation with Tenure year.
    numeric_df = merged_df2.select_dtypes(include=[np.number])

    # We have used spearman correlation and the result gives a vivid idea how Tenure year is deeply connected with client's  age, balance and number of accounts. here we are ignoring clnt_tenure_mnth, as it dose not make any sense of. 
    spearman_correlations= numeric_df.corrwith(merged_df2['clnt_tenure_yr'], method= 'spearman')
    spearman_correlation_sorted= spearman_correlations.sort_values(ascending= False)
    spearman_correlations_sorted_top = spearman_correlation_sorted[abs(spearman_correlation_sorted) > 0.1]
    print("Spearman Correlations:")
    display(spearman_correlations_sorted_top)


    # A heatmap is used to depict the same.
    correlation_matrix = numeric_df[spearman_correlations_sorted_top.index].corr()
    plt.figure(figsize=(6, 6))

    # Drawing the heatmap for the numerical columns
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")

    plt.title("Correlation Heatmap for Selected Numerical Variables")

    # Created a crosstab between gender and clinet tenure, and result has been shown using stacked bar.
    crosstab_result = pd.crosstab(merged_df2['clnt_tenure_yr'], merged_df2['gendr'])
    print("Crosstab Result:")
    display(crosstab_result)

    crosstab_result.plot(kind="bar", stacked=True)

    variables = ['clnt_tenure_yr', 'clnt_age', 'num_accts']
    control_group = merged_df2[merged_df2['Variation'] == 'Control'][variables].mean()
    test_group = merged_df2[merged_df2['Variation'] == 'Test'][variables].mean()

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define the position of bars
    y = np.arange(len(variables))

    # Define bar width
    bar_width = 0.4

    # Plot bars
    ax.barh(y - bar_width/2, control_group, bar_width, color='b', label='Control')
    ax.barh(y + bar_width/2, test_group, bar_width, color='g', label='Test')

    # Set labels
    ax.set_yticks(y)
    ax.set_yticklabels(variables)
    ax.set_xlabel('Value')
    ax.set_title('Grouped Bar Chart for Multiple Variables by Group')

    # Add a legend
    ax.legend()
    plt.show()




def visualize_data(merged_df2):
    merged_df2['date_time'] = pd.to_datetime(merged_df2['date_time'])

    # Sort the DataFrame by 'client_id', 'visit_id', and 'date_time'
    merged_df2 = merged_df2.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Calculate the duration for each step for each 'client_id' and 'visit_id'
    merged_df2['duration'] = merged_df2.groupby(['client_id', 'visit_id'])['date_time'].diff().dt.total_seconds()



    # Set the style
    sns.set(style="whitegrid")

    # Plot for Client Age
    plt.figure(figsize=(10, 6))
    sns.histplot(data=merged_df2, x='clnt_age', kde=True)
    plt.title('Distribution of Client Age')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()

    # Plot for Gender
    plt.figure(figsize=(10, 6))
    sns.countplot(data=merged_df2, x='gendr', order=merged_df2['gendr'].value_counts().index)
    plt.title('Count Plot for Gender')
    plt.xlabel('Gender')
    plt.ylabel('Count')
    plt.show()

    # Plot for Number of Accounts
    plt.figure(figsize=(10, 6))
    sns.countplot(data=merged_df2, x='num_accts')
    plt.title('Count Plot for Number of Accounts')
    plt.xlabel('Number of Accounts')
    plt.ylabel('Count')
    plt.show()

    # Plot for Balance
    plt.figure(figsize=(10, 6))
    sns.histplot(data=merged_df2, x='bal', kde=True)
    plt.title('Distribution of Balance')
    plt.xlabel('Balance')
    plt.ylabel('Frequency')
    plt.show()

    # Plot for Calls in Last 6 Months
    plt.figure(figsize=(10, 6))
    sns.histplot(data=merged_df2, x='calls_6_mnth', kde=True)
    plt.title('Distribution of Calls in Last 6 Months')
    plt.xlabel('Number of Calls')
    plt.ylabel('Frequency')
    plt.show()

    # Plot for Logons in Last 6 Months
    plt.figure(figsize=(10, 6))
    sns.histplot(data=merged_df2, x='logons_6_mnth', kde=True)
    plt.title('Distribution of Logons in Last 6 Months')
    plt.xlabel('Number of Logons')
    plt.ylabel('Frequency')
    plt.show()

    # Box Plot for Duration of Steps
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=merged_df2, x='duration')
    plt.title('Box Plot for Duration of Steps')
    plt.xlabel('Duration')
    plt.show()





def process_control_data(merged_df2):
    # Filter the dataframe for control group
    df_control = merged_df2[merged_df2['Variation'] == 'Control'].copy()
    df_control['date_time'] = pd.to_datetime(df_control['date_time'])

    # Sort the DataFrame by client_id, visitor_id, and date_time
    df_control = df_control.sort_values(by=['client_id', 'visitor_id', 'date_time'])

    # Initialize lists to store new dataframe data
    new_data = []

    # Dictionary to store start times, end times, and last step
    client_data = {}

    # Iterate over rows to collect start and confirm times, last step, and calculate other needed data
    for index, row in df_control.iterrows():
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
    control_df = pd.DataFrame(new_data, columns=['client_id', 'visitor_id', 'completed', 'duration', 'age', 'clnt_tenure', 'last_step'])

    # Add the extra column for completed
    control_df['completed_numeric'] = control_df['completed'].map({'yes': 1, 'no': 0})

    return control_df





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



def calculate_success_ratio(test_df,control_df):
    num_successes = (test_df['completed_numeric'] == 1).sum()

    # Calculate the total number of outcomes
    total_outcomes = test_df['completed_numeric'].count()

    # Calculate the success ratio
    success_ratio = num_successes / total_outcomes if total_outcomes > 0 else 0  # Avoid division by zero
    success_ratio_inpercent1 = round(success_ratio*100 ,2)
    

    num_successes = (control_df['completed_numeric'] == 1).sum()

    # Calculate the total number of outcomes
    total_outcomes = control_df['completed_numeric'].count()

    # Calculate the success ratio
    success_ratio = num_successes / total_outcomes if total_outcomes > 0 else 0  # Avoid division by zero
    success_ratio_inpercent2 = round(success_ratio*100 ,2)

    print(f"Success percentage of control group is: {success_ratio_inpercent2:.2f}%, Success percentage of test group is: {success_ratio_inpercent1:.2f}%")
    
    
    return success_ratio_inpercent1, success_ratio_inpercent2



def average_duration(merged_df2):
    merged_df2_test = merged_df2[merged_df2['Variation'] == 'Test']
    # Convert 'date_time' to datetime
    merged_df2_test['date_time'] = pd.to_datetime(merged_df2_test['date_time'])

    # Sort the DataFrame by 'client_id', 'visit_id', and 'date_time'
    merged_df2_test = merged_df2_test.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Calculate the duration for each step for each 'client_id' and 'visit_id'
    merged_df2_test['duration'] = merged_df2_test.groupby(['client_id', 'visit_id'])['date_time'].diff().dt.total_seconds()
    average_durations_test = merged_df2_test.groupby('process_step')['duration'].mean().reset_index()
 

    merged_df2_control = merged_df2[merged_df2['Variation'] == 'Control']
    merged_df2_control['date_time'] = pd.to_datetime(merged_df2_control['date_time'])
    merged_df2_control = merged_df2_control.sort_values(by=['client_id', 'visit_id', 'date_time'])
    merged_df2_control['duration'] = merged_df2_control.groupby(['client_id', 'visit_id'])['date_time'].diff().dt.total_seconds()
    average_durations_control = merged_df2_control.groupby('process_step')['duration'].mean().reset_index()
 

    return average_durations_test, average_durations_control
    
def error_rate(merged_df2):
    df_test_error = merged_df2[merged_df2['Variation'] == 'Test']

    df_control_error = merged_df2[merged_df2['Variation'] == 'Control']

    df_test_error['date_time'] = pd.to_datetime(df_test_error['date_time'])

    # Sort the DataFrame by 'client_id', 'visit_id', and 'date_time'
    df_test_error = df_test_error.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Define the order of steps
    step_order = {'start': 1, 'step_1': 2, 'step_2': 3, 'step_3': 4, 'confirm': 5}
    df_test_error['step_order'] = df_test_error['process_step'].map(step_order)

    # Calculate if there is a step reversal
    df_test_error['step_reversal'] = df_test_error.groupby(['client_id', 'visit_id'])['step_order'].diff() < 0

    # Calculate the total number of steps and the number of reversals
    total_steps = df_test_error.groupby(['client_id', 'visit_id']).size()
    total_reversals = df_test_error.groupby(['client_id', 'visit_id'])['step_reversal'].sum()

    # Calculate the error rate as the proportion of step reversals
    error_rate_test = (total_reversals / total_steps).mean()  

    

    df_control_error['date_time'] = pd.to_datetime(df_control_error['date_time'])

    # Sort the DataFrame by 'client_id', 'visit_id', and 'date_time'
    df_control_error = df_control_error.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Define the order of steps
    step_order = {'start': 1, 'step_1': 2, 'step_2': 3, 'step_3': 4, 'confirm': 5}
    df_control_error['step_order'] = df_control_error['process_step'].map(step_order)

    # Calculate if there is a step reversal
    df_control_error['step_reversal'] = df_control_error.groupby(['client_id', 'visit_id'])['step_order'].diff() < 0

    # Calculate the total number of steps and the number of reversals
    total_steps = df_control_error.groupby(['client_id', 'visit_id']).size()
    total_reversals = df_control_error.groupby(['client_id', 'visit_id'])['step_reversal'].sum()

    # Calculate the error rate as the proportion of step reversals
    error_rate_control = (total_reversals / total_steps).mean()

    return(f"Error rate of control group is: {error_rate_control:.2f}%, Error rate of test group is: {error_rate_test:.2f}%")



def perform_ttest(control_df, test_df, column='completed_numeric'):

    control_numeric_df = control_df[[column]]
    test_numeric_df = test_df[[column]]

    # Perform two-sample t-test
    t_stat, p_val = ttest_ind(control_numeric_df[column], test_numeric_df[column], equal_var=False)

    # Print results
    print(f"T-Statistic: {t_stat}")
    print(f"P-Value: {p_val}")

    # Perform one-sided t-test if alternative is 'greater'
    t_stat_greater, p_val_greater = ttest_ind(test_numeric_df[column], control_numeric_df[column], alternative='greater')

    # Print results for one-sided t-test
    print(f"T-Statistic (greater): {t_stat_greater}")
    print(f"P-Value (greater): {p_val_greater}")

def error_rate_with_hypothesis_test(merged_df2):
    # Separate the data into test and control groups
    df_test_error = merged_df2[merged_df2['Variation'] == 'Test']
    df_control_error = merged_df2[merged_df2['Variation'] == 'Control']

    # Convert date_time to datetime
    df_test_error['date_time'] = pd.to_datetime(df_test_error['date_time'])
    df_control_error['date_time'] = pd.to_datetime(df_control_error['date_time'])

    # Sort the DataFrames by 'client_id', 'visit_id', and 'date_time'
    df_test_error = df_test_error.sort_values(by=['client_id', 'visit_id', 'date_time'])
    df_control_error = df_control_error.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Define the order of steps
    step_order = {'start': 1, 'step_1': 2, 'step_2': 3, 'step_3': 4, 'confirm': 5}
    df_test_error['step_order'] = df_test_error['process_step'].map(step_order)
    df_control_error['step_order'] = df_control_error['process_step'].map(step_order)

    # Calculate if there is a step reversal
    df_test_error['step_reversal'] = df_test_error.groupby(['client_id', 'visit_id'])['step_order'].diff() < 0
    df_control_error['step_reversal'] = df_control_error.groupby(['client_id', 'visit_id'])['step_order'].diff() < 0

    # Calculate the total number of steps and the number of reversals
    total_steps_test = df_test_error.groupby(['client_id', 'visit_id']).size()
    total_reversals_test = df_test_error.groupby(['client_id', 'visit_id'])['step_reversal'].sum()

    total_steps_control = df_control_error.groupby(['client_id', 'visit_id']).size()
    total_reversals_control = df_control_error.groupby(['client_id', 'visit_id'])['step_reversal'].sum()

    # Calculate the error rate as the proportion of step reversals
    error_rate_test = (total_reversals_test / total_steps_test).mean()
    error_rate_control = (total_reversals_control / total_steps_control).mean()

    # Perform a one-tailed t-test
    t_stat, p_val = ttest_ind(total_reversals_test / total_steps_test, total_reversals_control / total_steps_control, alternative='greater', equal_var=False)

    # Return the error rates and the results of the hypothesis test
    return (f"Error rate of control group is: {error_rate_control:.2f}%, Error rate of test group is: {error_rate_test:.2f}%, "
            f"T-Statistic: {t_stat:.4f}, P-Value: {p_val:.4f}")    


def hypo_3(merged_df2):

    merged_df2_test = merged_df2[merged_df2['Variation'] == 'Test']
    # Convert 'date_time' to datetime
    merged_df2_test['date_time'] = pd.to_datetime(merged_df2_test['date_time'])

    # Sort the DataFrame by 'client_id', 'visit_id', and 'date_time'
    merged_df2_test = merged_df2_test.sort_values(by=['client_id', 'visit_id', 'date_time'])

    # Calculate the duration for each step for each 'client_id' and 'visit_id'
    merged_df2_test['duration'] = merged_df2_test.groupby(['client_id', 'visit_id'])['date_time'].diff().dt.total_seconds()
    average_durations_test = merged_df2_test.groupby('process_step')['duration'].mean().reset_index()
 

    merged_df2_control = merged_df2[merged_df2['Variation'] == 'Control']
    merged_df2_control['date_time'] = pd.to_datetime(merged_df2_control['date_time'])
    merged_df2_control = merged_df2_control.sort_values(by=['client_id', 'visit_id', 'date_time'])
    merged_df2_control['duration'] = merged_df2_control.groupby(['client_id', 'visit_id'])['date_time'].diff().dt.total_seconds()
    average_durations_control = merged_df2_control.groupby('process_step')['duration'].mean().reset_index()

    control_hypo_df = average_durations_control['duration']
    control_hypo_df = pd.DataFrame(control_hypo_df)
    control_hypo_df['cumulative_duration'] = control_hypo_df['duration'].cumsum()
    total_duration = control_hypo_df['duration'].sum()

    # Add the total duration as a new column
    control_hypo_df['total_duration'] = total_duration

    test_hypo_df = average_durations_test['duration']
    test_hypo_df = pd.DataFrame(test_hypo_df)
    test_hypo_df['cumulative_duration'] = test_hypo_df['duration'].cumsum()
    total_duration = test_hypo_df['duration'].sum()
    test_hypo_df['total_duration'] = total_duration

    t_stat, p_val = ttest_ind(test_hypo_df['total_duration'], control_hypo_df['total_duration'], equal_var=False, alternative='greater')


    return(f"P-Value: {p_val}")









    
