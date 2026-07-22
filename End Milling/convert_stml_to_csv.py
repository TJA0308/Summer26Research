import os
import csv
from pathlib import Path

def convert_stml_to_csv(input_file, output_file):
    """
    Convert a LabVIEW STML file to CSV format.
    Parses the STML file and extracts the data section after the header.
    """
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Find the data section (after the second ***End_of_Header***)
    header_count = 0
    data_start_idx = 0
    
    for i, line in enumerate(lines):
        if '***End_of_Header***' in line:
            header_count += 1
            if header_count == 2:
                data_start_idx = i + 1
                break
    
    # Extract data lines
    data_lines = []
    for line in lines[data_start_idx:]:
        line = line.strip()
        if line:  # Skip empty lines
            data_lines.append(line)
    
    # Parse tab-separated data
    rows = []
    for line in data_lines:
        # Split by tabs
        cells = line.split('\t')
        rows.append(cells)
    
    # Write to CSV with new headers
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write custom headers
        if rows:
            # Write headers (time, ai4, ai5, ai6)
            writer.writerow(['time', 'ai4', 'ai5', 'ai6'])
            
            # Write data rows (skip the original header row and comment column)
            for row in rows[1:]:  # Skip first row which is the original header
                if len(row) >= 4:
                    # Keep only the first 4 columns (X_Value, ai4, ai5, ai6), skip comment
                    writer.writerow(row[:4])
    
    print(f"Converted: {input_file} -> {output_file}")

def main():
    """Convert all 45 STML files to run1.csv-run45.csv, per README.md's
    run/stlml mapping table:
      stlml_10-45  -> run1-run36   (run_number = i - 9)
      stlml_1-9    -> run37-run45  (run_number = i + 36)
    The second range was missing originally -- README's table shows
    run37-39=stlml_1-3, run40-42=stlml_4-6, run43-45=stlml_7-9, i.e.
    stlml_1 -> run37, ..., stlml_9 -> run45."""
    data_dir = Path('data')

    for i in range(10, 46):  # stlml_10..45 -> run1..36
        stml_file = data_dir / f'stlml_{i}.txt'
        run_number = i - 9
        output_file = data_dir / f'run{run_number}.csv'
        if stml_file.exists():
            convert_stml_to_csv(str(stml_file), str(output_file))
        else:
            print(f"File not found: {stml_file}")

    for i in range(1, 10):  # stlml_1..9 -> run37..45
        stml_file = data_dir / f'stlml_{i}.txt'
        run_number = i + 36
        output_file = data_dir / f'run{run_number}.csv'
        if stml_file.exists():
            convert_stml_to_csv(str(stml_file), str(output_file))
        else:
            print(f"File not found: {stml_file}")

if __name__ == '__main__':
    main()
