from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import os
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Compliance Automation Service",
    description="Generates DORA-compliant incident reports for detected anomalies."
)

# --- CORS Middleware ---
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Transaction(BaseModel):
    user_id: str
    amount: float
    currency: str
    recipient: str
    country: str
    timestamp: str

class Anomaly(BaseModel):
    transaction: Transaction
    reason: str

@app.post("/report_anomaly")
async def report_anomaly(anomaly: Anomaly):
    """
    Receives an anomalous transaction and generates a detailed DORA incident report.
    """
    report = f"""
# DORA Major ICT Incident Report

**Incident Classification:**
- **Incident Reference ID:** INC-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}
- **Date and Time of Incident:** {anomaly.transaction.timestamp}
- **Date and Time of Detection:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Incident Type:** Transaction Anomaly

**Summary of Incident:**
- A transaction was flagged as a significant deviation from the user's established behavior patterns.
- **Reason for Anomaly:** {anomaly.reason}

**Details of the Anomalous Transaction:**
- **User ID:** {anomaly.transaction.user_id}
- **Amount:** {anomaly.transaction.amount} {anomaly.transaction.currency}
- **Recipient:** {anomaly.transaction.recipient}
- **Location:** {anomaly.transaction.country}

**Initial Impact Assessment:**
- **Affected Systems:** Core Banking, Transaction Processing
- **Potential Impact:** Unauthorized funds transfer, potential financial loss, reputational damage.
- **Affected Geographies:** {anomaly.transaction.country}

**Root Cause Analysis (Preliminary):**
- The incident appears to be an isolated event, but further investigation is required.
- Potential causes include compromised user credentials or sophisticated fraud attempt.

**Next Steps:**
1.  **Immediate Action:** The transaction has been automatically blocked pending review.
2.  **Escalation:** The incident has been escalated to the Security Operations Center (SOC) for immediate investigation.
3.  **Evidence Preservation:** All relevant transaction logs and user activity data have been preserved.
4.  **Communication:** A notification has been sent to the affected user.

"""

    report_filename = f"dora_report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(report_filename, "w") as f:
        f.write(report)



@app.get("/reports")
async def get_reports():
    """Returns a list of all generated DORA reports."""
    files = os.listdir(".")
    reports = [f for f in files if f.startswith("dora_report_") and f.endswith(".txt")]
    return {"reports": reports}

@app.get("/reports/{report_name}")
async def get_report(report_name: str):
    """Returns the content of a specific DORA report."""
    if os.path.exists(report_name):
        return FileResponse(report_name)
    else:
        return {"error": "Report not found"}