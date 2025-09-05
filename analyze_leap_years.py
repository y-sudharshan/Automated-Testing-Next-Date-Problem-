import pandas as pd

def is_leap_year(year):
    """Check if a year is a leap year"""
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def analyze_leap_year_conditions():
    print("=== LEAP YEAR ANALYSIS IN TEST CASES ===\n")
    
    # Analyze BVA Test Cases
    print("1. ANALYZING NextDate_BVA_TestCases.xlsx")
    print("-" * 50)
    
    try:
        df_bva = pd.read_excel('NextDate_BVA_TestCases.xlsx')
        
        leap_cases = []
        non_leap_cases = []
        
        # Start from row 3 where data begins
        for i in range(3, len(df_bva)):
            try:
                day = df_bva.iloc[i, 2]
                month = df_bva.iloc[i, 3] 
                year = df_bva.iloc[i, 4]
                expected = df_bva.iloc[i, 5]
                
                if pd.notna(day) and pd.notna(month) and pd.notna(year):
                    day, month, year = int(day), int(month), int(year)
                    
                    # Focus on February cases and year boundary cases
                    if month == 2 and day >= 28:
                        if is_leap_year(year):
                            leap_cases.append({
                                'date': f'{day:02d}/{month:02d}/{year}',
                                'year': year,
                                'expected': expected,
                                'type': 'Leap year February'
                            })
                        else:
                            non_leap_cases.append({
                                'date': f'{day:02d}/{month:02d}/{year}',
                                'year': year,
                                'expected': expected,
                                'type': 'Non-leap year February'
                            })
            except:
                continue
        
        print(f"LEAP YEAR CASES FOUND: {len(leap_cases)}")
        for case in leap_cases:
            print(f"  {case['date']} → {case['expected']} ({case['type']})")
        
        print(f"\nNON-LEAP YEAR CASES FOUND: {len(non_leap_cases)}")
        for case in non_leap_cases:
            print(f"  {case['date']} → {case['expected']} ({case['type']})")
            
    except Exception as e:
        print(f"Error analyzing BVA file: {e}")
    
    # Analyze comprehensive test cases
    print(f"\n2. ANALYZING next_date_test_cases.xlsx")
    print("-" * 50)
    
    try:
        df_comprehensive = pd.read_excel('next_date_test_cases.xlsx')
        
        leap_years_found = set()
        non_leap_years_found = set()
        feb_28_cases = []
        feb_29_cases = []
        
        for _, row in df_comprehensive.iterrows():
            try:
                day = int(row['Day'])
                month = int(row['Month'])
                year = int(row['Year'])
                
                # Look for February 28 and 29 cases
                if month == 2:
                    if day == 28:
                        feb_28_cases.append({
                            'year': year,
                            'is_leap': is_leap_year(year),
                            'test_id': row['Test Case ID']
                        })
                    elif day == 29:
                        feb_29_cases.append({
                            'year': year,
                            'is_leap': is_leap_year(year),
                            'test_id': row['Test Case ID']
                        })
                
                # Collect leap and non-leap years
                if is_leap_year(year):
                    leap_years_found.add(year)
                else:
                    non_leap_years_found.add(year)
                    
            except:
                continue
        
        print(f"LEAP YEARS IN DATASET: {sorted(leap_years_found)}")
        print(f"NON-LEAP YEARS IN DATASET: {sorted(non_leap_years_found)}")
        
        print(f"\nFEBRUARY 28 TEST CASES: {len(feb_28_cases)}")
        leap_feb28 = [case for case in feb_28_cases if case['is_leap']]
        non_leap_feb28 = [case for case in feb_28_cases if not case['is_leap']]
        print(f"  Leap years (Feb 28): {len(leap_feb28)} cases")
        print(f"  Non-leap years (Feb 28): {len(non_leap_feb28)} cases")
        
        print(f"\nFEBRUARY 29 TEST CASES: {len(feb_29_cases)}")
        leap_feb29 = [case for case in feb_29_cases if case['is_leap']]
        non_leap_feb29 = [case for case in feb_29_cases if not case['is_leap']]
        print(f"  Leap years (Feb 29): {len(leap_feb29)} cases")
        print(f"  Non-leap years (Feb 29): {len(non_leap_feb29)} cases")
        
        # Show specific examples
        print(f"\nSPECIFIC EXAMPLES:")
        if leap_feb28:
            print(f"  Leap year Feb 28: {leap_feb28[0]['test_id']} (Year {leap_feb28[0]['year']})")
        if non_leap_feb28:
            print(f"  Non-leap year Feb 28: {non_leap_feb28[0]['test_id']} (Year {non_leap_feb28[0]['year']})")
        if leap_feb29:
            print(f"  Leap year Feb 29: {leap_feb29[0]['test_id']} (Year {leap_feb29[0]['year']})")
        if non_leap_feb29:
            print(f"  Non-leap year Feb 29: {non_leap_feb29[0]['test_id']} (Year {non_leap_feb29[0]['year']})")
            
    except Exception as e:
        print(f"Error analyzing comprehensive file: {e}")
    
    # Analyze Gemini generated cases
    print(f"\n3. ANALYZING gemini_generated_testcases.csv")
    print("-" * 50)
    
    try:
        df_gemini = pd.read_csv('gemini_generated_testcases.csv', header=None, names=['input_date', 'expected_output'])
        
        gemini_leap_cases = []
        gemini_non_leap_cases = []
        
        for _, row in df_gemini.iterrows():
            try:
                date_str = row['input_date'].strip()
                expected = row['expected_output'].strip()
                
                # Parse YYYY-MM-DD format
                parts = date_str.split('-')
                if len(parts) == 3:
                    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                    
                    # Look for February cases
                    if month == 2 and day >= 28:
                        if is_leap_year(year):
                            gemini_leap_cases.append(f'{date_str} → {expected} (Leap year)')
                        else:
                            gemini_non_leap_cases.append(f'{date_str} → {expected} (Non-leap year)')
            except:
                continue
        
        print(f"GEMINI LEAP YEAR CASES: {len(gemini_leap_cases)}")
        for case in gemini_leap_cases:
            print(f"  {case}")
        
        print(f"\nGEMINI NON-LEAP YEAR CASES: {len(gemini_non_leap_cases)}")
        for case in gemini_non_leap_cases:
            print(f"  {case}")
            
    except Exception as e:
        print(f"Error analyzing Gemini file: {e}")
    
    print(f"\n=== SUMMARY ===")
    print("Leap year conditions are crucial for the Next Date problem because:")
    print("1. February 28 in leap years should go to February 29")
    print("2. February 28 in non-leap years should go to March 1")
    print("3. February 29 is only valid in leap years")
    print("4. Century years (1900, 2000) have special leap year rules")

if __name__ == "__main__":
    analyze_leap_year_conditions()
