@echo off
title Aero Airlines - Email Server

echo ==================================================
echo      AERO AIRLINES LOCAL SMTP MAIL SERVER
echo ==================================================
echo.

echo [SYSTEM] Checking dependencies...
py -m pip install aiosmtpd -q

echo [SYSTEM] Starting local mail server on port 1025...
echo [SYSTEM] Inbox is open. Waiting for alerts...
echo.
echo -------------------- INBOX -----------------------

:: This starts the modern Python local mail server
py -m aiosmtpd -n -l localhost:1025

pause