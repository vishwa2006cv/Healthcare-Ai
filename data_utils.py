import pandas as pd
import numpy as np
import base64
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class DataUtils:
    """
    Utility class for data processing, report generation, and sample data creation
    """
    
    def __init__(self):
        self.sample_conditions = [
            "None", "Prediabetes", "High Cholesterol", "Sleep Apnea", 
            "Thyroid Disorder", "Kidney Disease"
        ]
        
        self.sample_medications = [
            "", "Metformin", "Lisinopril", "Atorvastatin", "Aspirin", 
            "Levothyroxine", "Amlodipine", "Metoprolol"
        ]
    
    def generate_sample_population_data(self, num_patients: int = 100) -> pd.DataFrame:
        """
        Generate sample population data for testing and demonstration
        """
        np.random.seed(42)  # For reproducible results
        
        # Basic demographics
        ages = np.random.normal(45, 15, num_patients).astype(int)
        ages = np.clip(ages, 18, 85)
        
        genders = np.random.choice(["Male", "Female"], num_patients, p=[0.48, 0.52])
        
        # Physical measurements
        heights = np.where(
            genders == "Male", 
            np.random.normal(175, 10, num_patients),
            np.random.normal(162, 8, num_patients)
        )
        heights = np.clip(heights, 150, 200)
        
        # Weight correlated with age and height
        base_weights = np.where(
            genders == "Male",
            heights * 0.8 - 60,
            heights * 0.7 - 50
        )
        weight_variation = np.random.normal(0, 15, num_patients)
        age_weight_factor = (ages - 25) * 0.3  # Weight tends to increase with age
        weights = base_weights + weight_variation + age_weight_factor
        weights = np.clip(weights, 45, 150)
        
        bmis = weights / ((heights / 100) ** 2)
        
        # Vital signs with some correlation to BMI and age
        systolic_base = 110 + (ages - 20) * 0.5 + (bmis - 22) * 1.2
        systolic_bp = systolic_base + np.random.normal(0, 10, num_patients)
        systolic_bp = np.clip(systolic_bp, 90, 200).astype(int)
        
        diastolic_bp = (systolic_bp * 0.6 + np.random.normal(0, 8, num_patients)).astype(int)
        diastolic_bp = np.clip(diastolic_bp, 60, 120)
        
        resting_hr = np.random.normal(72, 12, num_patients).astype(int)
        resting_hr = np.clip(resting_hr, 50, 100)
        
        # Laboratory values with risk correlations
        glucose_base = 85 + (ages - 30) * 0.3 + (bmis - 22) * 1.5
        fasting_glucose = glucose_base + np.random.normal(0, 15, num_patients)
        fasting_glucose = np.clip(fasting_glucose, 70, 250).astype(int)
        
        cholesterol_base = 170 + (ages - 30) * 0.8
        cholesterol = cholesterol_base + np.random.normal(0, 30, num_patients)
        cholesterol = np.clip(cholesterol, 120, 350).astype(int)
        
        hdl_base = np.where(genders == "Male", 45, 55)
        hdl_cholesterol = hdl_base + np.random.normal(0, 12, num_patients)
        hdl_cholesterol = np.clip(hdl_cholesterol, 25, 90).astype(int)
        
        # Lifestyle factors
        smoking_status = np.random.choice(
            ["Never", "Former", "Current"], 
            num_patients, 
            p=[0.6, 0.25, 0.15]
        )
        
        exercise_days = np.random.choice(range(8), num_patients, p=[0.1, 0.15, 0.2, 0.25, 0.15, 0.1, 0.03, 0.02])
        
        alcohol_consumption = np.random.choice(
            ["None", "Light", "Moderate", "Heavy"],
            num_patients,
            p=[0.3, 0.4, 0.25, 0.05]
        )
        
        # Family history (age-correlated)
        family_diabetes_prob = np.clip((ages - 30) / 100 + 0.15, 0.1, 0.4)
        family_diabetes = np.random.binomial(1, family_diabetes_prob, num_patients).astype(bool)
        
        family_heart_disease_prob = np.clip((ages - 35) / 80 + 0.2, 0.15, 0.45)
        family_heart_disease = np.random.binomial(1, family_heart_disease_prob, num_patients).astype(bool)
        
        family_hypertension_prob = np.clip((ages - 25) / 60 + 0.25, 0.2, 0.5)
        family_hypertension = np.random.binomial(1, family_hypertension_prob, num_patients).astype(bool)
        
        # Medical conditions
        existing_conditions = []
        for i in range(num_patients):
            conditions = ["None"]
            if fasting_glucose[i] > 100 and np.random.random() < 0.3:
                conditions = ["Prediabetes"]
            if cholesterol[i] > 200 and np.random.random() < 0.4:
                if "None" in conditions:
                    conditions = ["High Cholesterol"]
                else:
                    conditions.append("High Cholesterol")
            if bmis[i] > 30 and np.random.random() < 0.2:
                if "None" in conditions:
                    conditions = ["Sleep Apnea"]
                else:
                    conditions.append("Sleep Apnea")
            existing_conditions.append(conditions)
        
        # Medications
        medications = []
        for i in range(num_patients):
            meds = []
            if "Prediabetes" in existing_conditions[i] and np.random.random() < 0.6:
                meds.append("Metformin")
            if systolic_bp[i] > 140 and np.random.random() < 0.7:
                meds.append(np.random.choice(["Lisinopril", "Amlodipine", "Metoprolol"]))
            if cholesterol[i] > 200 and np.random.random() < 0.5:
                meds.append("Atorvastatin")
            medications.append(", ".join(meds))
        
        # Create DataFrame
        df = pd.DataFrame({
            'patient_id': [f"P{i+1:04d}" for i in range(num_patients)],
            'age': ages,
            'gender': genders,
            'height_cm': heights.round(1),
            'weight_kg': weights.round(1),
            'bmi': bmis.round(1),
            'systolic_bp': systolic_bp,
            'diastolic_bp': diastolic_bp,
            'resting_hr': resting_hr,
            'fasting_glucose': fasting_glucose,
            'cholesterol': cholesterol,
            'hdl_cholesterol': hdl_cholesterol,
            'smoking': smoking_status,
            'exercise_days': exercise_days,
            'alcohol_consumption': alcohol_consumption,
            'family_diabetes': family_diabetes,
            'family_heart_disease': family_heart_disease,
            'family_hypertension': family_hypertension,
            'existing_conditions': [str(cond) for cond in existing_conditions],
            'medications': medications
        })
        
        # Calculate risk scores for population
        from health_risk_calculator import HealthRiskCalculator
        calculator = HealthRiskCalculator()
        
        diabetes_risks = []
        heart_disease_risks = []
        hypertension_risks = []
        
        for idx, row in df.iterrows():
            patient_data = row.to_dict()
            patient_data['existing_conditions'] = eval(patient_data['existing_conditions'])
            
            try:
                diabetes_risk = calculator.calculate_diabetes_risk(patient_data)
                heart_disease_risk = calculator.calculate_heart_disease_risk(patient_data)
                hypertension_risk = calculator.calculate_hypertension_risk(patient_data)
                
                diabetes_risks.append(diabetes_risk['score'])
                heart_disease_risks.append(heart_disease_risk['score'])
                hypertension_risks.append(hypertension_risk['score'])
                
            except Exception as e:
                # Handle any calculation errors
                diabetes_risks.append(0.0)
                heart_disease_risks.append(0.0)
                hypertension_risks.append(0.0)
        
        df['diabetes_risk'] = diabetes_risks
        df['heart_disease_risk'] = heart_disease_risks
        df['hypertension_risk'] = hypertension_risks
        
        # Add risk categories
        df['diabetes_risk_category'] = pd.cut(df['diabetes_risk'], 
                                            bins=[0, 0.4, 0.7, 1.0], 
                                            labels=['Low', 'Moderate', 'High'])
        df['heart_disease_risk_category'] = pd.cut(df['heart_disease_risk'], 
                                                 bins=[0, 0.4, 0.7, 1.0], 
                                                 labels=['Low', 'Moderate', 'High'])
        df['hypertension_risk_category'] = pd.cut(df['hypertension_risk'], 
                                                bins=[0, 0.4, 0.7, 1.0], 
                                                labels=['Low', 'Moderate', 'High'])
        
        return df
    
    def generate_risk_report(self, patient_data: Dict[str, Any], risks: Dict[str, Any]) -> str:
        """
        Generate a comprehensive risk assessment report
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("HEALTH RISK ASSESSMENT REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Patient information
        report_lines.append("PATIENT INFORMATION")
        report_lines.append("-" * 30)
        report_lines.append(f"Age: {patient_data['age']} years")
        report_lines.append(f"Gender: {patient_data['gender']}")
        report_lines.append(f"Height: {patient_data['height_cm']} cm")
        report_lines.append(f"Weight: {patient_data['weight_kg']} kg")
        report_lines.append(f"BMI: {patient_data['bmi']:.1f}")
        report_lines.append("")
        
        # Vital signs
        report_lines.append("VITAL SIGNS")
        report_lines.append("-" * 30)
        report_lines.append(f"Blood Pressure: {patient_data['systolic_bp']}/{patient_data['diastolic_bp']} mmHg")
        report_lines.append(f"Resting Heart Rate: {patient_data['resting_hr']} bpm")
        report_lines.append("")
        
        # Laboratory values
        report_lines.append("LABORATORY VALUES")
        report_lines.append("-" * 30)
        report_lines.append(f"Fasting Glucose: {patient_data['fasting_glucose']} mg/dL")
        report_lines.append(f"Total Cholesterol: {patient_data['cholesterol']} mg/dL")
        report_lines.append(f"HDL Cholesterol: {patient_data['hdl_cholesterol']} mg/dL")
        report_lines.append("")
        
        # Risk assessment results
        report_lines.append("RISK ASSESSMENT RESULTS")
        report_lines.append("-" * 30)
        
        for condition, risk_data in risks.items():
            condition_name = condition.replace('_', ' ').title()
            report_lines.append(f"{condition_name} Risk: {risk_data['score']:.1%} ({risk_data['risk_level']} Risk)")
            report_lines.append("Contributing Factors:")
            for factor in risk_data['factors']:
                report_lines.append(f"  • {factor}")
            report_lines.append("")
        
        # Recommendations summary
        report_lines.append("KEY RECOMMENDATIONS")
        report_lines.append("-" * 30)
        
        # High-priority recommendations based on highest risk
        max_risk = max(risks[condition]['score'] for condition in risks)
        if max_risk >= 0.7:
            report_lines.append("HIGH PRIORITY ACTIONS:")
            report_lines.append("• Schedule medical consultation within 2 weeks")
            report_lines.append("• Begin intensive lifestyle modifications immediately")
            report_lines.append("• Consider medication evaluation with physician")
        elif max_risk >= 0.4:
            report_lines.append("MODERATE PRIORITY ACTIONS:")
            report_lines.append("• Schedule medical consultation within 1 month")
            report_lines.append("• Implement lifestyle modifications")
            report_lines.append("• Increase monitoring frequency")
        else:
            report_lines.append("MAINTENANCE ACTIONS:")
            report_lines.append("• Continue current healthy practices")
            report_lines.append("• Regular preventive care")
            report_lines.append("• Annual health assessments")
        
        report_lines.append("")
        
        # Disclaimer
        report_lines.append("IMPORTANT DISCLAIMER")
        report_lines.append("-" * 30)
        report_lines.append("This assessment is for educational purposes only and should not")
        report_lines.append("replace professional medical advice. Please consult with qualified")
        report_lines.append("healthcare professionals for personalized medical care.")
        report_lines.append("")
        report_lines.append("=" * 60)
        
        return "\n".join(report_lines)
    
    def generate_care_plan_document(self, patient_data: Dict[str, Any], risks: Dict[str, Any], care_plans: Dict[str, Any]) -> str:
        """
        Generate a comprehensive care plan document
        """
        doc_lines = []
        doc_lines.append("=" * 60)
        doc_lines.append("PERSONALIZED HEALTH CARE PLAN")
        doc_lines.append("=" * 60)
        doc_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc_lines.append(f"Patient Age: {patient_data['age']} years")
        doc_lines.append("")
        
        # Immediate actions
        if care_plans['immediate_actions']:
            doc_lines.append("IMMEDIATE ACTIONS REQUIRED")
            doc_lines.append("-" * 40)
            for action in care_plans['immediate_actions']:
                doc_lines.append(f"• {action}")
            doc_lines.append("")
        
        # Lifestyle modifications
        doc_lines.append("LIFESTYLE MODIFICATION PLAN")
        doc_lines.append("-" * 40)
        
        for category, recommendations in care_plans['lifestyle'].items():
            if recommendations:
                category_title = category.replace('_', ' ').title()
                doc_lines.append(f"\n{category_title}:")
                for rec in recommendations:
                    doc_lines.append(f"  • {rec}")
        
        doc_lines.append("")
        
        # Medical follow-up
        doc_lines.append("MEDICAL FOLLOW-UP SCHEDULE")
        doc_lines.append("-" * 40)
        for followup in care_plans['medical_followup']:
            doc_lines.append(f"• {followup}")
        doc_lines.append("")
        
        # Monitoring schedule
        doc_lines.append("MONITORING SCHEDULE")
        doc_lines.append("-" * 40)
        for item in care_plans['monitoring_schedule']:
            doc_lines.append(f"Parameter: {item['Parameter']}")
            doc_lines.append(f"  Frequency: {item['Frequency']}")
            doc_lines.append(f"  Target: {item['Target']}")
            doc_lines.append(f"  Action: {item['Action']}")
            doc_lines.append("")
        
        # Goals and expectations
        doc_lines.append("HEALTH GOALS & EXPECTATIONS")
        doc_lines.append("-" * 40)
        doc_lines.append("• Reduce overall cardiovascular risk by 20% within 6 months")
        doc_lines.append("• Achieve and maintain healthy BMI (18.5-24.9)")
        doc_lines.append("• Establish consistent exercise routine (150+ min/week)")
        doc_lines.append("• Optimize blood pressure, glucose, and cholesterol levels")
        doc_lines.append("• Develop sustainable healthy lifestyle habits")
        doc_lines.append("")
        
        # Review schedule
        doc_lines.append("CARE PLAN REVIEW SCHEDULE")
        doc_lines.append("-" * 40)
        doc_lines.append("• Initial follow-up: 2-4 weeks")
        doc_lines.append("• Progress review: 3 months")
        doc_lines.append("• Comprehensive reassessment: 6 months")
        doc_lines.append("• Annual care plan update")
        doc_lines.append("")
        
        # Emergency contacts
        doc_lines.append("WHEN TO SEEK IMMEDIATE CARE")
        doc_lines.append("-" * 40)
        doc_lines.append("• Chest pain or pressure")
        doc_lines.append("• Severe shortness of breath")
        doc_lines.append("• Blood pressure >180/120 mmHg")
        doc_lines.append("• Blood glucose >400 mg/dL")
        doc_lines.append("• Any concerning symptoms")
        doc_lines.append("")
        
        # Disclaimer
        doc_lines.append("MEDICAL DISCLAIMER")
        doc_lines.append("-" * 40)
        doc_lines.append("This care plan is generated based on risk assessment algorithms")
        doc_lines.append("and general medical guidelines. It should be reviewed and modified")
        doc_lines.append("by qualified healthcare professionals. Always consult with your")
        doc_lines.append("physician before making significant changes to your health regimen.")
        doc_lines.append("")
        doc_lines.append("=" * 60)
        
        return "\n".join(doc_lines)
    
    def validate_patient_data(self, patient_data: Dict[str, Any]) -> List[str]:
        """
        Validate patient data and return list of validation errors
        """
        errors = []
        
        # Age validation
        if not 18 <= patient_data['age'] <= 120:
            errors.append("Age must be between 18 and 120 years")
        
        # BMI validation
        if not 15 <= patient_data['bmi'] <= 60:
            errors.append("BMI appears to be outside normal physiological range")
        
        # Blood pressure validation
        if patient_data['systolic_bp'] <= patient_data['diastolic_bp']:
            errors.append("Systolic blood pressure must be higher than diastolic")
        
        if not 70 <= patient_data['systolic_bp'] <= 250:
            errors.append("Systolic blood pressure outside expected range (70-250 mmHg)")
        
        if not 40 <= patient_data['diastolic_bp'] <= 150:
            errors.append("Diastolic blood pressure outside expected range (40-150 mmHg)")
        
        # Laboratory values validation
        if not 50 <= patient_data['fasting_glucose'] <= 400:
            errors.append("Fasting glucose outside expected range (50-400 mg/dL)")
        
        if not 100 <= patient_data['cholesterol'] <= 400:
            errors.append("Total cholesterol outside expected range (100-400 mg/dL)")
        
        if not 20 <= patient_data['hdl_cholesterol'] <= 150:
            errors.append("HDL cholesterol outside expected range (20-150 mg/dL)")
        
        # Heart rate validation
        if not 40 <= patient_data['resting_hr'] <= 150:
            errors.append("Resting heart rate outside expected range (40-150 bpm)")
        
        return errors
