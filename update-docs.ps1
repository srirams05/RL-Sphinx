param(
    [Parameter(Mandatory=$true)]
    [string]$MarkdownFile
)

# Ensure we're in the right directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Process LaTeX in the source directory
Push-Location source
Write-Host "Processing LaTeX in $MarkdownFile..."
python processlatex.py $MarkdownFile
$baseFile = [System.IO.Path]::GetFileNameWithoutExtension($MarkdownFile)
$ext = [System.IO.Path]::GetExtension($MarkdownFile)
$processedFile = "${baseFile}_processed${ext}"

# Replace original file with processed version if it exists
if (Test-Path $processedFile) {
    Remove-Item $MarkdownFile
    Rename-Item $processedFile $MarkdownFile
    Write-Host "Updated $MarkdownFile with processed content"
} else {
    Write-Host "Warning: No processed file was created"
    Pop-Location
    exit 1
}
Pop-Location

# Clean up build directory
Write-Host "Cleaning build directory..."
if (Test-Path "build") {
    Remove-Item -Recurse -Force .\build\
}
.\make.bat clean

# Generate new documentation
Write-Host "Building new documentation..."
.\make.bat html

Write-Host "Documentation update complete!"