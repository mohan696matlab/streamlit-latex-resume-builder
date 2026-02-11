import json
import os
import subprocess
from typing import Dict, List, Any

def render_latex(tex_file_path, output_pdf_dir="temp/resume"):
    # Ensure the file exists
    if not os.path.exists(tex_file_path):
        raise FileNotFoundError(f"{tex_file_path} not found.")
    
    os.makedirs(output_pdf_dir, exist_ok=True)

    # Run pdflatex twice to resolve references
    for _ in range(2):
        subprocess.run(
            [
                "pdflatex", 
                "-interaction=nonstopmode", 
                 f"-output-directory={output_pdf_dir}",
                tex_file_path],
            check=True
        )

    print("PDF rendered successfully.")

def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in text."""
    if not text:
        return ""
    
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text


def format_url(url: str, text: str = None) -> str:
    """Format a URL for LaTeX with optional display text."""
    if not url:
        return ""
    
    # Add https:// if not present
    if url and not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    display_text = text if text else url
    return f"\\href{{{url}}}{{\\textcolor{{linkcolor}}{{{escape_latex(display_text)}}}}}"


def generate_header(data: Dict[str, Any]) -> str:
    """Generate the LaTeX header section."""
    name = escape_latex(data.get('name', ''))
    job_title = escape_latex(data.get('job_title', ''))
    location = escape_latex(data.get('location', ''))
    email = data.get('email', '')
    phone = escape_latex(data.get('phone', ''))
    
    # Build contact links
    contact_links = []
    if data.get('linkedin'):
        contact_links.append(format_url(data['linkedin'], 'LinkedIn'))
    if data.get('github'):
        contact_links.append(format_url(data['github'], 'GitHub'))
    if data.get('website'):
        contact_links.append(format_url(data['website'], 'Website'))
    if data.get('google_scholar'):
        contact_links.append(format_url(data['google_scholar'], 'Google Scholar'))
    
    header = f"""\\begin{{tabular*}}{{\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
  \\textbf{{\\Large {name}}} & Email: \\href{{mailto:{email}}}{{{email}}} \\\\
  \\textbf{{\\large {job_title}}} \\\\
  {location} & Mobile: {phone} \\\\
"""
    
    # Add contact links in pairs
    if contact_links:
        for i in range(0, len(contact_links), 2):
            left = contact_links[i]
            right = contact_links[i + 1] if i + 1 < len(contact_links) else ''
            header += f"  {left} & {right} \\\\\n"
    
    header += "\\end{tabular*}\n"
    
    return header


def generate_education(education_list: List[Dict[str, Any]]) -> str:
    """Generate the education section."""
    if not education_list:
        return ""
    
    section = "\\section{Education}\n  \\resumeSubHeadingListStart\n"
    
    for edu in education_list:
        institution = escape_latex(edu.get('institution', ''))
        location = escape_latex(edu.get('location', ''))
        degree = escape_latex(edu.get('degree', ''))
        duration = escape_latex(edu.get('duration', ''))
        
        # Add lab link if available
        if edu.get('lab_name') and edu.get('lab_url'):
            lab_link = format_url(edu['lab_url'], edu['lab_name'])
            institution = f"{institution},  {lab_link}"
        
        section += f"""    \\resumeSubheading
      {{{institution}}}{{{location}}}
      {{{degree}}}{{{duration}}}
"""
    
    section += "  \\resumeSubHeadingListEnd\n"
    return section


def generate_work_experience(workex_list: List[Dict[str, Any]]) -> str:
    """Generate the work experience section."""
    if not workex_list:
        return ""
    
    section = "\\section{Work Experience}\n"
    
    for job in workex_list:
        company = escape_latex(job.get('company', ''))
        location = escape_latex(job.get('location', ''))
        role = escape_latex(job.get('role', ''))
        duration = escape_latex(job.get('duration', ''))
        
        section += f"""
    \\resumeSubHeadingListStart
    \\resumeSubheading
    {{{company}}}{{{location}}}
    {{{role}}}{{{duration}}}
"""
        
        # Add achievements
        achievements = job.get('achievements', [])
        if achievements:
            section += "    \\resumeItemListStart\n"
            for ach in achievements:
                title = escape_latex(ach.get('title', ''))
                achievement = escape_latex(ach.get('achievement', ''))
                if title and achievement:
                    section += f"    \\resumeSubItem{{{title}}}{{{achievement}}}\n"
            section += "\\resumeItemListEnd\n"
        
        section += "\\resumeSubHeadingListEnd\n"
    
    return section


def generate_projects(projects_list: List[Dict[str, Any]]) -> str:
    """Generate the projects section."""
    if not projects_list:
        return ""
    
    section = "\\section{Projects}\n\\resumeSubHeadingListStart\n"
    
    for project in projects_list:
        project_name = escape_latex(project.get('project_name', ''))
        achievement = escape_latex(project.get('achievement', ''))
        project_url = project.get('project_url', '')
        
        if project_name:
            if project_url:
                project_url = f"\\href{{{project_url}}}{{\\textcolor{{blue}}{{link}}}}"
                project_name = f"\\textbf{{{project_name}}} ({project_url})"
                section += f"\\resumeSubItem{{{project_name}}}{{{achievement}}}\n"
            else:
                section += f"\\resumeSubItem{{\\textbf{{{project_name}}}}}{{{achievement}}}\n"
   
    
    section += "\\resumeSubHeadingListEnd\n"
    return section


def generate_skills(skills_list: List[Dict[str, Any]]) -> str:
    """Generate the skills section."""
    if not skills_list:
        return ""
    
    section = "\\section{Skills}\n\\resumeSubHeadingListStart\n"
    
    for skill in skills_list:
        category = escape_latex(skill.get('skill_category', ''))
        skills = escape_latex(skill.get('skills', ''))
        
        if category:
            section += f"\\resumeSubItem{{\\textbf{{{category}}}}}{{{skills}}}\n"
        else:
            section += f"\\resumeSubItem{{}}{{{skills}}}\n"
    
    section += "\\resumeSubHeadingListEnd\n"
    return section


def generate_publications(publications_list: list[dict]) -> str:
    """Generate the publications section with DOI as a blue clickable 'DOI' link."""
    if not publications_list:
        return ""
    
    section = "\\section{Publications}\n\\resumeSubHeadingListStart\n"
    
    for pub in publications_list:
        title = escape_latex(pub.get('title', ''))
        venue = escape_latex(pub.get('venue', ''))
        year = escape_latex(pub.get('year', ''))
        doi = pub.get('doi', '')
        
        # Build publication entry
        pub_text = f"\\emph{{{venue}}}"
        if year:
            pub_text += f", {year}"
        
        if doi:
            # Ensure DOI is a full URL
            if not doi.startswith(('http://', 'https://')):
                doi_url = f"https://doi.org/{doi}"
            else:
                doi_url = doi
            
            # Add DOI as blue clickable link
            pub_text += f"  \\href{{{doi_url}}}{{\\textcolor{{blue}}{{(DOI)}}}}"
        
        section += f"  \\resumeSubItem{{{title}}}{{{pub_text}}}\n"
    
    section += "\\resumeSubHeadingListEnd\n"
    return section


def generate_latex_cv(json_data: dict, 
                      output_tex_file: str = "cv_output.tex",
                      output_pdf_dir: str = "cv_output") -> None:
    """
    Generate a LaTeX CV file from JSON input.
    
    Args:
        json_data: JSON data as a dictionary
        output_file: Path to the output LaTeX file
    """
    
    # Read JSON data
    data = json_data
    
    # LaTeX preamble
    latex_content = r"""%-------------------------
% Resume in Latex
% Author : Sourabh Bajaj
% Website: https://github.com/sb2nov/resume
% License : MIT
%------------------------
\PassOptionsToPackage{paperwidth=260mm, paperheight=297mm, margin=20mm}{geometry}
\documentclass[11pt]{article}

\usepackage{geometry} 
\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[pdftex]{hyperref}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{setspace}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\addtolength{\oddsidemargin}{-0.375in}
\addtolength{\evensidemargin}{-0.375in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}
\urlstyle{same}
\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

\newcommand{\resumeItem}[2]{\item\small{\textbf{#1}{: #2 \vspace{-2pt}}}}
\newcommand{\resumeSubheading}[4]{%
  \item
  \textbf{#1}\hfill #2\\
  \textit{\small #3}\hfill \textit{\small #4}
  \vspace{-5pt}
}
\newcommand{\resumeSubItem}[2]{\resumeItem{#1}{#2}\vspace{-1pt}}
\renewcommand{\labelitemii}{$\circ$}
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=*, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=*, label={}]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}
\definecolor{linkcolor}{rgb}{0.0, 0.0, 1.0}
\linespread{1.1}

\begin{document}

%----------HEADING-----------------
"""
    
    # Add sections
    latex_content += generate_header(data) + "\n"
    
    # Add summary if available (you can add this field to your JSON structure)
    if data.get('summary'):
        latex_content += f"\\section{{Summary}}\n{escape_latex(data['summary'])}\n\n"
    
    latex_content += generate_education(data.get('education', [])) + "\n"
    latex_content += generate_work_experience(data.get('work_experience', [])) + "\n"
    latex_content += generate_projects(data.get('projects', [])) + "\n"
    latex_content += generate_skills(data.get('skills', [])) + "\n"
    latex_content += generate_publications(data.get('publications', [])) + "\n"
    
    # End document
    latex_content += "\\end{document}"
    
    # Write to file
    with open(output_tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_content)
    
    print(f"LaTeX CV generated successfully: {output_tex_file}")
    print(f"To compile: pdflatex {output_tex_file}")
    
    render_latex(output_tex_file, output_pdf_dir=output_pdf_dir)