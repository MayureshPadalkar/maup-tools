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
st.title("Mass Balance check from TUFLOW output")

# File uploader widget
uploaded_files = st.file_uploader("Choose MB.csv file:", accept_multiple_files=True, type="csv")

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Ensure the necessary columns are present
        if 'Time (h)' in df.columns and 'dVol' in df.columns and 'Cum ME (%)' in df.columns:
            # Display the name of the uploaded file
            st.write(f"File: {uploaded_file.name}")

            # Create a new figure and axes
            fig, ax1 = plt.subplots()

            # Plot "Time (h)" vs "dVol" on the primary y-axis
            ax1.set_xlabel('Time (hours)')
            ax1.set_ylabel('Change in Volume (m³)')
            line1, = ax1.plot(df['Time (h)'], df['dVol'], color='tab:blue', label='dVol')
            ax1.tick_params(axis='y')

            # Create a secondary y-axis for "Cum ME (%)"
            ax2 = ax1.twinx()
            ax2.set_ylabel('Cumulative Mass Error (%)')
            line2, = ax2.plot(df['Time (h)'], df['Cum ME (%)'], color='tab:orange', label='Cum ME (%)')
            ax2.tick_params(axis='y')

            # Add horizontal grid lines to the secondary y-axis
            ax2.grid(axis='y')

            # Add legends
            lines = [line1, line2]
            labels = [line.get_label() for line in lines]
            ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.125), ncol=2)

            # Display the plot
            st.pyplot(fig)
        else:
            st.error(f"File {uploaded_file.name} does not have the required columns 'Time (h)', 'dVol', and 'Cum ME (%)'.")
else:
    st.warning("Please upload at least one CSV file.")
