import pandas as pd
from datetime import date, timedelta

# Function to compute next date safely
def get_next_date(d, m, y):
    try:
        current_date = date(y, m, d)
        next_date = current_date + timedelta(days=1)
        return next_date.strftime("%d-%m-%Y")
    except ValueError:
        return "Invalid Date"

# === Main Program ===
def fill_actual_results(input_file, output_file):
    # Load the Excel file
    df = pd.read_excel(input_file)

    for i in range(len(df)):
        # Extract Day, Month, Year from columns
        d = int(df.loc[i, "Day"])
        m = int(df.loc[i, "Month"])
        y = int(df.loc[i, "Year"])

        # Compute actual output
        actual = get_next_date(d, m, y)
        df.loc[i, "Actual Output"] = actual

        # Compare with expected (if Expected Output column exists)
        if "Expected Output" in df.columns:
            if str(df.loc[i, "Expected Output"]).strip() == actual.strip():
                df.loc[i, "Result (Pass/Fail)"] = "Pass"
            else:
                df.loc[i, "Result (Pass/Fail)"] = "Fail"
        else:
            # If no expected output column, just mark as computed
            df.loc[i, "Result (Pass/Fail)"] = "Computed"

    # Save updated Excel
    df.to_excel(output_file, index=False)
    print(f"Updated file saved as: {output_file}")


# === Run Example ===
# Replace file names with your actual file paths
if __name__ == "__main__":
    input_file = "next_date_test_cases.xlsx"        # your existing file
    output_file = "next_date_final_with_results.xlsx"     # new file with results
    fill_actual_results(input_file, output_file)
