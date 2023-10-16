import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Loading the Excel dataset
input_file = 'input_dataset.xlsx'
output_file = 'output_dataset-1.xlsx'

df = pd.read_excel(input_file, engine='openpyxl')

# 1A. Initial Data Exploration
attribute_types = {
    'SK_ID_CURR': 'numeric',
    'TARGET': 'categorical',
    'NAME_CONTRACT_TYPE': 'categorical',
    'CODE_GENDER': 'categorical',
    'FLAG_OWN_CAR': 'categorical',
    'FLAG_OWN_REALTY': 'categorical',
    'CNT_CHILDREN': 'numeric',
    'AMT_INCOME_TOTAL': 'numeric',
    'AMT_CREDIT': 'numeric',
    'AMT_ANNUITY': 'numeric',
    'AMT_GOODS_PRICE': 'numeric',
}

# Select 20 relevant attributes
relevant_attributes = [
    'SK_ID_CURR',
    'TARGET',
    'NAME_CONTRACT_TYPE',
    'CODE_GENDER',
    'FLAG_OWN_CAR',
    'FLAG_OWN_REALTY',
    'CNT_CHILDREN',
    'AMT_INCOME_TOTAL',
    'AMT_CREDIT',
    'AMT_ANNUITY',
    'AMT_GOODS_PRICE',
]

attribute_summaries = {}
for attr in relevant_attributes:
    if attribute_types[attr] == 'numeric':
        summary = df[attr].describe()
    elif attribute_types[attr] == 'categorical':
        summary = df[attr].value_counts()
    attribute_summaries[attr] = summary

# 1B. Data Preprocessing
# 1. Binning Techniques
# binning techniques to relevant attributes
df['DAYS_EMPLOYED_EQ_WIDTH'] = pd.cut(df['DAYS_EMPLOYED'], bins=5, labels=False)
print("Equi-width binning for 'DAYS_EMPLOYED' completed. Result stored in 'DAYS_EMPLOYED_EQ_WIDTH' column.")

# Equi-depth binning for 'DAYS_ID_PUBLISH'
df['DAYS_ID_PUBLISH_EQ_DEPTH'] = pd.qcut(df['DAYS_ID_PUBLISH'], q=5, labels=False)
print("Equi-depth binning for 'DAYS_ID_PUBLISH' completed. Result stored in 'DAYS_ID_PUBLISH_EQ_DEPTH' column.")

# 2. Normalization
# normalization techniques to relevant attributes
scaler = MinMaxScaler()
df['AMT_INCOME_TOTAL_MINMAX'] = scaler.fit_transform(df[['AMT_INCOME_TOTAL']])
print("Min-Max Normalization for 'AMT_INCOME_TOTAL' completed. Result stored in 'AMT_INCOME_TOTAL_MINMAX' column.")

mean_credit = df['AMT_CREDIT'].mean()
std_credit = df['AMT_CREDIT'].std()
df['AMT_CREDIT_Z_SCORE'] = (df['AMT_CREDIT'] - mean_credit) / std_credit
print("Z-score Normalization for 'AMT_CREDIT' completed. Result stored in 'AMT_CREDIT_Z_SCORE' column.")

# 3. Discretization
# Discretize relevant attributes into categories
df['AGE_CATEGORY'] = pd.cut(df['DAYS_BIRTH'], bins=[-10000, 0, 10000, 20000], labels=['Young Adults', 'Adults', 'Elderlies'])
print("Discretization for 'DAYS_BIRTH' into age categories completed. Result stored in 'AGE_CATEGORY' column.")

# 4. Binarization
# Binarize relevant categorical attributes
df['CODE_GENDER_BINARIZED'] = df['CODE_GENDER'].map({'F': 0, 'M': 1})
print("Binarization for 'CODE_GENDER' completed. Result stored in 'CODE_GENDER_BINARIZED' column.")


# Save the preprocessed data to a new Excel file
df.to_excel(output_file, index=False, engine='openpyxl')

print("Data preprocessing completed. Results saved to", output_file)
