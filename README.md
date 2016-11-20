# delivery-for-vscode-tasks
copy(delivery) to multiple work directories

tasks.json
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
        }
    ]
}
```
