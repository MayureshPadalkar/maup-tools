import streamlit as st

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
st.title("Manning's to Colebrook-White Roughness Converter")

st.markdown("""
    The calculations are based on work by Ackers P., Resistance of fluids flowing in channels and pipes, Paper No. 1, HMSO, London, 1958, which shows that if the relative roughness lies between 7 and 130, then Manning's roughness gives a good approximation to Colebrook-White roughness.
    """)

def manning_to_colebrook(n):
    # Empirical relationship commonly used in hydraulic engineering
    k_mm = (n * 83.3) ** 6
    return k_mm
    
# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Input box for Manning's n
    n = st.number_input("Enter Manning's roughness (n):", value=0.015, min_value=0.007, step=0.001, format="%.3f")

with col2:
    # Output box for Colebrook-White roughness
    k_mm = manning_to_colebrook(n) if n > 0 else ""
    #st.number_input("Corresponding Colebrook-White roughness (k in mm):", value=k_mm if k_mm else "", format="%.4f", disabled=True)
    st.text_input("Corresponding Colebrook-White roughness (k in mm):", value=f"{k_mm:.4f}" if k_mm else "", disabled=True)