#!/usr/bin/env python3
"""
Script to analyze MLflow experiments and select the best model
based on performance metrics.
"""

import os
import mlflow
import mlflow.sklearn
import pandas as pd
from pathlib import Path
import shutil

def analyze_mlflow_experiments():
    """Analyze all MLflow experiments and find the best model."""
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("./mlruns")
    
    # Get all experiments
    experiments = mlflow.search_experiments()
    
    all_runs = []
    
    print("🔍 Analyzing MLflow experiments...")
    print("=" * 60)
    
    for exp in experiments:
        print(f"\n📊 Experiment: {exp.name} (ID: {exp.experiment_id})")
        
        # Get all runs for this experiment
        runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
        
        if runs.empty:
            print("   No runs found in this experiment.")
            continue
            
        print(f"   Found {len(runs)} runs")
        
        # Add experiment info to runs
        runs['experiment_name'] = exp.name
        runs['experiment_id'] = exp.experiment_id
        
        all_runs.append(runs)
    
    if not all_runs:
        print("❌ No experiments found!")
        return None
    
    # Combine all runs
    combined_runs = pd.concat(all_runs, ignore_index=True)
    
    print(f"\n📈 Total runs across all experiments: {len(combined_runs)}")
    
    # Display summary of metrics
    print("\n📊 Available metrics:")
    metric_cols = [col for col in combined_runs.columns if col.startswith('metrics.')]
    for col in metric_cols:
        print(f"   - {col}")
    
    # Find the best run based on accuracy
    if 'metrics.accuracy' in combined_runs.columns:
        best_run = combined_runs.loc[combined_runs['metrics.accuracy'].idxmax()]
        
        print(f"\n🏆 Best Model Found:")
        print(f"   Run ID: {best_run['run_id']}")
        print(f"   Experiment: {best_run['experiment_name']}")
        print(f"   Accuracy: {best_run['metrics.accuracy']:.4f}")
        
        if 'metrics.precision' in combined_runs.columns:
            print(f"   Precision: {best_run['metrics.precision']:.4f}")
        if 'metrics.recall' in combined_runs.columns:
            print(f"   Recall: {best_run['metrics.recall']:.4f}")
        if 'metrics.f1_score' in combined_runs.columns:
            print(f"   F1-Score: {best_run['metrics.f1_score']:.4f}")
        
        # Display parameters
        param_cols = [col for col in combined_runs.columns if col.startswith('params.')]
        if param_cols:
            print(f"\n🔧 Model Parameters:")
            for col in param_cols:
                if pd.notna(best_run[col]):
                    print(f"   {col}: {best_run[col]}")
        
        return best_run
    else:
        print("❌ No accuracy metric found in experiments!")
        return None

def copy_best_model(best_run):
    """Copy the best model to the expected location for the Flask app."""
    
    if best_run is None:
        print("❌ No best model to copy!")
        return False
    
    try:
        # Create models directory
        os.makedirs('models', exist_ok=True)
        
        # Find the model artifact path
        run_id = best_run['run_id']
        experiment_id = best_run['experiment_id']
        
        # Look for model artifacts
        model_paths = [
            f"mlruns/{experiment_id}/{run_id}/artifacts/model.pkl",
            f"mlruns/{experiment_id}/{run_id}/artifacts/LogisticRegression_model/model.pkl",
            f"mlruns/{experiment_id}/{run_id}/artifacts/RandomForest_model/model.pkl",
            f"mlruns/{experiment_id}/{run_id}/artifacts/LightGBM_model/model.pkl"
        ]
        
        model_found = False
        for model_path in model_paths:
            if os.path.exists(model_path):
                print(f"📁 Found model at: {model_path}")
                shutil.copy2(model_path, 'models/model.pkl')
                print(f"✅ Copied best model to models/model.pkl")
                model_found = True
                break
        
        if not model_found:
            print("❌ Could not find model artifact!")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error copying model: {e}")
        return False

def main():
    """Main function to analyze and select the best model."""
    
    print("🚀 MLflow Model Selection Tool")
    print("=" * 60)
    
    # Analyze experiments
    best_run = analyze_mlflow_experiments()
    
    if best_run is not None:
        print(f"\n📋 Summary:")
        print(f"   Best Model: {best_run['experiment_name']}")
        print(f"   Run ID: {best_run['run_id']}")
        print(f"   Accuracy: {best_run['metrics.accuracy']:.4f}")
        
        # Ask user if they want to copy the model
        print(f"\n❓ Do you want to copy this model to models/model.pkl for the Flask app?")
        response = input("   (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            if copy_best_model(best_run):
                print(f"\n🎉 Best model successfully copied!")
                print(f"   You can now run the Docker container.")
            else:
                print(f"\n❌ Failed to copy the model.")
        else:
            print(f"\n⏭️  Model not copied. You can run this script again later.")
    else:
        print(f"\n❌ No suitable model found!")

if __name__ == "__main__":
    main()
