import streamlit as st
import re

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
st.title("Log File Checks from InfoWorks ICM")

st.markdown("""
    Upload your InfoWorks ICM log file, and check the important parameters as part of your checks.  
    SIM ID can be identified by right-clicking the run 'Model Group', clicking 'Open results manager', and checking 'ID' attribute beside the run.  
        
    """)
    
# Function to extract values from the log file
def extract_log_info(file_content):
    gpu_used = False
    volume_balance_error = None
    elapsed_clock_time = None
    network = None
    network_scenario = None
    inflow = None
    level = None
    rainfall_event = None
    innovyze_version = None
    event_details = None
    start_time = None
    requested_duration = None
    min_element_area = None
    max_element_area = None
    boundary_condition = None
    twod_zone_mass_error = None
    
    min_element_area_count = 0

    # Read the file content line by line
    lines = file_content.split('\n')

    # Check for Innovyze Workgroup Client version first
    for line in lines:
        if "InfoWorks ICM SIM" in line:
            match = re.search(r'InfoWorks ICM SIM\s*(.*)', line)
            if match:
                innovyze_version = match.group(1)

    # Process each line to extract other information
    for line in lines:
        if "VBEP -> Volume balance error %" in line:
            match = re.search(r'VBEP -> Volume balance error %\s*:\s*(-?\d+\.\d+)', line)
            if match:
                volume_balance_error = match.group(1)

        if "Elapsed clock time" in line:
            match = re.search(r'Elapsed clock time\s*=\s*(\d+s)', line)
            if match:
                elapsed_clock_time = match.group(1)

        if "GPU used successfully" in line:
            gpu_used = True

        if "Network:" in line:
            match = re.search(r'Network:\s*([-\w\s()#]+)', line)
            if match:
                network = match.group(1)

        if "Network Scenario:" in line:
            match = re.search(r'Network Scenario:\s*(\w+)', line)
            if match:
                network_scenario = match.group(1)

        if "Inflow:" in line:
            match = re.search(r'Inflow:\s*.*>\s*([\w\s%]+)', line)
            if match:
                inflow = match.group(1)
                
        if "Level:" in line:
            match = re.search(r'Level:\s*.*>\s*([^>]+)', line)
            if match:
                level = match.group(1).strip()

        if "Rainfall event:" in line:
            match = re.search(r'Rainfall event:\s*.*>\s*([^>]+)', line)
            if match:
                rainfall_event = match.group(1).strip()

        if "Event details:" in line and event_details is None:
            match = re.search(r'Event details:\s*(.*)', line)
            if match:
                event_details = match.group(1)

        if "Start time -" in line and start_time is None:
            match = re.search(r'Start time\s*-\s*(.*)', line)
            if match:
                start_time = match.group(1)

        if "Requested duration (min) -" in line and requested_duration is None:
            match = re.search(r'Requested duration \(min\)\s*-\s*(\d+)', line)
            if match:
                requested_duration = match.group(1)
                
        # Capture the second occurrence of Minimum Element Area
        if "Minimum element area (m2)" in line:
            min_element_area_count += 1
            if min_element_area_count == 2:
                match = re.search(r'Minimum element area \(m2\)\s*:\s*([\d\.]+)', line)
                if match:
                    min_element_area = match.group(1)

        if "Maximum element area (m2)" in line:
            match = re.search(r'Maximum element area \(m2\)\s*:\s*([\d\.]+)', line)
            if match:
                max_element_area = match.group(1)

        if "External Boundary Condition" in line:
            match = re.search(r'External Boundary Condition\s*:\s*(.*)', line)
            if match:
                boundary_condition = match.group(1).strip()
                
        if "2d Zone mass error (m3)" in line:
            match = re.search(r'2d Zone mass error \(m3\)\s*:\s*([\d\.]+)', line)
            if match:
                twod_zone_mass_error = match.group(1)

    return {
        "InfoWorks ICM version": innovyze_version,
        "Network": network,
        "Scenario": network_scenario,
        "Inflow": inflow,
        "Level": level,
        "Rainfall event": rainfall_event,
        "Event details": event_details,
        "Minimum Element Area (m2)": min_element_area,
        "Maximum Element Area (m2)": max_element_area,
        "External Boundary Condition": boundary_condition,
        "Start time": start_time,
        "Requested duration (min)": requested_duration,
        "VBEP": volume_balance_error,
        "2D Zone Mass Error (m3)": twod_zone_mass_error,
        "Elapsed clock time": elapsed_clock_time,
        "GPU used": "Yes" if gpu_used else "No"  
    }

uploaded_file = st.file_uploader("Upload a SIM.log file:", type="log")

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    log_info = extract_log_info(file_content)
    
    # Display additional information
    #st.subheader("Log Information:")
    
        # Display information in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("General Information:")
        st.write(f"InfoWorks ICM version: {log_info.get('InfoWorks ICM version', 'Not found')}")
        st.write(f"Network: {log_info.get('Network', 'Not found')}")
        st.write(f"Scenario: {log_info.get('Scenario', 'Not found')}")
        st.write(f"GPU used: {log_info.get('GPU used', 'Not found')}")
        st.write(f"Elapsed clock time: {log_info.get('Elapsed clock time', 'Not found')}")
    
        st.subheader("2D Zone Summary:")
        st.write(f"Minimum Element Area: {log_info.get('Minimum Element Area (m2)', 'Not found')}")
        st.write(f"Maximum Element Area: {log_info.get('Maximum Element Area (m2)', 'Not found')}")
    
        st.subheader("Boundary Conditions:")
        st.write(f"Inflow: {log_info.get('Inflow', 'Not found')}")
        st.write(f"Level: {log_info.get('Level', 'Not found')}")
        st.write(f"Rainfall event: {log_info.get('Rainfall event', 'Not found')}")
        st.write(f"External Boundary Condition: {log_info.get('External Boundary Condition', 'Not found')}")

    with col2:
        st.subheader("Event Details:")
        st.write(f"Event details: {log_info.get('Event details', 'Not found')}")
        st.write(f"Start time: {log_info.get('Start time', 'Not found')}")
        st.write(f"Requested duration (min): {log_info.get('Requested duration (min)', 'Not found')}")

        st.subheader("Mass Balance:")
        st.write(f"VBEP: {log_info.get('VBEP', 'Not found')}")
        st.write(f"2D Zone Mass Error (m3): {log_info.get('2D Zone Mass Error (m3)', 'Not found')}")
else:
    st.warning("Please upload a log file.")
