@echo off
setlocal enabledelayedexpansion

REM Read the .env file line by line
for /f "usebackq tokens=1,2 delims==" %%a in ("C:\Users\ssen\Documents\syenah\nlp-microservice-trojkn\.env") do (
    set "key=%%a"
    set "value=%%b"
    
    REM Remove surrounding quotes if present
    set "value=!value:"=!"

    REM Display the environment variable being set
    echo Setting !key! to !value!

    REM Set the environment variable for the current session
    set !key!=!value!
)

echo Environment variables have been set for the current session.
endlocal
