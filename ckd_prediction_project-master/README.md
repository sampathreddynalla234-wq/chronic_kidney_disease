# CKD Prediction System – Student Project

Educational full-stack demonstration: React + Flask + scikit-learn + optional MongoDB.

**Medical safety:** The bundled model is trained on generated synthetic data only. It is not clinically validated and must not be used to diagnose, screen, treat, or make decisions about real patients.

## Run it
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python train_model.py
python app.py
```
API: http://127.0.0.1:5000

### Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```
Open the Vite URL shown (normally http://localhost:5173).

### Optional MongoDB
Set `MONGO_URI=mongodb://localhost:27017/` before starting Flask. Demo submissions are stored in `ckd_project.predictions`. Prediction still works if MongoDB is not configured.

## API
- GET `/api/health`
- POST `/api/predict`

JSON fields: `age`, `blood_pressure`, `specific_gravity`, `albumin`, `sugar`, `blood_glucose`, `blood_urea`, `serum_creatinine`, `hemoglobin`, `packed_cell_volume`.

## Team roles (5 members)
1. Team Leader & Integration – planning, Git, integration and presentation.
2. Frontend Developer – React UI, forms, validation and results page.
3. Backend Developer – Flask APIs, validation and error handling.
4. ML Developer – dataset research, preprocessing, training and evaluation.
5. Database & Testing – MongoDB, API testing and documentation.

## For a genuine research project
Replace the synthetic generator with a properly licensed, representative dataset. Document provenance and limitations, use patient-level separation, perform external validation, and obtain qualified clinical review before making any clinical claims.
