"""
Main Execution Script for Patient Consent ML Analysis
Orchestrates the complete ML pipeline from data preprocessing to visualization
Based on the 2024 iDASH Blockchain Competition methodology
"""

import sys
from consent_preprocessing import ConsentDataPreprocessor
from consent_ml_models import ConsentMLModels
from consent_analysis import ConsentAnalyzer


def main():
    """Execute the complete ML pipeline."""
    
    print("\n" + "="*70)
    print(" PATIENT CONSENT MACHINE LEARNING ANALYSIS")
    print(" Based on 2024 iDASH Blockchain Competition Paper")
    print("="*70)
    
    try:
        # ========== STEP 1: DATA PREPROCESSING ==========
        print("\n[STEP 1/4] DATA PREPROCESSING")
        preprocessor = ConsentDataPreprocessor('patient_consent.csv')
        ml_data = preprocessor.preprocess_pipeline()
        
        # Save processed data
        preprocessor.processed_data.to_csv('processed_consent_data.csv', index=False)
        print("\n[OK] Processed data saved to: processed_consent_data.csv")
        
        # ========== STEP 2: MACHINE LEARNING MODELS ==========
        print("\n[STEP 2/4] MACHINE LEARNING MODELS")
        models = ConsentMLModels(ml_data)
        model_results = models.train_all_models()
        
        # ========== STEP 3: ANALYSIS & VISUALIZATION ==========
        print("\n[STEP 3/4] ANALYSIS & VISUALIZATION")
        analyzer = ConsentAnalyzer(ml_data, model_results, output_dir='results')
        analyzer.generate_all_visualizations()
        
        # ========== STEP 4: SUMMARY ==========
        print("\n[STEP 4/4] SUMMARY")
        print("\n" + "="*70)
        print(" EXECUTION COMPLETE - SUMMARY")
        print("="*70)
        
        print("\n[MODELS TRAINED]:")
        print("  [OK] K-Means Clustering (Patient Segmentation)")
        print(f"    - Silhouette Score: {model_results['clustering']['silhouette_score']:.3f}")
        print(f"    - Number of Clusters: {model_results['clustering']['n_clusters']}")
        
        print("\n  [OK] Random Forest Classifier (Demographics Consent Prediction)")
        print(f"    - Accuracy: {model_results['random_forest']['accuracy']:.2%}")
        print(f"    - F1-Score: {model_results['random_forest']['f1_score']:.3f}")
        
        print("\n  [OK] Logistic Regression (High Consent Likelihood)")
        print(f"    - Accuracy: {model_results['logistic_regression']['accuracy']:.2%}")
        print(f"    - F1-Score: {model_results['logistic_regression']['f1_score']:.3f}")
        
        print("\n[OUTPUT FILES]:")
        print("  - processed_consent_data.csv")
        print("  - results/clustering_results.csv")
        print("  - results/statistical_report.txt")
        print("  - results/visualizations/*.png")
        
        print("\n" + "="*70)
        print(" SUCCESS! All analysis complete.")
        print("="*70)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n[ERROR]: File not found - {e}")
        print("   Please ensure 'patient_consent.csv' is in the current directory.")
        return 1
        
    except Exception as e:
        print(f"\n[ERROR]: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
