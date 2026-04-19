# Assign Lab 2: Data Preprocessing and Exploration

## Overview
Based on the instruction diagram (`Assign-2.jpeg`) and the provided Python script (`preprocessing_lab.py`), Lab 2 is titled **"Practical Lab - 2 Data Engineering with Python"**. Its main goal is to teach you how to prepare real-world data for analysis and eventually machine learning models. 

The lab is divided into two primary sections according to the instruction diagram:
1. **Data Preprocessing and Exploration** (The part you currently have code for)
2. **Machine Learning oriented lab exercises** (Future classification/prediction tasks)

---

## What We Do in this Lab (The Code)

The `preprocessing_lab.py` script focuses exactly on Part I of the lab sheet. It processes a dataset named `patient_consent.csv` through four main steps:

### 1. Loading & Displaying Data
- **Objective:** Read the raw data file and understand its structure.
- **What the code does:** It uses `pd.read_csv()` to load `patient_consent.csv` into a Pandas DataFrame. It then prints the first 5 rows, data types (`df.info()`), and summary statistics (`df.describe()`).

### 2. Handling Missing Data
- **Objective:** Identify and fix gaps in the dataset (NaN / Null values).
- **What the code does:** It counts the missing values. If there are any missing numeric values, it imputes (fills) them using the **mean** (average) of that column.

### 3. Handling Categorical Data
- **Objective:** Convert non-numeric or special-format data into a format suitable for modeling.
- **What the code does:** 
  - It converts the `timestamp` string column into proper Datetime objects so Python understands the dates and times.
  - It applies **One-Hot Encoding** using `pd.get_dummies()` to the categorical target column `study_id`. This turns categories into binary columns (1s and 0s), which is a crucial step before feeding data into a machine learning algorithm.

### 4. Data Visualization & EDA (Exploratory Data Analysis)
- **Objective:** Analyze patterns and relationships visually to better understand the data.
- **What the code does:**
  - **Histograms:** Generates bar-like charts for each numeric column to show the distribution/frequency of data points.
  - **Correlation Heatmap:** Computes a correlation matrix to see how different numeric features are related to each other and maps it onto a color-coded grid using Seaborn.

#### Understanding `Histogram.png`
The histogram image displays the frequency distribution for all the different numeric columns in the dataset. 
- You can see how many times a given value appears. For example, columns like `demographics`, `clinical_info`, `family_history`, etc., appear to be categorical/binary flags (0 or 1). The histogram shows that almost all values for `clinical_info` are 1, while `mental_health` has a nearly equal split of 0s and 1s.
- Continuous or multi-valued columns like `patient_id` and `timestamp` have their ranges spread across the X-axis, telling you the volume of patients recorded across different IDs or times.

#### Understanding `HeatMap.png`
The heatmap visually represents the correlation matrix between the dataset's numerical columns ranging from -1 to 1.
- **Red squares (e.g., closer to 1.0):** Indicate a strong *positive* correlation. For instance, `patient_id` and `study_id` have a correlation of 0.78, which means as the patient ID goes up, the study ID tends to go up. Another high correlation is `genetic` and `sexual_reproductive` (0.60).
- **Blue squares (e.g., closer to -1.0):** Indicate a *negative* correlation. For example, `biospecimen` has a -0.31 correlation with `study_id` (so as one increases, the other tends to decrease).
- **White/Light blocks (closer to 0):** This means there is little to no linear relationship between those specific features.

---

## What We Do in this Assignment (Lab Tasks)
To complete your lab assignment, you are expected to do the following based on the instructions:
1. **Run the Preprocessing Script:** Execute `preprocessing_lab.py`. This covers the "Data Preprocessing and Exploration" half of the lab instruction sheet. It will read the `patient_consent.csv` data, fill in missing values, handle categorical columns, and output the visualizations you see in `Histogram.png` and `HeatMap.png`.
2. **Move on to Machine Learning Models:** After data preprocessing, the instruction sheet has a second part called "Machine Learning oriented lab exercises". As your next task in this assignment, you must write Python code to achieve the following:
   - Build a classification model on the **Iris Dataset** using Scikit-Learn (to classify flower species).
   - Build a predictive model on the **Titanic Dataset** (to predict passenger survival) using Logistic Regression or Random Forest.
