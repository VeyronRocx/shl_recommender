import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from recommender import AssessmentRecommender

# Set page configuration
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="📊",
    layout="wide"
)


# Initialize the recommender
@st.cache_resource
def load_recommender():
    return AssessmentRecommender()


recommender = load_recommender()

# Title and description
st.title("SHL Assessment Recommendation System")
st.write("""
This application helps hiring managers find the right SHL assessments for their needs.
Enter a query, paste a job description, or provide a URL to get personalized recommendations.
""")

# Create tabs for different input methods
tab1, tab2, tab3 = st.tabs(["Query", "Job Description", "URL"])

# Tab 1: Natural language query
with tab1:
    query = st.text_area(
        "Enter your query:",
        placeholder="Example: I am hiring for Java developers who can collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        height=100
    )

    col1, col2 = st.columns(2)
    with col1:
        max_recommendations = st.slider("Max recommendations", min_value=1, max_value=10, value=5)

    submit_button = st.button("Get Recommendations", key="query_submit")

    if submit_button and query:
        process_query = True
    else:
        process_query = False

# Tab 2: Job description text
with tab2:
    job_description = st.text_area(
        "Paste job description:",
        height=300
    )

    col1, col2 = st.columns(2)
    with col1:
        max_recommendations_jd = st.slider("Max recommendations", min_value=1, max_value=10, value=5, key="jd_slider")

    submit_button_jd = st.button("Get Recommendations", key="jd_submit")

    if submit_button_jd and job_description:
        query = job_description
        max_recommendations = max_recommendations_jd
        process_query = True
    elif not submit_button and not process_query:
        process_query = False

# Tab 3: URL input
with tab3:
    url = st.text_input("Enter job posting URL:")

    col1, col2 = st.columns(2)
    with col1:
        max_recommendations_url = st.slider("Max recommendations", min_value=1, max_value=10, value=5, key="url_slider")

    submit_button_url = st.button("Get Recommendations", key="url_submit")

    if submit_button_url and url:
        try:
            with st.spinner("Fetching content from URL..."):
                # Request the webpage
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                # Parse with BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')

                # Extract job description - focus on common containers
                job_desc_container = soup.find('div', class_=re.compile(r'job-?description|posting|details', re.I))

                if job_desc_container:
                    query = job_desc_container.get_text()
                else:
                    # Fallback to body text if no specific container found
                    query = soup.get_text()

                max_recommendations = max_recommendations_url
                process_query = True

                # Show a preview of the extracted text
                st.success("Content extracted from URL!")
                st.write("Preview of extracted content:")
                st.write(query[:500] + "...")

        except Exception as e:
            st.error(f"Error fetching URL content: {str(e)}")
            process_query = False
    elif not submit_button and not process_query:
        process_query = False

# Process the query and display recommendations
if process_query:
    with st.spinner("Analyzing and finding the best assessments..."):
        recommendations = recommender.recommend(query, max_recommendations)

    if not recommendations.empty:
        st.subheader("Recommended SHL Assessments")

        # Create a styled dataframe
        styled_recs = recommendations.copy()

        # Format the assessment names as clickable links
        styled_recs['Assessment'] = styled_recs.apply(
            lambda x: f"<a href='{x['url']}' target='_blank'>{x['name']}</a>",
            axis=1
        )

        # Reorder and rename columns for display
        display_df = styled_recs[[
            'Assessment', 'test_type', 'duration', 'remote_testing', 'adaptive_support'
        ]].rename(columns={
            'test_type': 'Test Type',
            'duration': 'Duration (min)',
            'remote_testing': 'Remote Testing',
            'adaptive_support': 'Adaptive'
        })

        # Display as HTML to enable clickable links
        st.markdown(
            display_df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )

        # Display extraction insights
        st.subheader("Query Analysis")

        # Extract information for display
        duration_limit = recommender._extract_duration_limit(query)
        skills = recommender._extract_skills(query)
        test_types = recommender._extract_test_types(query)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Duration Limit", f"{duration_limit} min" if duration_limit else "Not specified")

        with col2:
            st.write("**Detected Skills:**")
            st.write(", ".join(skills) if skills else "None detected")

        with col3:
            st.write("**Test Types:**")
            st.write(", ".join(test_types) if test_types else "Not specified")

    else:
        st.warning("No matching assessments found. Try adjusting your query or filters.")

# Add footer
st.markdown("---")
st.markdown("SHL Assessment Recommendation System | Built with Streamlit and Python")