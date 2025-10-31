import streamlit as st
import pandas as pd
import logging
from datetime import datetime

# ---------------------------------
# Logging setup
# ---------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('allocation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("FacultyAllocator")

# ---------------------------------
# Helper functions
# ---------------------------------
def identify_faculty_columns(table, ref_col='CGPA'):
    """Detect all faculty columns following the CGPA column."""
    try:
        index_pos = table.columns.get_loc(ref_col)
        faculties = table.columns[index_pos + 1:].tolist()
        logger.info(f"Faculty columns detected: {faculties}")
        return faculties
    except Exception as exc:
        logger.error(f"Error identifying faculty columns: {exc}")
        raise

def distribute_students(table, cgpa_field='CGPA'):
    """Distribute students to faculties sequentially based on sorted CGPA."""
    try:
        sorted_df = table.sort_values(by=cgpa_field, ascending=False).reset_index(drop=True)
        faculties = identify_faculty_columns(sorted_df, cgpa_field)
        allocations = []
        for idx, row in sorted_df.iterrows():
            faculty = faculties[idx % len(faculties)]
            allocations.append({
                'Roll Number': row['Roll'],
                'Full Name': row['Name'],
                'Email': row['Email'],
                'CGPA': row[cgpa_field],
                'Assigned Faculty': faculty
            })
        result = pd.DataFrame(allocations)
        logger.info("Student distribution completed successfully.")
        return result
    except Exception as exc:
        logger.error(f"Distribution failed: {exc}")
        raise

def summarize_faculty_preferences(table, cgpa_field='CGPA'):
    """Generate a summary count of student preferences for each faculty."""
    try:
        faculties = identify_faculty_columns(table, cgpa_field)
        summary = {fac: {i: 0 for i in range(1, len(faculties) + 1)} for fac in faculties}

        for _, row in table.iterrows():
            for fac in faculties:
                try:
                    rank = int(row[fac])
                    if rank in summary[fac]:
                        summary[fac][rank] += 1
                except Exception:
                    logger.warning(f"Invalid rank detected for {fac}: {row[fac]}")

        summary_df = pd.DataFrame(summary).T
        summary_df.columns = [f'Pref {i}' for i in range(1, len(faculties) + 1)]
        summary_df.index.name = 'Faculty'
        summary_df.reset_index(inplace=True)
        logger.info("Faculty preference summary prepared.")
        return summary_df
    except Exception as exc:
        logger.error(f"Error summarizing preferences: {exc}")
        raise

# ---------------------------------
# Streamlit UI Customization
# ---------------------------------
st.set_page_config(page_title="Faculty Allocation Dashboard", layout="wide")

# Custom CSS for style and color
st.markdown("""
    <style>
        .main {
            background-color: #f9fbff;
        }
        h1 {
            color: #1a5276;
            font-family: 'Helvetica Neue', sans-serif;
        }
        h2, h3, h4 {
            color: #154360;
        }
        div.stButton > button:first-child {
            background-color: #2E86C1;
            color: white;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
        }
        div.stButton > button:hover {
            background-color: #21618C;
        }
        .stDataFrame {
            border-radius: 10px;
        }
        .stMetric {
            background: #E8F8F5;
            padding: 10px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------
# Page Layout
# ---------------------------------
st.title("📘 Faculty Allocation Dashboard")
st.caption("Project Assignment Automation — built with Streamlit")

st.divider()

uploaded = st.file_uploader(
    "📂 Upload Student Preference CSV",
    type=["csv"],
    help="Expected columns: Roll, Name, Email, CGPA, followed by faculty preference columns."
)

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        logger.info(f"File uploaded: {uploaded.name} ({len(df)} rows)")
        st.success(f"✅ Successfully uploaded **{uploaded.name}** with {len(df)} records.")

        with st.expander("👁️ View Uploaded Data Sample"):
            st.dataframe(df.head(10), use_container_width=True)

        st.divider()

        if st.button("🚀 Start Allocation"):
            with st.spinner("Running allocation algorithm..."):
                allocation_df = distribute_students(df)
                summary_df = summarize_faculty_preferences(df)

            st.success("✅ Allocation Complete!")

            tab1, tab2 = st.tabs(["📋 Allocation Results", "📊 Preference Summary"])

            with tab1:
                st.dataframe(allocation_df, use_container_width=True)
                st.download_button(
                    "⬇️ Download Allocation CSV",
                    allocation_df.to_csv(index=False).encode('utf-8'),
                    "student_allocation.csv",
                    "text/csv"
                )

            with tab2:
                st.dataframe(summary_df, use_container_width=True)
                st.download_button(
                    "⬇️ Download Preference Stats CSV",
                    summary_df.to_csv(index=False).encode('utf-8'),
                    "faculty_preferences.csv",
                    "text/csv"
                )

            st.divider()
            st.subheader("📈 Summary Metrics")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Students", len(allocation_df))
            c2.metric("Total Faculties", len(identify_faculty_columns(df)))
            c3.metric("Average CGPA", f"{allocation_df['CGPA'].mean():.2f}")

            st.subheader("🎯 Faculty Assignment Count")
            fac_count = allocation_df['Assigned Faculty'].value_counts().reset_index()
            fac_count.columns = ["Faculty", "Assigned Students"]
            st.bar_chart(fac_count.set_index("Faculty"))

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        logger.error(f"Processing error: {e}", exc_info=True)
else:
    st.info("📤 Please upload a valid CSV file to continue.")
    st.markdown("""
    ### CSV Format Example:
    - Columns: `Roll`, `Name`, `Email`, `CGPA`, `Faculty_A`, `Faculty_B`, ...
    - Each faculty column contains ranking values (1 = highest preference).
    
    ### How the System Works:
    1. Sorts students in descending order of CGPA.  
    2. Allocates each student sequentially to faculties (round-robin style).  
    3. Generates statistical summaries of preferences.  
    """)

st.divider()
st.markdown("<p style='text-align:center;color:gray;'>© 2025 Allocation System | Logs saved to <code>allocation.log</code></p>", unsafe_allow_html=True)
