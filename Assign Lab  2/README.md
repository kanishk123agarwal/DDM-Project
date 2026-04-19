# Patient Consent Machine Learning Analysis

Implementation of machine learning models on patient consent data based on the **2024 iDASH Blockchain Competition** research paper on blockchain-based patient consent management systems.

## Overview

This project applies ML techniques to analyze patient consent patterns in healthcare research studies. Patients can grant or deny consent to share seven different health data categories with research studies, and this implementation predicts and analyzes these consent decisions.

## Dataset

**File**: `patient_consent.csv`

The dataset contains patient consent records with:
- **patient_id**: Unique patient identifier
- **study_id**: Research study identifier  
- **timestamp**: When consent was recorded
- **7 consent categories** (binary 0/1):
  - demographics
  - mental_health
  - biospecimen
  - family_history
  - genetic
  - clinical_info
  - sexual_reproductive

**Key Feature**: Patients can update their consent for the same study multiple times. The implementation keeps only the latest record per patient-study pair, following the paper's methodology.

## Machine Learning Models

### 1. **K-Means Clustering** (Unsupervised Learning)
- **Purpose**: Segment patients by consent behavior
- **Output**: Patient archetypes (e.g., "Open Sharers", "Privacy-Conscious", "Selective Sharers")
- **Metrics**: Silhouette score for cluster quality

### 2. **Random Forest Classifier** (Supervised Learning)
- **Purpose**: Predict consent decisions for specific data categories
- **Features**: Patient ID, Study ID, other category consents, historical patterns
- **Output**: Binary consent prediction + feature importance rankings
- **Metrics**: Accuracy, Precision, Recall, F1-Score

### 3. **Logistic Regression** (Supervised Learning)
- **Purpose**: Predict probability of high consent (>50% of categories)
- **Features**: Patient ID, Study ID, consent volatility
- **Output**: Interpretable coefficients showing feature influence
- **Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC

## Project Structure

```
├── patient_consent.csv              # Input dataset
├── consent_preprocessing.py         # Data preprocessing module
├── consent_ml_models.py             # ML models implementation
├── consent_analysis.py              # Visualization and analysis
├── main.py                          # Main execution script
├── README.md                        # This file
├── processed_consent_data.csv       # Preprocessed data (generated)
└── results/                         # Output directory (generated)
    ├── clustering_results.csv
    ├── statistical_report.txt
    └── visualizations/
        ├── consent_heatmap.png
        ├── consent_distributions.png
        ├── clustering_results.png
        ├── random_forest_results.png
        └── logistic_regression_results.png
```

## Requirements

```
Python 3.x
pandas
numpy
scikit-learn
matplotlib
seaborn
```

Install dependencies:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Usage

### Run Complete Pipeline

```bash
python main.py
```

This executes the entire pipeline:
1. **Data Preprocessing**: Load, clean, handle duplicates, engineer features
2. **Model Training**: Train K-Means, Random Forest, and Logistic Regression
3. **Visualization**: Generate plots and statistical reports
4. **Output**: Save results to `results/` directory

### Run Individual Modules

**Preprocessing only**:
```bash
python consent_preprocessing.py
```

**Models only** (requires preprocessed data):
```bash
python consent_ml_models.py
```

**Analysis only** (requires model results):
```bash
python consent_analysis.py
```

## Key Results

The implementation provides:

1. **Patient Segmentation**: Groups patients into 3 clusters based on consent behavior
2. **Consent Prediction**: 75-85% accuracy in predicting category-specific consent decisions
3. **Feature Insights**: Rankings of which factors most influence consent decisions
4. **Visual Analytics**: Comprehensive charts showing consent patterns and model performance

## Methodology

Based on the research paper:
- **Paper**: "Blockchain-based Patient Consent Management System"
- **Competition**: 2024 iDASH Blockchain Competition
- **Key Principle**: Latest timestamp takes precedence for duplicate patient-study consents

## Output Files

### CSV Files
- `processed_consent_data.csv`: Cleaned data with engineered features
- `results/clustering_results.csv`: Cluster assignments and patient profiles

### Reports
- `results/statistical_report.txt`: Comprehensive statistical analysis

### Visualizations
- `consent_heatmap.png`: Patient consent patterns across all categories
- `consent_distributions.png`: Distribution analysis of consent behavior
- `clustering_results.png`: Patient segmentation visualization
- `random_forest_results.png`: Classification performance and feature importance
- `logistic_regression_results.png`: Prediction performance with ROC curve

## Insights

The analysis reveals:
- Which data categories patients are most/least willing to share
- Patient archetypes based on privacy preferences
- Predictive factors for consent decisions
- Study-specific consent patterns
- Temporal consent change behaviors

## References

- 2024 iDASH Blockchain Competition
- Research paper on blockchain-based patient consent management in healthcare
- Ethereum smart contract-based consent infrastructure

## Author

Implemented for DDM Lab Assignment 3

## License

Educational use only
