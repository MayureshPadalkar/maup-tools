import streamlit as st
import dask_geopandas as dgpd
import dask
import os
from tempfile import NamedTemporaryFile

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
st.title("Visualise ICM Vectors in GIS")

st.markdown("""
    This tool converts InfoWorks ICM "2D Zones.shp" polygons to points, to visualise the output in any GIS software.  
    Please remove the double quotations if you're copying and pasting the shapefile as 'Copy as path'.  
    Optionally, there is a provision to download the QML file after the processing is complete to style the points shapefile in QGIS.  
        
    """)

def process_shapefile(file_path, output_path): 
    # Load the shapefile into a Dask GeoDataFrame
    ddf = dgpd.read_file(file_path, npartitions=4)

    # Filter out rows with zero DEPTH2D, i.e. remove rows of 0 depths
    ddf = ddf[ddf['DEPTH2D'] != 0]

    # Calculate centroids and create a new Dask GeoDataFrame
    ddf_points = ddf.copy()
    ddf_points['geometry'] = ddf.geometry.centroid

    # Calculate X and Y components
    ddf_points['X'] = ddf['SPEED2D'] * dask.array.cos(ddf['MAXANGLE2D'])
    ddf_points['Y'] = ddf['SPEED2D'] * dask.array.sin(ddf['MAXANGLE2D'])

    # Compute and save the Dask GeoDataFrame to a new shapefile
    ddf_points.compute().to_file(output_path)

# Provide an option to select a pre-uploaded file
uploaded_file = st.file_uploader("Upload a Shapefile (.shp):", type="shp")

# Get output path from user
output_path = st.text_input("Enter the output path including filename and .shp extension:")

if uploaded_file is not None:
    try:
        # Save the uploaded file to a temporary location
        with NamedTemporaryFile(delete=False, suffix=".shp") as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_file_path = temp_file.name

        # Process the shapefile
        process_shapefile(temp_file_path, output_path)
        
        st.success(f"Processed shapefile is saved as {output_path}.")
    
    except FileNotFoundError as e:
        st.error(f"Error: {str(e)}")
    except ValueError as e:
        st.error(f"Error: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.warning("Please upload a shapefile to process.")
