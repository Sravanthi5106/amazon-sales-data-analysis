# ==================================================
# IMPORT LIBRARY
# ==================================================
import pandas as pd

# ==================================================
# LOAD DATASET
# ==================================================
df = pd.read_csv("amazon_sales_dataset.csv")

print("========== DATA QUALITY CHECK ==========")

# Preview
print("\nFirst 5 rows:")
print(df.head())

# Info
print("\nDataset Info:")
df.info()

# Missing BEFORE
print("\nMissing Values BEFORE Cleaning:")
print(df.isnull().sum())

print("\nTotal Missing BEFORE:", df.isnull().sum().sum())

# Duplicates BEFORE
print("\nDuplicates BEFORE:", df.duplicated().sum())

# ==================================================
# DATA CLEANING
# ==================================================

print("\n========== DATA CLEANING ==========")

df_clean = df.copy()

# -----------------------------
# 1. FIX DATE COLUMN
# -----------------------------
df_clean['order_date'] = pd.to_datetime(df_clean['order_date'], errors='coerce')

# Fill missing dates completely
df_clean['order_date'] = df_clean['order_date'].ffill().bfill()

# -----------------------------
# 2. HANDLE MISSING VALUES
# -----------------------------
df_clean = df_clean.ffill().bfill()

# -----------------------------
# 3. REMOVE DUPLICATES
# -----------------------------
df_clean = df_clean.drop_duplicates()

# -----------------------------
# 4. REMOVE INVALID VALUES
# -----------------------------
numeric_columns = ['price', 'discount_percent', 'discounted_price',
                   'quantity_sold', 'total_revenue', 'rating', 'review_count']

for col in numeric_columns:
    if col in df_clean.columns:
        df_clean = df_clean[df_clean[col] >= 0]

# -----------------------------
# 5. VALIDATE REVENUE
# -----------------------------
df_clean['total_revenue'] = df_clean['discounted_price'] * df_clean['quantity_sold']

# -----------------------------
# 6. FEATURE ENGINEERING
# -----------------------------
df_clean['month'] = df_clean['order_date'].dt.month
df_clean['year'] = df_clean['order_date'].dt.year

# FIXED bins (no missing issue)
df_clean['discount_level'] = pd.cut(
    df_clean['discount_percent'],
    bins=[-1, 10, 30, 100],
    labels=['Low', 'Medium', 'High']
)

# -----------------------------
# 7. FINAL CHECK
# -----------------------------
print("\n========== FINAL RESULTS ==========")

print(f"Rows BEFORE: {df.shape[0]}")
print(f"Rows AFTER: {df_clean.shape[0]}")

print("\nMissing AFTER Cleaning:")
print(df_clean.isnull().sum())

print("\nTotal Missing AFTER:", df_clean.isnull().sum().sum())

print("\nDuplicates AFTER:", df_clean.duplicated().sum())

# -----------------------------
# 8. SAVE FILE
# -----------------------------
df_clean.to_csv("cleaned_amazon_sales_dataset.csv", index=False)

print("\nCleaned dataset saved successfully!")