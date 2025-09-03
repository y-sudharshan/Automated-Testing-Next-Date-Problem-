import pandas as pd

# Read the results file
df = pd.read_excel('next_date_final_with_results.xlsx')

print("=== NEXT DATE TEST RESULTS SUMMARY ===")
print(f"Total test cases: {len(df)}")
print(f"Valid dates (computed): {len(df[df['Actual Output'] != 'Invalid Date'])}")
print(f"Invalid dates: {len(df[df['Actual Output'] == 'Invalid Date'])}")

print("\n=== SAMPLE RESULTS ===")
print(df[['Test Case ID', 'testing', 'Day', 'Month', 'Year', 'Actual Output', 'Result (Pass/Fail)']].head(10).to_string())

print("\n=== INVALID DATE EXAMPLES ===")
invalid_cases = df[df['Actual Output'] == 'Invalid Date'].head(5)
print(invalid_cases[['Test Case ID', 'Day', 'Month', 'Year', 'Actual Output']].to_string())

print("\n=== VALID DATE EXAMPLES ===")
valid_cases = df[df['Actual Output'] != 'Invalid Date'].head(5)
print(valid_cases[['Test Case ID', 'Day', 'Month', 'Year', 'Actual Output']].to_string())
