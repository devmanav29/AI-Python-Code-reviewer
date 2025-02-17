# GenAI Code Reviewer

An AI-powered Python code review application built with Streamlit and OpenAI API.

## Features
- Submit Python code for review
- Receive detailed bug reports
- Get suggested fixes and improvements
- Clean and intuitive interface

## Installation
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage
1. Run the application:
   ```bash
   streamlit run app.py
   ```
2. Paste your Python code in the text area
3. Click 'Review Code'
4. View the analysis and suggested fixes

## Requirements
- Python 3.7+
- OpenAI API key
