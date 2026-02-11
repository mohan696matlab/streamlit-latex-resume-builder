# Streamlit LaTeX Resume Builder

Minimal Streamlit app to build LaTeX resumes from simple inputs.

## Repo structure
- `resume_template_app.py` — Streamlit application entrypoint
- `utlis.py` — helper utilities

## Setup (Linux)
1. Create a virtual environment using `venv`:

```bash
python3 -m venv .venv
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Install dependencies (if a `requirements.txt` exists):

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run resume_template_app.py
```

## Notes
- This repo does not pin dependencies by default — add a `requirements.txt` if you want reproducible installs.
- The virtual environment will be created in `.venv` (ignored by `.gitignore`).

## Installing pdfLaTeX

If you want to compile LaTeX to PDF locally (required for producing final resume PDFs), install a TeX distribution with `pdflatex`.

- Linux (Debian/Ubuntu):

	- Lightweight (recommended):

		```bash
		sudo apt update
		sudo apt install texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
		```

	- Full (large, but includes everything):

		```bash
		sudo apt update
		sudo apt install texlive-full
		```

- Windows:

	- Install MiKTeX (recommended for most Windows users):
		1. Download the installer from https://miktex.org/download
		2. Run the installer and follow the prompts (enable on-the-fly package installation if asked).

	- Or install TeX Live using the Windows installer from https://tug.org/texlive/

Verify installation by running:

```bash
pdflatex --version
```

And test by compiling a `.tex` file:

```bash
pdflatex resume.tex
```


## Contact
Open an issue or edit the README if you'd like additional setup instructions.
