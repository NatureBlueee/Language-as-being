import sys
import re
from bs4 import BeautifulSoup

def clean_text(text):
    # Replace multiple spaces/newlines with single space
    return re.sub(r'\s+', ' ', text).strip()

def convert_html_to_md(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {input_path}")
        return

    soup = BeautifulSoup(content, 'html.parser')
    
    # Pre-cleaning: Remove buttons and sr-only elements
    for hidden in soup.find_all(class_=['sr-only', 'button']):
        hidden.decompose()
        
    md_output = []
    
    # Title
    title = soup.find('h1', class_='ltx_title_document')
    if title:
        md_output.append(f"# {clean_text(title.get_text())}\n")
    
    # Authors
    authors = soup.find_all('span', class_='ltx_personname')
    if authors:
        # Check if orcid link is stuck to name
        cleaned_authors = []
        for a in authors:
             # Remove orcid links from text if they are just spans/svgs that result in garbage text
             # looking at HTML: <span class="ltx_personname">Chidimma Opara<span class="ltx_ERROR undefined">\orcidlink</span>...</span>
             # decompsing ltx_ERROR might help
             for err in a.find_all(class_='ltx_ERROR'):
                 err.decompose()
             cleaned_authors.append(clean_text(a.get_text()))
        md_output.append(f"**Authors:** {', '.join(cleaned_authors)}\n")

    # Abstract
    abstract = soup.find('div', class_='ltx_abstract')
    if abstract:
        md_output.append("## Abstract\n")
        abs_p = abstract.find('p', class_='ltx_p')
        if abs_p:
             md_output.append(f"{clean_text(abs_p.get_text())}\n")

    # Content loop
    sections = soup.find_all('section', class_='ltx_section')
    
    for section in sections:
        # Section Title
        sec_title = section.find('h2', class_='ltx_title_section')
        if sec_title:
            # get_text with separator to avoid "1Introduction"
            md_output.append(f"\n## {clean_text(sec_title.get_text(separator=' '))}\n")
        
        for child in section.children:
            if child.name == 'div' and 'ltx_para' in child.get('class', []):
                p = child.find('p', class_='ltx_p')
                if p:
                    md_output.append(f"{clean_text(p.get_text(separator=' '))}\n")
            
            elif child.name == 'section' and 'ltx_subsection' in child.get('class', []):
                process_subsection(child, md_output)
            
            elif child.name == 'figure' and 'ltx_table' in child.get('class', []):
                process_table(child, md_output)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_output))
    
    print(f"Successfully converted to {output_path}")

def process_subsection(subsection, md_output):
    sub_title = subsection.find('h3', class_='ltx_title_subsection')
    if sub_title:
        md_output.append(f"\n### {clean_text(sub_title.get_text(separator=' '))}\n")
    
    for child in subsection.children:
        if child.name == 'div' and 'ltx_para' in child.get('class', []):
            p = child.find('p', class_='ltx_p')
            if p:
                md_output.append(f"{clean_text(p.get_text(separator=' '))}\n")
        elif child.name == 'section' and 'ltx_subsubsection' in child.get('class', []):
             process_subsubsection(child, md_output)
        elif child.name == 'figure' and 'ltx_table' in child.get('class', []):
                process_table(child, md_output)

def process_subsubsection(subsubsection, md_output):
    sub_title = subsubsection.find('h4', class_='ltx_title_subsubsection')
    if sub_title:
        md_output.append(f"\n#### {clean_text(sub_title.get_text(separator=' '))}\n")
    
    for child in subsubsection.children:
        # Sometimes ltx_para is not direct child but inside logic? usually direct.
        if child.name == 'div': # lax check for para containers
             if 'ltx_para' in child.get('class', []):
                process_para_div(child, md_output)
        elif child.name == 'section' and 'ltx_paragraph' in child.get('class', []):
             para_title = child.find('h5', class_='ltx_title_paragraph')
             if para_title:
                 md_output.append(f"\n**{clean_text(para_title.get_text(separator=' '))}**\n")
             
             for subchild in child.children:
                 if subchild.name == 'div' and 'ltx_para' in subchild.get('class', []):
                     process_para_div(subchild, md_output)

def process_para_div(div, md_output):
    # Handle blockquotes and normal paragraphs
    blockquote = div.find('blockquote')
    if blockquote:
        # Extract text from blockquote
        # It might contain p tags
        text = clean_text(blockquote.get_text(separator=' '))
        md_output.append(f"> {text}\n")
    else:
        p = div.find('p')
        if p:
             md_output.append(f"{clean_text(p.get_text(separator=' '))}\n")

def process_table(table_fig, md_output):
    table = table_fig.find('table')
    if not table:
        return
    
    rows = table.find_all('tr')
    if not rows:
        return

    headers = []
    # Identify header row? Usually the first one.
    # Note: LTX tables can be complex.
    first_row = rows[0]
    cols = first_row.find_all(['td', 'th'])
    for col in cols:
        headers.append(clean_text(col.get_text(separator=' ')))
    
    # If headers are empty or it's a layout table, we might need to be careful.
    # Assuming standard data table.
    
    md_output.append(f"\n| {' | '.join(headers)} |")
    md_output.append(f"| {' | '.join(['---'] * len(headers))} |")

    for row in rows[1:]:
        cols = row.find_all(['td', 'th'])
        row_data = [clean_text(c.get_text(separator=' ')) for c in cols]
        
        if len(row_data) < len(headers):
             row_data += [''] * (len(headers) - len(row_data))
        
        md_output.append(f"| {' | '.join(row_data)} |")
    
    md_output.append("\n")
    
    caption = table_fig.find('figcaption')
    if caption:
        md_output.append(f"_{clean_text(caption.get_text(separator=' '))}_\n")


if __name__ == "__main__":
    convert_html_to_md(r"d:\Profolio\Language-as-being\.html", r"d:\Profolio\Language-as-being\paper.md")
