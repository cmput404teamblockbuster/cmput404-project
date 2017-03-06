Dim WinScriptHost
Set WinScriptHost=CreateObject("wscript.shell")

WinScriptHost.run "node_modules\.bin\webpack --watch"
WinScriptHost.run "python manage.py runserver"