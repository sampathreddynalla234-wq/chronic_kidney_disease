import numpy as np
import pandas as pd
from pathlib import Path
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

FEATURES = ["age","blood_pressure","specific_gravity","albumin","sugar",
            "blood_glucose","blood_urea","serum_creatinine","hemoglobin",
            "packed_cell_volume"]

def main():
    # Synthetic labels are created only to demonstrate the ML workflow.
    rng = np.random.default_rng(42)
    n = 1200
    age = rng.integers(18, 90, n)
    bp = rng.normal(78, 13, n).clip(45, 150)
    sg = rng.choice([1.005,1.010,1.015,1.020,1.025], n)
    albumin = rng.choice([0,1,2,3,4,5], n, p=[.55,.18,.12,.08,.05,.02])
    sugar = rng.choice([0,1,2,3,4,5], n)
    glucose = rng.normal(115,35,n).clip(55,350)
    urea = rng.normal(38,22,n).clip(5,180)
    creat = rng.lognormal(np.log(1.0),.55,n).clip(.3,12)
    hb = rng.normal(13.2,2.1,n).clip(5,19)
    pcv = (hb*3.1+rng.normal(0,3,n)).clip(15,60)
    score = ((albumin>=2)*1.4 + (creat>1.5)*1.5 + (urea>50)*.8 +
             (hb<11)*.8 + (sg<=1.010)*.5 + (age>65)*.2 +
             (glucose>180)*.3 + rng.normal(0,.65,n))
    y = (score > 1.55).astype(int)
    X = pd.DataFrame(dict(age=age,blood_pressure=bp,specific_gravity=sg,
        albumin=albumin,sugar=sugar,blood_glucose=glucose,blood_urea=urea,
        serum_creatinine=creat,hemoglobin=hb,packed_cell_volume=pcv))[FEATURES]
    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=.2,random_state=42,stratify=y)
    model = Pipeline([
        ("imputer",SimpleImputer(strategy="median")),
        ("scale",StandardScaler()),
        ("classifier",RandomForestClassifier(n_estimators=180,max_depth=8,
                         random_state=42,class_weight="balanced"))
    ])
    model.fit(X_train,y_train)
    print("DEMO ONLY – synthetic data; metrics are not clinically meaningful.")
    print(classification_report(y_test,model.predict(X_test),zero_division=0))
    joblib.dump({"model":model,"features":FEATURES},
                Path(__file__).with_name("ckd_demo_model.joblib"))
    print("Saved ckd_demo_model.joblib")

if __name__ == "__main__":
    main()
