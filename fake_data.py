

folder=r"\P2a_Labels"
# output_file=r"C:\Users\nanda\Desktop\DAI\P2b\combined_scores"
output_file = "combined_scores_1"
########################################################################################################################
#Working code for kohen's kappa
import os
import openpyxl
import pandas as pd

folder = r"C:\Users\nanda\Desktop\DAI\P2b\P2a_Labels"
output_file = r"C:\Users\nanda\Desktop\DAI\P2b\combined_scores.xlsx"

output_wb = openpyxl.Workbook()
output_sheet = output_wb.active
output_sheet.title = 'Combined Data'

x = 1  
y = 1  

for filename in os.listdir(folder):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder, filename)
        sheet_name = "Sheet1"

        data = pd.read_excel(file_path)

        for row in data.iterrows():
            fake_data_detected = False  # Initialize a flag for fake data detection
            for i, value in enumerate(row[1]):
                output_sheet.cell(row=x, column=i + 1, value=value)

                # Example rule for fake data detection: Check if the cell contains the word "fake"
                if isinstance(value, str) and "fake" in value.lower():
                    fake_data_detected = True
            x = x + 1

            # If fake data is detected, you can report the file that contains fake data
            if fake_data_detected:
                print(f"Fake data detected in file: {filename}")
output_wb.save(output_file)

