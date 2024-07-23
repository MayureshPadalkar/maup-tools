import streamlit as st

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
st.title("Roughness Converter")

st.markdown("""
    This calculator converts Manning's roughness (n) to Colebrook-White roughness (k in mm) and vice-versa.
    """)

st.markdown("""
    The calculations are based on work by Ackers P., Resistance of fluids flowing in channels and pipes, Paper No. 1, HMSO, London, 1958, which shows that if the relative roughness lies between 7 and 130, then Manning's roughness gives a good approximation to Colebrook-White roughness.
    """)

def manning_to_colebrook(n):
    # Empirical relationship commonly used in hydraulic engineering
    k_mm = (n * 83.3) ** 6
    return k_mm
    
def colebrook_to_manning(k_mm):
    # Empirical relationship commonly used in hydraulic engineering
    n = k_mm ** (1/6) / 83.3
    return n
    
# Callbacks to update the values
def update_from_n():
    if st.session_state.n_value < 0.008:
        st.session_state.n_value = 0.008
    st.session_state.k_value = manning_to_colebrook(st.session_state.n_value)

def update_from_k():
    min_k_value = manning_to_colebrook(0.008)
    if st.session_state.k_value < min_k_value:
        st.session_state.k_value = min_k_value
    st.session_state.n_value = colebrook_to_manning(st.session_state.k_value)

# Initialize session state variables with default values
if 'n_value' not in st.session_state:
    st.session_state['n_value'] = 0.013
if 'k_value' not in st.session_state:
    st.session_state['k_value'] = manning_to_colebrook(st.session_state['n_value'])

# Create two columns
col1, col2 = st.columns(2)

# Input in the first column for Manning's n
with col1:
    #st.header("Convert Manning's n to Colebrook's k")
    st.number_input("Enter Manning's roughness (n):", value=st.session_state.n_value, min_value=0.007, step=0.001, format="%.3f", key='n_value', on_change=update_from_n)
    #st.write(f"Colebrook's k: {st.session_state.k_value:.6f} mm")

# Input in the second column for Colebrook's k
with col2:
    #st.header("Convert Colebrook's k to Manning's n")
    min_k_value = manning_to_colebrook(0.007)
    st.number_input("Enter Colebrook-White roughness (k in mm):", value=st.session_state.k_value, min_value=min_k_value, step=0.1, format="%.4f", key='k_value', on_change=update_from_k)
    #st.write(f"Manning's n: {st.session_state.n_value:.6f}")
