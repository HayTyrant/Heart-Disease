import joblib
import streamlit as st
import numpy as np

model = joblib.load(open('grid.pkl', 'rb'))
scaler = joblib.load(open('scaler.pkl', 'rb'))

#Page Configuration
st.set_page_config(
    page_title='Heart Disease Prediction',
    page_icon='🫀',
    layout='centered',
    initial_sidebar_state='collapsed'
)

#Page Title and Style
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        color: #D2042D;
        font-size: 40px;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("<h1 class='main-title'>🫀 Heart Disease Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>An intelligent health prediction tool powered by Machine Learning</p>", unsafe_allow_html=True)

#st.title('Heart Prediction')

#st.write("""
#        This app uses a machine learning model trained on patient health data to predict the likelihood of heart disease.
#        By entering your health details such as age, blood pressure, cholesterol, and other indicators,  
#        the model analyzes your risk and provides a quick, data-driven prediction.  
#        This tool is designed to support early awareness, it is not a medical diagnosis. 
#         """)

st.subheader('Enter Patient Details')

age = st.number_input('Age: ', 18, 100, 40)
sex = st.selectbox('Sex: ', ['Male', 'Female'])
cp = st.selectbox('Type of chest pain: ', ['Typical angina', 'Atypical angina', 'Non-angina pain', 'Asymptomatic'])
trestbps = st.number_input('Resting blood sugar: ', 90,200,120)
chol = st.number_input('Serum cholestoral in mg/dl: ', 100,600,200)
fbs = st.selectbox('Fasting blood sugar above 120 mg/dl: ', ['Yes', 'No'])
restecg = st.selectbox('Resting electrocardiographic results: ', ['Normal', 'Having ST-T wave abnormality', 'Showing probable or definite left ventricular hypertrophy by Estes criteria'])
thalach = st.number_input('Maximum heart rate acheived: ', 60,220,150)
exang = st.selectbox('Exercise induced angina: ', ['Yes', 'No'])
oldpeak = st.number_input('ST depression induced by exercise relative to rest: ', 0.1,10.0,1.0, step=0.1)
slope = st.selectbox('T slope of the peak exercise ST segment: ', ['Upsloping', 'Flat', 'Downsloping'])
ca = st.selectbox('Number of major vessels: ', ['0','1','2','3'])
thal = st.selectbox('Thal condition: ', ['Normal', 'Fixed defect', 'Reversible defect'])

cp_mapping = {
    'Typical angina' : 0,
    'Atypical angina' : 1,
    'Non-anginal pain' : 2,
    'Asymptomatic' : 3
}
restecg_mapping = {
    'Normal' : 0, 
    'Having ST-T wave abnormality' : 1, 
    'Showing probable or definite left ventricular hypertrophy by Estes criteria' : 2
}
slope_mapping = {
    'Upsloping' : 0, 
    'Flat' : 1, 
    'Downsloping' : 2
}
thal_mapping = {
    'Normal' : 0, 
    'Fixed defect' : 1, 
    'Reversible defect' : 2
}

sex = 1 if sex == 'Male' else 0
cp = cp_mapping.get(cp)
fbs = 1 if fbs == 'Yes' else 0
restecg = restecg_mapping.get(restecg)
exang = 1 if exang == 'Yes' else 0
slope = slope_mapping.get(slope)
ca = int(ca)
thal = thal_mapping.get(thal)


if st.button('Predict'):
    input_data = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
    scaled_input = scaler.transform(input_data)
    prediction = model.predict(scaled_input)[0]
    probability = model.predict_proba(scaled_input)[0][1]
    #result = 'This patient does not have heart disease' if prediction == 0 else 'This patient has heart disease'
    #st.success(result)
    if prediction == 1:
        st.markdown(
            f"""
            <div style="background-color:#ff4b4b;padding:25px;border-radius:10px;text-align:center;">
                <h3 style="color:white;">🫀 This patient has <b>Heart Disease</b></h3>
                <p style="color:white;">Prediction confidence: {probability*100:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color:#4CAF50;padding:25px;border-radius:10px;text-align:center;">
                <h3 style="color:white;">🫀 This patient is <b>Healthy</b></h3>
                <p style="color:white;">Prediction confidence: {(1-probability)*100:.2f}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

#Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Made with ❤️ by Emmanuel | Powered by Logistic Regression</p>", unsafe_allow_html=True)