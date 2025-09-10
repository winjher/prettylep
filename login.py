"""
Login and registration forms for the butterfly breeding management system
"""

import streamlit as st
from auth.authentication import AuthenticationManager, init_session_state, User

def render_login_form():
    """Render the main login/registration interface"""

    # Initialize authentication
    init_session_state()
    auth_manager = AuthenticationManager()

    # Apply custom CSS for the login form.
    # The main selector targets the Streamlit container that holds our login UI
    # by looking for a unique child element (.login-header) inside it.
    st.markdown(
        """
        <style>
        /* This selector targets the container that wraps all our login elements */
        div[data-testid="stVerticalBlock"]:has(div.login-header) {
            max-width: 450px;
            margin: 0 auto;
            padding: 40px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-top: 50px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            color: #4a5568;
            font-size: 2rem;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .login-header p {
            color: #718096;
            font-size: 1rem;
            margin: 0;
        }
        
        /* Custom styling for the buttons to act as tabs */
        .stButton > button {
            border-radius: 8px;
            padding: 12px;
            transition: all 0.3s ease;
            background-color: #f7fafc;
            color: #718096;
            border: none;
        }

        .stButton > button:hover {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
        }
        
        .admin-info {
            background: #f0f4f8;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 0.9rem;
            color: #4a5568;
            text-align: center;
        }
        
        .admin-info strong {
            color: #2d3748;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #4a5568;
        }
        
        .stSelectbox > div > div {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
        }
        
        .stTextInput > div > div > input {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 12px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Primary button styling */
        .stButton > button[kind="primary"] {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
        }
        
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Use a single container to wrap all login UI elements
    with st.container():
        # Header
        st.markdown(
            """
            <div class="login-header">
                <h1>🦋 Butterfly Breeding</h1>
                <p>Professional Breeding Management System</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Tab selection
        tab_col1, tab_col2 = st.columns(2)

        if 'active_auth_tab' not in st.session_state:
            st.session_state.active_auth_tab = 'login'

        with tab_col1:
            if st.button("Login", key="login_tab", use_container_width=True):
                st.session_state.active_auth_tab = 'login'

        with tab_col2:
            if st.button("Register", key="register_tab", use_container_width=True):
                st.session_state.active_auth_tab = 'register'

        # Render appropriate form based on the active tab
        if st.session_state.active_auth_tab == 'login':
            render_login_tab(auth_manager)
        else:
            render_register_tab(auth_manager)

def render_login_tab(auth_manager):
    """Render login form"""
    
    with st.form("login_form"):
        st.markdown("### Login to Your Account")
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        login_submitted = st.form_submit_button("🔐 Login", type="primary", use_container_width=True)
        
        if login_submitted:
            if username and password:
                success, user = auth_manager.authenticate_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.user_type = user.user_type
                    st.success(f"Welcome back, {user.first_name}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please fill in all fields")

    # Admin info
    st.markdown(
        """
        <div class="admin-info">
            <strong>Default Admin Login:</strong><br>
            Username: admin<br>
            Password: admin123
        </div>
        """,
        unsafe_allow_html=True
    )

def render_register_tab(auth_manager):
    """Render registration form"""
    
    with st.form("register_form"):
        st.markdown("### Create New Account")
        
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name *",
                placeholder="John",
                key="reg_first_name"
            )
            
            username = st.text_input(
                "Username *",
                placeholder="john_doe",
                key="reg_username"
            )
            
            user_type = st.selectbox(
                "User Type *",
                options=['breeder', 'purchaser', 'student', 'faculty', 'enthusiast'],
                key="reg_user_type"
            )
        
        with col2:
            last_name = st.text_input(
                "Last Name *",
                placeholder="Doe",
                key="reg_last_name"
            )
            
            email = st.text_input(
                "Email *",
                placeholder="john@example.com",
                key="reg_email"
            )
            
            contact_number = st.text_input(
                "Contact Number",
                placeholder="+1234567890",
                key="reg_contact"
            )
        
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Enter a strong password",
            key="reg_password",
            help="Password must be at least 8 characters with uppercase, lowercase, and numbers"
        )
        
        confirm_password = st.text_input(
            "Confirm Password *",
            type="password",
            placeholder="Confirm your password",
            key="reg_confirm_password"
        )
        
        address = st.text_area(
            "Address",
            placeholder="Enter your full address (optional)",
            key="reg_address",
            height=80
        )
        
        register_submitted = st.form_submit_button("📝 Create Account", type="primary", use_container_width=True)
        
        if register_submitted:
            # Validate required fields
            if not all([first_name, last_name, username, email, password, confirm_password]):
                st.error("Please fill in all required fields marked with *")
                return
            
            # Validate password confirmation
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            # Register user
            success, message = auth_manager.register_user(
                username=username,
                password=password,
                email=email,
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                address=address if address else None,
                contact_number=contact_number if contact_number else None
            )
            
            if success:
                st.success("Account created successfully! Please login with your new credentials.")
                st.session_state.active_auth_tab = 'login'
                st.rerun()
            else:
                st.error(message)

def create_default_admin():
    """Create default admin user if not exists"""
    try:
        auth_manager = AuthenticationManager()
        
        # Check if admin user exists
        admin_user = auth_manager.session.query(User).filter(User.username == 'admin').first()
        
        if not admin_user:
            success, message = auth_manager.register_user(
                username='admin',
                password='admin123',
                email='admin@butterfly.com',
                user_type='breeder',
                first_name='Admin',
                last_name='User',
                address='System Administrator',
                contact_number='+1234567890'
            )
            
            if success:
                print("Default admin user created successfully")
            else:
                print(f"Failed to create admin user: {message}")
    
    except Exception as e:
        print(f"Error creating default admin: {e}")

# Example of how to run this page (assuming you have a main app file)
# if __name__ == "__main__":
#     render_login_form()

