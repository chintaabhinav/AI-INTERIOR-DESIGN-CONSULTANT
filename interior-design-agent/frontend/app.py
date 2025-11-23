# frontend/app.py
"""
Streamlit Frontend for AI Interior Design Consultant
Professional web interface for the interior design agent system
"""

import streamlit as st
import sys
import os
from pathlib import Path
import time
import json

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import run_design_consultation

# Page configuration
st.set_page_config(
    page_title="AI Interior Design Consultant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E4057;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #5C6E91;
        margin-bottom: 3rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3rem;
        font-size: 1.2rem;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 20px 0;
    }
    .info-box {
        padding: 15px;
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        border-radius: 5px;
        margin: 10px 0;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E4057;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'design_generated' not in st.session_state:
    st.session_state.design_generated = False
if 'design_result' not in st.session_state:
    st.session_state.design_result = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Sidebar - About & Instructions
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    This AI-powered system uses **5 specialized agents** working together to create 
    professional interior design plans.
    
    **The Team:**
    - 🏗️ Space Analysis Agent
    - 🎨 Style Consultant Agent
    - 🛋️ Furniture Specialist Agent
    - 💰 Budget Optimizer Agent
    - 📋 Project Manager Agent
    """)
    
    st.header("🚀 How It Works")
    st.write("""
    1. Fill in your room details
    2. Describe your style preferences
    3. Set your budget
    4. Click "Generate Design Plan"
    5. Wait 2-5 minutes while AI agents collaborate
    6. Get your complete design plan!
    """)
    
    st.header("⚙️ Powered By")
    st.write("""
    - **AI Model:** Llama 3.3 (via Groq)
    - **Framework:** CrewAI
    - **Custom Tool:** Room Layout Optimizer
    """)
    
    st.divider()
    
    st.caption("💡 **Tip:** Be specific about your preferences for best results!")

# Main content
st.markdown('<p class="main-header">🏠 AI Interior Design Consultant</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your space with AI-powered design recommendations</p>', unsafe_allow_html=True)

# Only show form if results not being displayed
if not st.session_state.show_results:
    st.markdown('<p class="section-header">📝 Tell Us About Your Space</p>', unsafe_allow_html=True)
    
    # Input Form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Room Details")
        
        room_type = st.selectbox(
            "Room Type",
            ["Living Room", "Bedroom", "Office", "Dining Room", "Kitchen", "Guest Room"],
            help="What type of room are you designing?"
        )
        
        room_length = st.number_input(
            "Length (feet)",
            min_value=6.0,
            max_value=50.0,
            value=15.0,
            step=0.5,
            help="Room length in feet"
        )
        
        room_width = st.number_input(
            "Width (feet)",
            min_value=6.0,
            max_value=50.0,
            value=12.0,
            step=0.5,
            help="Room width in feet"
        )
        
        room_height = st.number_input(
            "Ceiling Height (feet)",
            min_value=7.0,
            max_value=15.0,
            value=9.0,
            step=0.5,
            help="Ceiling height in feet"
        )
        
        st.subheader("Architectural Features")
        
        windows = st.text_input(
            "Windows",
            value="One large window on north wall",
            help="Describe window locations and sizes"
        )
        
        doors = st.text_input(
            "Doors",
            value="Entry door on south wall",
            help="Describe door locations"
        )
    
    with col2:
        st.subheader("Design Preferences")
        
        style_preference = st.selectbox(
            "Design Style",
            [
                "Modern Scandinavian",
                "Mid-Century Modern",
                "Industrial",
                "Bohemian",
                "Minimalist",
                "Traditional",
                "Coastal",
                "Farmhouse",
                "Contemporary",
                "Transitional"
            ],
            help="Choose your preferred design style"
        )
        
        color_preference = st.text_area(
            "Color Preferences",
            value="Warm whites, light grays, natural wood tones",
            height=80,
            help="Describe your color preferences"
        )
        
        must_haves = st.text_area(
            "Must-Have Items/Features",
            value="Comfortable seating for 4-5, TV area, storage",
            height=80,
            help="What furniture or features are essential?"
        )
        
        avoid = st.text_area(
            "Things to Avoid",
            value="Nothing too minimal or cold, heavy dark furniture",
            height=80,
            help="What styles or items should we avoid?"
        )
        
        st.subheader("Budget")
        
        budget = st.number_input(
            "Total Budget (USD)",
            min_value=500,
            max_value=50000,
            value=4000,
            step=100,
            help="Your total budget for furniture and decor"
        )
    
    st.markdown("---")
    
    # Show summary before generation
    with st.expander("📋 Review Your Input"):
        st.write(f"**Room:** {room_type} ({room_length}' × {room_width}')")
        st.write(f"**Style:** {style_preference}")
        st.write(f"**Budget:** ${budget:,}")
        st.write(f"**Must-haves:** {must_haves}")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎨 Generate My Design Plan", type="primary"):
            # Store form data in session state BEFORE switching pages
            st.session_state.form_data = {
                'room_type': room_type,
                'room_length': room_length,
                'room_width': room_width,
                'room_height': room_height,
                'windows': windows,
                'doors': doors,
                'style_preference': style_preference,
                'color_preference': color_preference,
                'must_haves': must_haves,
                'avoid': avoid,
                'budget': budget
            }
            st.session_state.show_results = True
            st.rerun()

# Results page
if st.session_state.show_results:
    
    if not st.session_state.design_generated:
        st.markdown('<p class="section-header">🤖 AI Agents Working on Your Design</p>', unsafe_allow_html=True)
        
        st.info("⏱️ This will take approximately **2-5 minutes**. Please be patient while our AI agents collaborate!")
        
        # Progress indicators
        progress_container = st.container()
        
        with progress_container:
            # Agent status
            st.markdown("### 👥 Agent Status")
            
            agent_status = st.empty()
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate agent progress
            agents_list = [
                ("🏗️ Space Analysis Agent", "Analyzing room dimensions and layout..."),
                ("🎨 Style Consultant Agent", "Defining design style and aesthetics..."),
                ("🛋️ Furniture Specialist Agent", "Searching for perfect furniture pieces..."),
                ("💰 Budget Optimizer Agent", "Optimizing costs and finding deals..."),
                ("📋 Project Manager Agent", "Compiling final design report...")
            ]
            
            # Create status display
            status_html = '<div style="background: #f0f2f6; padding: 20px; border-radius: 10px;">'
            for agent_name, agent_task in agents_list:
                status_html += f'<p>⏳ <strong>{agent_name}:</strong> {agent_task}</p>'
            status_html += '</div>'
            
            agent_status.markdown(status_html, unsafe_allow_html=True)
            
            # Get form data from session state
            form_data = st.session_state.form_data
            
            # Actually run the consultation
            try:
                with st.spinner("AI agents are collaborating..."):
                    result = run_design_consultation(
                        room_type=form_data['room_type'].lower(),
                        room_length=float(form_data['room_length']),
                        room_width=float(form_data['room_width']),
                        room_height=float(form_data['room_height']),
                        windows=form_data['windows'],
                        doors=form_data['doors'],
                        style_preference=form_data['style_preference'],
                        color_preference=form_data['color_preference'],
                        must_haves=form_data['must_haves'],
                        budget=int(form_data['budget']),
                        avoid=form_data['avoid']
                    )
                
                progress_bar.progress(100)
                status_text.success("✅ Design plan generated successfully!")
                
                # Store result in session state
                st.session_state.design_result = result
                st.session_state.design_generated = True
                
                time.sleep(1)  # Brief pause to show success
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error generating design plan: {str(e)}")
                st.warning("Please try again or contact support if the issue persists.")
                
                # Show detailed error for debugging
                with st.expander("🔍 Error Details (for debugging)"):
                    st.code(str(e))
                    import traceback
                    st.code(traceback.format_exc())
                
                if st.button("← Back to Form"):
                    st.session_state.show_results = False
                    st.rerun()
    
    else:
        # Show results
        result = st.session_state.design_result
        form_data = st.session_state.form_data
        
        if result and result.get("success"):
            st.markdown('<p class="section-header">✅ Your Design Plan is Ready!</p>', unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button("🔄 Create New Design"):
                    st.session_state.design_generated = False
                    st.session_state.design_result = None
                    st.session_state.show_results = False
                    st.session_state.form_data = {}
                    st.rerun()
            
            with col2:
                if result.get("report_file") and os.path.exists(result["report_file"]):
                    with open(result["report_file"], 'r') as f:
                        st.download_button(
                            label="📥 Download Report",
                            data=f.read(),
                            file_name=f"design_plan_{result['timestamp']}.txt",
                            mime="text/plain"
                        )
            
            st.markdown("---")
            
            # Display the design plan
            st.markdown("### 📄 Complete Design Plan")
            
            # Create tabs for different sections
            tab1, tab2, tab3 = st.tabs(["📋 Full Report", "💡 Quick Summary", "📊 Metadata"])
            
            with tab1:
                st.markdown("""
                <div style='background: white; padding: 30px; border-radius: 10px; 
                            border: 2px solid #4CAF50;'>
                """, unsafe_allow_html=True)
                
                # Display the full report
                report_text = result.get("result", "")
                st.markdown(report_text)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with tab2:
                # Extract key info for summary
                st.success("✅ Design plan created successfully!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Room Type", form_data.get('room_type', 'N/A'))
                    st.metric("Room Size", f"{form_data.get('room_length', 0)}' × {form_data.get('room_width', 0)}'")
                
                with col2:
                    st.metric("Design Style", form_data.get('style_preference', 'N/A'))
                    st.metric("Budget", f"${form_data.get('budget', 0):,}")
                
                with col3:
                    st.metric("Report File", "✅ Saved")
                    st.metric("Timestamp", result.get("timestamp", "N/A"))
                
                st.info(f"📁 **Full report saved to:** `{result.get('report_file', 'N/A')}`")
            
            with tab3:
                st.json(result.get("metadata", {}))
        
        else:
            st.error("❌ Failed to generate design plan")
            if result:
                st.error(f"Error: {result.get('error', 'Unknown error')}")
                
                # Show detailed error
                with st.expander("🔍 Error Details"):
                    st.json(result)
            
            if st.button("← Back to Form"):
                st.session_state.show_results = False
                st.session_state.design_generated = False
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏠 <strong>AI Interior Design Consultant</strong> | Powered by CrewAI & Llama 3.3</p>
    <p style='font-size: 0.9rem;'>Built with ❤️ using Python, Streamlit, and Multi-Agent AI</p>
</div>
""", unsafe_allow_html=True)