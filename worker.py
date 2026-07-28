import pyodbc
import time 
import random

CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=SassaTrackerDB;"
    "Trusted_Connection=yes;"
)

def process_pending_applications():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    # Fetch all pending applications along with applicant email
    cursor.execute(
        """
        SELECT a.ApplicationID, apr.FullName, apr.EmailAddress, a.GrantType
        FROM Applications a
        JOIN Applicants apr ON a.IDNumber = apr.IDNumber
        WHERE a.CurrentStatus = 'Pending'
        """
    )

    pending_jobs = cursor.fetchall()

    if not pending_jobs:
        print("No pending applications found, Checking again later.")
        conn.close()
        return

    for job in pending_jobs:
        app_id, name, email, grant = job

        # Randomly choose to Approve or Reject to simulate an evaluation process
        new_status = random.choice(["Approved", "Rejected"])

        # 1. Update the application status
        cursor.execute(
            """
            UPDATE Applications
            SET CurrentStatus = ?, LastUpdated = GETDATE()
            WHERE ApplicationID = ?
            """,
            new_status,
            app_id,
        )

        # 2. Log the notification triggered for the applicant
        cursor.execute(
            """
            INSERT INTO NotificationsLogs (ApplicationID, NotificationType )
            VALUES (?, Email)
            """,
            app_id,
            
        )

        #3. Simulate Email output
        print(f"-->[EMAIL SENT] To: {email} | Dear {name}, your {grant} status is now: {new_status}.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Worker engine active. Scanning for database every 30 seconds...")
    while True:
        process_pending_applications()
        time.sleep(30)  # Wait for 30 seconds before checking again