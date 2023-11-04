########################################################################################################################

# Steps
# 1. (i) Accept Data from all the excel files , (ii) Combine them to form a single file
# 2. Perform Crowdsourcing, that is, create a file for crowdsourced labels from all the labels given
# 3. (i) Find the most prominent categories of consent and (ii) Extract most common word embeddings that occur with these categories

########################################################################################################################

import os
import openpyxl
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

output_wb = openpyxl.Workbook()
output_sheet = output_wb.active
output_sheet.title = 'Combined Data'

x = 1

##########################
#LOAD DATA
##########################
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


#############################################################################################################################################################
                                         #  CROWDSOURCING #
#############################################################################################################################################################
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

###########################################################################################################################################################
                                         #  MERGING TWO EXCEL FILES  #
###########################################################################################################################################################
file1_path = "P2-a-submission-v3.xlsx"
output_file_path = "merged_file.xlsx"

# Load the data from the first Excel file (only first two columns)
df2 = new_data.iloc[:, 0:3]

# Loading the data from the second Excel file (only first three columns)
df1 = pd.read_excel(file1_path, usecols=[0, 1])

# Merge the two dataframes
merged_df = pd.concat([df1, df2], axis=1)
print("merged df is:")
print(merged_df)
# Save the merged dataframe to a new Excel file
merged_df.to_excel(output_file_path, index=False)


############################################################################################################################################################
       #  EXTRACT COMMON WORD EMBEDDINGS FOR TOP LABELS  #
############################################################################################################################################################

nltk.download('stopwords')

# Load the merged Excel file
file_path = 'final_merged_file.xlsx'
df = pd.read_excel(file_path)


label_columns = ['First violation', 'Second violation', 'Third violation']

# Combine labels from all columns, handling NaN and empty values
all_labels = []
for column in label_columns:
    labels = df[column].dropna()
    labels = labels.apply(lambda x: x.strip() if isinstance(x, str) else "")
    all_labels.extend(labels.str.split(','))

# Create 1D Array
all_labels = [label.strip() for sublist in all_labels for label in sublist if label.strip()]

# Tokenize
label_word_frequencies = nltk.FreqDist(all_labels)

# Picking the top three most common consent labels
top_consent_labels = [label for label, count in label_word_frequencies.most_common(3)]
common_words_dict = {label: Counter() for label in top_consent_labels}


for index, row in df.iterrows():
    labels = [row[column] for column in label_columns]
    for label in labels:
        if label in top_consent_labels:
            text = row['title'] + ' ' + row['review']
            tokens = word_tokenize(text)
            tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stopwords.words('english')]
            common_words_dict[label].update(tokens)

# Printing the most common words for each top_consent_label
for label in top_consent_labels:
    common_words = common_words_dict[label].most_common(10)
    top_words = [word for word, count in common_words if word]
    print(f"{label}: {', '.join(top_words)}")







