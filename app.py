import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import base64
import io

from health_risk_calculator import HealthRiskCalculator
from care_plan_generator import CareplanGenerator
from data_utils import DataUtils
from watson_ai_integration import WatsonAIIntegration

# Page configuration
st.set_page_config(
    page_title="Health AI - Risk Assessment & Care Planning",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
risk_calculator = HealthRiskCalculator()
care_generator = CareplanGenerator()
data_utils = DataUtils()

# Initialize Watson AI (with error handling)
try:
    watson_ai = WatsonAIIntegration()
    watson_available = True
except Exception as e:
    watson_ai = None
    watson_available = False
    print(f"Watson AI not available: {e}")

def main():
    # Main title
    st.title("🏥 Health AI - Risk Assessment & Care Planning")
    st.markdown("**AI-powered health risk prediction and personalized care planning system**")
    
    # Medical disclaimer
    st.warning("""
    **⚠️ MEDICAL DISCLAIMER**: This application is for educational and informational purposes only. 
    It does not provide medical advice, diagnosis, or treatment. Always consult with qualified healthcare 
    professionals for medical decisions. This tool should not replace professional medical consultation.
    """)
    
    # Sidebar for patient data input
    with st.sidebar:
        st.header("📋 Patient Information")
        
        # Basic Information
        st.subheader("Basic Details")
        age = st.number_input("Age", min_value=18, max_value=120, value=35, help="Patient's age in years")
        gender = st.selectbox("Gender", ["Male", "Female"], help="Biological sex")
        
        # Physical Measurements
        st.subheader("Physical Measurements")
        height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=170, help="Height in centimeters")
        weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=300, value=70, help="Weight in kilograms")
        
        # Calculate BMI
        bmi = weight_kg / ((height_cm / 100) ** 2)
        st.metric("BMI", f"{bmi:.1f}", help="Body Mass Index calculated automatically")
        
        # Vital Signs
        st.subheader("Vital Signs")
        systolic_bp = st.number_input("Systolic Blood Pressure", min_value=80, max_value=250, value=120, help="Upper blood pressure reading (mmHg)")
        diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=40, max_value=150, value=80, help="Lower blood pressure reading (mmHg)")
        resting_hr = st.number_input("Resting Heart Rate", min_value=40, max_value=150, value=72, help="Beats per minute at rest")
        
        # Laboratory Values
        st.subheader("Laboratory Values")
        fasting_glucose = st.number_input("Fasting Glucose (mg/dL)", min_value=50, max_value=400, value=90, help="Blood glucose after 8+ hours fasting")
        cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=180, help="Total cholesterol level")
        hdl_cholesterol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=150, value=50, help="High-density lipoprotein (good cholesterol)")
        
        # Lifestyle Factors
        st.subheader("Lifestyle Factors")
        smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"], help="Current smoking status")
        exercise_days = st.number_input("Exercise Days per Week", min_value=0, max_value=7, value=3, help="Days of moderate exercise per week")
        alcohol_consumption = st.selectbox("Alcohol Consumption", ["None", "Light", "Moderate", "Heavy"], help="Weekly alcohol consumption pattern")
        
        # Family History
        st.subheader("Family History")
        family_diabetes = st.checkbox("Family History of Diabetes", help="Diabetes in immediate family members")
        family_heart_disease = st.checkbox("Family History of Heart Disease", help="Heart disease in immediate family members")
        family_hypertension = st.checkbox("Family History of Hypertension", help="High blood pressure in immediate family members")
        
        # Medical History
        st.subheader("Medical History")
        existing_conditions = st.multiselect(
            "Existing Medical Conditions",
            ["None", "Prediabetes", "High Cholesterol", "Sleep Apnea", "Thyroid Disorder", "Kidney Disease"],
            default=["None"],
            help="Select all that apply"
        )
        
        medications = st.text_area("Current Medications", placeholder="List current medications (optional)", help="Include dosages if known")
        
        # Assessment button
        assess_button = st.button("🔍 Assess Health Risks", type="primary", use_container_width=True)
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Risk Assessment", "📋 Care Plan", "🤖 AI Health Analysis", "📊 Population Dashboard", "❓ Help & Info"])
    
    # Prepare patient data
    patient_data = {
        'age': age,
        'gender': gender,
        'height_cm': height_cm,
        'weight_kg': weight_kg,
        'bmi': bmi,
        'systolic_bp': systolic_bp,
        'diastolic_bp': diastolic_bp,
        'resting_hr': resting_hr,
        'fasting_glucose': fasting_glucose,
        'cholesterol': cholesterol,
        'hdl_cholesterol': hdl_cholesterol,
        'smoking': smoking,
        'exercise_days': exercise_days,
        'alcohol_consumption': alcohol_consumption,
        'family_diabetes': family_diabetes,
        'family_heart_disease': family_heart_disease,
        'family_hypertension': family_hypertension,
        'existing_conditions': existing_conditions,
        'medications': medications
    }
    
    with tab1:
        st.header("🎯 Health Risk Assessment")
        
        if assess_button:
            # Calculate risks
            try:
                diabetes_risk = risk_calculator.calculate_diabetes_risk(patient_data)
                heart_disease_risk = risk_calculator.calculate_heart_disease_risk(patient_data)
                hypertension_risk = risk_calculator.calculate_hypertension_risk(patient_data)
                
                # Store results in session state
                st.session_state['risks'] = {
                    'diabetes': diabetes_risk,
                    'heart_disease': heart_disease_risk,
                    'hypertension': hypertension_risk
                }
                st.session_state['patient_data'] = patient_data
                
            except Exception as e:
                st.error(f"Error calculating risks: {str(e)}")
                return
        
        # Display results if available
        if 'risks' in st.session_state:
            risks = st.session_state['risks']
            
            # Risk overview cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_color = "red" if risks['diabetes']['score'] >= 0.7 else "orange" if risks['diabetes']['score'] >= 0.4 else "green"
                st.metric(
                    "Diabetes Risk",
                    f"{risks['diabetes']['score']:.1%}",
                    delta=f"{risks['diabetes']['risk_level']} Risk",
                    delta_color="inverse"
                )
                
            with col2:
                risk_color = "red" if risks['heart_disease']['score'] >= 0.7 else "orange" if risks['heart_disease']['score'] >= 0.4 else "green"
                st.metric(
                    "Heart Disease Risk",
                    f"{risks['heart_disease']['score']:.1%}",
                    delta=f"{risks['heart_disease']['risk_level']} Risk",
                    delta_color="inverse"
                )
                
            with col3:
                risk_color = "red" if risks['hypertension']['score'] >= 0.7 else "orange" if risks['hypertension']['score'] >= 0.4 else "green"
                st.metric(
                    "Hypertension Risk",
                    f"{risks['hypertension']['score']:.1%}",
                    delta=f"{risks['hypertension']['risk_level']} Risk",
                    delta_color="inverse"
                )
            
            # Risk visualization
            st.subheader("Risk Score Visualization")
            
            # Create radar chart
            categories = ['Diabetes', 'Heart Disease', 'Hypertension']
            scores = [risks['diabetes']['score'], risks['heart_disease']['score'], risks['hypertension']['score']]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name='Risk Scores',
                line_color='rgb(255, 99, 71)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=True,
                title="Health Risk Profile"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed risk factors
            st.subheader("Risk Factor Analysis")
            
            for condition, risk_data in risks.items():
                with st.expander(f"{condition.replace('_', ' ').title()} Risk Factors"):
                    st.write(f"**Overall Risk Score:** {risk_data['score']:.1%} ({risk_data['risk_level']} Risk)")
                    st.write("**Contributing Factors:**")
                    for factor in risk_data['factors']:
                        st.write(f"• {factor}")
            
            # Download risk report
            if st.button("📄 Download Risk Assessment Report", use_container_width=True):
                report_data = data_utils.generate_risk_report(patient_data, risks)
                st.download_button(
                    label="Download Report (PDF)",
                    data=report_data,
                    file_name=f"health_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        else:
            st.info("👈 Please complete the patient information in the sidebar and click 'Assess Health Risks' to view results.")
    
    with tab2:
        st.header("📋 Personalized Care Plan")
        
        if 'risks' in st.session_state and 'patient_data' in st.session_state:
            risks = st.session_state['risks']
            patient_data = st.session_state['patient_data']
            
            # Generate care plans
            care_plans = care_generator.generate_comprehensive_care_plan(patient_data, risks)
            
            # Enhance with AI insights if Watson is available
            if watson_available and watson_ai:
                try:
                    care_plans = watson_ai.enhance_care_plan_with_ai(care_plans, patient_data, risks)
                except Exception as e:
                    print(f"Warning: Could not enhance care plan with AI: {e}")
            
            st.subheader("🤖 AI-Enhanced Personalized Recommendations")
            
            # Show Watson AI status
            if watson_available:
                st.success("✅ IBM Watson AI insights integrated")
            else:
                st.info("ℹ️ Running in standard mode (Watson AI not available)")
            
            # Display AI insights if available
            if 'ai_insights' in care_plans and care_plans['ai_insights']:
                st.markdown("### 🧠 AI-Powered Health Insights")
                for insight in care_plans['ai_insights']:
                    st.info(insight)
            
            # Display priority recommendations
            if 'priority_recommendations' in care_plans and care_plans['priority_recommendations']:
                st.markdown("### 🎯 Priority Actions")
                for priority in care_plans['priority_recommendations']:
                    st.warning(f"• {priority}")
            
            # Immediate actions
            if care_plans['immediate_actions']:
                st.markdown("### 🚨 Immediate Actions Required")
                for action in care_plans['immediate_actions']:
                    st.warning(f"• {action}")
            
            # Lifestyle modifications
            st.markdown("### 🏃‍♂️ Lifestyle Modifications")
            for category, recommendations in care_plans['lifestyle'].items():
                with st.expander(f"{category.replace('_', ' ').title()} Recommendations"):
                    for rec in recommendations:
                        st.write(f"• {rec}")
            
            # Medical follow-up
            st.markdown("### 🩺 Medical Follow-up")
            for item in care_plans['medical_followup']:
                st.info(f"• {item}")
            
            # Monitoring schedule
            st.markdown("### 📅 Monitoring Schedule")
            monitoring_df = pd.DataFrame(care_plans['monitoring_schedule'])
            st.dataframe(monitoring_df, use_container_width=True)
            
            # Download care plan
            if st.button("📄 Download Care Plan", use_container_width=True):
                care_plan_data = data_utils.generate_care_plan_document(patient_data, risks, care_plans)
                st.download_button(
                    label="Download Care Plan (Text)",
                    data=care_plan_data,
                    file_name=f"care_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        else:
            st.info("Please complete a risk assessment first to generate a personalized care plan.")
    
    with tab3:
        st.header("🤖 AI-Powered Health Analysis")
        
        if watson_available:
            st.success("✅ IBM Watson AI Natural Language Understanding active")
            
            # Symptom Analysis Section
            st.subheader("🩺 Intelligent Symptom Analysis")
            st.markdown("Describe any symptoms, health concerns, or questions in natural language:")
            
            symptoms_text = st.text_area(
                "Health Concerns Description",
                placeholder="Example: I've been feeling tired lately and have occasional headaches...",
                height=100,
                help="Describe your symptoms or health concerns in your own words. The AI will analyze the text for urgency and provide recommendations."
            )
            
            if st.button("🔍 Analyze with Watson AI", type="primary"):
                if symptoms_text.strip():
                    try:
                        with st.spinner("Analyzing your health concerns with IBM Watson AI..."):
                            analysis = watson_ai.analyze_symptoms_text(symptoms_text)
                        
                        st.markdown("### 📊 Analysis Results")
                        
                        # Urgency Level
                        urgency_color = {"low": "🟢", "moderate": "🟡", "high": "🔴"}
                        urgency_emoji = urgency_color.get(analysis['urgency_level'], "🟡")
                        st.metric("Urgency Level", f"{urgency_emoji} {analysis['urgency_level'].title()}")
                        
                        # Key Symptoms Identified
                        if analysis['key_symptoms']:
                            st.markdown("**Key Health Concepts Identified:**")
                            for symptom in analysis['key_symptoms']:
                                st.write(f"• {symptom}")
                        
                        # Recommendations
                        st.markdown("**AI Recommendations:**")
                        for rec in analysis['recommendations']:
                            if analysis['urgency_level'] == 'high':
                                st.error(f"• {rec}")
                            elif analysis['urgency_level'] == 'moderate':
                                st.warning(f"• {rec}")
                            else:
                                st.info(f"• {rec}")
                        
                        # Sentiment Analysis
                        if 'sentiment_analysis' in analysis and analysis['sentiment_analysis']:
                            sentiment = analysis['sentiment_analysis']
                            if 'score' in sentiment:
                                st.markdown("**Emotional Tone Analysis:**")
                                score = sentiment.get('score', 0)
                                label = sentiment.get('label', 'neutral')
                                if score > 0.1:
                                    st.success(f"Positive tone detected (confidence: {abs(score):.2f})")
                                elif score < -0.1:
                                    st.error(f"Negative tone detected (confidence: {abs(score):.2f})")
                                else:
                                    st.info("Neutral tone detected")
                        
                    except Exception as e:
                        st.error(f"Error analyzing symptoms: {str(e)}")
                        st.info("Please ensure your IBM Watson credentials are correctly configured.")
                else:
                    st.warning("Please enter your health concerns or symptoms to analyze.")
            
            # Health Education Section
            st.subheader("📚 AI-Enhanced Health Education")
            
            condition_options = ["diabetes", "heart_disease", "hypertension"]
            selected_condition = st.selectbox(
                "Select a condition to learn more about:",
                options=condition_options,
                format_func=lambda x: x.replace('_', ' ').title()
            )
            
            if st.button("📖 Get Health Education Content"):
                try:
                    education_content = watson_ai.get_health_education_content(selected_condition)
                    
                    st.markdown(f"### {selected_condition.replace('_', ' ').title()} Information")
                    
                    st.markdown("**Overview:**")
                    st.write(education_content.get('overview', 'No information available'))
                    
                    st.markdown("**Prevention Tips:**")
                    for tip in education_content.get('prevention_tips', []):
                        st.write(f"• {tip}")
                    
                    st.markdown("**Warning Signs:**")
                    for sign in education_content.get('warning_signs', []):
                        st.write(f"• {sign}")
                        
                except Exception as e:
                    st.error(f"Error retrieving education content: {str(e)}")
            
            # Patient Data Analysis
            if 'risks' in st.session_state and 'patient_data' in st.session_state:
                st.subheader("🎯 Personalized AI Health Insights")
                
                try:
                    insights = watson_ai.generate_personalized_insights(
                        st.session_state['patient_data'], 
                        st.session_state['risks']
                    )
                    
                    st.markdown("Based on your health profile, here are AI-generated insights:")
                    for insight in insights:
                        st.info(insight)
                        
                except Exception as e:
                    st.error(f"Error generating insights: {str(e)}")
            else:
                st.info("Complete a risk assessment first to get personalized AI insights.")
                
        else:
            st.warning("⚠️ IBM Watson AI is not available")
            st.info("To enable AI features, please ensure IBM Watson credentials are properly configured.")
            st.markdown("""
            **Required Environment Variables:**
            - `IBM_WATSON_API_KEY`: Your Watson service API key
            - `IBM_WATSON_URL`: Your Watson service URL
            
            **Features available with Watson AI:**
            - 🧠 Intelligent symptom analysis
            - 📊 Sentiment and emotion analysis of health concerns  
            - 🎯 Enhanced personalized insights
            - 📚 AI-powered health education content
            - 🔍 Natural language processing of health descriptions
            """)
    
    with tab4:
        st.header("📊 Population Health Dashboard")
        
        # Sample data generation
        st.subheader("Population Data Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.markdown("### Data Management")
            
            # Generate sample data
            if st.button("🔄 Generate Sample Population Data", use_container_width=True):
                sample_data = data_utils.generate_sample_population_data(100)
                st.session_state['population_data'] = sample_data
                st.success("Sample data generated successfully!")
            
            # File upload
            uploaded_file = st.file_uploader("📁 Upload Population Data (CSV)", type=['csv'])
            if uploaded_file is not None:
                try:
                    population_data = pd.read_csv(uploaded_file)
                    st.session_state['population_data'] = population_data
                    st.success("Data uploaded successfully!")
                except Exception as e:
                    st.error(f"Error uploading file: {str(e)}")
        
        with col1:
            # Display population analytics
            if 'population_data' in st.session_state:
                pop_data = st.session_state['population_data']
                
                st.markdown("### Population Risk Distribution")
                
                # Risk distribution charts
                risk_cols = ['diabetes_risk', 'heart_disease_risk', 'hypertension_risk']
                
                for risk_col in risk_cols:
                    if risk_col in pop_data.columns:
                        fig = px.histogram(
                            pop_data, 
                            x=risk_col, 
                            title=f"{risk_col.replace('_', ' ').title()} Distribution",
                            nbins=20
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Risk by demographics
                if 'age' in pop_data.columns and 'gender' in pop_data.columns:
                    st.markdown("### Risk by Demographics")
                    
                    # Age group analysis
                    pop_data['age_group'] = pd.cut(pop_data['age'], bins=[0, 30, 45, 60, 100], labels=['18-30', '31-45', '46-60', '60+'])
                    
                    risk_by_age = pop_data.groupby('age_group')[risk_cols].mean().reset_index()
                    
                    fig = px.bar(
                        risk_by_age.melt(id_vars='age_group', var_name='risk_type', value_name='avg_risk'),
                        x='age_group',
                        y='avg_risk',
                        color='risk_type',
                        title="Average Risk Scores by Age Group",
                        barmode='group'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Download enriched dataset
                if st.button("📥 Download Enriched Dataset", use_container_width=True):
                    csv_data = pop_data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"enriched_population_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                # Data summary
                st.markdown("### Dataset Summary")
                st.write(f"**Total Records:** {len(pop_data)}")
                st.write(f"**Features:** {len(pop_data.columns)}")
                
                # Display first few rows
                st.markdown("### Data Preview")
                st.dataframe(pop_data.head(), use_container_width=True)
                
            else:
                st.info("Generate sample data or upload a CSV file to view population analytics.")
    
    with tab5:
        st.header("❓ Help & Information")
        
        # About the application
        st.subheader("About Health AI")
        st.markdown("""
        Health AI is an educational tool designed to help understand health risks and promote preventive care. 
        It uses evidence-based algorithms to assess risk factors for common chronic conditions.
        
        **Key Features:**
        - **Risk Assessment**: Calculates probability scores for diabetes, heart disease, and hypertension
        - **Personalized Care Plans**: Generates customized recommendations based on individual risk profiles
        - **Population Analytics**: Analyzes health trends across groups of patients
        - **Educational Resources**: Provides information about risk factors and prevention strategies
        """)
        
        # How it works
        st.subheader("How Risk Calculation Works")
        st.markdown("""
        Our risk calculation algorithms use validated medical criteria and research-based risk factors:
        
        **Diabetes Risk Factors:**
        - Age, BMI, family history
        - Fasting glucose levels
        - Blood pressure, physical activity
        - Demographic factors
        
        **Heart Disease Risk Factors:**
        - Age, gender, smoking status
        - Cholesterol levels (total and HDL)
        - Blood pressure, BMI
        - Family history, exercise habits
        
        **Hypertension Risk Factors:**
        - Current blood pressure readings
        - Age, BMI, sodium intake
        - Family history, lifestyle factors
        - Existing medical conditions
        """)
        
        # Risk level interpretation
        st.subheader("Risk Level Interpretation")
        
        risk_table = pd.DataFrame({
            'Risk Level': ['Low', 'Moderate', 'High'],
            'Score Range': ['0-39%', '40-69%', '70-100%'],
            'Interpretation': [
                'Below average risk, maintain healthy lifestyle',
                'Elevated risk, consider preventive measures',
                'High risk, medical consultation recommended'
            ],
            'Recommended Action': [
                'Continue current healthy practices',
                'Implement lifestyle modifications',
                'Seek immediate medical evaluation'
            ]
        })
        
        st.dataframe(risk_table, use_container_width=True)
        
        # Limitations and disclaimers
        st.subheader("Important Limitations")
        st.warning("""
        **Please note the following limitations:**
        
        - This tool is for educational purposes only and should not replace professional medical advice
        - Risk predictions are based on population studies and may not reflect individual circumstances
        - Many health factors cannot be captured in a simple questionnaire
        - Results should be discussed with qualified healthcare professionals
        - Emergency medical situations require immediate professional care
        - The tool does not diagnose medical conditions
        """)
        
        # Contact and support
        st.subheader("Support & Resources")
        st.markdown("""
        **For Medical Emergencies:** Call your local emergency number immediately
        
        **Healthcare Resources:**
        - Consult your primary care physician for personalized medical advice
        - Visit certified healthcare facilities for comprehensive health assessments
        - Consider preventive health screenings based on age and risk factors
        
        **Technical Support:**
        - Report application issues through your healthcare system's IT support
        - Ensure data privacy by not sharing personal health information unnecessarily
        """)

if __name__ == "__main__":
    main()
