Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\VisFSP\autorunfsp.bat" & Chr(34), 0
Set WshShell = Nothing