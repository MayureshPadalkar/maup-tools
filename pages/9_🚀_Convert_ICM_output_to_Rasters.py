import streamlit as st
import os
import subprocess

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
    
# Function to list directories in a given path
def list_dirs(path):
    try:
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    except Exception as e:
        st.warning(f"Please enter a valid input folder path.")
        return []

# Function to rasterize shapefiles to GeoTIFF, using folder names for output filenames
def rasterize_shapefiles(input_folder, output_folder, raster_types, cell_size):
    for root, dirs, files in os.walk(input_folder):
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

# Main input folder selection
root_input_folder = st.text_input('Enter the input folder:', value='C:/')
input_subdirs = list_dirs(root_input_folder)
selected_input_subdir = st.selectbox('Select input folder:', input_subdirs)

if selected_input_subdir:
    main_input_folder = os.path.join(root_input_folder, selected_input_subdir)
else:
    main_input_folder = None

# Output folder selection
root_output_folder = st.text_input('Enter the output folder:', value='C:/mention/the/output/folder')
if root_output_folder:
    final_output_folder = os.path.abspath(root_output_folder)
else:
    final_output_folder = None
    st.warning("Please enter a valid output folder path.")

# Raster type selection
raster_type = st.selectbox('Select the hydraulic parameter that you want to process:', ['DEPTH2D', 'elevation2', 'Both'], index=2)

# Cell size selection
cell_size = st.number_input('Enter cell size:', min_value=0.5, value=2.0, step=0.5, format="%.1f")

# Process button
if st.button('Process Shapefile'):
    if not selected_input_subdir or not root_output_folder:
        st.error('Please select both input and output folders.')
    else:
        # Convert paths to absolute paths
        main_input_folder = os.path.abspath(main_input_folder)
        final_output_folder = os.path.abspath(final_output_folder)
        
        # Create output folder if it doesn't exist
        os.makedirs(final_output_folder, exist_ok=True)
        
        # Determine rasterize types based on user selection
        if raster_type == 'Both':
            rasterize_types = ['DEPTH2D', 'elevation2']
        else:
            rasterize_types = [raster_type]
        
        # Call the rasterize function
        rasterize_shapefiles(main_input_folder, final_output_folder, rasterize_types, cell_size)