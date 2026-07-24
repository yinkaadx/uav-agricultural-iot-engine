import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="UAV-Assisted IoT Engine", layout="wide")

st.title("Serverless UAV Edge-Cloud Pipeline")
st.caption("Agricultural IoT Disconnected Environment Simulation & UAV Swarm Data Harvesting")

st.sidebar.header("Network Configuration")
selected_zone = st.sidebar.selectbox("Infrastructure-Limited Zone", ["Remote Alpine Pasture (Soil Sensors)", "Deep Forest Canopy (Micro-Climate)", "Disaster Impact Area (Seismic)"])
uav_frequency = st.sidebar.slider("UAV Swarm Harvesting Interval (Seconds)", 5, 20, 10)
run_simulation = st.sidebar.button("Initialize Disconnected IoT Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: Local Caching -> UAV Burst Retrieval -> AWS Lambda Sync")

if run_simulation:
    st.subheader(f"Active Disconnected Environment: {selected_zone}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_buffer = col1.empty()
    metric_uav = col2.empty()
    metric_cloud = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(1515)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    local_buffer_size = []
    cloud_database_size = []
    
    current_buffer = 0
    current_cloud = 0
    
    for i in range(100):
        data_generated = int(np.random.uniform(500, 1500))
        current_buffer += data_generated
        
        is_uav_harvesting = (i % uav_frequency == 0 and i != 0)
        
        if is_uav_harvesting:
            harvested_data = current_buffer
            current_buffer = 0 
            current_cloud += harvested_data
            uav_status = "HARVESTING"
            network_status = "UAV PROXIMITY LINK ACTIVE"
        else:
            uav_status = "PATROLLING"
            network_status = "TERRESTRIAL NETWORK DISCONNECTED"
            
        local_buffer_size.append(current_buffer)
        cloud_database_size.append(current_cloud)
        
        metric_buffer.metric("Ground Sensor Local Cache", f"{current_buffer:,} Nodes", "Offline Storage")
        
        if is_uav_harvesting:
            metric_uav.metric("UAV Edge Node Status", uav_status, f"+{harvested_data:,} Retrieved")
        else:
            metric_uav.metric("UAV Edge Node Status", uav_status, "Awaiting Intercept")
            
        metric_cloud.metric("AWS Cloud Central Database", f"{current_cloud:,} Nodes", "Serverless Ledger")
        
        if is_uav_harvesting:
            metric_status.metric("System State", network_status, "Burst Transmission")
        else:
            metric_status.metric("System State", network_status, "Hibernation Mode", delta_color="inverse")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=local_buffer_size, mode='lines', name='Disconnected Sensor Cache', fill='tozeroy', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=cloud_database_size, mode='lines', name='Total Cloud Ingestion', yaxis='y2', line=dict(color='blue')))
        
        fig.update_layout(
            title="Infrastructure-Limited IoT: Ground Caching vs UAV Burst Harvesting",
            xaxis=dict(title="Mission Timeline"),
            yaxis=dict(title="Local Cache Volume (Nodes)"),
            yaxis2=dict(title="Total Cloud Storage", overlaying='y', side='right', range=[0, max(1000, current_cloud + 5000)]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if is_uav_harvesting:
            log_placeholder.success(f"UAV SWARM INTERCEPT: Mobile edge node established connection at {time_steps[i].strftime('%H:%M:%S')}. Initiating high-bandwidth burst transmission to AWS Lambda. {harvested_data:,} telemetry nodes successfully synchronized.")
        else:
            log_placeholder.warning(f"Log: Tick {i} generated. No cellular infrastructure detected. IoT sensors defaulting to Information-Centric local caching to preserve battery.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless edge-cloud architecture successfully preserved 100% of telemetry in a completely disconnected agricultural environment.")
else:
    st.info("Click 'Initialize Disconnected IoT Engine' in the sidebar to simulate UAV data harvesting.")