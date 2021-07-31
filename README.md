# delivery-for-vscode-tasks
copy(delivery) to multiple work directories

Tasks are defined in a workspace tasks.json file and VS Code has templates for common task runners. In the Command Palette (Ctrl+Shift+P), you can filter on 'task' and can see the various Task related commands.

Select the Tasks: Configure Task Runner command and you will see a list of task runner templates. Select Others to create a task which runs an external command.

## Default Setting
tasks.json [2.0.0]
```json
{
    "version" : "2.0.0",
    "tasks": [
        {
            "taskName": "singleFile",
            "command": "python .vscode/delivery.py ${relativeFile}",
            "type":"shell",
            "group": {
                "kind":"build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "silent",
                "echo": false
            }
        },
        {
            "taskName": "all",
            "command": "python .vscode/delivery.py all",
            "type":"shell",
            "presentation": {
                "reveal": "silent",
                "echo": false
            }
        },
        {
            "taskName": "ftpCheck",
            "command": "python .vscode/delivery.py ftpCheck",
            "type":"shell",
            "presentation": {
                "reveal": "silent",
                "echo": false
            }
        }
    ]
}
```

tasks.json [0.1.0]
```json
{
    "version": "0.1.0",
    "command": "python",
    "args": [".vscode/delivery.py"],
    "showOutput": "silent",
    "suppressTaskName": true,
    "tasks": [
        {
            "taskName": "singleFile",
            "args": ["${file}"],
            "isBuildCommand": true
        },
        {
            "taskName": "all",
            "args": ["all"]
        },
        {
            "taskName": "ftpCheck",
            "args": ["ftpCheck"]
        }
    ]
}
```

delivery.ini
```ini
[common]
es6_translate = Y #use DukPy(pypi.org/project/dukpy)

[project name]
method = ftp
host = [host name]
userid = [ftp id]
password = [password]
port = 21
#source_location = src_location/sub
location = /home/user/project/subdir

[local project name]
method = local
#source_location = src_location/sub
location = c:\delivery_test
```

delivery.py and delivery-conf.ini files copy to .vscode/

## TypeScript compile
if you want compile TypeScript then install TypeScript globally by npm. "npm install -g typescript".
'filename.ts' save then automatically save to 'filename.js' and delivered.

## ES6 to ES5 translate
if you want translate ES6 to ES5 then use DukPy(pypi.org/project/dukpy).   
DukPy Install and set script filename like 'filename.es6' and run.   
Then automatically save to 'filename.js' and delivered.

## History
- 0.1.10
typescript compile support
- 0.1.9
minor bug fix
- 0.1.8   
minor update, add error comment
- 0.1.7   
es6 translate utf-8 support
- 0.1.6   
es6 translate support - use DukPy(pypi.org/project/dukpy)