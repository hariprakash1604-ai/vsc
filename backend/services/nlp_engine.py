"""
Natural Language Processing Engine
Provides Artificial Intelligence logic mapping hard statistics into readable text, 
and supports a basic Chatbot interface loop.
"""

def generate_natural_language_insight(metric_name: str, trend_data: list, anomalies: int) -> str:
    """NLG function parsing mathematical facts to human sentences."""
    direction = "upward" if trend_data[-1] > trend_data[0] else "downward"
    insight = (
        f"The metric '{metric_name}' is showing an overall {direction} trend over the analyzed period. "
    )
    if anomalies > 0:
        insight += f"WARNING: We detected {anomalies} significant anomalies (deviations from norm). "
        insight += "Consider applying immediate quality checks."
    else:
        insight += "The data appears stable with zero detected anomalies."
    
    return insight

def process_chat_query(query: str) -> str:
    """
    Mock AI chatbot processing NLP query into SQL/Data lookup.
    """
    q = query.lower()
    if 'anomaly' in q or 'fraud' in q:
        return "I can run an Isolation Forest or DBSCAN clustering model to find fraud patterns in your datasets. Just upload a dataset and select an attribute!"
    elif 'report' in q or 'summary' in q:
        return "You can generate automated PDF reports summarizing the data. Just upload your data and click the Export button below the charts."
    elif 'trend' in q or 'forecast' in q:
        return "I use Exponential Smoothing and Time-Series Neural networks to project future trends. Select any numerical KPI you want me to forecast."
    else:
        return "I am the Intelligent Analytics Assistant. I can help you uncover hidden patterns, detect anomalies, compile PDF reports, or connect to your CRM/ERP."
