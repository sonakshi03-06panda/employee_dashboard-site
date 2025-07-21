import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import io
from PIL import Image

st.set_page_config(layout="wide")
# Tech-themed background + transparent header and UI styling
st.markdown("""
    <style>
    /* ✅ Background image on the full app */
    .stApp {
        background: url("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* ✅ Transparent widgets and containers */
    [data-testid="stSidebar"], .css-1d391kg, .css-18ni7ap, .block-container {
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(2px);
        border-radius: 10px;
        padding: 1rem;
    }

    /* ✅ Header with transparency */
    .custom-header {
        background-color: rgba(255, 255, 255, 0.7);
        padding: 1.2rem 2rem;
        margin-bottom: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    h1, h2, h3, h4, h5, h6, p, label {
        color: #000 !important;
        text-shadow: none;
    }
    h1 {font-size: 2rem !important;}
    h2 {font-size: 1.5rem !important;}
    h3 {font-size: 1.2rem !important;} p, label {font-size: 0.95rem !important;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-header">', unsafe_allow_html=True)
st.markdown("<h1>📊 Salary Explorer Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p>Explore trends in salaries based on age, education, gender, and more using the Adult Income Dataset.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("adult.csv")
    df.replace("?", np.nan, inplace=True)
    df.dropna(inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filter the Data")
education_filter = st.sidebar.multiselect("Education", sorted(df["education"].unique()), default=sorted(df["education"].unique()))
gender_filter = st.sidebar.multiselect("Gender", sorted(df["gender"].unique()), default=sorted(df["gender"].unique()))
country_filter = st.sidebar.multiselect("Native Country", sorted(df["native-country"].unique()), default=sorted(df["native-country"].unique()))
age_range = st.sidebar.slider("Age Range", int(df["age"].min()), int(df["age"].max()), (25, 50))

# Apply filters
filtered_df = df[
    (df["education"].isin(education_filter)) &
    (df["gender"].isin(gender_filter)) &
    (df["native-country"].isin(country_filter)) &
    (df["age"].between(age_range[0], age_range[1]))
]

st.markdown(f"### 🔍 Showing {len(filtered_df)} records")

# Layout
col1, col2 = st.columns(2)

# 📊 Salary Distribution
with col1:
    st.subheader("Salary Distribution")
    fig1 = px.histogram(filtered_df, x="income", color="gender", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

# 🍕 Occupation Pie
with col2:
    st.subheader("Salary Share by Occupation")
    pie_data = filtered_df.groupby("occupation")["income"].value_counts().unstack().fillna(0)
    if ">50K" in pie_data.columns:
        fig2 = px.pie(pie_data, names=pie_data.index, values=">50K", title="High Earners by Occupation")
        st.plotly_chart(fig2, use_container_width=True)

# 📦 Box Plot: Hours Worked
st.subheader("⏱️ Weekly Hours Worked vs Income")
fig3 = px.box(filtered_df, x="income", y="hours-per-week", color="income", points="all")
st.plotly_chart(fig3, use_container_width=True)


# 🔥 Correlation Heatmap
st.subheader("📊 Correlation Heatmap")

numerics = filtered_df.select_dtypes(include=["int64", "float64"])
corr = numerics.corr()

# Create a figure
fig4, ax4 = plt.subplots(figsize=(6, 3.5), dpi=100)
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax4)

# Save figure to a bytes buffer
buf = io.BytesIO()
fig4.savefig(buf, format="png", bbox_inches="tight", transparent=True)
buf.seek(0)

# Display as an image with custom width
st.image(Image.open(buf), caption="Correlation Heatmap", width=600)
st.plotly_chart(fig4, use_container_width=True)