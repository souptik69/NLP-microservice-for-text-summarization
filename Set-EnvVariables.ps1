Get-Content .env | ForEach-Object {
    if ($_ -match "^\s*$" -or $_ -match "^#") {
        # Skip empty lines and comments
        return
    }
    $name, $value = $_ -split '=', 2
    [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process')
}

