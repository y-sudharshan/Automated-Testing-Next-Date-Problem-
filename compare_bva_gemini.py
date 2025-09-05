import pandas as pd
from datetime import datetime, date, timedelta

def parse_bva_file():
    """Parse the NextDate_BVA_TestCases.xlsx file to extract test cases"""
    df = pd.read_excel('NextDate_BVA_TestCases.xlsx')
    
    test_cases = []
    
    # Start from row 3 (index 3) where actual data begins
    for index, row in df.iterrows():
        if index < 3:  # Skip header rows
            continue
            
        try:
            # Extract data from the specific columns
            serial_no = row.iloc[1] if pd.notna(row.iloc[1]) else None
            day = row.iloc[2] if pd.notna(row.iloc[2]) else None
            month = row.iloc[3] if pd.notna(row.iloc[3]) else None
            year = row.iloc[4] if pd.notna(row.iloc[4]) else None
            expected = row.iloc[5] if pd.notna(row.iloc[5]) else None
            valid = row.iloc[6] if pd.notna(row.iloc[6]) else None
            
            # Skip rows without complete data
            if not all([serial_no, day, month, year, expected]):
                continue
                
            # Convert to proper format
            input_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            
            # Parse expected output
            if expected == "Invalid" or str(valid).strip().lower() == "no":
                expected_output = "INVALID"
            else:
                try:
                    # Try to parse the expected date (format: DD/MM/YYYY)
                    if "/" in str(expected):
                        parts = str(expected).split("/")
                        if len(parts) == 3:
                            exp_day, exp_month, exp_year = parts
                            expected_output = f"{int(exp_year):04d}-{int(exp_month):02d}-{int(exp_day):02d}"
                        else:
                            expected_output = "INVALID"
                    else:
                        expected_output = "INVALID"
                except:
                    expected_output = "INVALID"
            
            test_cases.append({
                'serial_no': int(serial_no),
                'input_date': input_date,
                'expected_output': expected_output,
                'day': int(day),
                'month': int(month),
                'year': int(year),
                'valid': str(valid).strip() if valid else "Unknown"
            })
            
        except Exception as e:
            continue  # Skip problematic rows
    
    return test_cases

def compare_bva_with_gemini():
    print("=== COMPARING NextDate_BVA_TestCases.xlsx WITH GEMINI GENERATED TEST CASES ===\n")
    
    # Parse BVA test cases
    try:
        bva_cases = parse_bva_file()
        print(f"Loaded BVA test cases: {len(bva_cases)} test cases")
    except FileNotFoundError:
        print("Error: NextDate_BVA_TestCases.xlsx not found")
        return
    except Exception as e:
        print(f"Error parsing BVA file: {e}")
        return
    
    # Read Gemini generated test cases
    try:
        gemini_df = pd.read_csv('gemini_generated_testcases.csv', header=None, names=['input_date', 'expected_output'])
        print(f"Loaded Gemini test cases: {len(gemini_df)} test cases\n")
    except FileNotFoundError:
        print("Error: gemini_generated_testcases.csv not found")
        return
    
    # Convert BVA cases to dictionary for easy lookup
    bva_dict = {case['input_date']: case['expected_output'] for case in bva_cases}
    
    # Convert Gemini cases to dictionary
    gemini_dict = {}
    for _, row in gemini_df.iterrows():
        input_date = row['input_date'].strip()
        expected = row['expected_output'].strip()
        if expected.upper() == "INVALID":
            expected = "INVALID"
        gemini_dict[input_date] = expected
    
    # Compare the two datasets
    positive_cases = []
    negative_cases = []
    bva_only_cases = []
    gemini_only_cases = []
    
    # Check BVA cases against Gemini
    for input_date, bva_expected in bva_dict.items():
        if input_date in gemini_dict:
            gemini_expected = gemini_dict[input_date]
            if bva_expected == gemini_expected:
                positive_cases.append({
                    'input': input_date,
                    'bva_output': bva_expected,
                    'gemini_output': gemini_expected,
                    'status': 'MATCH'
                })
            else:
                negative_cases.append({
                    'input': input_date,
                    'bva_output': bva_expected,
                    'gemini_output': gemini_expected,
                    'status': 'MISMATCH'
                })
        else:
            bva_only_cases.append({
                'input': input_date,
                'bva_output': bva_expected,
                'status': 'BVA_ONLY'
            })
    
    # Check for Gemini-only cases
    for input_date, gemini_expected in gemini_dict.items():
        if input_date not in bva_dict:
            gemini_only_cases.append({
                'input': input_date,
                'gemini_output': gemini_expected,
                'status': 'GEMINI_ONLY'
            })
    
    # Print comprehensive summary
    print("=== COMPARISON SUMMARY ===")
    print(f"Positive cases (matches): {len(positive_cases)}")
    print(f"Negative cases (mismatches): {len(negative_cases)}")
    print(f"Cases only in BVA: {len(bva_only_cases)}")
    print(f"Cases only in Gemini: {len(gemini_only_cases)}")
    print(f"Total overlapping comparisons: {len(positive_cases) + len(negative_cases)}")
    
    # Show BVA test cases details
    print(f"\n=== BVA TEST CASES DETAILS ===")
    for case in bva_cases[:10]:  # Show first 10
        print(f"TC{case['serial_no']:02d}: {case['input_date']} ({case['day']:02d}/{case['month']:02d}/{case['year']}) → {case['expected_output']} (Valid: {case['valid']})")
    
    # Show positive cases
    if positive_cases:
        print(f"\n=== POSITIVE CASES (MATCHES) ===")
        for i, case in enumerate(positive_cases):
            print(f"{i+1}. Input: {case['input']} | BVA: {case['bva_output']} | Gemini: {case['gemini_output']} | Status: {case['status']}")
    
    # Show negative cases (differences)
    if negative_cases:
        print(f"\n=== NEGATIVE CASES (DIFFERENCES) ===")
        for i, case in enumerate(negative_cases):
            print(f"{i+1}. Input: {case['input']} | BVA Expected: {case['bva_output']} | Gemini Expected: {case['gemini_output']} | Status: {case['status']}")
    else:
        print(f"\n=== NO DIFFERENCES FOUND IN OVERLAPPING CASES ===")
    
    # Show samples of unique cases
    if bva_only_cases:
        print(f"\n=== SAMPLE CASES ONLY IN BVA (showing first 5) ===")
        for i, case in enumerate(bva_only_cases[:5]):
            print(f"{i+1}. Input: {case['input']} | BVA Expected: {case['bva_output']} | Status: {case['status']}")
    
    if gemini_only_cases:
        print(f"\n=== SAMPLE CASES ONLY IN GEMINI (showing first 5) ===")
        for i, case in enumerate(gemini_only_cases[:5]):
            print(f"{i+1}. Input: {case['input']} | Gemini Expected: {case['gemini_output']} | Status: {case['status']}")
    
    # Calculate accuracy if there are overlapping cases
    total_overlapping = len(positive_cases) + len(negative_cases)
    if total_overlapping > 0:
        accuracy = (len(positive_cases) / total_overlapping) * 100
        print(f"\n=== ACCURACY METRICS ===")
        print(f"Overlap accuracy: {accuracy:.1f}% ({len(positive_cases)}/{total_overlapping})")
    
    # Save detailed results
    all_results = positive_cases + negative_cases + bva_only_cases + gemini_only_cases
    if all_results:
        results_df = pd.DataFrame(all_results)
        results_df.to_csv('bva_gemini_comparison.csv', index=False)
        print(f"\n=== DETAILED RESULTS SAVED ===")
        print("Detailed comparison saved to: bva_gemini_comparison.csv")

if __name__ == "__main__":
    compare_bva_with_gemini()
