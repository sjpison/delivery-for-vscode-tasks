# delivery-for-vscode-tasks
copy(delivery) to multiple work directories

Tasks are defined in a workspace tasks.json file and VS Code has templates for common task runners. In the Command Palette (Ctrl+Shift+P), you can filter on 'task' and can see the various Task related commands.

Select the Tasks: Configure Task Runner command and you will see a list of task runner templates. Select Others to create a task which runs an external command.

tasks.json [2.0.0]
```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
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
