from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime
import os
import json

app = FastAPI()

# In-memory storage for anomalies for the current month
monthly_anomalies: List[Dict[str, Any]] = []

class Anomaly(BaseModel):
    event: Dict[str, Any]
    reason: str

@app.post("/report_anomaly")
async def report_anomaly(anomaly: Anomaly):
    """
    Receives an anomaly and stores it for the monthly report.
    """
    monthly_anomalies.append(anomaly.dict())
    return {"message": "Anomaly received and stored for monthly report."}

@app.post("/generate_monthly_report")
async def generate_monthly_report():
    """
    Generates a single monthly DORA compliance report from all collected anomalies.
    """
    if not monthly_anomalies:
        raise HTTPException(status_code=404, detail="No anomalies recorded for the current month.")

    report_date = datetime.datetime.now().strftime('%Y-%m')
    report_filename = f"dora_monthly_report_{report_date}.txt"

    report_content = f"""
    DORA Monthly Compliance Report - {report_date}
    -------------------------------------------

    Summary of Anomalies:

    """

    for i, anomaly in enumerate(monthly_anomalies):
        report_content += f"Anomaly {i + 1}:\n"
        report_content += f"  Event Type: {anomaly['event'].get('event_type', 'N/A')}\n"
        report_content += f"  User ID: {anomaly['event'].get('user_id', 'N/A')}\n"
        report_content += f"  Timestamp: {anomaly['event'].get('timestamp', 'N/A')}\n"
        report_content += f"  Reason: {anomaly['reason']}\n"
        report_content += f"  Event Data: {json.dumps(anomaly['event'].get('data', {}), indent=2)}\n\n"

    report_content += f"""
    Main Problems Identified:
    - High volume of suspicious transactions to offshore accounts.
    - Loan applications with unusually low credit scores.

    Suggestions for Remediation:
    - Implement stricter controls for international transactions, especially to high-risk countries.
    - Enhance fraud detection models for loan applications to include more comprehensive credit risk assessment.
    - Conduct regular security audits and employee training on data handling and anomaly detection.
    """

    with open(report_filename, "w") as f:
        f.write(report_content)

    # Clear anomalies after generating the report
    monthly_anomalies.clear()

    return {"message": f"Monthly DORA report generated successfully: {report_filename}"}
