# Email Forwarder

## Project Description
The Email Forwarder is a Python-based service designed to automate the process of fetching unseen emails from an IMAP server, cleaning their content by removing digital signatures (PGP, S/MIME), and forwarding the processed email data to a specified API endpoint. This service is built using FastAPI for its web interface, allowing for easy integration and triggering of the forwarding process.

## Features
- **IMAP Integration:** Connects securely to any IMAP server to retrieve emails.
- **Unseen Email Processing:** Focuses on processing only new, unseen emails to avoid duplicates.
- **Digital Signature Removal:** Automatically strips PGP and S/MIME signatures from email bodies for cleaner content.
- **Footer Removal:** Removes common email footers and signatures.
- **Configurable API Forwarding:** Sends processed email data as JSON to a user-defined API endpoint.
- **FastAPI Interface:** Provides a simple HTTP endpoint to trigger the email forwarding process.

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/your-username/email-forwarder.git
cd email-forwarder
\`\`\`

### 2. Set up your environment variables
Create a `.env` file in the root directory of the project based on the `.env.example` file:

\`\`\`
EMAIL_HOST=your_imap_host_address
EMAIL_USER=your_email_address
EMAIL_PASSWORD=your_email_app_password # Use an app password if your email provider supports it
NEXT_API_ROUTE=your_frontend_api_route # e.g., https://your-frontend.com/api/receive-email
\`\`\`

- \`EMAIL_HOST\`: The IMAP server address (e.g., \`imap.gmail.com\`).
- \`EMAIL_USER\`: The email address whose inbox you want to monitor.
- \`EMAIL_PASSWORD\`: The password for the email account. It's highly recommended to use an application-specific password if your email provider (like Gmail) offers them, for security reasons.
- \`NEXT_API_ROUTE\`: The URL of your API endpoint where the processed email content will be sent.

### 3. Install Dependencies
Using `uv` (recommended):
\`\`\`bash
uv sync
\`\`\`

Or using `pip`:
\`\`\`bash
python -m venv .venv
source .venv/bin/activate # On Windows use \`.venv\\Scripts\\activate\`
pip install -r requirements.txt # You might need to generate this first with `pip freeze > requirements.txt` or `uv pip freeze > requirements.txt`
\`\`\`

### 4. Run the Application

#### Development (using Uvicorn)
\`\`\`bash
uvicorn src.main:app --reload
\`\`\`
The API will be accessible at `http://127.0.0.1:8000`.

#### Triggering the Email Check
Once the FastAPI application is running, you can trigger the email forwarding process by sending a POST request to the `/run-email-check` endpoint.

Using `curl`:
\`\`\`bash
curl -X POST http://127.0.0.1:8000/run-email-check
\`\`\`

Using `requests` in Python:
\`\`\`python
import requests
response = requests.post("http://127.0.0.1:8000/run-email-check")
print(response.json())
\`\`\`

## Project Structure
\`\`\`
.
├── .env.example              # Example environment variables
├── pyproject.toml            # Project dependencies and metadata
├── README.md                 # This file
└── src/
    ├── main.py               # FastAPI application entry point
    ├── worker.py             # Core logic for fetching, processing, and forwarding emails
    └── helpers/
        └── remove_digital_signatures.py # Helper to clean email bodies
\`\`\`

## Contributing
Feel free to fork the repository, open issues, and submit pull requests.

## License
This project is open-sourced under the MIT License. See the `LICENSE` file (if present) for more details.
