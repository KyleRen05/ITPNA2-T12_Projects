# Aero Airlines - Question 3 Alert System

## Testing the Email Alerts

To test the automated SMTP email alerts for Question 3 without needing a live internet connection, please use the included batch script.

**Steps to test:**
1. Double-click `start_mail_server.bat` to open the local inbox terminal.
2. Run `server.py` to start the monitoring system.
3. Run `sensor.py` to start generating flight data.

When a safety threshold is violated, the generated email will automatically print directly into the Mail Server terminal.
