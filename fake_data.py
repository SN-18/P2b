
############################################################################################################################
                                                            # LOAD DATA #
############################################################################################################################
import os
import pandas as pd
from scipy.stats import mannwhitneyu
from sklearn.preprocessing import LabelEncoder

folder = r"C:\Users\nanda\Desktop\P2b\Pb2\P2a_Labels"
directory_path = folder

# List all files in the directory
file_paths = [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith('.xlsx')]

# Initialize a list to store potential fake files
potential_fake_files = []

# Initialize a label encoder
label_encoder = LabelEncoder()

# Process the data from the Excel files
for file_path in file_paths:
    try:
        data = pd.read_excel(file_path)

        if not all(col in data.columns for col in ['First violation', 'Second violation', 'Third violation']):
            continue

        violation_columns = ['First violation', 'Second violation', 'Third violation']

        #Processing to numerical values from string labels
        for col in violation_columns:
            data[col] = label_encoder.fit_transform(data[col])

#########################################################################################################################
                                      #  PERFORM THE MANN-Whitney U Test  #
#########################################################################################################################


        u_stat, p_value = mannwhitneyu(data['First violation'], data['Second violation'])


        significance_level = 0.1

        if p_value < significance_level:
            potential_fake_files.append(file_path)
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")
        continue


print("Potential fake files:")
for file in potential_fake_files:
    print(file)
