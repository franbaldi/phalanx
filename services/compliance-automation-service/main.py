from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()

class Anomaly(BaseModel):
    query: str
    timestamp: str

@app.post("/report_anomaly")
async def report_anomaly(anomaly: Anomaly):
    """
    Receives an anomaly and generates a DORA incident report.
    """
    report = f"""
    DORA Incident Report
    --------------------

    Date of Incident: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Date of Detection: {anomaly.timestamp}

    Description of Incident:
    Anomalous database query detected.

    Anomalous Query:
    {anomaly.query}

    Initial Assessment:
    Potential unauthorized access or data exfiltration attempt.

    Next Steps:
    - Escalate to security team for investigation.
    - Preserve relevant logs and evidence.
    """

    with open(f"dora_report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "w") as f:
        f.write(report)

    return {"message": "DORA report generated successfully."}
