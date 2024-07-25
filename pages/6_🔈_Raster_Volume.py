import streamlit as st
import rasterio
import numpy as np

st.logo("images/logo.png", icon_image="images/logo.png")

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
st.title("Calculate Volume of a Depth Raster")

st.markdown("""
    This tool uses the depth values and cell size from a raster to calculate the total volume.  
    Negative values will reduce the total volume.  
    No data values are ignored. 
    """)
    
st.markdown("""
    This tool should particularly be used after you've clipped the depth raster behind the reservoir/bund in QGIS 3.x or ArcMap.  
    """)

def calculate_volume(geotiff_file):
    with rasterio.open(geotiff_file) as src:
        # Read the depth values from the raster
        depths = src.read(1, masked=True).astype(np.float64)  # Ensure using a data type with large range

        # Get the cell size from the raster metadata
        cell_size_x = src.transform[0]
        cell_size_y = -src.transform[4]
       
        # Calculate volume per cell
        with np.errstate(over='ignore'):  # Ignore overflow warnings
            volumes = depths * cell_size_x * cell_size_y

        # Check for any infinities resulted from overflow
        if np.isinf(volumes).any():
            print("Warning: Overflow encountered during volume calculation.")

        # Calculate total volume
        total_volume = np.nansum(volumes)  # Use nansum to handle masked elements

        return total_volume
        
uploaded_file = st.file_uploader("Upload a raster file (ASCII or GeoTIFF):", type=["asc", "tif", "tiff"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("uploaded_file.tif", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Calculate the volume
    volume = calculate_volume("uploaded_file.tif")

    # Format the volume to display with three decimal places
    formatted_volume = "{:.3f}".format(volume)

    st.write("Total Volume:", formatted_volume, "cubic units")
else:
    st.warning("Please upload a raster file.")