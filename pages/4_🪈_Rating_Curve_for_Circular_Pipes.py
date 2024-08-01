import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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
st.title("Rating Curve Calculator for Circular Pipes")

st.write("""
    Generates a rating (H-Q) curve for a circular pipe after you mention a diameter, slope, roughness, and invert level.  
    The output can be used as a 1d_bc boundary condition for the downstream node of your last pipe leaving the system in 1D ESTRY (TUFLOW).
    """)

def partial_flow_area(diameter, depth):
    """Calculate the cross-sectional area of flow in a partially full circular pipe."""
    if depth <= 0:
        return 0
    if depth >= diameter:
        return (math.pi * diameter**2) / 4
    theta = 2 * math.acos((diameter - 2 * depth) / diameter)
    area = (diameter**2 / 8) * (theta - math.sin(theta))
    return area

def partial_flow_hydraulic_radius(diameter, depth):
    """Calculate the hydraulic radius of flow in a partially full circular pipe."""
    if depth <= 0:
        return 0
    if depth >= diameter:
        return diameter / 4
    theta = 2 * math.acos((diameter - 2 * depth) / diameter)
    wetted_perimeter = diameter * theta / 2
    area = partial_flow_area(diameter, depth)
    return area / wetted_perimeter

def flow_rate(diameter, slope, manning_n, depth):
    """Calculate the flow rate for a given depth in a circular pipe using Manning's equation."""
    area = partial_flow_area(diameter, depth)
    hydraulic_radius = partial_flow_hydraulic_radius(diameter, depth)
    if hydraulic_radius == 0:
        return 0
    flow_rate = (1 / manning_n) * area * (hydraulic_radius**(2/3)) * (slope**0.5)
    return flow_rate

def generate_rating_curve(diameter, slope, manning_n, invert_level, num_points=100):
    """Generate a rating curve for a circular pipe."""
    depths = np.linspace(0, diameter, num_points)
    elevations = invert_level + depths
    flow_rates = [flow_rate(diameter, slope, manning_n, depth) for depth in depths]

    # Create a DataFrame
    data = {
        # 'Depth (m)': depths,
        'Elevation (mOD)': elevations,
        'Flow (m³/s)': flow_rates
    }
    df = pd.DataFrame(data)

    return df

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'curve_generated' not in st.session_state:
    st.session_state.curve_generated = False
if 'plot' not in st.session_state:
    st.session_state.plot = None
    
# Input parameters
diameter = st.number_input("Diameter (m):", min_value=0.0, value=1.0, step=0.1, format="%.1f")
slope = st.number_input("Slope (m/m):", value=0.01, format="%.4f")
manning_n = st.number_input("Manning's roughness coefficient (n):", min_value=0.009, step=0.001, value=0.013, format="%.3f")
invert_level = st.number_input("Invert Level (mOD):", format="%.3f")

# Button to generate and plot rating curve
if st.button("Generate Rating Curve"):
    try:
        # Generate rating curve
        st.session_state.df = generate_rating_curve(diameter, slope, manning_n, invert_level)
        st.session_state.curve_generated = True
        
        # Plot the rating curve
        fig, ax = plt.subplots()
        ax.plot(st.session_state.df['Flow (m³/s)'], st.session_state.df['Elevation (mOD)'])
        ax.set_ylabel("Elevation (mOD)")
        ax.set_xlabel("Flow (m³/s)")
        ax.grid(True)
        st.session_state.plot = fig
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.curve_generated = False

# Display plot if it exists
if st.session_state.plot is not None:
    st.pyplot(st.session_state.plot)
    
# File path input and save button (outside the main if-block)
if st.session_state.curve_generated:
    file_path = st.text_input("Enter the full path and file name with extension for the CSV (e.g., C:\\Specify\\Your\\Path\\rating_curve.csv):", value="")
    if st.button("Save to specified path"):
        if file_path:
            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                # Save the DataFrame to the specified CSV file
                st.session_state.df.to_csv(file_path, index=False)
                st.success(f"File saved successfully.")
            except Exception as save_error:
                st.error(f"Error saving file: {str(save_error)}")
        else:
            st.warning("Please enter a file path before saving.")
