import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Load data
data_path = os.path.join('data', 'Housing.csv')
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Dataset not found at {data_path}. Please download it first.")

df = pd.read_csv(data_path)

# Binary mapping for yes/no columns
binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
for col in binary_cols:
    df[col] = df[col].map({'yes': 1, 'no': 0})

# One-hot encode furnishingstatus
# Keeping columns consistent: furnishingstatus_semi-furnished and furnishingstatus_unfurnished
# (where furnishingstatus_furnished is when both are 0)
df = pd.get_dummies(df, columns=['furnishingstatus'], drop_first=True)

# Extract features and target
X = df.drop('price', axis=1)
y = df['price']

# Save feature list for alignment in app
feature_cols = list(X.columns)

# Train-Test Split (80% training, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale all features (required for Linear Regression and good practice)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train and evaluate models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=150, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, random_state=42)
}

best_model = None
best_r2 = -float('inf')
best_model_name = ""
model_results = {}

print("Training models...")
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    
    # Calculate training score for overfitting check
    train_preds = model.predict(X_train_scaled)
    train_r2 = r2_score(y_train, train_preds)
    
    model_results[name] = {
        'R2': r2, 
        'Train_R2': train_r2,
        'MAE': mae, 
        'RMSE': rmse
    }
    print(f"- {name:20s} | Train R2: {train_r2:.4f} | Test R2: {r2:.4f} | MAE: {mae:.2f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model = model
        best_model_name = name

print(f"\n[BEST MODEL] {best_model_name} with test R2 score of {best_r2:.4f}")

# Save the selected model, scaler, and configuration metadata
joblib.dump(best_model, os.path.join('models', 'house_price_model.joblib'))
joblib.dump(scaler, os.path.join('models', 'scaler.joblib'))
joblib.dump({
    'features': feature_cols,
    'binary_cols': binary_cols,
    'best_model_name': best_model_name,
    'results': model_results
}, os.path.join('models', 'model_metadata.joblib'))

print("All artifacts saved to 'models/' successfully!")
