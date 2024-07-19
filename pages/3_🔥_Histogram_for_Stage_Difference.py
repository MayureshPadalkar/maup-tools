import streamlit as st
import rasterio
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import tempfile

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
st.title("Generate histogram from stage difference rasters")

def generate_bin_labels(bin_edges):
    """Generate bin labels based on bin edges."""
    bin_labels = []
    for i in range(len(bin_edges) - 1):
        if i == 0:
            bin_labels.append(f'< {bin_edges[i+1]}')
        elif i == len(bin_edges) - 2:
            bin_labels.append(f'> {bin_edges[i]}')
        else:
            bin_labels.append(f'{bin_edges[i]} to {bin_edges[i+1]}')
    return bin_labels

def create_histogram_with_labels(raster_path, bin_edges):
    # Generate bin labels from bin edges
    bin_labels = generate_bin_labels(bin_edges)
    
    # Open the raster file
    with rasterio.open(raster_path) as src:
        data = src.read(1)
    
    # Mask the nodata values
    data = np.ma.masked_equal(data, src.nodata)
    
    # Flatten the data and remove masked elements
    data = data.compressed()

    # Create a DataFrame to hold the data and categories
    df = pd.DataFrame(data, columns=['value'])
    
    # Categorize the data into the custom bins
    df['category'] = pd.cut(df['value'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    
    # Calculate total number of data points
    n_total = len(df)
    
    # Calculate frequencies as percentages
    bin_counts = df['category'].value_counts().reindex(bin_labels)
    bin_percentages = (bin_counts / n_total) * 100
    
    # Plot the histogram using seaborn
    fig, ax = plt.subplots()
    sns.histplot(df['category'], bins=bin_edges, discrete=True, stat='percent', ax=ax)
    plt.xlabel('Difference in Peak Stage (m)')
    plt.ylabel('Percentage Occurrence')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.ylim(0, 105)  # Set y-axis limits to range up to 100
    
    # Annotate values above bars
    for i, (rect, percentage) in enumerate(zip(ax.patches, bin_percentages)):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 0.005, f'{percentage:.2f}%', 
                ha='center', va='bottom')

    st.pyplot(fig)

uploaded_file = st.file_uploader("Upload a stage difference raster file (ASCII or GeoTIFF):", type=["asc", "tif", "tiff"])
bin_edges_input = st.text_input("Enter bin edges separated by commas:", "-100, -0.1, -0.05, -0.01, 0.01, 0.05, 0.1, 100")

# Convert input bin edges to a list of floats
try:
    bin_edges = list(map(float, bin_edges_input.split(',')))
except ValueError:
    st.error("Please enter valid bin edges separated by commas.")
    st.stop()

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_raster_path = tmp_file.name
    
    if st.button("Generate Histogram"):
        create_histogram_with_labels(tmp_raster_path, bin_edges)
else:
    st.warning("Please upload a raster file.")
