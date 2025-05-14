param(
    [Parameter(Mandatory=$true)]
    [string]$MarkdownFile,
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "Update documentation"
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

# Create .nojekyll file to prevent GitHub Pages from ignoring _static
if (-not (Test-Path "docs\.nojekyll")) {
    New-Item -Path "docs\.nojekyll" -ItemType File -Force
}

# Copy build/html contents to docs directory for GitHub Pages
Write-Host "Updating docs directory..."
if (-not (Test-Path "docs")) {
    New-Item -ItemType Directory -Path "docs"
}
Copy-Item -Path "build/html/*" -Destination "docs" -Recurse -Force

# Git operations
Write-Host "Performing Git operations..."
# Stage changes
git add "source/$MarkdownFile"
git add docs/

# Commit changes
git commit -m "$CommitMessage"

# Push to GitHub
git push origin main

Write-Host "Documentation update and Git push complete!"