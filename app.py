import streamlit as st
from modules.rag_engine import ask_trading_question
from modules.image_analyzer import (
    analyze_chart_image,
    answer_chart_question
)
# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="DhanX",
    page_icon="📈",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>

/* Sidebar width */
section[data-testid="stSidebar"] {
    width: 320px !important;
}

/* Sidebar radio buttons */
div[role="radiogroup"] label {
    font-size: 22px !important;
    font-weight: 600 !important;
    padding-top: 10px !important;
    padding-bottom: 10px !important;
}

/* Remove extra top spacing */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

page = st.sidebar.radio(
    "",
    [
        "Trading Chatbot",
        "Chart Analyzer",
        "Live Market Analyzer"
    ]
)

# -------------------------
# DHANX LOGO
# -------------------------

st.markdown(
    """
    <h1 style="
    text-align:left;
    font-size:64px;
    font-weight:900;
    margin-bottom:25px;
    ">
    <span style="color:#2196F3;">Dhan</span><span style="color:#F44336;">X</span>
    </h1>
    """,
    unsafe_allow_html=True
)

# -------------------------
# CHATBOT PAGE
# -------------------------
if page == "Trading Chatbot":

    st.title("📚 Trading Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input(
        "Ask any trading question..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                chat_history = ""

                for msg in st.session_state.messages[-6:]:

                    chat_history += (
                        f"{msg['role']}: "
                        f"{msg['content']}\n"
                    )

                answer = ask_trading_question(
                    question=prompt,
                    chat_history=chat_history
                )

                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )
# -------------------------
# CHART ANALYZER PAGE
# -------------------------

elif page == "Chart Analyzer":

    st.title("📊 Chart Analyzer")

    st.write(
        "Upload a trading chart for analysis."
    )

    uploaded_file = st.file_uploader(
        "Upload Chart",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file:
        import tempfile

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png"
        ) as tmp_file:

            tmp_file.write(
                uploaded_file.getvalue()
            )

            image_path = tmp_file.name

        st.session_state["chart_path"] = image_path
        st.image(
            uploaded_file,
            use_container_width=True
        )

        st.success(
            "Chart uploaded successfully."
        )
        if st.button("Analyze Chart"):

            with st.spinner(
                "Analyzing chart..."
            ):

                result = analyze_chart_image(
                    st.session_state["chart_path"]
                )

            st.session_state[
                "chart_analysis"
            ] = result

    if "chart_analysis" in st.session_state:

        st.subheader(
            "Analysis Result"
        )

        st.write(
            st.session_state[
                "chart_analysis"
            ]
        )

        st.divider()

        chart_question = st.text_input(
            "Ask about this chart"
        )

        if st.button("Ask Chart Question"):

            answer = answer_chart_question(
                st.session_state[
                    "chart_path"
                ],
                chart_question
            )

            st.write(answer)
# -------------------------
# LIVE MARKET ANALYZER
# -------------------------

elif page == "Live Market Analyzer":

    st.title("🌍 Live Market Analyzer")

    st.write(
        "Analyze live crypto, forex and stock markets."
    )

    symbol = st.text_input(
        "Enter Symbol",
        placeholder="BTC/USDT"
    )

    if st.button(
        "Analyze Market"
    ):

        if symbol:

            st.info(
                f"Live analysis for {symbol} will be connected next."
            )