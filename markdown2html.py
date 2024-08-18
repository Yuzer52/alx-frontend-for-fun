#!/usr/bin/python3
"""
Script to convert a Markdown file to an HTML file.

Takes two arguments:
    - First argument: The Markdown file name.
    - Second argument: The output HTML file name.
"""

import sys
import os
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    """Converts the Markdown content to HTML and writes to the output file."""
    unordered_start, ordered_start, paragraph = False, False, False

    with open(input_file, 'r') as md_file, open(output_file, 'w') as html_file:
        for line in md_file:
            # Process bold and italic
            line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)

            # Process MD5 transformation
            md5_matches = re.findall(r'\[\[(.+?)\]\]', line)
            if md5_matches:
                md5_hash = hashlib.md5(md5_matches[0].encode()).hexdigest()
                line = line.replace(f'[[{md5_matches[0]}]]', md5_hash)

            # Remove the letter 'C' and 'c'
            c_removal_matches = re.findall(r'\(\((.+?)\)\)', line)
            if c_removal_matches:
                cleaned_text = ''.join(c for c in c_removal_matches[0] if c not in 'Cc')
                line = line.replace(f'(({c_removal_matches[0]}))', cleaned_text)

            # Process headings
            heading_level = len(line) - len(line.lstrip('#'))
            if 1 <= heading_level <= 6:
                line = f'<h{heading_level}>{line.lstrip("#").strip()}</h{heading_level}>\n'

            # Process unordered lists
            if line.startswith('- '):
                if not unordered_start:
                    html_file.write('<ul>\n')
                    unordered_start = True
                line = f'<li>{line.lstrip("-").strip()}</li>\n'
            elif unordered_start:
                html_file.write('</ul>\n')
                unordered_start = False

            # Process ordered lists
            if line.startswith('* '):
                if not ordered_start:
                    html_file.write('<ol>\n')
                    ordered_start = True
                line = f'<li>{line.lstrip("*").strip()}</li>\n'
            elif ordered_start:
                html_file.write('</ol>\n')
                ordered_start = False

            # Process paragraphs
            if not heading_level and not unordered_start and not ordered_start:
                if len(line.strip()) > 0:
                    if not paragraph:
                        html_file.write('<p>\n')
                        paragraph = True
                    else:
                        html_file.write('<br/>\n')
                elif paragraph:
                    html_file.write('</p>\n')
                    paragraph = False

            # Write the processed line to the HTML file
            if len(line.strip()) > 0:
                html_file.write(line)

        # Close any open lists or paragraphs
        if unordered_start:
            html_file.write('</ul>\n')
        if ordered_start:
            html_file.write('</ol>\n')
        if paragraph:
            html_file.write('</p>\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py <input_markdown_file> <output_html_file>', file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)

