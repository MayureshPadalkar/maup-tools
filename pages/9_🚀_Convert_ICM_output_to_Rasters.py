import streamlit as st
import os
import subprocess
import tkinter as tk
from tkinter import filedialog

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
st.title("Convert InfoWorks ICM 2D Zones to Depth and Stage Rasters")

st.markdown("""
    This tool converts InfoWorks ICM "2D Zones.shp" to depth and/or stage GeoTIFF raster/s.  
    The user has flexibility to choose the cell size.  
    In InfoWorks ICM, the shapefile should be exported using Results > Export Maxima to GIS > To SHP, and with no threshold.  
        
    """)
    
# Function to rasterize shapefiles to GeoTIFF, using folder names for output filenames
def rasterize_shapefiles(input_folders, output_folder, raster_types, cell_size):
    for folder in input_folders:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file == '2D Zones.shp':
                    shapefile_path = os.path.join(root, file)
                    folder_name = os.path.basename(root)
                    for raster_type in raster_types:
                        if raster_type == 'DEPTH2D':
                            output_filename = f"{folder_name}_d_Max.tif"
                        else:
                            output_filename = f"{folder_name}_h_Max.tif"
                        output_tiff_path = os.path.join(output_folder, output_filename)
                        command = [
                            "gdal_rasterize",
                            "-a",
                            raster_type,
                            "-tr",
                            str(cell_size),
                            str(cell_size),
                            "-a_nodata",
                            "-9999",
                            shapefile_path,
                            output_tiff_path
                        ]
                        subprocess.run(command, check=True)
    st.success('2D Zones.shp are converted to rasters successfully.')

# Allow user to input the root directory
root_dir = st.text_input("Enter the root directory containing your input folders:")

input_folders = []
if root_dir and os.path.isdir(root_dir):
    # Get list of folders in the root directory
    folder_list = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]
    
    # Allow users to select multiple input folders
    selected_folders = st.multiselect("Select input folders", folder_list)
    
    # Convert selected folder names to full paths
    input_folders = [os.path.join(root_dir, folder) for folder in selected_folders]
else:
    st.warning("Please enter a valid root directory path.")

# Output folder selection using text input
output_folder = st.text_input('Enter the output folder:')
if output_folder:
    if not os.path.isdir(output_folder):
        st.warning(f"Please enter a valid output folder path.")
else:
    st.warning("Please enter a valid output folder path.")

# Raster type selection
raster_type = st.selectbox('Select the hydraulic parameter that you want to process:', ['DEPTH2D', 'elevation2', 'Both'], index=2)

# Cell size selection
cell_size = st.number_input('Enter cell size:', min_value=0.5, value=2.0, step=0.5, format="%.1f")

# Process button
if st.button('Process Shapefile'):
    if not input_folders or not output_folder:
        st.error('Please select both input and output folders.')
    else:
        os.makedirs(output_folder, exist_ok=True)
        if raster_type == 'Both':
            rasterize_types = ['DEPTH2D', 'elevation2']
        else:
            rasterize_types = [raster_type]
        try:
            rasterize_shapefiles(input_folders, output_folder, rasterize_types, cell_size)
        except Exception as e:
            st.error(f"Error during rasterization: {e}")
