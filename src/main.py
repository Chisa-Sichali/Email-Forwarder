from fastapi import FastAPI
from worker import fetch_and_forward_emails

app = FastAPI()

@app.post("/run-email-check")
async def run_email_check():
    try:
        fetch_and_forward_emails()  # synchronous here; could make async if needed
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
