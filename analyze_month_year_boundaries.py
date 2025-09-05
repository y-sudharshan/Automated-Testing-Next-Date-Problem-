import pandas as pd

def analyze_month_year_boundaries():
    print("=== MONTH AND YEAR BOUNDARY ANALYSIS ===\n")
    
    # Days in each month (non-leap year)
    days_in_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 
                     7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def get_max_day(month, year):
        if month == 2 and is_leap_year(year):
            return 29
        return days_in_month.get(month, 30)
    
    # Analyze BVA Test Cases
    print("1. ANALYZING NextDate_BVA_TestCases.xlsx")
    print("-" * 50)
    
    try:
        df_bva = pd.read_excel('NextDate_BVA_TestCases.xlsx')
        
        year_boundaries = []
        month_boundaries = []
        
        for i in range(3, len(df_bva)):
            try:
                day = df_bva.iloc[i, 2]
                month = df_bva.iloc[i, 3] 
                year = df_bva.iloc[i, 4]
                expected = df_bva.iloc[i, 5]
                
                if pd.notna(day) and pd.notna(month) and pd.notna(year):
                    day, month, year = int(day), int(month), int(year)
                    
                    # Check for December 31 (year boundary)
                    if month == 12 and day == 31:
                        year_boundaries.append({
                            'date': f'{day:02d}/{month:02d}/{year}',
                            'expected': expected,
                            'type': 'Year boundary (Dec 31)'
                        })
                    
                    # Check for month-end boundaries
                    max_day = get_max_day(month, year)
                    if day == max_day:
                        month_boundaries.append({
                            'date': f'{day:02d}/{month:02d}/{year}',
                            'expected': expected,
                            'type': f'Month-end boundary (last day of month {month})'
                        })
            except:
                continue
        
        print(f"YEAR BOUNDARIES (Dec 31): {len(year_boundaries)}")
        for case in year_boundaries:
            print(f"  {case['date']} → {case['expected']} ({case['type']})")
        
        print(f"\nMONTH-END BOUNDARIES: {len(month_boundaries)}")
        for case in month_boundaries:
            print(f"  {case['date']} → {case['expected']} ({case['type']})")
            
    except Exception as e:
        print(f"Error analyzing BVA file: {e}")
    
    # Analyze comprehensive test cases
    print(f"\n2. ANALYZING next_date_test_cases.xlsx")
    print("-" * 50)
    
    try:
        df_comprehensive = pd.read_excel('next_date_test_cases.xlsx')
        
        dec_31_cases = []
        month_end_cases = []
        year_transitions = set()
        
        for _, row in df_comprehensive.iterrows():
            try:
                day = int(row['Day'])
                month = int(row['Month'])
                year = int(row['Year'])
                test_id = row['Test Case ID']
                
                # Check for December 31
                if month == 12 and day == 31:
                    dec_31_cases.append({
                        'test_id': test_id,
                        'year': year,
                        'date': f'{day:02d}/{month:02d}/{year}'
                    })
                    year_transitions.add(f'{year} → {year+1}')
                
                # Check for month-end cases
                max_day = get_max_day(month, year)
                if day == max_day:
                    month_end_cases.append({
                        'test_id': test_id,
                        'month': month,
                        'year': year,
                        'date': f'{day:02d}/{month:02d}/{year}'
                    })
                    
            except:
                continue
        
        print(f"DECEMBER 31 CASES: {len(dec_31_cases)}")
        for case in dec_31_cases:
            print(f"  {case['test_id']}: {case['date']} (Year {case['year']} → {case['year']+1})")
        
        print(f"\nMONTH-END CASES BY MONTH:")
        months_with_endings = {}
        for case in month_end_cases:
            month_name = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                         7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}[case['month']]
            if month_name not in months_with_endings:
                months_with_endings[month_name] = []
            months_with_endings[month_name].append(case)
        
        for month, cases in sorted(months_with_endings.items()):
            print(f"  {month}: {len(cases)} cases")
            for case in cases[:3]:  # Show first 3 examples
                print(f"    {case['test_id']}: {case['date']}")
            if len(cases) > 3:
                print(f"    ... and {len(cases)-3} more")
        
        print(f"\nYEAR TRANSITIONS: {len(year_transitions)}")
        for transition in sorted(year_transitions):
            print(f"  {transition}")
            
    except Exception as e:
        print(f"Error analyzing comprehensive file: {e}")
    
    # Analyze Gemini generated cases
    print(f"\n3. ANALYZING gemini_generated_testcases.csv")
    print("-" * 50)
    
    try:
        df_gemini = pd.read_csv('gemini_generated_testcases.csv', header=None, names=['input_date', 'expected_output'])
        
        gemini_dec31_cases = []
        gemini_month_ends = []
        
        for _, row in df_gemini.iterrows():
            try:
                date_str = row['input_date'].strip()
                expected = row['expected_output'].strip()
                
                # Parse YYYY-MM-DD format
                parts = date_str.split('-')
                if len(parts) == 3:
                    year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                    
                    # Check for December 31
                    if month == 12 and day == 31:
                        gemini_dec31_cases.append(f'{date_str} → {expected} (Year {year} → {year+1})')
                    
                    # Check for month-end cases
                    max_day = get_max_day(month, year)
                    if day == max_day:
                        month_name = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
                                     7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}[month]
                        gemini_month_ends.append(f'{date_str} → {expected} ({month_name} month-end)')
            except:
                continue
        
        print(f"GEMINI DECEMBER 31 CASES: {len(gemini_dec31_cases)}")
        for case in gemini_dec31_cases:
            print(f"  {case}")
        
        print(f"\nGEMINI MONTH-END CASES: {len(gemini_month_ends)}")
        for case in gemini_month_ends:
            print(f"  {case}")
            
    except Exception as e:
        print(f"Error analyzing Gemini file: {e}")
    
    print(f"\n=== BOUNDARY CONDITIONS SUMMARY ===")
    print("Critical month/year boundaries for Next Date problem:")
    print("1. December 31 → January 1 (year rollover)")
    print("2. Month-end → Next month's 1st (month rollover)")
    print("3. February 28/29 → March 1 (or Feb 29 in leap years)")
    print("4. 30-day months (Apr, Jun, Sep, Nov) → Next month")
    print("5. 31-day months → Next month")

if __name__ == "__main__":
    analyze_month_year_boundaries()
