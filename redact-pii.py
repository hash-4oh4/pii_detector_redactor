import os
import pandas as pd
import zipfile
import subprocess

# -------- 1. Clean Dataset --------
df = pd.read_csv("iscp_pii_dataset_-_Sheet1.csv")

# Example masking of PII
if "email" in df.columns:
    df["email"] = df["email"].str.replace(r"(.+)@(.+)", r"***@\2", regex=True)
if "phone" in df.columns:
    df["phone"] = df["phone"].astype(str).str.replace(r"\d{6}$", "******", regex=True)

df.to_excel("iscp_pii_dataset_cleaned.xlsx", index=False)

# -------- 2. Create Diagram --------
mermaid_code = """
flowchart LR
    Client["Security Engineer (Browser)"]
    Frontend["Frontend (Next.js + Tailwind)"]
    Backend["Backend (Express + MCP)"]
    DB[(SQLite Database)]
    Services["External Services/Tools"]

    Client --> Frontend
    Frontend --> Backend
    Backend --> DB
    Backend --> Services
"""
with open("architecture.mmd", "w") as f:
    f.write(mermaid_code)

# -------- 3. Create README --------
readme_content = """
# ISCP PII Project

## Overview
This project demonstrates:
- Cleaning Personally Identifiable Information (PII) from datasets
- System architecture documentation using Mermaid diagrams
- Packaged project for GitHub deployment

## Contents
- `iscp_pii_dataset_cleaned.xlsx` → Cleaned dataset with masked PII
- `architecture.mmd` → System architecture diagram
- `README.md` → Project documentation
"""
with open("README.md", "w") as f:
    f.write(readme_content)

# -------- 4. Zip for Release --------
with zipfile.ZipFile("iscp_pii_project.zip", "w") as zipf:
    zipf.write("iscp_pii_dataset_cleaned.xlsx")
    zipf.write("architecture.mmd")
    zipf.write("README.md")

# -------- 5. Initialize Git & Push to GitHub --------
repo_name = "iscp-pii-project"
github_user = "YOUR_GITHUB_USERNAME"
github_token = "YOUR_GITHUB_TOKEN"   # generate from https://github.com/settings/tokens

# Create repo locally
if not os.path.exists(".git"):
    subprocess.run(["git", "init"])
    subprocess.run(["git", "branch", "-M", "main"])

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Initial commit - ISCP PII Project"])

# Set remote and push
remote_url = f"https://{github_user}:{github_token}@github.com/{github_user}/{repo_name}.git"
subprocess.run(["git", "remote", "add", "origin", remote_url])
subprocess.run(["git", "push", "-u", "origin", "main", "--force"])

print(f"✅ Project pushed to GitHub repo: https://github.com/{github_user}/{repo_name}")
