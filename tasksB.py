# tasksB.py
# Phase B: LLM-based Automation Agent for DataWorks Solutions

import os
import subprocess
from fastapi import HTTPException

# B1 & B2: Security Checks
def B12(filepaths):
    """Ensure all file paths are within /data."""
    for filepath in filepaths:
        if not filepath.startswith('/data'):
            return False
    return True

# B3: Fetch Data from an API and save it
def B3(url, save_path):
    if not B12([save_path]):
        raise PermissionError("save_path must be under /data")
    import requests
    response = requests.get(url)
    with open(save_path, 'w') as file:
        file.write(response.text)

# B4: Clone a Git Repo and make a commit
def B4(repo_url, commit_message):
    print(f"Called B4 with repo_url: {repo_url} and commit_message: {commit_message}")
    repo_dir = "/data/repo"
    
    # Ensure /data directory exists
    if not os.path.exists("/data"):
        try:
            os.makedirs("/data")
            print(f"Created directory /data")
        except Exception as e:
            print(f"Error creating /data directory: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating /data directory: {str(e)}")
    
    # Clone into /data/repo only if it doesn't exist already
    if not os.path.exists(repo_dir):
        try:
            print(f"Cloning repository {repo_url} into {repo_dir}")
            result = subprocess.run(["git", "clone", repo_url, repo_dir], check=True, capture_output=True, text=True)
            print(f"Clone output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e.stderr}")
            raise HTTPException(status_code=500, detail=f"Error cloning repository: {e.stderr}")
    
    # Check if the directory contains a .git folder to confirm it's a valid git repository
    if not os.path.exists(os.path.join(repo_dir, ".git")):
        print("The directory is not a valid git repository.")
        raise HTTPException(status_code=500, detail="The directory is not a valid git repository.")
    
    # Append the commit message to a dummy file
    dummy_file = os.path.join(repo_dir, "commit.txt")
    try:
        print(f"Writing commit message to {dummy_file}")
        with open(dummy_file, "a") as f:
            f.write(commit_message + "\n")
    except Exception as e:
        print(f"Error writing to dummy file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error writing to dummy file: {str(e)}")
    
    try:
        print("Adding commit.txt to git")
        subprocess.run(["git", "-C", repo_dir, "add", "commit.txt"], check=True)
        print("Committing changes")
        subprocess.run(["git", "-C", repo_dir, "commit", "-m", commit_message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e.stderr}")
        raise HTTPException(status_code=500, detail=f"Error committing changes: {e.stderr}")

    return {"message": "Repository cloned and commit made successfully."}

# B5: Run SQL Query on a SQLite or DuckDB database
def B5(db_path, query, output_filename):
    if not B12([db_path, output_filename]):
        raise PermissionError("Both db_path and output_filename must be under /data")
    import sqlite3, duckdb
    if db_path.endswith('.db'):
        conn = sqlite3.connect(db_path)
    else:
        conn = duckdb.connect(db_path)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    with open(output_filename, 'w') as file:
        file.write(str(result))
    return result

# B6: Extract data (scrape) from a website and save it
def B6(url, output_filename):
    if not B12([output_filename]):
        raise PermissionError("output_filename must be under /data")
    import requests
    result = requests.get(url).text
    with open(output_filename, 'w') as file:
        file.write(result)

# B7: Compress or resize an image
def B7(image_path, output_path, resize=None):
    from PIL import Image
    if not B12([image_path, output_path]):
        raise PermissionError("Both image_path and output_path must be under /data")
    img = Image.open(image_path)
    if resize:
        img = img.resize(tuple(resize))
    img.save(output_path)

# B8: Transcribe audio from an MP3 file (stub implementation)
def B8(audio_path, output_filename):
    if not B12([audio_path, output_filename]):
         raise PermissionError("Both audio_path and output_filename must be under /data")
    # Stub transcription – in production, integrate with a transcription service/library.
    text = "Transcribed audio text (stub)."
    with open(output_filename, "w") as f:
         f.write(text)
    return text

# B9: Convert Markdown to HTML
def B9(md_path, output_path):
    import markdown
    if not B12([md_path, output_path]):
        raise PermissionError("Both md_path and output_path must be under /data")
    with open(md_path, 'r') as file:
        html = markdown.markdown(file.read())
    with open(output_path, 'w') as file:
        file.write(html)

# B10: Filter a CSV file based on a column value and return JSON data
def B10(csv_path, filter_column, filter_value):
    import pandas as pd
    if not B12([csv_path]):
         raise PermissionError("csv_path must be under /data")
    df = pd.read_csv(csv_path)
    filtered = df[df[filter_column] == filter_value]
    return filtered.to_dict(orient='records')
