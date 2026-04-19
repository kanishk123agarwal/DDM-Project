"""
Machine Learning Models for Patient Consent Analysis
Implements K-Means Clustering, Random Forest, and Logistic Regression
Based on the 2024 iDASH Blockchain Competition methodology
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_recall_fscore_support,
    silhouette_score
)
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class ConsentMLModels:
    """
    Machine Learning models for patient consent analysis.
    """
    
    def __init__(self, ml_data):
        """
        Initialize ML models with preprocessed data.
        
        Args:
            ml_data: Dictionary containing preprocessed ML data
        """
        self.ml_data = ml_data
        self.clustering_model = None
        self.random_forest_model = None
        self.logistic_regression_model = None
        self.scaler = StandardScaler()
        self.results = {}
        
    def perform_clustering(self, n_clusters=3, random_state=42):
        """
        Perform K-Means clustering to segment patients by consent behavior.
        
        Args:
            n_clusters: Number of patient segments to create
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary with clustering results
        """
        print("\n" + "="*60)
        print("K-MEANS CLUSTERING: Patient Segmentation")
        print("="*60)
        
        # Get clustering features and scale them
        features = self.ml_data['clustering_features']
        features_scaled = self.scaler.fit_transform(features)
        
        # Perform K-Means clustering
        self.clustering_model = KMeans(
            n_clusters=n_clusters, 
            random_state=random_state,
            n_init=10
        )
        cluster_labels = self.clustering_model.fit_predict(features_scaled)
        
        # Calculate silhouette score (measure of cluster quality)
        silhouette = silhouette_score(features_scaled, cluster_labels)
        
        # Add cluster labels to the data
        self.ml_data['full_data']['cluster'] = cluster_labels
        
        # Analyze clusters
        print(f"\nCreated {n_clusters} patient clusters")
        print(f"Silhouette Score: {silhouette:.3f} (higher is better)")
        
        print("\nCluster Analysis:")
        for cluster_id in range(n_clusters):
            cluster_data = self.ml_data['full_data'][
                self.ml_data['full_data']['cluster'] == cluster_id
            ]
            
            print(f"\n  Cluster {cluster_id} ({len(cluster_data)} patients):")
            print(f"    Mean consent ratio: {cluster_data['consent_ratio'].mean():.2%}")
            print(f"    Mean privacy score: {cluster_data['privacy_score'].mean():.2%}")
            print(f"    Mean volatility: {cluster_data['consent_volatility'].mean():.2f}")
            print(f"    Full consents: {cluster_data['is_full_consent'].sum()}")
            
            # Characterize cluster
            if cluster_data['consent_ratio'].mean() > 0.7:
                label = "OPEN SHARERS"
            elif cluster_data['consent_ratio'].mean() < 0.3:
                label = "PRIVACY-CONSCIOUS"
            else:
                label = "SELECTIVE SHARERS"
            print(f"    Profile: {label}")
        
        # Store results
        self.results['clustering'] = {
            'model': self.clustering_model,
            'labels': cluster_labels,
            'silhouette_score': silhouette,
            'n_clusters': n_clusters,
            'cluster_data': self.ml_data['full_data']
        }
        
        return self.results['clustering']
    
    def train_random_forest(self, target_category='demographics', test_size=0.3, random_state=42):
        """
        Train Random Forest to predict consent for a specific category.
        
        Args:
            target_category: The consent category to predict
            test_size: Proportion of data for testing
            random_state: Random seed
            
        Returns:
            Dictionary with model results
        """
        print("\n" + "="*60)
        print(f"RANDOM FOREST: Predicting {target_category.upper()} Consent")
        print("="*60)
        
        # Prepare data
        full_data = self.ml_data['full_data']
        
        # Features: patient_id, study_id, other consent categories, derived features
        other_categories = [c for c in ['demographics', 'mental_health', 'biospecimen', 
                                        'family_history', 'genetic', 'clinical_info', 
                                        'sexual_reproductive'] if c != target_category]
        
        feature_cols = ['patient_id', 'study_id'] + other_categories + [
            'consent_count', 'consent_ratio', 'consent_volatility'
        ]
        
        X = full_data[feature_cols].values
        y = full_data[target_category].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        print(f"\nTraining set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Class distribution - Consent: {y.sum()}, No Consent: {len(y) - y.sum()}")
        
        # Train Random Forest
        self.random_forest_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=random_state,
            class_weight='balanced'
        )
        
        self.random_forest_model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = self.random_forest_model.predict(X_test)
        y_pred_proba = self.random_forest_model.predict_proba(X_test)[:, 1]
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='binary', zero_division=0
        )
        
        print(f"\nModel Performance:")
        print(f"  Accuracy: {accuracy:.2%}")
        print(f"  Precision: {precision:.2%}")
        print(f"  Recall: {recall:.2%}")
        print(f"  F1-Score: {f1:.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': self.random_forest_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 5 Most Important Features:")
        for idx, row in feature_importance.head(5).iterrows():
            print(f"  {row['feature']}: {row['importance']:.4f}")
        
        # Cross-validation score
        cv_scores = cross_val_score(
            self.random_forest_model, X, y, cv=3, scoring='accuracy'
        )
        print(f"\nCross-Validation Accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
        
        # Store results
        self.results['random_forest'] = {
            'model': self.random_forest_model,
            'target_category': target_category,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'feature_importance': feature_importance,
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'cv_scores': cv_scores
        }
        
        return self.results['random_forest']
    
    def train_logistic_regression(self, test_size=0.3, random_state=42):
        """
        Train Logistic Regression to predict overall consent likelihood.
        
        This model predicts whether a patient will give consent to majority of categories.
        
        Args:
            test_size: Proportion of data for testing
            random_state: Random seed
            
        Returns:
            Dictionary with model results
        """
        print("\n" + "="*60)
        print("LOGISTIC REGRESSION: Predicting High Consent Likelihood")
        print("="*60)
        
        # Prepare data
        full_data = self.ml_data['full_data']
        
        # Features: patient_id, study_id, consent_volatility
        feature_cols = ['patient_id', 'study_id', 'consent_volatility']
        X = full_data[feature_cols].values
        
        # Target: high consent (>50% of categories)
        y = (full_data['consent_ratio'] > 0.5).astype(int).values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"\nTraining set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        print(f"Class distribution - High Consent: {y.sum()}, Low Consent: {len(y) - y.sum()}")
        
        # Train Logistic Regression
        self.logistic_regression_model = LogisticRegression(
            random_state=random_state,
            max_iter=1000,
            class_weight='balanced'
        )
        
        self.logistic_regression_model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.logistic_regression_model.predict(X_test_scaled)
        y_pred_proba = self.logistic_regression_model.predict_proba(X_test_scaled)[:, 1]
        
        # Evaluate
        accuracy = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average='binary', zero_division=0
        )
        
        print(f"\nModel Performance:")
        print(f"  Accuracy: {accuracy:.2%}")
        print(f"  Precision: {precision:.2%}")
        print(f"  Recall: {recall:.2%}")
        print(f"  F1-Score: {f1:.3f}")
        
        # Model coefficients (interpretability)
        coefficients = pd.DataFrame({
            'feature': feature_cols,
            'coefficient': self.logistic_regression_model.coef_[0]
        }).sort_values('coefficient', ascending=False)
        
        print("\nModel Coefficients (Feature Impact):")
        for idx, row in coefficients.iterrows():
            direction = "increases" if row['coefficient'] > 0 else "decreases"
            print(f"  {row['feature']}: {row['coefficient']:.4f} ({direction} consent likelihood)")
        
        # Cross-validation score
        cv_scores = cross_val_score(
            self.logistic_regression_model, X_train_scaled, y_train, cv=3, scoring='accuracy'
        )
        print(f"\nCross-Validation Accuracy: {cv_scores.mean():.2%} (+/- {cv_scores.std():.2%})")
        
        # Store results
        self.results['logistic_regression'] = {
            'model': self.logistic_regression_model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'coefficients': coefficients,
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'cv_scores': cv_scores
        }
        
        return self.results['logistic_regression']
    
    def get_all_results(self):
        """Return all model results."""
        return self.results
    
    def train_all_models(self):
        """
        Train all ML models in sequence.
        
        Returns:
            Dictionary with all model results
        """
        print("\n" + "="*60)
        print("TRAINING ALL ML MODELS")
        print("="*60)
        
        # 1. K-Means Clustering
        self.perform_clustering(n_clusters=3)
        
        # 2. Random Forest Classification
        self.train_random_forest(target_category='demographics')
        
        # 3. Logistic Regression
        self.train_logistic_regression()
        
        print("\n" + "="*60)
        print("ALL MODELS TRAINED SUCCESSFULLY")
        print("="*60)
        
        return self.results


if __name__ == "__main__":
    # This would typically be run after preprocessing
    print("This module requires preprocessed data from consent_preprocessing.py")
    print("Run main.py to execute the complete pipeline")
