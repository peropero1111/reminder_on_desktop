Set FSO = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

AppDir = FSO.GetParentFolderName(WScript.ScriptFullName)
WshShell.CurrentDirectory = AppDir

PythonExe = "C:\Users\~ pythonw 가 위차한 장소~ pythonw.exe"
ScriptFile = "reminder.py"

WshShell.Run """" & PythonExe & """ """ & ScriptFile & """", 0, False
