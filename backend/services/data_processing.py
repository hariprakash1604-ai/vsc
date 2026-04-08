import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by handling missing values and duplicates.
    """
    df = df.drop_duplicates()
    
    # Fill numeric columns with the median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Fill categorical columns with mode
    cat_cols = df.select_dtypes(exclude=[np.number]).columns
    for col in cat_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])
            
    return df

def generate_eda_stats(df: pd.DataFrame) -> dict:
    """
    Generates Exploratory Data Analysis metrics natively.
    """
    numeric_cols = df.select_dtypes(include=[np.number])
    
    if numeric_cols.empty:
        return {"error": "No numeric columns available for EDA"}
        
    stats = {}
    for col in numeric_cols.columns:
        stats[col] = {
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "variance": float(df[col].var()),
            "std_dev": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max())
        }
    
    # Generate correlation matrix dropping NaNs
    corr = numeric_cols.corr().fillna(0).to_dict()
    
    return {
        "descriptive_statistics": stats,
        "correlation_matrix": corr
    }
