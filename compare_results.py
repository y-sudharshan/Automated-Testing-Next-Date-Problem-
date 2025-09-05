import pandas as pd
from datetime import datetime

def compare_results():
    print("=== COMPARING FINAL RESULTS WITH GEMINI GENERATED TEST CASES ===\n")
    
    # Read the final results (Excel)
    try:
        final_results = pd.read_excel('next_date_final_with_results.xlsx')
        print(f"Loaded final results: {len(final_results)} test cases")
    except FileNotFoundError:
        print("Error: next_date_final_with_results.xlsx not found")
        return
    
    # Read Gemini generated test cases (CSV)
    try:
        gemini_cases = pd.read_csv('gemini_generated_testcases.csv', header=None, names=['input_date', 'expected_output'])
        print(f"Loaded Gemini test cases: {len(gemini_cases)} test cases\n")
    except FileNotFoundError:
        print("Error: gemini_generated_testcases.csv not found")
        return
    
    # Convert final results to comparable format
    final_dict = {}
    for _, row in final_results.iterrows():
        day, month, year = int(row['Day']), int(row['Month']), int(row['Year'])
        input_date = f"{year:04d}-{month:02d}-{day:02d}"
        
        # Convert actual output to YYYY-MM-DD format or keep as "Invalid Date"
        actual_output = row['Actual Output']
        if actual_output != "Invalid Date":
            try:
                # Parse DD-MM-YYYY format and convert to YYYY-MM-DD
                parsed_date = datetime.strptime(actual_output, "%d-%m-%Y")
                actual_output = parsed_date.strftime("%Y-%m-%d")
            except:
                actual_output = "Invalid Date"
        
        final_dict[input_date] = actual_output
    
    # Compare with Gemini results
    positive_cases = []
    negative_cases = []
    gemini_only_cases = []
    final_only_cases = []
    
    # Check Gemini cases against final results
    for _, row in gemini_cases.iterrows():
        gemini_input = row['input_date'].strip()
        gemini_expected = row['expected_output'].strip()
        
        if gemini_input in final_dict:
            final_output = final_dict[gemini_input]
            if final_output == gemini_expected or (final_output == "Invalid Date" and gemini_expected.upper() == "INVALID"):
                positive_cases.append({
                    'input': gemini_input,
                    'gemini_output': gemini_expected,
                    'final_output': final_output,
                    'status': 'MATCH'
                })
            else:
                negative_cases.append({
                    'input': gemini_input,
                    'gemini_output': gemini_expected,
                    'final_output': final_output,
                    'status': 'MISMATCH'
                })
        else:
            gemini_only_cases.append({
                'input': gemini_input,
                'gemini_output': gemini_expected,
                'status': 'GEMINI_ONLY'
            })
    
    # Check for cases only in final results
    for input_date, final_output in final_dict.items():
        gemini_inputs = set(gemini_cases['input_date'].str.strip())
        if input_date not in gemini_inputs:
            final_only_cases.append({
                'input': input_date,
                'final_output': final_output,
                'status': 'FINAL_ONLY'
            })
    
    # Print summary
    print("=== COMPARISON SUMMARY ===")
    print(f"Positive cases (matches): {len(positive_cases)}")
    print(f"Negative cases (mismatches): {len(negative_cases)}")
    print(f"Cases only in Gemini: {len(gemini_only_cases)}")
    print(f"Cases only in Final results: {len(final_only_cases)}")
    print(f"Total comparisons made: {len(positive_cases) + len(negative_cases)}")
    
    # Show sample positive cases
    if positive_cases:
        print(f"\n=== SAMPLE POSITIVE CASES (showing first 5) ===")
        for i, case in enumerate(positive_cases[:5]):
            print(f"{i+1}. Input: {case['input']} | Expected: {case['gemini_output']} | Actual: {case['final_output']} | Status: {case['status']}")
    
    # Show all negative cases (differences)
    if negative_cases:
        print(f"\n=== ALL NEGATIVE CASES (DIFFERENCES) ===")
        for i, case in enumerate(negative_cases):
            print(f"{i+1}. Input: {case['input']} | Gemini Expected: {case['gemini_output']} | Final Actual: {case['final_output']} | Status: {case['status']}")
    else:
        print(f"\n=== NO DIFFERENCES FOUND ===")
    
    # Show sample cases only in one dataset
    if gemini_only_cases:
        print(f"\n=== SAMPLE CASES ONLY IN GEMINI (showing first 5) ===")
        for i, case in enumerate(gemini_only_cases[:5]):
            print(f"{i+1}. Input: {case['input']} | Expected: {case['gemini_output']} | Status: {case['status']}")
    
    if final_only_cases:
        print(f"\n=== SAMPLE CASES ONLY IN FINAL RESULTS (showing first 5) ===")
        for i, case in enumerate(final_only_cases[:5]):
            print(f"{i+1}. Input: {case['input']} | Actual: {case['final_output']} | Status: {case['status']}")
    
    # Save detailed comparison to file
    all_comparisons = positive_cases + negative_cases + gemini_only_cases + final_only_cases
    if all_comparisons:
        comparison_df = pd.DataFrame(all_comparisons)
        comparison_df.to_csv('detailed_comparison_results.csv', index=False)
        print(f"\n=== DETAILED COMPARISON SAVED ===")
        print("Detailed comparison saved to: detailed_comparison_results.csv")

if __name__ == "__main__":
    compare_results()
