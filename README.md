# Agency Sign-Up Verification Automation System

This project is a **Streamlit-based application** that automates the process of verifying agency sign-ups. It uses web scraping and the Gemini AI API to analyze agency websites and decide whether to approve or reject applications. The system also integrates email functionality to notify agencies of the decision and maintains a CSV log of results.

## Features

- **Automated Website Scraping**: Scrapes content from agency websites using BeautifulSoup.
- **AI-Powered Analysis**: Leverages Google Gemini API to evaluate website content against partnership criteria.
- **Email Notifications**: Sends approval or rejection emails automatically.
- **Data Logging**: Saves all processed results to a CSV file for record-keeping.
- **User-Friendly Interface**: Simple and intuitive Streamlit application for data input and processing.

---

## Installation

1. Clone this repository:
    ```bash
   git clone https://github.com/Syam1815/Agency-verification.git
   
    ```
2. Navigate to the project directory:
    ```bash
    cd Agency-verification
    ```
3. Create a virtual environment
    ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate 
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Create a `.env` file in the project directory and add the following:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key
    EMAIL_PASSWORD=your_email_password
    ```

---

## Usage

1. Run the application:
    ```bash
    streamlit run app.py
    ```
2. Open the application in your browser (usually at `http://localhost:8501`).
3. Enter the **Agency Name**, **Website Link**, and **Email Address** in the form.
4. Click **Submit** to process the data.
5. Check the status of approval or rejection on the application interface and in the agency's email.

---

## Technical Details

### Tools and Libraries

- **Python**: Primary programming language.
- **Streamlit**: For creating the user interface.
- **BeautifulSoup**: For web scraping.
- **Google Gemini API**: For AI-powered content analysis.
- **smtplib**: For sending emails.
- **csv**: For logging results in a CSV file.

### Workflow

1. The user inputs agency details into the form.
2. The application scrapes the provided website to extract content.
3. The extracted content is analyzed by the Gemini API to determine approval or rejection.
4. An email is sent to the agency with the decision and remarks.
5. The result is logged in a CSV file for future reference.

---
## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your proposed changes.


