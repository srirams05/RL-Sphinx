# Creating a Sphinx Documentation Project with GitHub Pages

## 1. Set up Python Environment
```powershell
# Create project directory
mkdir Sphinx
cd Sphinx

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate
```

## 2. Install Required Packages
```powershell
pip install sphinx sphinx-rtd-theme myst-parser sphinx-math-dollar
```

## 3. Initialize Sphinx Project
```powershell
sphinx-quickstart
```
Answer the prompts:
- Separate source and build directories? `yes`
- Project name: `Your Project Name`
- Author name: `Your Name`
- Project version: `1.0`

## 4. Configure Sphinx
Update `conf.py`:

````python
# -- Project information -----------------------------------------------------
project = 'Your Project Name'
copyright = '2025, Your Name'
author = 'Your Name'

# -- General configuration ---------------------------------------------------
extensions = [
    'myst_parser',
    'sphinx_rtd_theme',
    'sphinx.ext.mathjax',
    'sphinx_math_dollar'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add these lines for GitHub Pages
html_baseurl = '/your-repo-name/'  # Replace with your repository name
html_use_index = True
html_copy_source = False

# MathJax configuration
mathjax3_config = {
    "tex": {
        "inlineMath": [['$', '$'], ['\\(', '\\)']],
        "displayMath": [['$$', '$$'], ['\\[', '\\]']],
        "processEscapes": True
    }
}
````

## 5. Create Initial Documentation
Create `index.md`:

````markdown
# Welcome to Your Project

## Contents
```{toctree}
:maxdepth: 2
:caption: Contents

Chapter 1 <chapter1>
Chapter 2 <chapter2>
```
````

## 6. Create LaTeX Processing Script
Create `processlatex.py`:

````python
#!/usr/bin/env python3
import re
import sys
import os

def process_markdown_latex(content):
    r"""
    Processes markdown content to normalize LaTeX delimiters.
    """
    # Replace inline math \( -- \) with $ -- $
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)

    # Replace displaystyle math \[ -- \] with $$ format
    display_pattern = r'\\\[\s*(.*?)\s*\\\]'
    display_replacement = '\n$$\n\\1\n$$\n'
    content = re.sub(display_pattern, display_replacement, content, flags=re.DOTALL)

    return content

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <filename.md>")
        sys.exit(1)

    input_file = sys.argv[1]
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_processed{ext}"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        modified_content = process_markdown_latex(original_content)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
````

## 7. Create Update Script
Create update-docs.ps1:

````powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$MarkdownFile,
    [Parameter(Mandatory=$false)]
    [string]$CommitMessage = "Update documentation"
)

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Push-Location source
Write-Host "Processing LaTeX in $MarkdownFile..."
python processlatex.py $MarkdownFile
$baseFile = [System.IO.Path]::GetFileNameWithoutExtension($MarkdownFile)
$ext = [System.IO.Path]::GetExtension($MarkdownFile)
$processedFile = "${baseFile}_processed${ext}"

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

Write-Host "Cleaning build directory..."
if (Test-Path "build") {
    Remove-Item -Recurse -Force .\build\
}
.\make.bat clean

Write-Host "Building new documentation..."
.\make.bat html

Write-Host "Updating docs directory..."
if (-not (Test-Path "docs")) {
    New-Item -ItemType Directory -Path "docs"
}
Copy-Item -Path "build/html/*" -Destination "docs" -Recurse -Force

if (-not (Test-Path "docs\.nojekyll")) {
    New-Item -Path "docs\.nojekyll" -ItemType File -Force
}

git add "source/$MarkdownFile"
git add docs/
git commit -m "$CommitMessage"
git push origin main

Write-Host "Documentation update complete!"
````

## 8. Set up GitHub Repository
1. Create `.gitignore`:
````text
__pycache__/
.venv/
build/
*.pyc
````

2. Initialize Git and GitHub:
- Create new repository on GitHub
- Initialize local repository:
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

## 9. Configure GitHub Pages
1. Go to repository Settings > Pages
2. Set source to:
   - Deploy from branch
   - Branch: main
   - Folder: /docs
3. Save changes

## 10. Usage
After making changes to markdown files:
```powershell
.\update-docs.ps1 -MarkdownFile "chapter1.md" -CommitMessage "Updated content"
```

Your documentation will be available at:
`https://username.github.io/repository-name/`