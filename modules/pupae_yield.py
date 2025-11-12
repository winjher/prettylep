import streamlit as st
import numpy as np
import pandas as pd
import joblib # Used for caching/saving model components

# --- ML/DL Imports ---
# FIX: Ensuring train_test_split is imported for use in train_models function
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# --- 1. Deep Learning Check and Imports ---
try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout
    DL_AVAILABLE = True
except ImportError:
    DL_AVAILABLE = False


# --- 2. Configuration and Data Simulation (Modified) ---

# Define the full list of species
SPECIES_LIST = [
    'Butterfly-Clippers', 'Butterfly-Common Jay', 'Butterfly-Common Lime',
    'Butterfly-Common Mime', 'Butterfly-Common Mormon', 'Butterfly-Emerald Swallowtail',
    'Butterfly-Golden Birdwing', 'Butterfly-Gray Glassy Tiger', 'Butterfly-Great Eggfly',
    'Butterfly-Great Yellow Mormon', 'Butterfly-Paper Kite', 'Butterfly-Pink Rose',
    'Butterfly-Plain Tiger', 'Butterfly-Red Lacewing', 'Butterfly-Scarlet Mormon',
    'Butterfly-Tailed Jay', 'Moth-Atlas', 'Moth-Luzon Lesser'
]

# Define all feature columns
FEATURE_COLUMNS = [
    'Temperature_C', 'Humidity_Perc', 'Airflow_CFM', 'Larval_Density_per_sqm',
    'Protein_Feed_Perc', 'Substrate_Moisture_Perc', 'Cycle_Day', 'Mortality_Rate_Perc',
    'Larval_Development_Observation', 'Ants_Pee_Contamination',
    'Dietary_Toxicity_Score', 'Environmental_Turbulence_Score'
]

@st.cache_data
def generate_simulated_data(n_samples=5000):
    """
    Generates a simulated dataset with new risk factors and species.
    """
    data = {
        # Environmental and Larval Metrics (from original script)
        'Temperature_C': np.random.uniform(25, 32, n_samples),
        'Humidity_Perc': np.random.uniform(50, 75, n_samples),
        'Airflow_CFM': np.random.uniform(100, 300, n_samples),
        'Larval_Density_per_sqm': np.random.uniform(10000, 40000, n_samples),
        'Protein_Feed_Perc': np.random.uniform(15, 30, n_samples),
        'Substrate_Moisture_Perc': np.random.uniform(60, 80, n_samples),
        'Cycle_Day': np.random.randint(15, 25, n_samples),
        'Mortality_Rate_Perc': np.random.uniform(0.5, 5.0, n_samples),

        # New Risk Factors (0=Low Risk, 10=High Risk/Deviation)
        # Larval Development Observations (e.g., deviation from expected size/color)
        'Larval_Development_Observation': np.random.uniform(0, 5, n_samples),
        # Ant's pee chemical contamination score (e.g., formicine acid exposure)
        'Ants_Pee_Contamination': np.random.uniform(0, 10, n_samples),
        # Dietary toxicity of dried leaves (e.g., secondary metabolites)
        'Dietary_Toxicity_Score': np.random.uniform(0, 10, n_samples),
        # Environmental turbulence (travel/transfer stress)
        'Environmental_Turbulence_Score': np.random.uniform(0, 8, n_samples),

        # Categorical Species Data
        'Species': np.random.choice(SPECIES_LIST, n_samples)
    }

    df = pd.DataFrame(data)

    # Base Yield Calculation (linear combination)
    df['Pupae_Yield_g'] = (
        + 0.5 * df['Temperature_C']
        + 5.0 * df['Protein_Feed_Perc']
        - 10.0 * df['Mortality_Rate_Perc']
        - 0.001 * df['Larval_Density_per_sqm']
    )

    # Apply Penalties for New Risk Factors (non-linear impact)
    df['Pupae_Yield_g'] -= (
        + 15.0 * df['Larval_Development_Observation']
        + 25.0 * np.log1p(df['Ants_Pee_Contamination']) # Logarithmic penalty
        + 30.0 * df['Dietary_Toxicity_Score'] ** 0.5
        + 10.0 * df['Environmental_Turbulence_Score']
    )

    # Species-Specific Baseline (Moths generally yield more than certain Butterflies)
    species_yield_map = {
        'Moth-Atlas': 1200, 'Moth-Luzon Lesser': 900, 'Butterfly-Golden Birdwing': 1100,
        'Butterfly-Paper Kite': 750, 'Butterfly-Common Mormon': 850
    }
    df['Species_Base_Yield'] = df['Species'].apply(lambda x: species_yield_map.get(x, 600))
    df['Pupae_Yield_g'] += df['Species_Base_Yield']

    # Add final noise and ensure non-negative, plausible yields
    df['Pupae_Yield_g'] += np.random.normal(0, 75, n_samples)
    df['Pupae_Yield_g'] = np.maximum(200, df['Pupae_Yield_g']) # Min viable yield

    return df.drop(columns=['Species_Base_Yield'])


# --- 3. Model Training Function ---

@st.cache_resource
def train_models(df):
    """Encodes data, splits, trains RF and DL models, and returns components."""
    
    # One-Hot Encode the Species column
    X = pd.get_dummies(df.drop('Pupae_Yield_g', axis=1), columns=['Species'], drop_first=True)
    y = df['Pupae_Yield_g']
    
    # train_test_split is now correctly in scope from the imports section
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. Random Forest (ML)
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=12)
    rf_model.fit(X_train, y_train)

    # Store the final feature column names after encoding
    final_features = X_train.columns.tolist()

    # 2. Deep Learning (DL)
    dl_model, scaler_X = None, None
    if DL_AVAILABLE:
        # Standard Scaler for DL model
        scaler_X = StandardScaler()
        X_train_scaled = scaler_X.fit_transform(X_train)

        dl_model = Sequential([
            Dense(128, activation='relu', input_shape=(X_train_scaled.shape[1],)),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        dl_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        dl_model.fit(X_train_scaled, y_train, epochs=40, batch_size=32, verbose=0, validation_split=0.1)

    return rf_model, dl_model, scaler_X, final_features, X_test, y_test


# --- 4. Prediction Function ---

def make_prediction(rf_model, dl_model, scaler_X, final_features, user_inputs):
    """Processes user input and predicts yield using the models."""

    # Create a DataFrame from user inputs
    input_df = pd.DataFrame([user_inputs])

    # Handle Categorical Encoding
    species_col = input_df['Species']
    input_df = input_df.drop(columns=['Species'])

    # Recreate the one-hot encoding structure expected by the model
    prediction_df = pd.DataFrame(0, index=[0], columns=final_features)
    
    # Fill in the user's continuous values
    for col in FEATURE_COLUMNS:
        if col in prediction_df.columns:
            prediction_df.loc[0, col] = input_df.loc[0, col]

    # Fill in the user's species choice in the correct one-hot column
    species_encoded_name = f'Species_{species_col.iloc[0]}'
    if species_encoded_name in prediction_df.columns:
        prediction_df.loc[0, species_encoded_name] = 1

    # --- Random Forest Prediction ---
    rf_pred = rf_model.predict(prediction_df)[0]
    
    # Get Feature Importance
    importances = pd.Series(rf_model.feature_importances_, index=rf_model.feature_names_in_)
    top_importances = importances.nlargest(5)
    
    # --- Deep Learning Prediction ---
    dl_pred = None
    if DL_AVAILABLE:
        # Scale the input data using the trained scaler
        input_scaled = scaler_X.transform(prediction_df)
        dl_pred = dl_model.predict(input_scaled).flatten()[0]

    return rf_pred, dl_pred, top_importances


# --- 5. Streamlit Application Layout ---

def main():
    st.set_page_config(layout="wide", page_title="Lepidoptera Pupae Harvest Predictor")

    st.title("🦋 Pupae Harvest Yield Estimator")
    st.markdown("A Machine Learning tool to predict pupae harvest (grams/tray) based on environmental, larval, and critical risk factors.")
    st.sidebar.header("Model Training Status")

    # 1. Generate and Train Models (Cached)
    with st.spinner('Generating synthetic data and training models...'):
        df_simulated = generate_simulated_data()
        rf_model, dl_model, scaler_X, final_features, X_test, y_test = train_models(df_simulated)
    
    st.sidebar.success("Model Training Complete! (5,000 samples)")

    # 2. Model Evaluation (Display metrics)
    y_pred_rf_test = rf_model.predict(X_test)
    rf_mae = mean_absolute_error(y_test, y_pred_rf_test)
    rf_r2 = r2_score(y_test, y_pred_rf_test)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Model Performance (Test Set)")
    st.sidebar.metric(label="Random Forest MAE (g)", value=f"${rf_mae:,.2f}")
    st.sidebar.metric(label="Random Forest R²", value=f"{rf_r2:.4f}")

    if DL_AVAILABLE:
        X_test_scaled = scaler_X.transform(X_test)
        _, dl_mae = dl_model.evaluate(X_test_scaled, y_test, verbose=0)
        y_pred_dl_test = dl_model.predict(X_test_scaled, verbose=0).flatten()
        dl_r2 = r2_score(y_test, y_pred_dl_test)
        st.sidebar.metric(label="Deep Learning MAE (g)", value=f"${dl_mae:,.2f}")
        st.sidebar.metric(label="Deep Learning R²", value=f"{dl_r2:.4f}")
    else:
        st.sidebar.warning("TensorFlow not installed. DL predictions disabled.")
    
    st.markdown("---")
    
    # 3. User Input Interface (Main Content)
    
    col1, col2, col3 = st.columns(3)

    # --- Column 1: Core Metrics ---
    col1.header("Core Farming Inputs")
    input_species = col1.selectbox("Species", SPECIES_LIST, index=SPECIES_LIST.index('Moth-Atlas'))
    input_temp = col1.slider("Temperature ($^\circ$C)", 25.0, 32.0, 28.0)
    input_humidity = col1.slider("Humidity (%)", 50.0, 75.0, 65.0)
    input_airflow = col1.number_input("Airflow (CFM)", 100, 300, 200)
    
    # --- Column 2: Larval/Feed Metrics ---
    col2.header("Larval & Substrate Metrics")
    input_density = col2.number_input("Larval Density ($m^{-2}$)", 10000, 40000, 25000)
    input_protein = col2.slider("Protein Feed (%)", 15.0, 30.0, 22.0)
    input_moisture = col2.slider("Substrate Moisture (%)", 60.0, 80.0, 70.0)
    input_day = col2.slider("Cycle Day (15-25)", 15, 25, 20)
    input_mortality = col2.slider("Mortality Rate (%)", 0.5, 5.0, 1.5)

    # --- Column 3: Advanced Risk Factors ---
    col3.header("Risk Assessment Scores (0=Low, 10=High)")
    
    # Scores are based on observed deviation or testing results
    # input_obs = col3.slider("Larval Development Observations (Deviation)", 0.0, 10.0, 1.0, 0.1)
    # col3.caption("Score higher for poor color, slow growth, or unusual behavior.")
    
    input_contam = col3.slider("Ant's Pee Chemical Contamination Score", 0.0, 10.0, 0.5, 0.1)
    col3.caption("Score based on lab testing of substrate for formicine acids/ammonia traces.")
    
    input_tox = col3.slider("Dietary Toxicity of Dried Leaves (Score)", 0.0, 10.0, 1.0, 0.1)
    col3.caption("Score based on presence of known anti-feedants or secondary metabolites in feed.")
    
    input_turb = col3.slider("Environmental Turbulence (Travel/Transfer Stress)", 0.0, 10.0, 1.0, 0.1)
    col3.caption("Score based on frequency and duration of travel/transfer events.")

    
    # --- Prediction Button and Output ---
    st.markdown("---")
    
    user_inputs = {
        'Species': input_species,
        'Temperature_C': input_temp,
        'Humidity_Perc': input_humidity,
        'Airflow_CFM': input_airflow,
        'Larval_Density_per_sqm': input_density,
        'Protein_Feed_Perc': input_protein,
        'Substrate_Moisture_Perc': input_moisture,
        'Cycle_Day': input_day,
        'Mortality_Rate_Perc': input_mortality,
        'Larval_Development_Observation': input_obs,
        'Ants_Pee_Contamination': input_contam,
        'Dietary_Toxicity_Score': input_tox,
        'Environmental_Turbulence_Score': input_turb
    }
    
    
    if st.button("Calculate Potential Harvest Yield", type="primary"):
        rf_pred, dl_pred, top_importances = make_prediction(
            rf_model, dl_model, scaler_X, final_features, user_inputs
        )
        
        st.subheader("Predicted Pupae Harvest")
        
        pred_col1, pred_col2, pred_col3 = st.columns([1, 1, 2])
        
        pred_col1.metric("Random Forest Prediction (g)", f"${rf_pred:,.2f}")
        
        if DL_AVAILABLE:
             pred_col2.metric("Deep Learning Prediction (g)", f"${dl_pred:,.2f}")
        else:
             pred_col2.metric("Deep Learning", "N/A (TF Missing)")

        st.subheader("Key Impact Factors (Random Forest)")
        st.bar_chart(top_importances)
        st.markdown(
            """
            <div style='font-size: small; color: gray;'>
            *The chart above shows the top 5 features the Random Forest model considered most important 
            in making this specific prediction.*
            </div>
            """, 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
