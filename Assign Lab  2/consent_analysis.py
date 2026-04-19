"""
Analysis and Visualization Module for Patient Consent Analysis
Creates comprehensive visualizations and statistical analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import os

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class ConsentAnalyzer:
    """
    Generates visualizations and statistical analysis for consent data.
    """
    
    def __init__(self, ml_data, model_results, output_dir='results'):
        """
        Initialize the analyzer.
        
        Args:
            ml_data: Preprocessed ML data
            model_results: Results from trained ML models
            output_dir: Directory to save output files
        """
        self.ml_data = ml_data
        self.model_results = model_results
        self.output_dir = output_dir
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'visualizations'), exist_ok=True)
        
        print(f"\nAnalyzer initialized. Output directory: {output_dir}")
    
    def plot_consent_heatmap(self):
        """Create heatmap showing consent patterns across categories."""
        print("\nGenerating consent heatmap...")
        
        full_data = self.ml_data['full_data']
        consent_categories = [
            'demographics', 'mental_health', 'biospecimen', 
            'family_history', 'genetic', 'clinical_info', 'sexual_reproductive'
        ]
        
        # Create consent matrix
        consent_matrix = full_data[consent_categories].values
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(
            consent_matrix.T, 
            cmap='RdYlGn',
            cbar_kws={'label': 'Consent (0=No, 1=Yes)'},
            yticklabels=[c.replace('_', ' ').title() for c in consent_categories],
            xticklabels=[f"P{pid}-S{sid}" for pid, sid in zip(
                full_data['patient_id'], full_data['study_id']
            )]
        )
        plt.title('Patient Consent Patterns Across Categories', fontsize=14, fontweight='bold')
        plt.xlabel('Patient-Study Combinations')
        plt.ylabel('Data Categories')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, 'visualizations', 'consent_heatmap.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filepath}")
    
    def plot_consent_distribution(self):
        """Plot distribution of consent counts."""
        print("\nGenerating consent distribution plots...")
        
        full_data = self.ml_data['full_data']
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Consent count distribution
        axes[0, 0].hist(full_data['consent_count'], bins=8, color='skyblue', edgecolor='black')
        axes[0, 0].set_xlabel('Number of Categories Consented')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Distribution of Consent Counts')
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # 2. Consent ratio distribution
        axes[0, 1].hist(full_data['consent_ratio'], bins=10, color='lightcoral', edgecolor='black')
        axes[0, 1].set_xlabel('Consent Ratio (0=None, 1=All)')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Distribution of Consent Ratios')
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # 3. Category-wise consent rates
        consent_categories = [
            'demographics', 'mental_health', 'biospecimen', 
            'family_history', 'genetic', 'clinical_info', 'sexual_reproductive'
        ]
        consent_rates = [full_data[cat].mean() * 100 for cat in consent_categories]
        category_labels = [c.replace('_', '\n').title() for c in consent_categories]
        
        axes[1, 0].barh(category_labels, consent_rates, color='mediumseagreen', edgecolor='black')
        axes[1, 0].set_xlabel('Consent Rate (%)')
        axes[1, 0].set_title('Consent Rates by Category')
        axes[1, 0].grid(axis='x', alpha=0.3)
        
        # 4. Study-wise consent patterns
        study_consent = full_data.groupby('study_id')['consent_ratio'].mean() * 100
        axes[1, 1].bar(study_consent.index.astype(str), study_consent.values, 
                       color='orange', edgecolor='black')
        axes[1, 1].set_xlabel('Study ID')
        axes[1, 1].set_ylabel('Average Consent Ratio (%)')
        axes[1, 1].set_title('Average Consent Ratio by Study')
        axes[1, 1].grid(axis='y', alpha=0.3)
        
        plt.suptitle('Patient Consent Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, 'visualizations', 'consent_distributions.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filepath}")
    
    def plot_clustering_results(self):
        """Visualize patient clustering results."""
        if 'clustering' not in self.model_results:
            print("\nSkipping clustering visualization (no results available)")
            return
        
        print("\nGenerating clustering visualizations...")
        
        clustering = self.model_results['clustering']
        cluster_data = clustering['cluster_data']
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Scatter plot: Consent Ratio vs Privacy Score
        for cluster_id in range(clustering['n_clusters']):
            cluster_points = cluster_data[cluster_data['cluster'] == cluster_id]
            axes[0].scatter(
                cluster_points['consent_ratio'],
                cluster_points['privacy_score'],
                label=f'Cluster {cluster_id}',
                s=100,
                alpha=0.6
            )
        
        axes[0].set_xlabel('Consent Ratio')
        axes[0].set_ylabel('Privacy Score')
        axes[0].set_title('Patient Clusters: Consent vs Privacy')
        axes[0].legend()
        axes[0].grid(alpha=0.3)
        
        # 2. Cluster size and characteristics
        cluster_summary = cluster_data.groupby('cluster').agg({
            'consent_ratio': 'mean',
            'privacy_score': 'mean',
            'consent_volatility': 'mean',
            'patient_id': 'count'
        }).rename(columns={'patient_id': 'count'})
        
        x = np.arange(len(cluster_summary))
        width = 0.25
        
        axes[1].bar(x - width, cluster_summary['consent_ratio'] * 100, width, 
                   label='Consent Ratio (%)', color='skyblue')
        axes[1].bar(x, cluster_summary['privacy_score'] * 100, width,
                   label='Privacy Score (%)', color='lightcoral')
        axes[1].bar(x + width, cluster_summary['consent_volatility'] * 10, width,
                   label='Volatility (x10)', color='lightgreen')
        
        axes[1].set_xlabel('Cluster ID')
        axes[1].set_ylabel('Percentage / Score')
        axes[1].set_title('Cluster Characteristics')
        axes[1].set_xticks(x)
        axes[1].legend()
        axes[1].grid(axis='y', alpha=0.3)
        
        plt.suptitle(f'K-Means Clustering Results (Silhouette Score: {clustering["silhouette_score"]:.3f})',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, 'visualizations', 'clustering_results.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filepath}")
    
    def plot_random_forest_results(self):
        """Visualize Random Forest classification results."""
        if 'random_forest' not in self.model_results:
            print("\nSkipping Random Forest visualization (no results available)")
            return
        
        print("\nGenerating Random Forest visualizations...")
        
        rf = self.model_results['random_forest']
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Feature importance
        top_features = rf['feature_importance'].head(10)
        axes[0].barh(top_features['feature'], top_features['importance'], color='steelblue')
        axes[0].set_xlabel('Importance Score')
        axes[0].set_title('Top 10 Feature Importances')
        axes[0].invert_yaxis()
        axes[0].grid(axis='x', alpha=0.3)
        
        # 2. Confusion matrix
        cm = rf['confusion_matrix']
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1],
                   xticklabels=['No Consent', 'Consent'],
                   yticklabels=['No Consent', 'Consent'])
        axes[1].set_xlabel('Predicted')
        axes[1].set_ylabel('Actual')
        axes[1].set_title('Confusion Matrix')
        
        plt.suptitle(f'Random Forest: {rf["target_category"].title()} Prediction '
                    f'(Accuracy: {rf["accuracy"]:.2%})',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, 'visualizations', 'random_forest_results.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filepath}")
    
    def plot_logistic_regression_results(self):
        """Visualize Logistic Regression results."""
        if 'logistic_regression' not in self.model_results:
            print("\nSkipping Logistic Regression visualization (no results available)")
            return
        
        print("\nGenerating Logistic Regression visualizations...")
        
        lr = self.model_results['logistic_regression']
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # 1. Confusion matrix
        cm = lr['confusion_matrix']
        sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', ax=axes[0],
                   xticklabels=['Low Consent', 'High Consent'],
                   yticklabels=['Low Consent', 'High Consent'])
        axes[0].set_xlabel('Predicted')
        axes[0].set_ylabel('Actual')
        axes[0].set_title('Confusion Matrix')
        
        # 2. ROC Curve
        fpr, tpr, _ = roc_curve(lr['y_test'], lr['y_pred_proba'])
        roc_auc = auc(fpr, tpr)
        
        axes[1].plot(fpr, tpr, color='darkorange', lw=2, 
                    label=f'ROC curve (AUC = {roc_auc:.2f})')
        axes[1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
        axes[1].set_xlabel('False Positive Rate')
        axes[1].set_ylabel('True Positive Rate')
        axes[1].set_title('ROC Curve')
        axes[1].legend(loc='lower right')
        axes[1].grid(alpha=0.3)
        
        plt.suptitle(f'Logistic Regression: High Consent Prediction (Accuracy: {lr["accuracy"]:.2%})',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        filepath = os.path.join(self.output_dir, 'visualizations', 'logistic_regression_results.png')
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filepath}")
    
    def generate_statistical_report(self):
        """Generate a comprehensive statistical report."""
        print("\nGenerating statistical report...")
        
        report_lines = []
        report_lines.append("="*70)
        report_lines.append("PATIENT CONSENT ANALYSIS - STATISTICAL REPORT")
        report_lines.append("="*70)
        report_lines.append("")
        
        # Dataset summary
        full_data = self.ml_data['full_data']
        report_lines.append("DATASET SUMMARY")
        report_lines.append("-" * 70)
        report_lines.append(f"Total unique patient-study consents: {len(full_data)}")
        report_lines.append(f"Unique patients: {full_data['patient_id'].nunique()}")
        report_lines.append(f"Unique studies: {full_data['study_id'].nunique()}")
        report_lines.append("")
        
        # Consent statistics
        report_lines.append("CONSENT STATISTICS")
        report_lines.append("-" * 70)
        report_lines.append(f"Mean consent count: {full_data['consent_count'].mean():.2f}")
        report_lines.append(f"Mean consent ratio: {full_data['consent_ratio'].mean():.2%}")
        report_lines.append(f"Std consent ratio: {full_data['consent_ratio'].std():.2%}")
        report_lines.append(f"Full consents (all 7 categories): {full_data['is_full_consent'].sum()}")
        report_lines.append(f"No consents (0 categories): {full_data['is_no_consent'].sum()}")
        report_lines.append("")
        
        # Model results
        if 'clustering' in self.model_results:
            clustering = self.model_results['clustering']
            report_lines.append("K-MEANS CLUSTERING RESULTS")
            report_lines.append("-" * 70)
            report_lines.append(f"Number of clusters: {clustering['n_clusters']}")
            report_lines.append(f"Silhouette score: {clustering['silhouette_score']:.3f}")
            report_lines.append("")
        
        if 'random_forest' in self.model_results:
            rf = self.model_results['random_forest']
            report_lines.append("RANDOM FOREST CLASSIFICATION RESULTS")
            report_lines.append("-" * 70)
            report_lines.append(f"Target category: {rf['target_category']}")
            report_lines.append(f"Accuracy: {rf['accuracy']:.2%}")
            report_lines.append(f"Precision: {rf['precision']:.2%}")
            report_lines.append(f"Recall: {rf['recall']:.2%}")
            report_lines.append(f"F1-Score: {rf['f1_score']:.3f}")
            report_lines.append(f"Cross-validation accuracy: {rf['cv_scores'].mean():.2%} (+/- {rf['cv_scores'].std():.2%})")
            report_lines.append("")
        
        if 'logistic_regression' in self.model_results:
            lr = self.model_results['logistic_regression']
            report_lines.append("LOGISTIC REGRESSION RESULTS")
            report_lines.append("-" * 70)
            report_lines.append(f"Accuracy: {lr['accuracy']:.2%}")
            report_lines.append(f"Precision: {lr['precision']:.2%}")
            report_lines.append(f"Recall: {lr['recall']:.2%}")
            report_lines.append(f"F1-Score: {lr['f1_score']:.3f}")
            report_lines.append(f"Cross-validation accuracy: {lr['cv_scores'].mean():.2%} (+/- {lr['cv_scores'].std():.2%})")
            report_lines.append("")
        
        report_lines.append("="*70)
        
        report_text = "\n".join(report_lines)
        
        # Save report
        filepath = os.path.join(self.output_dir, 'statistical_report.txt')
        with open(filepath, 'w') as f:
            f.write(report_text)
        
        print(f"  Saved: {filepath}")
        print("\n" + report_text)
        
        return report_text
    
    def generate_all_visualizations(self):
        """Generate all visualizations and reports."""
        print("\n" + "="*60)
        print("GENERATING ANALYSIS AND VISUALIZATIONS")
        print("="*60)
        
        # Generate all plots
        self.plot_consent_heatmap()
        self.plot_consent_distribution()
        self.plot_clustering_results()
        self.plot_random_forest_results()
        self.plot_logistic_regression_results()
        
        # Generate statistical report
        self.generate_statistical_report()
        
        # Save clustering results to CSV
        if 'clustering' in self.model_results:
            cluster_data = self.model_results['clustering']['cluster_data']
            cluster_filepath = os.path.join(self.output_dir, 'clustering_results.csv')
            cluster_data.to_csv(cluster_filepath, index=False)
            print(f"\nClustering results saved to: {cluster_filepath}")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"\nAll outputs saved to: {self.output_dir}/")


if __name__ == "__main__":
    print("This module requires ML results.")
    print("Run main.py to execute the complete pipeline")
