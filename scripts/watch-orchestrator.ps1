[CmdletBinding()]
param(
    [string] $LogPath = (Join-Path $env:USERPROFILE ".ai-orchestrator\state\orchestration-events.jsonl"),
    [int] $Tail = 30,
    [int] $PollSeconds = 1,
    [switch] $Once
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Format-OrchestratorEvent {
    param([string] $Line)

    if ([string]::IsNullOrWhiteSpace($Line)) {
        return $null
    }

    try {
        $event = $Line | ConvertFrom-Json
    }
    catch {
        return "invalid-json  $Line"
    }

    try {
        $time = ([DateTimeOffset]::Parse([string]$event.timestamp)).ToLocalTime().ToString("HH:mm:ss")
    }
    catch {
        $time = "--:--:--"
    }

    $agent = if ($event.agent) { [string]$event.agent } else { "-" }
    $name = if ($event.event) { [string]$event.event } else { "-" }
    $task = if ($event.task_id) { [string]$event.task_id } else { "-" }
    $route = if ($event.target_agent) { " -> $($event.target_agent)" } else { "" }
    $status = if ($event.status) { " [$($event.status)]" } else { "" }
    $summary = if ($event.summary) { " $($event.summary)" } else { "" }

    "{0}  {1,-12} {2,-22} {3}{4}{5}{6}" -f $time, $agent, $name, $task, $route, $status, $summary
}

$printed = 0

while ($true) {
    if (-not (Test-Path -LiteralPath $LogPath)) {
        if ($Once) {
            "No events yet: $LogPath"
            break
        }
        Start-Sleep -Seconds $PollSeconds
        continue
    }

    $lines = @(Get-Content -LiteralPath $LogPath)
    if ($printed -eq 0 -and $Tail -gt 0 -and $lines.Count -gt $Tail) {
        $printed = $lines.Count - $Tail
    }

    for ($i = $printed; $i -lt $lines.Count; $i++) {
        $formatted = Format-OrchestratorEvent -Line $lines[$i]
        if ($formatted) {
            $formatted
        }
    }
    $printed = $lines.Count

    if ($Once) {
        break
    }

    Start-Sleep -Seconds $PollSeconds
}

