import streamlit as st


# =========================================================
# LOAD THEME
# =========================================================

def load_theme():

    st.markdown(
        """
        <style>

        .stApp {

            background-color: #0e1117;

            color: white;
        }

        section[data-testid="stSidebar"] {

            background-color: #111827;
        }

        .dhanx-logo {

            font-size: 38px;

            font-weight: bold;

            text-align: center;

            margin-top: -20px;

            margin-bottom: 20px;
        }

        .dhan-blue {

            color: #3b82f6;
        }

        .dhan-red {

            color: #ef4444;

            font-style: italic;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

def render_sidebar():

    with st.sidebar:

        st.sidebar.markdown(
    """
    <div style='padding-top:10px;padding-bottom:20px'>
        <span style='font-size:38px;
                     font-weight:800;
                     color:#00B0FF;'>
            Dhan
        </span>
        <span style='font-size:38px;
                     font-weight:800;
                     color:red;
                     font-style:italic;'>
            X
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

        st.markdown("---")

        refresh = st.button(
            "🔄 Refresh Data"
        )

        return {

            "refresh": refresh
        }