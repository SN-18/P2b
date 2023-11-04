########################################################################################################################
#Working code, working inside of a copy of github repo, another copy exists by the name of P2b on desktop
import os
import openpyxl
import pandas as pd

output_wb = openpyxl.Workbook()
output_sheet = output_wb.active
output_sheet.title = 'Combined Data'

x = 1

#LOAD DATA
folder = r"P2a_Labels"
output_file = "combined_scores"

combined_data = pd.DataFrame()
for filename in os.listdir(folder):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder, filename)
        sheet_name = "Sheet1"

        # Ignore unformatted files
        try:
            data = pd.read_excel(file_path)
            if 'title' in data.columns and 'review' in data.columns:
                # Combine Data
                combined_data = pd.concat([combined_data, data.drop(['title', 'review'], axis=1)], axis=1, ignore_index=True)

                for row in data.iterrows():
                    for i, value in enumerate(row[1]):
                        output_sheet.cell(row=x, column=i + 1, value=value)

                    x += 1
            else:
                print(f"Skipping file {filename} because it doesn't have 'title' and 'review' columns.")

        # Report unformatted files, and continue
        except Exception as e:
            print(f"Error reading file {filename}: {str(e)}")

output_wb.save(output_file)
print(combined_data)



# Crowdsourcing
combined_data = combined_data.dropna(axis=1, how='all')
def most_common_violations(row):
    violations = [violation for violation in row if not pd.isna(violation)]
    if not violations:
        return None

    violations_count = {}
    for violation in violations:
        if violation in violations_count:
            violations_count[violation] += 1
        else:
            violations_count[violation] = 1

    sorted_violations = sorted(violations_count, key=violations_count.get, reverse=True)

    if len(sorted_violations) > 2:
        return [sorted_violations[0], sorted_violations[1], sorted_violations[2]]
    elif len(sorted_violations) > 1:
        return [sorted_violations[0], sorted_violations[1], None]
    elif sorted_violations:
        return [sorted_violations[0], None, None]
    else:
        return [None, None, None]


new_data = combined_data.apply(most_common_violations, axis=1, result_type='expand')
new_data.columns = ['First violation', 'Second violation', 'Third violation']

# Overflow check
if new_data.shape[0] > 2500:
    new_data = new_data.iloc[:2500, :]

print(new_data)
new_data.to_excel('condensed_violations.xlsx', index=False)

###########################################################################################################################
#merging two excel files
import pandas as pd



file1_path = "P2-a-submission-v3.xlsx"
output_file_path = "merged_file.xlsx"

# Load the data from the first Excel file (only first two columns)
df2 = new_data.iloc[:, 0:3]

# Load the data from the second Excel file (only first three columns)
df1 = pd.read_excel(file1_path, usecols=[0, 1])

# Merge the two dataframes
merged_df = pd.concat([df1, df2], axis=1)
print("merged df is:")
print(merged_df)
# Save the merged dataframe to a new Excel file
merged_df.to_excel(output_file_path, index=False)



















