[CmdletBinding()]
param(
    [string] $LogPath = (Join-Path $env:USERPROFILE ".ai-orchestrator\state\orchestration-events.jsonl"),
    [Parameter(Mandatory = $true)]
    [string] $Agent,
    [Parameter(Mandatory = $true)]
    [string] $Role,
    [Parameter(Mandatory = $true)]
    [string] $Event,
    [string] $TaskId = "",
    [string] $TargetAgent = "",
    [string] $Status = "",
    [string] $WorkDir = "",
    [string] $StateDir = "",
    [string] $Summary = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$dir = Split-Path -Parent $LogPath
if ($dir -and -not (Test-Path -LiteralPath $dir)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$record = [ordered]@{
    timestamp = (Get-Date).ToUniversalTime().ToString("o")
    agent = $Agent
    role = $Role
    event = $Event
    task_id = $TaskId
    target_agent = $TargetAgent
    status = $Status
    work_dir = $WorkDir
    state_dir = $StateDir
    summary = $Summary
}

($record | ConvertTo-Json -Compress -Depth 6) | Add-Content -LiteralPath $LogPath -Encoding UTF8

