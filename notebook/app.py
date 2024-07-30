import streamlit as st
from backend import load_data ,get_summary,plot_


def main():

st.title('Vangurad customer ex')

#To load data
data = load_data()

# Interactive widgets
st.sidebar.header('Controls')
min_rating = st.sidebar.slider('Minimum rating', min_value= 0, max_value_value= 10, value=5, step=1)

min_rating = st.sidebar.multiselect
min_rating = st.sidebar.radio
£Filter by rating
filtered_data =  data[data['Rating']>= min_rating]
#summary statistics
updated_summary = get_summary(filtered_data)
st.write('### Summary statistics')
st.table(updated_summary)



#Display raw data
st.write('### Raw data')
plt = = plot_st.pyplot(plt)



if_name_ == '_main_':
    main()
