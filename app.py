import streamlit as st
from ai_engine import analyze_text_waste
# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="WASTE.AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL STYLE
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f4f7f5;
    }

    /* Main content width */
    .block-container {
        max-width: 1150px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Text styling */
    h1 {
        color: #17382b !important;
    }

    h2 {
        color: #17382b !important;
    }

    h3 {
        color: #254b3a !important;
    }

    p {
        color: #68776f;
    }

    /* Buttons */
    .stButton > button {
        background-color: #20563f;
        color: white;
        border: none;
        border-radius: 8px;
        height: 48px;
        font-weight: 600;
        font-size: 15px;
        width: 230px;
    }

    .stButton > button:hover {
        background-color: #163e2d;
        color: white;
    }

   .stTextInput input {
    background-color: #f8faf9 !important;
    color: #1f3329 !important;
    border: 1px solid #cbd8d1 !important;
    border-radius: 8px !important;
    height: 48px !important;
    font-size: 14px !important;
    padding-left: 14px !important;
    caret-color: #20563f !important;
}

/* Placeholder text */
    .stTextInput input::placeholder {
    color: #7a8780 !important;
    opacity: 1 !important;
}

/* Text when user types */
    .stTextInput input:focus {
    background-color: #ffffff !important;
    color: #1f3329 !important;
    border: 1px solid #4d8c6c !important;
    box-shadow: 0 0 0 2px rgba(77, 140, 108, 0.12) !important;
}

/* Streamlit input wrapper */
    .stTextInput > div > div > input {
    color: #1f3329 !important;
    background-color: #f8faf9 !important;
}

    .stTextInput input:focus {
        border-color: #4d8c6c;
        box-shadow: 0 0 0 2px rgba(77,140,108,0.10);
    }

    /* File uploader */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        border: 1px dashed #b7cbbf !important;
        border-radius: 10px !important;
    }

    /* Alerts */
    .stAlert {
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# TOP NAVIGATION
# =========================================================

nav_left, nav_right = st.columns([3, 1])

with nav_left:

    st.markdown(
        "<h3 style='margin-bottom:0;'>WASTE<span style='color:#4d8c6c;'>.AI</span></h3>",
        unsafe_allow_html=True
    )

with nav_right:

    st.markdown(
        "<p style='text-align:right; margin-top:12px; "
        "font-size:12px; font-weight:600; letter-spacing:1px;'>"
        "INTELLIGENT WASTE ANALYSIS"
        "</p>",
        unsafe_allow_html=True
    )


st.divider()


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    "<p style='color:#4d8c6c; font-size:12px; font-weight:700; "
    "letter-spacing:2px; margin-top:35px;'>"
    "AI-POWERED ENVIRONMENTAL INTELLIGENCE"
    "</p>",
    unsafe_allow_html=True
)

st.title("Intelligent Waste Segregation")

st.markdown(
    """
    <p style="
        max-width:700px;
        font-size:17px;
        line-height:1.7;
        color:#68776f;
    ">
    Identify waste materials, understand their environmental impact,
    and discover appropriate methods for segregation, recycling,
    reuse and responsible disposal.
    </p>
    """,
    unsafe_allow_html=True
)


st.write("")


# =========================================================
# ANALYSIS SECTION
# =========================================================

# =========================================================
# TWO INPUT COLUMNS
# =========================================================

text_column, image_column = st.columns(2, gap="large")


# =========================================================
# TEXT ANALYSIS
# =========================================================

with text_column:

    st.markdown(
        """
        **INPUT METHOD 1**

        ### Text Analysis

        Enter the name or description of the waste item.

        Examples: plastic bottle, food waste, broken glass,
        electronic device.
        """
    )

    waste_text = st.text_input(
        "Waste description",
        placeholder="Enter waste description...",
        label_visibility="collapsed"
    )


# =========================================================
# IMAGE ANALYSIS
# =========================================================

with image_column:

    st.markdown(
        """
        **INPUT METHOD 2**

        ### Image Analysis

        Upload a clear image of the waste item.
        The AI system will identify the visible material
        and classify it accordingly.
        """
    )

    uploaded_image = st.file_uploader(
        "Upload waste image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )


# =========================================================
# IMAGE PREVIEW
# =========================================================

if uploaded_image is not None:

    st.write("")

    st.markdown("**IMAGE PREVIEW**")

    st.image(
        uploaded_image,
        width=420
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.write("")

button_left, button_center, button_right = st.columns(
    [1, 1, 1]
)

with button_center:

    analyze_button = st.button(
        "Analyze Waste",
        use_container_width=True
    )


# =========================================================
# TEMPORARY TEST RESPONSE
# =========================================================

# =========================================================
# TEXT AI ANALYSIS
# =========================================================

if analyze_button:

    if not waste_text and uploaded_image is None:

        st.warning(
            "Please enter a waste description or upload an image."
        )

    elif waste_text:

        with st.spinner("Analyzing waste..."):

            result = analyze_text_waste(waste_text)

        if "error" in result:

            st.error(
                "Unable to analyze the waste. "
                "Please check your API configuration and try again."
            )

            st.caption(result["error"])

        else:

            st.session_state["waste_result"] = result


























# =========================================================
# SMART RESULT
# =========================================================

if "waste_result" in st.session_state:

    result = st.session_state["waste_result"]

    st.write("")
    st.write("")
    st.divider()
    st.write("")

    st.markdown(
        "<p style='color:#4d8c6c; font-size:12px; "
        "font-weight:700; letter-spacing:2px;'>"
        "AI ANALYSIS RESULT"
        "</p>",
        unsafe_allow_html=True
    )

    st.subheader("Waste Classification")

    # Analysis source
    st.caption(
        f"Analysis source: {result.get('source', 'AI System')}"
    )

    st.write(
        "The following information has been generated "
        "from the provided waste description."
    )

    st.write("")

    # ---------------------------------------------
    # BASIC INFORMATION
    # ---------------------------------------------

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:

        st.markdown("**Waste Name**")

        st.info(
            result.get("waste_name", "Not available")
        )

    with result_col2:

        st.markdown("**Category**")

        st.info(
            result.get("category", "Not available")
        )

    with result_col3:

        st.markdown("**Recyclable**")

        st.info(
            result.get("recyclable", "Not available")
        )

    st.write("")

    # ---------------------------------------------
    # BIODEGRADABILITY
    # ---------------------------------------------

    st.markdown("### Biodegradability")

    st.write(
        result.get(
            "biodegradable",
            "Information not available."
        )
    )

    st.write("")

    # ---------------------------------------------
    # DISPOSAL
    # ---------------------------------------------

    st.markdown("### Recommended Disposal Method")

    st.write(
        result.get(
            "disposal_method",
            "Information not available."
        )
    )

    st.write("")

    # ---------------------------------------------
    # ENVIRONMENTAL IMPACT
    # ---------------------------------------------

    st.markdown("### Environmental Impact")

    st.write(
        result.get(
            "environmental_impact",
            "Information not available."
        )
    )

    st.write("")

    # ---------------------------------------------
    # REUSE / RECYCLING
    # ---------------------------------------------

    st.markdown("### Reuse and Recycling")

    st.write(
        result.get(
            "reuse_or_recycling",
            "Information not available."
        )
    )

    st.write("")

    # ---------------------------------------------
    # AWARENESS
    # ---------------------------------------------

    st.markdown("### Awareness Recommendation")

    st.success(
        result.get(
            "awareness_tip",
            "Dispose of waste responsibly."
        )
    )


# =========================================================
# CAPABILITIES
# =========================================================

st.write("")
st.write("")
st.divider()
st.write("")

st.markdown(
    "<p style='color:#4d8c6c; font-size:12px; font-weight:700; "
    "letter-spacing:2px;'>SYSTEM CAPABILITIES</p>",
    unsafe_allow_html=True
)

st.subheader(
    "Designed for Responsible Waste Management"
)

st.write(
    "The system combines artificial intelligence with practical "
    "waste management information to help users understand "
    "appropriate segregation and disposal methods."
)







    









































feature1, feature2, feature3 = st.columns(3, gap="medium")


# =========================================================
# FEATURE 1
# =========================================================

with feature1:

    with st.container(border=True):

        st.markdown("### Intelligent Classification")

        st.write(
            "Identify the type and category of waste using "
            "AI-based text and image analysis."
        )


# =========================================================
# FEATURE 2
# =========================================================

with feature2:

    with st.container(border=True):

        st.markdown("### Responsible Disposal")

        st.write(
            "Receive practical guidance about segregation, "
            "recycling and appropriate disposal methods."
        )


# =========================================================
# FEATURE 3
# =========================================================

with feature3:

    with st.container(border=True):

        st.markdown("### Environmental Awareness")

        st.write(
            "Understand potential environmental impacts "
            "and learn simple ways to reduce waste."
        )


# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("")
st.divider()

st.markdown(
    "<p style='text-align:center; color:#8a968f; font-size:12px;'>"
    "WASTE.AI &nbsp; | &nbsp; "
    "AI Waste Segregation and Awareness System"
    "<br><br>"
    "Academic Project"
    "</p>",
    unsafe_allow_html=True
)