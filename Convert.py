# Use this to convert .xlsx files to .csv for convenience

import pandas as pd

file = pd.read_excel("Input.xlsx")
file.to_csv("Input.csv", index=False)

file = pd.read_excel("Output Data Structure.xlsx")
file.to_csv("Output Data Structure.csv", index=False)
