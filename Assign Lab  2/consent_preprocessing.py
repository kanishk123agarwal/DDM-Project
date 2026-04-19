"""
Data Preprocessing Module for Patient Consent Analysis
Based on the 2024 iDASH Blockchain Competition methodology
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split

class ConsentDataPreprocessor:
    """
    Preprocesses patient consent data from CSV file.
    Handles duplicate records, feature engineering, and data splitting.
    """
    
    def __init__(self, csv_path):
        """
        Initialize the preprocessor with the dataset path.
        
        Args:
            csv_path: Path to the patient_consent.csv file
        """
        self.csv_path = csv_path
        self.raw_data = None
        self.processed_data = None
        self.consent_categories = [
            'demographics', 'mental_health', 'biospecimen', 
            'family_history', 'genetic', 'clinical_info', 'sexual_reproductive'
        ]
        
    def load_data(self):
        """Load the CSV data into a pandas DataFrame."""
        print("Loading patient consent data...")
        self.raw_data = pd.read_csv(self.csv_path)
        print(f"Loaded {len(self.raw_data)} consent records")
        print(f"Columns: {list(self.raw_data.columns)}")
        return self.raw_data
    
    def parse_timestamps(self):
        """Convert timestamp strings to datetime objects."""
        print("\nParsing timestamps...")
        self.raw_data['timestamp'] = pd.to_datetime(
            self.raw_data['timestamp'], 
            format='%d-%m-%Y %H:%M'
        )
        print("Timestamps parsed successfully")
        
    def handle_duplicate_consents(self):
        """
        Handle duplicate patient-study pairs by keeping only the latest record.
        This implements the key business rule from the paper:
        "the later choice with a larger Timestamp would override the former"
        """
        print("\nHandling duplicate consent records...")
        initial_count = len(self.raw_data)
        
        # Sort by timestamp to ensure latest records are kept
        self.raw_data = self.raw_data.sort_values('timestamp', ascending=True)
        
        # Keep only the last record for each patient-study combination
        self.processed_data = self.raw_data.groupby(
            ['patient_id', 'study_id'], 
            as_index=False
        ).last()
        
        final_count = len(self.processed_data)
        duplicates_removed = initial_count - final_count
        
        print(f"Removed {duplicates_removed} duplicate records")
        print(f"Keeping {final_count} unique patient-study consent records")
        
        return self.processed_data
    
    def engineer_features(self):
        """
        Create derived features from consent data.
        
        Features created:
        - consent_count: Total number of categories consented to
        - consent_ratio: Proportion of categories consented (0.0 to 1.0)
        - privacy_score: Inverse of consent ratio (higher = more privacy-conscious)
        - is_full_consent: Binary flag if all 7 categories are consented
        - is_no_consent: Binary flag if no categories are consented
        """
        print("\nEngineering features...")
        
        # Calculate consent count (sum of all consent columns)
        self.processed_data['consent_count'] = self.processed_data[
            self.consent_categories
        ].sum(axis=1)
        
        # Calculate consent ratio (proportion of categories consented)
        self.processed_data['consent_ratio'] = (
            self.processed_data['consent_count'] / len(self.consent_categories)
        )
        
        # Calculate privacy score (inverse of consent ratio)
        self.processed_data['privacy_score'] = (
            1 - self.processed_data['consent_ratio']
        )
        
        # Binary flags
        self.processed_data['is_full_consent'] = (
            self.processed_data['consent_count'] == len(self.consent_categories)
        ).astype(int)
        
        self.processed_data['is_no_consent'] = (
            self.processed_data['consent_count'] == 0
        ).astype(int)
        
        print("Features engineered:")
        print("  - consent_count")
        print("  - consent_ratio")
        print("  - privacy_score")
        print("  - is_full_consent")
        print("  - is_no_consent")
        
        return self.processed_data
    
    def calculate_consent_volatility(self):
        """
        Calculate how many times each patient changed their consent for studies.
        This measures patient indecisiveness or changing preferences.
        """
        print("\nCalculating consent volatility...")
        
        # Count total records per patient in original data
        patient_record_counts = self.raw_data.groupby('patient_id').size()
        
        # Count unique patient-study pairs per patient in processed data
        unique_consents = self.processed_data.groupby('patient_id').size()
        
        # Volatility = total records - unique combinations
        volatility = {}
        for patient_id in self.processed_data['patient_id'].unique():
            total = patient_record_counts.get(patient_id, 1)
            unique = unique_consents.get(patient_id, 1)
            volatility[patient_id] = total - unique
        
        self.processed_data['consent_volatility'] = (
            self.processed_data['patient_id'].map(volatility)
        )
        
        print(f"Consent volatility calculated for {len(volatility)} patients")
        
        return self.processed_data
    
    def get_summary_statistics(self):
        """Generate summary statistics of the processed data."""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        print(f"\nTotal unique patient-study consents: {len(self.processed_data)}")
        print(f"Unique patients: {self.processed_data['patient_id'].nunique()}")
        print(f"Unique studies: {self.processed_data['study_id'].nunique()}")
        
        print("\nConsent Statistics:")
        print(f"  Mean consent count: {self.processed_data['consent_count'].mean():.2f}")
        print(f"  Mean consent ratio: {self.processed_data['consent_ratio'].mean():.2%}")
        print(f"  Full consents: {self.processed_data['is_full_consent'].sum()}")
        print(f"  No consents: {self.processed_data['is_no_consent'].sum()}")
        
        print("\nConsent by Category:")
        for cat in self.consent_categories:
            consent_pct = self.processed_data[cat].mean() * 100
            print(f"  {cat}: {consent_pct:.1f}%")
        
        print("\nConsent Volatility:")
        print(f"  Mean volatility: {self.processed_data['consent_volatility'].mean():.2f}")
        print(f"  Max volatility: {self.processed_data['consent_volatility'].max()}")
        
        return self.processed_data.describe()
    
    def prepare_ml_data(self, test_size=0.3, random_state=42):
        """
        Prepare data for machine learning by creating feature and target sets.
        
        Args:
            test_size: Proportion of data to use for testing
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary containing various train/test splits
        """
        print(f"\nPreparing ML data (test_size={test_size})...")
        
        # Feature matrix for clustering (unsupervised)
        clustering_features = self.processed_data[
            self.consent_categories + ['consent_ratio', 'privacy_score', 'consent_volatility']
        ].values
        
        # For classification: predict individual category consents
        classification_features = self.processed_data[
            ['patient_id', 'study_id', 'consent_count', 'consent_ratio', 'consent_volatility']
        ].values
        
        # Store patient and study IDs for reference
        patient_ids = self.processed_data['patient_id'].values
        study_ids = self.processed_data['study_id'].values
        
        ml_data = {
            'clustering_features': clustering_features,
            'classification_features': classification_features,
            'consent_matrix': self.processed_data[self.consent_categories].values,
            'patient_ids': patient_ids,
            'study_ids': study_ids,
            'full_data': self.processed_data
        }
        
        print("ML data prepared successfully")
        print(f"  Clustering features shape: {clustering_features.shape}")
        print(f"  Classification features shape: {classification_features.shape}")
        
        return ml_data
    
    def preprocess_pipeline(self):
        """
        Execute the complete preprocessing pipeline.
        
        Returns:
            Dictionary containing prepared ML data
        """
        print("\n" + "="*60)
        print("PATIENT CONSENT DATA PREPROCESSING PIPELINE")
        print("="*60)
        
        # Step 1: Load data
        self.load_data()
        
        # Step 2: Parse timestamps
        self.parse_timestamps()
        
        # Step 3: Handle duplicates (keep latest per patient-study)
        self.handle_duplicate_consents()
        
        # Step 4: Engineer features
        self.engineer_features()
        
        # Step 5: Calculate consent volatility
        self.calculate_consent_volatility()
        
        # Step 6: Display summary statistics
        self.get_summary_statistics()
        
        # Step 7: Prepare ML data
        ml_data = self.prepare_ml_data()
        
        print("\n" + "="*60)
        print("PREPROCESSING COMPLETE")
        print("="*60)
        
        return ml_data


if __name__ == "__main__":
    # Test the preprocessing module
    preprocessor = ConsentDataPreprocessor('patient_consent.csv')
    ml_data = preprocessor.preprocess_pipeline()
    
    # Save processed data
    preprocessor.processed_data.to_csv('processed_consent_data.csv', index=False)
    print("\nProcessed data saved to: processed_consent_data.csv")
