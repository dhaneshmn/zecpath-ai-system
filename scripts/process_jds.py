import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from parsers.jd_parser import process_jd_batch

input_dir = "data/raw_jds"
output_dir = "data/processed_jds"

saved_files = process_jd_batch(input_dir, output_dir)
print(f"Saved {len(saved_files)} JSON files to {output_dir}")