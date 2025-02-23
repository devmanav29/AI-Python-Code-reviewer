import streamlit as st
import time
import google.generativeai as genai
import os

header = {
    "authorization": st.secrets["GOOGLE_API_KEY"]
    "content-type": "application/json"
}

# Ensure the API key is correctly loaded
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)
if GOOGLE_API_KEY is None:
    st.error("API key is missing. Please set GOOGLE_API_KEY in Streamlit secrets.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Initialize AI Model
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Error initializing AI model: {str(e)}")

# Streamlit app title
st.title("GenAI App - AI Code Reviewer")

# User input for Python code
st.write("Enter your Python code below:")
code = st.text_area("Code Input", height=300)

# Function to review code using Google AI API
def review_code(code):
    prompt = f"""
    Review the following Python code and identify potential bugs, errors, or areas of improvement.
    Provide a detailed explanation of the issues and suggest fixes. Also, provide the corrected code snippet.

    Code:
    {code}
    """

    for attempt in range(5):  # Retry up to 5 times
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if attempt < 4:  # If not the last attempt
                st.warning(f"Attempt {attempt + 1}: API error occurred. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"API request failed after multiple attempts. Error: {str(e)}"

# Button to trigger code review
if st.button("Review Code"):
    if code.strip() == "":
        st.warning("Please enter some Python code to review.")
    else:
        with st.spinner("Reviewing your code..."):
            review = review_code(code)
            if review:
                st.subheader("Code Review Feedback")
                st.markdown(review)  # Format text for better readability
                
                # Extract fixed code snippet (Assuming the model formats it properly)
                if "Fixed Code:" in review:
                    fixed_code = review.split("Fixed Code:")[-1]
                    st.subheader("Suggested Fix")
                    st.code(fixed_code.strip(), language="python")
            else:
                st.error("Could not process the code review. Please try again later.")

# Instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Paste your Python code in the text area.
2. Click 'Review Code'.
3. View the code review feedback, including errors and suggested fixes.
""")
