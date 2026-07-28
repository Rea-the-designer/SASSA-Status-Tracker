from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pyodbc
import sys

app = FastAPI()

# Database Connection String (Update Server and Database names if needed)
CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=SassaTrackerDB;"
    "Trusted_Connection=yes;"
)

# Input validation model
class ApplicantRequest(BaseModel):
    id_number: str = Field(..., min_length=13, max_length=13, description="Applicant's 13-digit ID number")
    full_name: str = Field(..., description="Applicant's full name")
    phone_number: str = Field(..., description="Applicant's phone number")
    email_address: str = Field(..., description="Applicant's email address")
    grant_type: str = Field(..., description="Type of grant applied for") # e.g., "SRD R370".

# Output model for package versions


@app.post("/register_applicant")
def register_applicant(data: ApplicantRequest):
    #Length validation for ID number
    if not data.id_number.isdigit():
        raise HTTPException(status_code=400, detail="ID number must be numeric.")
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    try:
       # 1. Insert into Applicants if they don't already exist
        cursor.execute(
            """
            IF NOT EXISTS (SELECT 1 FROM Applicants WHERE id_number = ?)
            INSERT INTO Applicants (IDNumber, FullName, PhoneNumber, EmailAddress)
            VALUES (?, ?, ?, ?)

            """,
            data.id_number,
            data.full_name,
            data.phone_number,
            data.email_address,
            data.grant_type,
        )

        # 2. Create a Application record for the applicant
        cursor.execute(
            """
            INSERT INTO Applications (IDNumber, GrantType)
            VALUES (?, ?)
            """,
            data.id_number,
            data.grant_type,
        )
        conn.commit()
        return {"status": "Success", "message": "Application logged as pending."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Run with: uvicorn app:app --reload
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="info")
