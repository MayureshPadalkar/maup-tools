import streamlit as st
import dask_geopandas as dgpd
import dask
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
st.title("Visualise ICM Vectors in GIS")

st.markdown("""
    This tool converts InfoWorks ICM "2D Zones.shp" polygons to points, to visualise the output in GIS.  
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
uploaded_file = st.text_input("Upload a Shapefile:", value="mention/the/path.shp")

# Get output path from user
output_path = st.text_input("Enter the output path including filename and .shp extension:")


if st.button("Process Shapefile"):
    if not uploaded_file or uploaded_file == "mention/the/path.shp":
        st.warning("Please upload a shapefile.")
    else:
        try:
            if not os.path.exists(uploaded_file):
                raise FileNotFoundError(f"The file {uploaded_file} does not exist.")
            
            if not output_path:
                raise ValueError("Please specify an output path.")

            process_shapefile(uploaded_file, output_path)
            st.success(f"Processed shapefile is saved.")
            
            # Add download button for QML file
            qml_path = "themes/Point_Vectors.qml"
            if os.path.exists(qml_path):
                with open(qml_path, "rb") as file:
                    btn = st.download_button(
                        label="Download QML File",
                        data=file,
                        file_name="Point_Vectors.qml",
                        mime="application/octet-stream"
                    )
            else:
                st.warning("QML file not found. Unable to provide download option.")
            
        except FileNotFoundError as e:
            st.error(f"Error: {str(e)}")
        except ValueError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
