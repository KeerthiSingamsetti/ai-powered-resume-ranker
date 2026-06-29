"""
Run this once to generate sample test PDFs:
    python create_test_resumes.py
"""
import os
import subprocess
import sys

# Install fpdf2 if not present
try:
    from fpdf import FPDF
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF


def make_pdf(filename, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    for line in content.strip().splitlines():
        safe = line.encode("latin-1", errors="replace").decode("latin-1")
        pdf.cell(0, 8, safe, new_x="LMARGIN", new_y="NEXT")
    pdf.output(f"test_data/{filename}")
    print(f"Created: test_data/{filename}")


os.makedirs("test_data", exist_ok=True)

# --- Resume 1: Strong candidate ---
make_pdf("Alice_Resume.pdf", """
Alice Johnson  |  alice@email.com

EDUCATION
B.Tech Computer Science, IIT Delhi - Graduated 2020

EXPERIENCE
Senior Data Scientist - TechCorp (Jan 2021 - Present)
Machine Learning Engineer - StartupXYZ (Jun 2020 - Dec 2020)

SKILLS
Python, Machine Learning, Deep Learning, NLP, TensorFlow, PyTorch
Scikit-learn, Pandas, NumPy, SQL, AWS, Docker, Git
Communication, Leadership, Agile, Scrum

CERTIFICATIONS
AWS Certified Machine Learning Specialist
Google Data Analytics Certificate

4 years of experience in machine learning and data science.
""")

# --- Resume 2: Weak candidate with fake experience claim ---
make_pdf("Bob_Resume.pdf", """
Bob Smith  |  bob@email.com

EDUCATION
B.Sc Mathematics, Mumbai University - Graduated 2022

EXPERIENCE
Junior Developer - WebAgency (Mar 2023 - Present)
Intern - LocalShop (Jan 2023 - Feb 2023)

SKILLS
Python, HTML, CSS, SQL, Git

10 years of experience in software development.
""")

# --- Sample Job Description ---
jd = """We are hiring a Senior Data Scientist.

Requirements:
- 3+ years experience in Machine Learning and NLP
- Proficient in Python, TensorFlow, PyTorch, Scikit-learn
- Experience with AWS, Docker, and Git
- Strong communication and leadership skills
- Knowledge of SQL and data pipelines
- Deep Learning experience preferred
- Agile and Scrum team experience
"""

with open("test_data/sample_job_description.txt", "w") as f:
    f.write(jd)

print("Created: test_data/sample_job_description.txt")
print("\nAll test files ready in the test_data/ folder!")
