import streamlit as st
import os
#from modules.database import init_database
from modules.auth import handle_authentication
from modules.breeding_management import breeding_management_app
from modules.ai_classification import ai_classification_app
#from modules.point_of_sale import point_of_sale_app
#from modules.sales_tracking import sales_tracking_app
#from modules.booking_system import booking_system_app
#from modules.student_dashboard import student_dashboard_app
#from modules.faculty_dashboard import faculty_dashboard_app
#from modules.purchaser_profile import purchaser_profile_app
from modules.profile_management import profile_management_app
#from modules.premium_system import premium_system_app, admin_premium_management
#from modules.email_notifications import email_notifications_app
#from modules.landing_page import enhanced_landing_page
# from modules.database import initialize_databases
#from modules.ui_components import apply_glassmorphism_style, set_background_image
from modules.larval_stages import larval_stages_app
#from modules.database import database_app
#from modules.profit_calculator import calculate_batch_app
# from modules.batch_management import get_active_batches_count
# from modules.hostplants import get_host_plants, get_species_list, get_all_host_plants, get_plant_characteristics, get_species_by_plant, calculate_daily_foliage_demand
# Page configuration
import datetime
import base64 
def set_background_image(image_path):
    """
    Sets a background image for the Streamlit application using CSS.
    Args:
        image_path (str): The path to the local image file.
    """
    try:
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{_get_base64_image(image_path)}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"Background image '{image_path}' not found. Please ensure it's in the correct path.")
    except Exception as e:
        st.error(f"Error setting background image: {e}")

def _get_base64_image(image_path):
    """Helper to convert local image to base64 for CSS background."""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- Apply the background image ---
# Ensure 'icon/bg.png' is in the correct path relative to your Streamlit app's root
set_background_image('icon/bg.jpg') 
#set_background_image('icon/bgbutterfly.jpg') 
# --- Glasmorphism CSS ---
st.markdown(
    """
    <style>
    body {
        color: #333333;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #222222;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stTextInput label, .stSelectbox label, .stRadio label, .stFileUploader label, .stCameraInput label {
        color: #333333;
        font-weight: bold;
    }
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: #333333;
        transition: all 0.3s ease;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.3);
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }
    .col-card {
            flex: 1 1 calc(25% - 20px);
            min-width: 220px;
            max-width: 250px;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            background-color: #fcfcfc;
            transition: transform 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    .css-pkaj6s { /* Common class for the sidebar parent div */
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin-right: 10px;
    }
    .glasmorphism-card {
        background: rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 15px;
        margin-bottom: 15px;
    }
    .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card h3 {
            color: #4a5568;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .stat-card h4 {
            font-size: 2rem;
            margin-bottom: 10px;
        }

        .stat-card p {
            opacity: 0.9;
            font-size: 1.1rem;
        }

        .batch-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }

        .batch-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }

        .batch-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }

        .batch-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .batch-id {
            font-weight: bold;
            color: #4a5568;
            font-size: 1.1rem;
        }

        .lifecycle-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
        }

        .lifecycle-egg { background: #ffeaa7; color: #2d3436; }
        .lifecycle-larva { background: #74b9ff; color: white; }
        .lifecycle-pupa { background: #fd79a8; color: white; }
        .lifecycle-adult { background: #00b894; color: white; }

        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }

        .status-healthy { background: #00b894; }
        .status-warning { background: #fdcb6e; }
        .status-critical { background: #e17055; }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #4a5568;
        }

        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #667eea;
        }

        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
            margin-right: 10px;
            margin-bottom: 10px;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #718096;
        }

        .btn-danger {
            background: #e53e3e;
        }

        .btn-success {
            background: #38a169;
        }

        .btn-small {
            padding: 8px 16px;
            font-size: 0.9rem;
        }

        .alert {
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid;
        }

        .alert-success {
            background: #f0fff4;
            border-color: #38a169;
            color: #22543d;
        }

        .alert-warning {
            background: #fffbf0;
            border-color: #d69e2e;
            color: #744210;
        }

        .alert-danger {
            background: #fff5f5;
            border-color: #e53e3e;
            color: #742a2a;
        }

        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transition: width 0.3s ease;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
        }

        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 15px;
            width: 90%;
            max-width: 800px;
            position: relative;
            max-height: 80vh;
            overflow-y: auto;
        }

        .close {
            position: absolute;
            right: 20px;
            top: 20px;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            color: #718096;
        }

        .close:hover {
            color: #4a5568;
        }

        .qr-code {
            text-align: center;
            margin: 20px 0;
        }

        .qr-code img {
            max-width: 200px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .nav-tabs {
                flex-direction: column;
            }
            
            .batch-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            padding: 15px 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            z-index: 1001;
            max-width: 300px;
            transform: translateX(350px);
            transition: transform 0.3s ease;
        }

        .notification.show {
            transform: translateX(0);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ADD this as the very first Streamlit command:
st.set_page_config(page_title="AI Butterfly Classification", page_icon="🦋", layout="wide")

# st.set_page_config(
#     page_title="🦋 Butterfly Breeding Ecosystem",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Initialize databases and directories
# initialize_databases()

# Apply styling
# apply_glassmorphism_style()
# try:
#     set_background_image('icon/bg.png')
# except:
#     pass  # Background image is optional

def main():
    """Main application entry point"""

    # Handle authentication
    if not handle_authentication():
        return

    # Main navigation
    st.sidebar.title("🦋 LepVision")
    st.sidebar.write(f"Welcome, **{st.session_state.username}**!")

    # Navigation menu with role-based access
    apps = {
        "🏠 Dashboard": "dashboard",
        "👤 My Profile": "profile",
        # "💎 Premium System": "premium",
        "🦋 Breeding Management": "breeding",
        "🐛 Larval Stages": "larval_stages",
        "🤖 AI Classification": "ai_classification",
        # "💰 Point of Sale": "pos",
        # "📊 Sales Tracking": "sales_tracking",
        # "🌱 Host Plants": "host_plants",
        # "🌱 Batch Management": "batch_management",
        # "🌍 Farm Booking": "booking",
        
    }

    # Add admin-only features
    if st.session_state.get('user_role') == 'admin':
        apps["🔧 Premium Admin"] = "premium_admin"
        apps["📧 Email Notifications"] = "email_notifications"

    # Add role-specific dashboards
    if st.session_state.get('user_role') == 'student':
        apps["🎓 Student Dashboard"] = "student_dashboard"
    
    if st.session_state.get('user_role') == 'faculty':
        apps["🎓 Faculty Dashboard"] = "faculty_dashboard"

    if st.session_state.get('user_role') == 'purchaser':
        apps["🛒 Purchaser Profile"] = "purchaser_profile"

    # Role-based feature highlighting
    if st.session_state.get('user_role') in ['breeder', 'faculty']:
        st.sidebar.info("🔬 You have access to advanced breeding features")
    elif st.session_state.get('user_role') == 'purchaser':
        st.sidebar.info("🛒 Enhanced purchasing features available")
    elif st.session_state.get('user_role') == 'student':
        st.sidebar.success("📚 Student Dashboard with TESDA modules available")
    elif st.session_state.get('user_role') == 'enthusiast/tourist':
        st.sidebar.info("🦋 Tourism and booking features optimized for you")
    elif st.session_state.get('user_role') == 'admin':
        st.sidebar.info("🔧 Admin features available"
                        "\n- Manage Premium Users"
                        "\n- Send Email Notifications")
    selected_app = st.sidebar.selectbox("Select Application", list(apps.keys()))

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Route to selected application
    app_key = apps[selected_app]

    if app_key == "dashboard":
        dashboard_app()
    elif app_key == "profile":
        profile_management_app()
    # elif app_key == "premium":
    #     premium_system_app()
    # elif app_key == "premium_admin":
    #     admin_premium_management()
    # elif app_key == "email_notifications":
    #     email_notifications_app()
    elif app_key == "breeding":
        breeding_management_app()
    elif app_key == "ai_classification":
        ai_classification_app()
    # elif app_key == "pos":
    #     point_of_sale_app()
    # elif app_key == "sales_tracking":
    #     sales_tracking_app()
    # elif app_key == "booking":
    #     booking_system_app()
    # elif app_key == "student_dashboard":
    #     student_dashboard_app()
    # elif app_key == "faculty_dashboard":
    #     faculty_dashboard_app()
    # elif app_key == "purchaser_profile":
    #     purchaser_profile_app()
    elif app_key == "larval_stages":
        larval_stages_app()
    # elif app_key == "batch_management":
    #     batch_management_app()
    # elif app_key == "host_plants":
    #     host_plants_app()

def dashboard_app():
    """Dashboard overview of the entire ecosystem"""

    # Show enhanced landing page with signup bonus
    # enhanced_landing_page()

def get_active_batches_count():
    """Get count of active breeding batches"""
    try:
        import pandas as pd
        if os.path.exists('breeding_batches.csv'):
            df = pd.read_csv('breeding_batches.csv')
            return len(df)
    except:
        pass
    return 0

def get_species_count():
    """Get count of butterfly species"""
    from Data.butterfly_species_info import BUTTERFLY_SPECIES_INFO
    return len(BUTTERFLY_SPECIES_INFO)

def get_monthly_sales():
    """Get monthly sales count"""
    try:
        import pandas as pd
        from datetime import datetime, timedelta
        if os.path.exists('butterfly_purchases.csv'):
            df = pd.read_csv('butterfly_purchases.csv')
            # Filter for current month
            current_month = datetime.now().replace(day=1)
            df['Date'] = pd.to_datetime(df['Date'])
            monthly_sales = df[df['Date'] >= current_month]
            return len(monthly_sales)
    except:
        pass
    return 0

def get_booking_count():
    """Get farm booking count"""
    try:
        import pandas as pd
        if os.path.exists('farm_bookings.csv'):
            df = pd.read_csv('farm_bookings.csv')
            return len(df)
    except:
        pass
    return 0

 
def get_premium_users_count():
    """Get count of premium users"""
    try:
        import pandas as pd
        if os.path.exists('users.csv'):
            df = pd.read_csv('users.csv')
            premium_users = df[df['is_premium'] == True]
            return len(premium_users)
    except:
        pass
    return 0 
   


if __name__ == "__main__":
    main()
