# Vanguard-ab-test

## Summary

We have carried out a thorough analysis to comprehend if the new digital design leads better user experience and higher process completion rates. The datasets incudes variables like client age, client tenure month, number of accounts, balance for both users who uses traditional process and who uses the digital interface. The primary objective is to decode the experiment’s performance. 


![Dashboard (1)](https://github.com/user-attachments/assets/3cf72a4e-2292-4d4d-9768-c8fdf38321c0)






## Project Overview

The digital world is evolving, and so are Vanguard’s clients. Vanguard is US-based investment management company. Vanguard believed that a more intuitive and modern User Interface (UI), coupled with timely in-context prompts (cues, messages, hints, or instructions provided to users directly within the context of their current task or action), could make the online process smoother for clients. The critical question was: **Would these changes encourage more clients to complete the process?**

Vanguard just launched an exciting digital experiment. Our goal as Customer Experience team is helping the company to uncover the results of the experiment. To address the critical question, we have developed a set of hypotheses to guide our analysis and determine whether the new UI and in-context prompts effectively enhance client engagement and completion rates as follows: <br>
1. The new feature would encourage more clients to complete the process. <br>
2. The new feature would reduce the time spent on each step of the process, leading to more efficient completion. <br>
3. The new feature would reduce the error rates during the process, leading to smoother completion. <br>



## Data cleaning and merging

Before diving into in-depth analysis or visualization, our first task is to perform an initial round of data cleaning. This is crucial for ensuring that we can work seamlessly with the data across various datasets that we've collated into a single DataFrame

## About the dataset

The dataset consists of 3 tables.
Client Profiles : Demographics like age, gender, and account details of our clients.
Digital Footprints : A detailed trace of client interactions online, divided into two parts: pt_1 and pt_2. It’s recommended to merge these two files prior to a comprehensive data analysis.
Experiment Roster : A list revealing which clients were part of the grand experiment.

## Key Demographics

<img width="200" alt="image" src="https://github.com/user-attachments/assets/b59c3413-6018-4b78-a3b7-fbe8066b29dc">
<img width="200" alt="image" src="https://github.com/user-attachments/assets/cc4b9f56-4f4e-4db6-842e-da30d78cccc0">
<img width="200" alt="image" src="https://github.com/user-attachments/assets/4fadb97b-db47-4515-8260-c60714026531">
<img width="200" alt="image" src="https://github.com/user-attachments/assets/50353301-043b-4889-8145-700575c07bb1">






### KPI and Hypothesis testing

The main KPIs-
1. Completion Rate
2. Time Spent on Each Step
3. Error Rates

   



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
