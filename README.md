# Vanguard-ab-test

## Summary

We have carried out a thorough analysis to comprehend if the new digital design leads better user experience and higher process completion rates. The datasets incudes variables like client age, client tenure month, number of accounts, balance for both users who uses traditional process and who uses the digital interface. The primary objective is to decode the experiment’s performance. 


![Dashboard Page 1](https://github.com/user-attachments/assets/296583e3-913a-417a-a5c3-41eae1d2a54c)




## Project Overview

1. An overview of the demographics or client behaviour analysis or who are the primary customers.
2. A comparative analysis of the key performance indicators (KPIs) , which in our case are
   2.1 Completion Rate(Percentage of users who have reached the confirm stage.)

    2.2 Time Spent on Each Step (The average duration users spend on each step) 

    2.3 Error Rates (If there’s a step where users go back to a previous step, it may indicate confusion or an error. You should consider moving           from a later step to an earlier one as an error)
3. 3. Based on the KPIs, we have conducted hypothesis testing to make data-driven conclusions about the effectiveness of the redesign.
4. Experiment Evaluation

    4.1 The  experiment was well-structured, as we see significant change in response rates.

    4.2 The users were randomly and equally divided between the old and new designs

    4.3 There could be biases, as we feel the information we received is not sufficient enough. The should be more details/insights on the steps,/ every page, to figure out what could be the probable reasons of the results we got.  



## Data cleaning and merging

Before diving into in-depth analysis or visualization, our first task is to perform an initial round of data cleaning. This is crucial for ensuring that we can work seamlessly with the data across various datasets that we've collated into a single DataFrame

## About the dataset

The dataset consists of 3 tables.
Client Profiles : Demographics like age, gender, and account details of our clients.
Digital Footprints : A detailed trace of client interactions online, divided into two parts: pt_1 and pt_2. It’s recommended to merge these two files prior to a comprehensive data analysis.
Experiment Roster : A list revealing which clients were part of the grand experiment.

## Key Demographics

After carefully analysing all the variables, we have consisdered, Tenure year, client age, gender as the most significant ones which might have a direct impact on the success rate(process_step) and how  they are related. To serve the purpose we did a bi-variate analysis.

![heatmap](https://github.com/user-attachments/assets/98b0a1a6-a264-4ff1-b2eb-f7c938187175)



### KPI and Hypothesis testing

The main KPIs-
1. Completion Rate
2. Time Spent on Each Step
3. Error Rates

   
![CB 3](https://github.com/user-attachments/assets/f83d021b-47e1-4f56-bbe8-e09e61198109)


## Milestones

  1. Project Preparation-Organize the project team-Create [Notion board](https://teal-server-788.notion.site/Vanguard-A-B-Testing-7139a9cc4a19438698eae03777b9accd)
  2. Define problem statement-Identify Business Question
  3. Code Review and Testing-Review code from Local and Dev branches-Once reviewed and approved, merge 
     into Main branch
  4. Presentation
  

## :toolbox: Tools and Technologies Used


- Python: The main programming language used for data visualization.
- Jupyter Notebook: Used for data visualization and addressing the project questions.
- Plotly, Seaborn python graphing library
- Power Bi, [Streamlit](http://localhost:8502/) for data vizualization

## Project Structure

The project structure is as follows:

- `Clean data/clean.ipynb`: The Jupyter Notebook containing the data processing, analysis, and visualization code.
- `Clean data/main.py` : Main file
- `Clean data/function.py`: Function file
- `data/`: A folder containing the dataset files obtained from the IEA.
- `Raw data/`: A folder containing the raw datsets, drafts ipynb.
- `slides/`: A folder containing the slides.
- `resources/`: A folder containing all the images.
- `requirements.txt`: A file specifying the dependencies required to run the project.


## Conclusion

The modern UI design has a higher confirmation rate compared to the traditional website. However, users interacting with the modern UI experience a higher error rate, as indicated by a greater frequency of going back to previous pages. This suggests that there is room for improvement, particularly in refining the steps to enhance user experience.The increased time on the "start" and "step_1" steps in the test group suggests that these changes either made the steps more engaging or added complexity. Further investigation would be needed to determine if this additional time was due to positive engagement 
