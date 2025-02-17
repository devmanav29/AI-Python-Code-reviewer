import streamlit as st
import time
from openai import OpenAI # OpenAI API client

# Securely load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit app title
st.title("GenAI App - AI Code Reviewer")

# User input for Python code
st.write("Enter your Python code below:")
code = st.text_area("Code Input", height=300)

# Function to review code using OpenAI API
def review_code(code):
    prompt = f"""
    Review the following Python code and identify potential bugs, errors, or areas of improvement.
    Provide a detailed explanation of the issues and suggest fixes. Also, provide the corrected code snippet.

    Code:
    {code}
    """

    for attempt in range(5):  # Retry up to 5 times in case of failure
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": "You are an AI code reviewer."},
                          {"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt < 4:  # If not the last attempt, retry with exponential backoff
                st.warning(f"API error occurred. Retrying... Error: {str(e)}")
                time.sleep(2 ** attempt)
            else:
                st.error(f"API request failed. Please try again later. Error: {str(e)}")
                return None

# Button to trigger code review
if st.button("Review Code"):
    if code.strip() == "":
        st.warning("Please enter some Python code to review.")
    else:
        with st.spinner("Reviewing your code..."):
            review = review_code(code)
            if review:
                st.subheader("Code Review Feedback")
                st.write(review)

# Instructions
st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Paste your Python code in the text area  
2. Click 'Review Code'  
3. View the code review feedback  
""")
