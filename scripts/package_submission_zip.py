"""
Package CropShield AI Submission Archive
Creates a clean, competition-compliant zip file that:
  - Excludes all private environment files (.env, .env.local)
  - Excludes build bundles (dist/, node_modules/, .git/, __pycache__)
  - Includes complete source code, technical reports (.pdf, .docx, .md), tests, wiki, and sentinel analysis.
"""

import os
import zipfile
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_ZIP = ROOT_DIR.parent / "cropshield-ai-submission.zip"

EXCLUDED_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".gradle",
    "dist",
    "build",
    ".idea",
    ".vscode"
}

EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".DS_Store"
}

def is_excluded(rel_path: Path) -> bool:
    parts = rel_path.parts
    # Check if any parent folder is in EXCLUDED_DIRS
    for part in parts:
        if part in EXCLUDED_DIRS:
            return True
    # Check filename
    filename = rel_path.name
    if filename.startswith(".env") or filename in {".gitignore"}:
        # Keep .gitignore, exclude .env*
        if filename.startswith(".env"):
            return True
    if rel_path.suffix in EXCLUDED_EXTENSIONS:
        return True
    return False

def package_submission():
    print(f"Creating clean submission archive: {OUTPUT_ZIP}")
    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(ROOT_DIR):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                abs_path = Path(root) / file
                rel_path = abs_path.relative_to(ROOT_DIR)

                if is_excluded(rel_path):
                    continue

                zip_entry_name = Path("cropshield-ai") / rel_path
                zipf.write(abs_path, str(zip_entry_name))
                file_count += 1
                total_uncompressed_bytes += abs_path.stat().st_size

    zip_size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"Successfully created: {OUTPUT_ZIP}")
    print(f"Total files included: {file_count}")
    print(f"Archive compressed size: {zip_size_mb:.2f} MB")
    print("Verification: No .env, .env.local, or dist/ files included.")

if __name__ == "__main__":
    package_submission()
