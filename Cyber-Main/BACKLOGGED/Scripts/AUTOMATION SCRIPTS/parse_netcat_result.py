# Add the path to the file in the variable file_input.
# Output will be the file_input + "_output.csv"

import pandas as pd

file_input = ''
file_output = file_input + '_output.csv'
cols = ['Aunonomous_System_Number', 'IP_Address', 'BGP_Prefix', 'Country_Code', 'Date_Allocated', 'Aunonomous_System_Name']
df = pd.read_csv(file_input, sep='|', skiprows=[0], header=None, names=cols, index_col=False)

for col in df.columns[1:]:
    df[col] = df[col].str.strip()
df.to_csv(file_output, index=False)
