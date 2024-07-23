import streamlit as st

st.set_page_config(
	page_title="Streamlit Multipage App"
)

#st.logo("images/logo.png", icon_image="images/logo.png")
st.title("Modelling checks and Geospatial applications for Flood Modellers")

st.markdown(
    """
    This multi-page web app can be used for the following:  
        - Mass balance checks from TUFLOW output  
        - Courant numbers checks from HPC TUFLOW output  
        - Histogram for plotting stage difference rasters  
        - Rating curve calculator for a circular pipe  
        - Roughness converter: Manning's to Colebrook-White roughness and vice-versa

    """
)

st.info("Click on the left sidebar menu to navigate to the different apps.")

st.subheader("Developed by")
st.image("images/developedby.gif")

st.subheader("Acknowledgements")
st.markdown(
    """
    To my family, colleagues, and alma mater.

    """
)

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
