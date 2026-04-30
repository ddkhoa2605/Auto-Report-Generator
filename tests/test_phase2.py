import json
import pandas as pd
from app.validator import validate_pipeline
from app.metrics import build_metrics_payload
from app.ai_engine import generate_insight

def test_full_ai_pipeline():
    print("\n" + "="*50)
    print("RUNNING INTEGRATION TEST: PHASE 2 (METRICS + AI)")
    print("="*50)
    
    file_path = "data/sample/ecommerce_sample.csv"
    
    try:
        # 1. Load & Validate
        print("[STEP 1] Validating data...")
        df = validate_pipeline(file_path)
        
        # 2. Build Metrics Payload
        print("[STEP 2] Building metrics payload...")
        payload = build_metrics_payload(df)
        print("Payload created successfully.")
        # print(json.dumps(payload, indent=2)) # Debug
        
        # 3. Generate AI Insight
        print("[STEP 3] Calling AI Engine (OpenAI)...")
        insights = generate_insight(payload)
        
        print("\n" + "-"*30)
        print("AI ANALYSIS RESULT RECEIVED:")
        print(f"Summary length: {len(insights.get('summary', ''))} characters")
        print(f"Sentiment: {insights.get('sentiment')}")
        print(f"Insights count: {len(insights.get('insights', []))}")
        print(f"Recommendations count: {len(insights.get('recommendations', []))}")
        print("-" * 30)
        
        print("[SUCCESS] Integration test Phase 2 passed.")
        
    except Exception as e:
        print(f"[ERROR] Integration test failed: {e}")

if __name__ == "__main__":
    test_full_ai_pipeline()
