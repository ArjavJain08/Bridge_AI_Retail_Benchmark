import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import sqlite3
import random

def generate_synthetic_benchmark_dataset():
    """Generates enterprise-grade benchmark data across all required scopes."""
    brands = ["Intel", "AMD", "Qualcomm", "Apple"]
    oems = ["Dell", "HP", "Lenovo", "Acer", "Asus", "MSI", "Apple"]
    categories = ["Notebook", "Desktop", "Workstation", "Tablet", "CPU/GPU Component"]
    platforms = [("Newegg (US)", "US"), ("Mercado Libre (Brazil)", "Brazil")]
    
    rows = []
    np.random.seed(42)
    random.seed(42)
    
    for i in range(1, 65):
        brand = random.choice(brands)
        oem = "Apple" if brand == "Apple" else random.choice([o for o in oems if o != "Apple"])
        category = random.choices(categories, weights=[0.5, 0.25, 0.1, 0.1, 0.05])[0]
        platform, country = random.choice(platforms)
        
        # CPU/GPU components have no OEM value
        if category == "CPU/GPU Component": oem = None
            
        sku = f"SKU-{platform[:2].upper()}-{1000+i}"
        list_price = round(float(np.random.uniform(700, 3200)), 2)
        is_promo = random.random() < 0.3
        price = round(list_price * random.choice([0.75, 0.85, 0.90]), 2) if is_promo else list_price
        
        # Page Rubric Checks (S1-S2, P1-P5)
        checks = [random.random() > 0.15 for _ in range(7)]
        raw_score = sum(checks) / 7.0 * 100.0
        
        rows.append({
            'sku': sku, 'brand': brand, 'oem': oem, 'category': category,
            'platform': platform, 'country': country,
            'title': f"{oem or brand} {category} - {brand} Edition",
            'price': price, 'list_price': list_price,
            'is_on_promotion': is_promo,
            'discount_pct': round(((list_price - price) / list_price) * 100, 1) if is_promo else 0.0,
            'compliance_score': round(raw_score, 1),
            'search_rank': random.randint(1, 15),
            'has_homepage_banner': random.random() < 0.2
        })
    return pd.DataFrame(rows)

def run_pipeline():
    print("Gathering Multi-Brand Intelligence...")
    df = generate_synthetic_benchmark_dataset()
    
    print("Running Isolation Forest AI for Price Drop Detection...")
    model = IsolationForest(contamination=0.12, random_state=42)
    df['is_anomaly'] = model.fit_predict(df['price'].values.reshape(-1, 1))
    df['alert_flag'] = df['is_anomaly'].apply(lambda x: "🚨 SHARP DROP ALERT" if x == -1 else "Normal")
    
    conn = sqlite3.connect('retail_advanced.db')
    df.to_sql('products', conn, if_exists='replace', index=False)
    conn.close()
    print(f"✅ Pipeline complete! {len(df)} products saved to database.")

if __name__ == "__main__":
    run_pipeline()
