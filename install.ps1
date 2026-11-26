# Skill Compass - Windows wrapper. Usage: .\install.ps1 [install|status|uninstall|export|hosts] [options]
$ErrorActionPreference = "Stop"
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { Write-Error "Python 3.8+ is required (https://www.python.org/downloads/)." ; exit 1 }
$cmdArgs = if ($args.Count -eq 0) { @("install") } else { $args }
& $py.Source (Join-Path $PSScriptRoot "installer\compass.py") @cmdArgs
exit $LASTEXITCODE
