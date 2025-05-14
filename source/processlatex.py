#!/usr/bin/env python3
import re
import sys
import os

def process_markdown_latex(content):
    r"""
    Processes markdown content to normalize LaTeX delimiters.

    1. Replaces inline math \( -- \) with $ -- $
    2. Replaces displaystyle math \[ -- \] with
       \newline
       $$
       --
       $$
       \newline
    """

    # 1. Replace inline math \( -- \) with $ -- $
    # Pattern r'\\\(' :
    #   - r'' is a raw string.
    #   - In the raw string, '\\' gives a literal backslash to the regex engine.
    #   - In the raw string, '\(' gives a literal '(' to the regex engine *after* the literal backslash.
    #   - So regex matches a literal '\' followed by a literal '('. This is correct for input "\(".
    #   - Python issues a SyntaxWarning for '\(' in the raw string, but the behavior is correct.
    # Replacement r'$\1$' is fine.
    content = re.sub(r'\\\((.*?)\\\)', r'$\1$', content)

    # 2. Replace displaystyle math \[ -- \] with specified $$ format
    # Pattern r'\\\[...\\\]' uses similar logic as above for matching literal '\[...\]'.
    # Python will issue SyntaxWarning for '\[' and '\]'.
    # Replacement string is NOT raw, so:
    #   - '\n' becomes an actual newline character.
    #   - '\\1' becomes '\1' for re.sub, which uses it as a backreference.
    display_pattern = r'\\\[\s*(.*?)\s*\\\]'
    # Note: The prompt explicitly asks for the *string* "\newline", then actual newlines.
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
        # Read input with UTF-8 encoding
        with open(input_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Process the content
        modified_content = process_markdown_latex(original_content)

        # Write output with UTF-8 encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        print(f"Successfully processed '{input_file}'")
        print(f"Output written to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)