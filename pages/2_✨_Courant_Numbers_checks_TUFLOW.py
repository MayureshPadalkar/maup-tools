import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

#st.logo("images/logo.png", icon_image="images/logo.png")

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Mayuresh Padalkar for debugging, suggestions and improvements in the app on  
    - mayuresh.padalkar@gmail.com  
       
    """
)

st.sidebar.title("Follow")
st.sidebar.info(
    """
    Mayuresh Padalkar on  
    - [LinkedIn](https://www.linkedin.com/in/mayuresh-padalkar-830b4817/)
    """
)

# Title of the application
st.title("Nu, Nc, Nd check from HPC TUFLOW output")

st.markdown(
    """
    Please check the thresholds as follows in the plots:  
        - An Nu value of 1.0 or greater may indicate that the velocity is unusually high  
        - An Nc value of 1.0 or higher could be caused by an erroneously low cell elevation, resulting in an artificially large water depth  
        - An Nd value of 0.3 or higher might suggest that there is poor boundary setup, or insufficient SX cells linked to a 1D structure  

    """
)

st.markdown(
    """
    'dtStar' column is divided by 3600, and then it is cummulated.  

    """
)

# File uploader widget
uploaded_files = st.file_uploader("Choose a HPC.dt.csv file:", accept_multiple_files=True, type="csv")

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the dataframe
        st.write(f"File: {uploaded_file.name}")
        
        # Perform the calculations
        df['dtStar_divided'] = df['dtStar'] / 3600
        df['dtStar_cumsum'] = df['dtStar_divided'].cumsum()

        # Plot dtStar_cumsum on x-axis, and Nu, Nc, and Nd on y-axis
        plt.figure(figsize=(10, 5))
        plt.plot(df['dtStar_cumsum'], df['Nu'], label='Nu')
        plt.plot(df['dtStar_cumsum'], df['Nc'], label='Nc')
        plt.plot(df['dtStar_cumsum'], df['Nd'], label='Nd')

        # Add horizontal lines
        plt.axhline(y=0.3, color='r', linestyle='--')
        plt.axhline(y=1, color='g', linestyle='-.')

        # Add labels and legend
        plt.xlabel('Time (hours)')
        plt.ylabel('Nu, Nc, Nd')
        plt.legend(bbox_to_anchor=(0.5, -0.25), loc='lower center', ncol=3)
        plt.title(f"Plot for {uploaded_file.name}")

        # Display the plot
        st.pyplot(plt)

else:
    st.warning("Please upload at least one CSV file.")
