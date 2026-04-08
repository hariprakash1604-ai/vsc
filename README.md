# Intelligent Business Analytics Platform

An advanced, end-to-end analytics engine and dashboard built to extract deep insights from raw datasets. Handles structural data ingestion, performs automated Exploratory Data Analysis, and utilizes machine learning for complex anomaly detection and time-series forecasting.

## System Architecture

```mermaid
graph TD
    %% Define Styles
    classDef client fill:#6366f1,stroke:#4f46e5,stroke-width:2px,color:#fff
    classDef api fill:#10b981,stroke:#059669,stroke-width:2px,color:#fff
    classDef data fill:#f59e0b,stroke:#d97706,stroke-width:2px,color:#fff
    classDef ai fill:#ec4899,stroke:#db2777,stroke-width:2px,color:#fff

    User((User / Browser)) -->|Uploads CSV / Queries| Client
    Client[React Dashboard]:::client

    Client -->|HTTP POST Request| API
    
    API[FastAPI Gateway]:::api
    
    API -->|Ingests Data| DataCore
    DataCore(Pandas / Data Engineering Layer):::data
    
    DataCore -->|Calculates Stats| EDA(EDA Engine)
    DataCore -->|Transmits Matrix| MLModels
    
    MLModels[Scikit-Learn ML Cluster]:::ai
    MLModels -->|Univariate Spikes| Isolation[Isolation Forest]
    MLModels -->|Multivariate Clusters| DBScan[DBSCAN]
    MLModels -->|Trends| Forecast[Tensorflow / Prophet]
    
    EDA --> NLP[NLG Bot]
    Isolation --> NLP
    
    NLP -->|Human-readable Insights| API
    NLP -->|Generates PDF| ReportGenerator[ReportLab Engine]
    
    ReportGenerator -->|Downloads| Client
```

## Running the Platform
Navigate to the frontend to launch the React App:
`npm run dev`

Navigate to the backend to launch the API:
`uvicorn main:app --reload`
