import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
import csv

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
]

# File for results
csv_file = "agency_verification_results.csv"

# Create CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Agency Name", "URL", "Decision", "Email", "Remarks"])

# Email function
def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    from_email = "syamks6521@gmail.com"
    from_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        return "Success"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        server.quit()

# Analyze with Gemini API
def analyze_with_gemini(content):
    if not content:
        return "reject"

    prompt = f"""
    Does this agency align with partnership requirements? 

    Evaluate this decision based on the content scraped from the website. 

    Relevant requirements: 

    - Web design services
    - Web development
    - SEO agency
    - Ads agency
    - Digital marketing agency
    - Agency, Website creation

    Analyze the content and determine if the website mentions these aspects. 
    Reply with "approve" if the agency meets the requirements, otherwise "reject".

    Website content:: {content}
    """

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        result = response.text.strip().lower()
        return "approve" if "approve" in result else "reject"
    except Exception as e:
        return f"Error: {str(e)}"

# Scraping function
def scrape_website(url):
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator=" ").lower()
        return text
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state
if "agency_name" not in st.session_state:
    st.session_state.agency_name = ""
if "website" not in st.session_state:
    st.session_state.website = ""
if "email" not in st.session_state:
    st.session_state.email = ""

# # Function to clear form fields
# def clear_form():
#     st.session_state.agency_name = ""
#     st.session_state.website = ""
#     st.session_state.email = ""

# Streamlit Interface
st.title("Agency Sign-Up Verification")

st.write("Enter the agency details below:")
# Input form
with st.form("agency_form"):
    agency_name = st.text_input("Agency Name", st.session_state.agency_name, key="agency_name")
    website = st.text_input("Website Link", st.session_state.website, key="website")
    email = st.text_input("Email Address", st.session_state.email, key="email")
    submit_button = st.form_submit_button("Submit")
    # clear_button = st.form_submit_button("Clear", on_click=clear_form)

# Handle Submit Button
if submit_button:
    if not agency_name or not website or not email:
        st.error("Please fill out all fields.")
    else:
        with st.spinner("Processing..."):
            content = scrape_website(website)
            if "Error" in content:
                st.error(f"Failed to scrape {website}. Error: {content}")
            else:
                decision = analyze_with_gemini(content)
                email_status = "Not Sent"

                # Send email based on the decision
                if decision == "approve":
                    subject = "Welcome to CookieYes!"
                    body = f"Congratulations {agency_name}! Your agency has been approved."
                    email_status = send_email(email, subject, body)
                elif decision == "reject":
                    subject = "CookieYes Agency Sign-Up"
                    body = (
                        f"Thank you {agency_name} for applying. "
                        "Unfortunately, your agency does not meet our requirements."
                        "At this time, we are unable to move forward with your application."
                    )
                    email_status = send_email(email, subject, body)

                # Save results to CSV
                with open(csv_file, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([agency_name, website, decision, email, email_status])

                # Display results
                if decision == "approve":
                    st.success("Status: Approved")
                else:
                    st.error("Status: Rejected")
                
                # if email_status=="Success":
                #     st.write("Please check your mail")
