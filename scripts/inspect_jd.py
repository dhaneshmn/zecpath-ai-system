# scripts/inspect_jd.py
import json
from pathlib import Path

def main():
    jd_dir = Path("data/processed_jds")
    if not jd_dir.exists():
        print(f"Directory {jd_dir} not found.")
        return

    json_files = list(jd_dir.glob("*.json"))
    if not json_files:
        print("No JSON files found in", jd_dir)
        return

    # Pick the first file
    jd_file = json_files[0]
    print(f"Inspecting: {jd_file}\n")

    with open(jd_file, encoding='utf-8') as f:
        data = json.load(f)

    # Display key fields
    print(f"Job ID: {data.get('job_id')}")
    print(f"Title: {data.get('title')}")
    print(f"Company: {data.get('company')}")
    print(f"Location: {data.get('location')}")
    print(f"Employment Type: {data.get('employment_type')}")
    print(f"Experience Required: {data.get('experience_required')}")
    print("\nEducation Required:")
    for edu in data.get('education_required', []):
        print(f"  - {edu}")
    print("\nSkills Required (with importance):")
    for skill in data.get('skills_required', []):
        print(f"  - {skill['name']}: {skill['importance']}")
    print(f"\nSalary Range: {data.get('salary_range')}")
    print(f"Posted Date: {data.get('posted_date')}")
    print(f"Deadline: {data.get('application_deadline')}")
    print("\nFirst 200 characters of responsibilities:")
    resp = data.get('responsibilities', [])
    if resp:
        print(resp[0][:200])
    else:
        print("(none)")

if __name__ == "__main__":
    main()