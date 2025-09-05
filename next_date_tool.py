import argparse
import csv
import os
import requests
from typing import List, Tuple, Dict
import openpyxl
from dotenv import load_dotenv


# --- Gemini API Test Case Generation ---
def generate_next_date_cases_gemini(api_key: str, num_cases: int = 10) -> List[Tuple[str, str]]:
    """
    Generate test cases for the next date problem using Gemini 2.0 API.
    Returns list of (input_date, expected_next_date).
    """
    # Gemini 2.0 Flash model name: gemini-2.0-flash
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    prompt = (
        f"Generate {num_cases} test cases for the next date problem using robust boundary value analysis and normal test cases. "
        "Include both positive (valid) and negative (invalid) cases, focusing on boundary values such as month ends, leap years, minimum and maximum years, and invalid dates. "
        "Each test case should be in the format: YYYY-MM-DD,YYYY-MM-DD (input_date,expected_next_date) for valid cases, and YYYY-MM-DD,INVALID for invalid cases. "
        "Separate each test case by a newline. Only output the test cases."
    )
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    params = {"key": api_key}
    response = requests.post(url, headers=headers, params=params, json=data)
    cases = []
    if response.status_code == 200:
        try:
            result = response.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            for line in text.strip().split("\n"):
                parts = line.split(",")
                if len(parts) == 2:
                    cases.append((parts[0].strip(), parts[1].strip()))
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
    else:
        print(f"Gemini API error: {response.status_code} {response.text}")
    return cases

# --- File Comparison ---
def read_test_file(file_path: str) -> List[Tuple[str, str]]:
    """Read test cases from a file. Supports CSV and XLSX. Format: input_date,expected_next_date"""
    cases = []
    if file_path.lower().endswith('.xlsx'):
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
        for row in ws.iter_rows(min_row=1, values_only=True):
            if row and len(row) >= 2:
                cases.append((str(row[0]).strip(), str(row[1]).strip()))
    else:
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    cases.append((row[0].strip(), row[1].strip()))
    return cases

def compare_cases(generated: List[Tuple[str, str]], uploaded: List[Tuple[str, str]]) -> Dict[str, int]:
    """Compare generated and uploaded cases. Return counts of positive/negative matches."""
    gen_dict = {inp: out for inp, out in generated}
    pos, neg = 0, 0
    for inp, out in uploaded:
        if inp in gen_dict and gen_dict[inp] == out:
            pos += 1
        else:
            neg += 1
    return {"positive": pos, "negative": neg, "total": len(uploaded)}

# --- CLI ---
def save_test_cases_to_csv(test_cases: List[Tuple[str, str]], filename: str):
    """Save test cases to a CSV file."""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for inp, out in test_cases:
            writer.writerow([inp, out])

def main():
    # Automatically load environment variables from .env file
    load_dotenv()
    parser = argparse.ArgumentParser(description="Next Date Problem Test Case Tool")
    parser.add_argument('--generate', type=int, default=10, help='Number of test cases to generate')
    parser.add_argument('--upload', type=str, help='Path to uploaded test case file (CSV/XLSX)')
    parser.add_argument('--gemini', action='store_true', help='Use Gemini API to generate test cases')
    parser.add_argument('--api-key', type=str, help='Gemini API key (or set GEMINI_API_KEY in .env)')
    args = parser.parse_args()

    if args.gemini:
        api_key = args.api_key or os.environ.get('GEMINI_API_KEY')
        if not api_key:
            print("Gemini API key required. Use --api-key or set GEMINI_API_KEY in .env file.")
            return
        generated = generate_next_date_cases_gemini(api_key, args.generate)
        # Save generated test cases to CSV
        save_test_cases_to_csv(generated, 'gemini_generated_testcases.csv')
        print(f"Gemini-generated test cases saved to gemini_generated_testcases.csv")
    else:
        print("Please use --gemini to generate test cases via Gemini API.")
        return

    print(f"Generated {len(generated)} test cases.")
    for inp, out in generated:
        print(f"{inp} -> {out}")

    if args.upload:
        if not os.path.exists(args.upload):
            print(f"File not found: {args.upload}")
            return
        uploaded = read_test_file(args.upload)
        result = compare_cases(generated, uploaded)
        print("\nComparison Results:")
        print(f"Positive cases: {result['positive']}")
        print(f"Negative cases: {result['negative']}")
        print(f"Total cases checked: {result['total']}")

if __name__ == "__main__":
    main()
