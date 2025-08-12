# app.py

import streamlit as st
from dotenv import load_dotenv
import os
from mission_controller import MissionController

# --- Page Configuration ---
# This must be the first Streamlit command in your script.
# It sets the overall look and feel of your page.
st.set_page_config(
    page_title="Web Audit AI: Privacy Unit",
    page_icon="🛡️",
    layout="wide",  # Use the full width of the page
    initial_sidebar_state="expanded"  # Keep the sidebar open by default
)

# --- Custom CSS for a professional dark theme ---
# We inject custom CSS to override Streamlit's default styles.
st.markdown("""
<style>
    /* Main page background */
    .stApp {
        background-color: #121212; /* A darker background */
        color: #EAEAEA;
    }
    /* Sidebar styling */
    .st-emotion-cache-6q9sum {
        background-color: #1E1E1E; /* Slightly lighter than main background */
    }
    /* Button styling */
    .stButton>button {
        border: 2px solid #00A67E;
        border-radius: 5px;
        color: #00A67E; /* A vibrant accent color */
        background-color: transparent;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        border-color: #FFFFFF;
        color: #FFFFFF;
        background-color: #00A67E;
    }
    /* Expander styling for the final report */
    .st-emotion-cache-p5msec {
        background-color: #2D2D2D;
        border: 1px solid #444444;
        border-radius: 5px;
    }
    /* Success message box styling */
    .st-emotion-cache-1xy3gy {
        border-color: #00A67E;
    }
</style>
""", unsafe_allow_html=True)


def main():
    load_dotenv()
    
    # --- Sidebar for Controls and Information ---
    # Putting all the controls in the sidebar cleans up the main page.
    with st.sidebar:
        st.header("🛡️ Web Audit AI")
        st.markdown("### Privacy Intelligence Unit")
        
        url_input = st.text_input(
            "Enter Website URL to Audit:", 
            placeholder="https://www.forbes.com"
        )

        run_button = st.button("Deploy Intelligence Unit")
        
        st.markdown("---")
        st.markdown("**How It Works:**")
        st.markdown(
            "1. **Field Agent (Scout):** A Selenium-powered agent scans the site, bypassing bot-blockers to gather raw intelligence.\n"
            "2. **The Analyst (Expert):** A specialist agent analyzes the data against a known threat database.\n"
            "3. **OSINT Analyst (Investigator):** A research agent investigates unknown domains using live web searches.\n"
            "4. **Mission Controller (Manager):** Synthesizes all intel into a final, human-readable report."
        )
        st.markdown("---")

    # --- Main Page for Displaying Results ---
    # The main page is now dedicated to showing the output.
    st.title("Mission Debrief")
    st.markdown("Results from the AI agent team will be displayed below.")

    # st.session_state is Streamlit's way of "remembering" variables between reruns.
    if "last_report" not in st.session_state:
        st.session_state.last_report = ""
    
    if "mission_log" not in st.session_state:
        st.session_state.mission_log = "Awaiting deployment..."

    # Use a container for the dynamic log messages
    log_container = st.container()
    
    if run_button:
        if not url_input or not url_input.startswith(('http://', 'https://')):
            st.warning("Please enter a valid URL in the sidebar.")
        else:
            # Instantiate the Mission Controller. Using @st.cache_resource
            # ensures it's created only once and persists across reruns.
            @st.cache_resource
            def get_mission_controller():
                return MissionController()
            mission_controller = get_mission_controller()

            with st.spinner("Mission in progress... This may take some time."):
                report = mission_controller.run_mission(url_input)
                st.session_state.last_report = report
                st.session_state.mission_log = "Mission Complete! Final report generated."

    # Display the final log message and the report
    if st.session_state.last_report:
        log_container.success(st.session_state.mission_log)
        with st.expander("Show Final Intelligence Debrief", expanded=True):
            st.markdown(st.session_state.last_report)
    else:
        log_container.info(st.session_state.mission_log)


if __name__ == '__main__':
    main()