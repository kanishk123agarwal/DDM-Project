# Assignment Lab 3: An Easy-to-Understand Guide

Lab 3 is all about **Machine Learning (ML)**. By using a dataset of patient consent forms, we apply Machine Learning to uncover patterns, make predictions, and group similar patients. 

Think of Lab 3 as a factory with a **pipeline** that takes raw data on one end and outputs smart insights on the other.

This Lab is divided into 4 main steps (each handled by a different Python script).

---

## 1. Data Preprocessing (`consent_preprocessing.py`)
*The "Cleaning and Prep" step.*

Before we can teach a computer to learn from data, we have to clean the data and format it properly.
- **What it does:** It loads the raw `patient_consent.csv` file. It removes any duplicate entries (if a patient filled out the form twice, we keep the newest one).
- **Feature Engineering:** It creates new, helpful columns (features). For example, it counts how many things a patient consented to and calculates a `"privacy_score"`.
- **Getting Ready for ML:** It splits the data into two parts: one part to *train* the machine learning models, and another part to *test* how well they learned.

## 2. Machine Learning Models (`consent_ml_models.py`)
*The "Brain" step.*

This is where the actual learning happens. We use three different types of Artificial Intelligence models to look at the cleaned data:

1. **K-Means Clustering:** 
   - *Goal:* Grouping patients without knowing the "right" answer.
   - *How it works:* It looks closely at all patients and groups them into 3 buckets based on similarities in their consent behavior (e.g., "Open Sharers", "Selective Sharers").
2. **Random Forest Classifier:** 
   - *Goal:* Predicting a specific outcome.
   - *How it works:* It acts like a large group of decision trees. We ask it to predict whether a patient will consent to sharing their demographic data based on their other answers.
3. **Logistic Regression:**
   - *Goal:* Estimating probability.
   - *How it works:* We use it to predict the *overall likelihood* (high or low) that a patient will consent.

## 3. Analysis & Visualisation (`consent_analysis.py`)
*The "Reporting and Charts" step.*

Looking at raw numbers is hard. This script turns the complex results from the ML models into easy-to-read charts and reports.
- **What it creates:** It generates colorful heatmaps, bar charts showing how consents are distributed, a scatter plot showing the patient clusters, and "confusion matrices" that grade how well our predictive models performed.
- **Why it matters:** It provides the visual proof of what the AI discovered.

## 4. The Orchestrator (`main.py`)
*The "Manager" step.*

Instead of you manually running the first three scripts one by one, `main.py` is the boss that runs the whole show.
- **What it does:** When you run `main.py`, it automatically calls Step 1 to clean the data, then passes it to Step 2 to train the models, and finally passes the results to Step 3 to draw the charts. 
- **The Output:** It prints a nice summary on your screen telling you exactly what was accomplished and how accurate the AI predictions were!
