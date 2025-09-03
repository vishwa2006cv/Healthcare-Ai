from typing import Dict, List, Any
from datetime import datetime, timedelta

class CareplanGenerator:
    """
    Generates personalized care plans based on risk assessments and patient data
    """
    
    def __init__(self):
        self.risk_thresholds = {
            'low': 0.4,
            'moderate': 0.7
        }
    
    def generate_comprehensive_care_plan(self, patient_data: Dict[str, Any], risks: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive care plan based on risk assessment results
        """
        care_plan = {
            'immediate_actions': [],
            'lifestyle': {
                'diet_nutrition': [],
                'physical_activity': [],
                'stress_management': [],
                'sleep_hygiene': [],
                'substance_use': []
            },
            'medical_followup': [],
            'monitoring_schedule': []
        }
        
        # Analyze each risk category
        diabetes_risk = risks['diabetes']['score']
        heart_disease_risk = risks['heart_disease']['score']
        hypertension_risk = risks['hypertension']['score']
        
        # Immediate actions for high-risk conditions
        self._add_immediate_actions(care_plan, patient_data, risks)
        
        # Lifestyle recommendations
        self._add_diet_recommendations(care_plan, patient_data, risks)
        self._add_exercise_recommendations(care_plan, patient_data, risks)
        self._add_stress_management(care_plan, patient_data, risks)
        self._add_sleep_recommendations(care_plan, patient_data, risks)
        self._add_substance_use_recommendations(care_plan, patient_data, risks)
        
        # Medical follow-up recommendations
        self._add_medical_followup(care_plan, patient_data, risks)
        
        # Monitoring schedule
        self._add_monitoring_schedule(care_plan, patient_data, risks)
        
        return care_plan
    
    def _add_immediate_actions(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add immediate actions for high-risk situations"""
        
        # Blood pressure emergency
        if patient_data['systolic_bp'] >= 180 or patient_data['diastolic_bp'] >= 120:
            care_plan['immediate_actions'].append(
                "URGENT: Seek immediate medical attention for hypertensive crisis (BP ≥180/120)"
            )
        
        # Severe hyperglycemia
        if patient_data['fasting_glucose'] >= 250:
            care_plan['immediate_actions'].append(
                "URGENT: Seek immediate medical attention for severe hyperglycemia (glucose ≥250 mg/dL)"
            )
        
        # High diabetes risk with symptoms
        if risks['diabetes']['score'] >= 0.8:
            care_plan['immediate_actions'].append(
                "Schedule medical evaluation within 2 weeks for diabetes screening and management"
            )
        
        # Very high heart disease risk
        if risks['heart_disease']['score'] >= 0.8:
            care_plan['immediate_actions'].append(
                "Schedule cardiology consultation within 1 month for comprehensive cardiac risk assessment"
            )
        
        # Uncontrolled hypertension
        if risks['hypertension']['score'] >= 0.8 and patient_data['systolic_bp'] >= 160:
            care_plan['immediate_actions'].append(
                "Schedule medical appointment within 1 week to initiate or adjust blood pressure medication"
            )
    
    def _add_diet_recommendations(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add dietary recommendations based on risk factors"""
        
        recommendations = care_plan['lifestyle']['diet_nutrition']
        
        # General healthy eating
        recommendations.append("Follow a balanced diet rich in fruits, vegetables, whole grains, and lean proteins")
        
        # BMI-based recommendations
        if patient_data['bmi'] >= 30:
            recommendations.append("Implement a structured weight loss plan targeting 1-2 pounds per week")
            recommendations.append("Consider consultation with a registered dietitian for personalized meal planning")
            recommendations.append("Practice portion control using smaller plates and measuring portions")
        elif patient_data['bmi'] >= 25:
            recommendations.append("Focus on portion control and increase vegetable intake to achieve healthy weight")
        
        # Diabetes risk recommendations
        if risks['diabetes']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Limit refined carbohydrates and added sugars")
            recommendations.append("Choose complex carbohydrates with low glycemic index")
            recommendations.append("Include fiber-rich foods (≥25g daily) to help manage blood sugar")
            recommendations.append("Eat regular meals to maintain stable blood glucose levels")
        
        # Heart disease risk recommendations
        if risks['heart_disease']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Follow heart-healthy diet (Mediterranean or DASH diet)")
            recommendations.append("Limit saturated fat to <7% of total calories")
            recommendations.append("Include omega-3 fatty acids from fish 2-3 times per week")
            recommendations.append("Limit sodium intake to <2,300mg daily (ideally <1,500mg)")
        
        # Hypertension risk recommendations
        if risks['hypertension']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Follow DASH diet emphasizing fruits, vegetables, and low-fat dairy")
            recommendations.append("Reduce sodium intake to <1,500mg daily")
            recommendations.append("Increase potassium-rich foods (bananas, oranges, spinach)")
            recommendations.append("Limit processed and packaged foods")
        
        # Cholesterol management
        if patient_data['cholesterol'] >= 200:
            recommendations.append("Increase soluble fiber intake (oats, beans, apples)")
            recommendations.append("Include plant sterols and stanols in diet")
            recommendations.append("Choose lean proteins and limit red meat consumption")
    
    def _add_exercise_recommendations(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add physical activity recommendations"""
        
        recommendations = care_plan['lifestyle']['physical_activity']
        current_exercise = patient_data['exercise_days']
        
        # Base recommendations
        if current_exercise < 3:
            recommendations.append("Gradually increase to 150 minutes of moderate-intensity aerobic activity per week")
            recommendations.append("Start with 10-15 minute walks and progressively increase duration")
            recommendations.append("Include resistance training 2-3 times per week")
        elif current_exercise < 5:
            recommendations.append("Aim for 150-300 minutes of moderate-intensity exercise weekly")
            recommendations.append("Add variety with different types of cardio activities")
        else:
            recommendations.append("Maintain current excellent exercise routine")
            recommendations.append("Consider adding high-intensity interval training 1-2 times per week")
        
        # Condition-specific recommendations
        if patient_data['bmi'] >= 30:
            recommendations.append("Focus on low-impact activities initially (swimming, cycling, walking)")
            recommendations.append("Incorporate strength training to preserve muscle mass during weight loss")
        
        if risks['diabetes']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Include both aerobic and resistance training for optimal glucose control")
            recommendations.append("Exercise at consistent times to help regulate blood sugar")
            recommendations.append("Monitor blood glucose before and after exercise if diabetic")
        
        if risks['heart_disease']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Start with cardiac-safe exercise program, progressing gradually")
            recommendations.append("Include warm-up and cool-down periods in all exercise sessions")
            recommendations.append("Monitor heart rate during exercise (target 50-85% max heart rate)")
        
        if risks['hypertension']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Emphasize aerobic exercise which effectively lowers blood pressure")
            recommendations.append("Avoid heavy weightlifting initially; focus on moderate resistance training")
            recommendations.append("Monitor blood pressure response to exercise")
    
    def _add_stress_management(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add stress management recommendations"""
        
        recommendations = care_plan['lifestyle']['stress_management']
        
        # General stress management
        recommendations.append("Practice daily stress-reduction techniques (meditation, deep breathing)")
        recommendations.append("Maintain social connections and seek support when needed")
        recommendations.append("Consider mindfulness-based stress reduction (MBSR) programs")
        
        # High-risk specific recommendations
        if risks['heart_disease']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Learn and practice progressive muscle relaxation techniques")
            recommendations.append("Consider counseling or therapy for chronic stress management")
        
        if risks['hypertension']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Practice daily meditation or yoga to help lower blood pressure")
            recommendations.append("Identify and address major stressors in work and personal life")
        
        recommendations.append("Engage in enjoyable hobbies and recreational activities")
        recommendations.append("Maintain work-life balance and take regular vacations")
    
    def _add_sleep_recommendations(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add sleep hygiene recommendations"""
        
        recommendations = care_plan['lifestyle']['sleep_hygiene']
        
        # General sleep hygiene
        recommendations.append("Maintain consistent sleep schedule (7-9 hours nightly)")
        recommendations.append("Create a comfortable, dark, and quiet sleep environment")
        recommendations.append("Avoid screens 1 hour before bedtime")
        recommendations.append("Limit caffeine intake after 2 PM")
        
        # Condition-specific recommendations
        if 'Sleep Apnea' in patient_data['existing_conditions']:
            recommendations.append("Ensure compliance with CPAP therapy if prescribed")
            recommendations.append("Sleep on side rather than back to reduce apnea episodes")
        
        if patient_data['bmi'] >= 30:
            recommendations.append("Weight loss can significantly improve sleep quality and reduce sleep apnea risk")
        
        if risks['diabetes']['score'] >= self.risk_thresholds['moderate']:
            recommendations.append("Maintain regular sleep schedule to help regulate blood sugar")
            recommendations.append("Avoid large meals close to bedtime")
        
        recommendations.append("Consider relaxation techniques before bed (reading, gentle stretching)")
    
    def _add_substance_use_recommendations(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add recommendations for substance use"""
        
        recommendations = care_plan['lifestyle']['substance_use']
        
        # Smoking cessation
        if patient_data['smoking'] == "Current":
            recommendations.append("PRIORITY: Quit smoking immediately - consider nicotine replacement therapy")
            recommendations.append("Join smoking cessation program or seek counseling support")
            recommendations.append("Avoid triggers and develop healthy coping strategies")
            recommendations.append("Consider prescription medications for smoking cessation (consult physician)")
        elif patient_data['smoking'] == "Former":
            recommendations.append("Continue to avoid tobacco products and secondhand smoke")
            recommendations.append("Maintain smoke-free environment at home and work")
        
        # Alcohol recommendations
        if patient_data['alcohol_consumption'] == "Heavy":
            recommendations.append("Reduce alcohol intake to moderate levels or consider abstinence")
            recommendations.append("Seek support for alcohol reduction if needed")
            recommendations.append("Limit alcohol to ≤1 drink/day (women) or ≤2 drinks/day (men)")
        elif patient_data['alcohol_consumption'] == "Moderate":
            recommendations.append("Maintain current moderate alcohol consumption or consider reducing further")
        
        # High-risk specific recommendations
        if risks['heart_disease']['score'] >= 0.7 or risks['hypertension']['score'] >= 0.7:
            if patient_data['alcohol_consumption'] != "None":
                recommendations.append("Consider eliminating alcohol completely to maximize cardiovascular benefits")
    
    def _add_medical_followup(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add medical follow-up recommendations"""
        
        followup = care_plan['medical_followup']
        
        # Regular checkups based on age and risk
        if patient_data['age'] >= 40:
            followup.append("Annual comprehensive physical examination")
        else:
            followup.append("Physical examination every 2-3 years, or annually if risk factors present")
        
        # Diabetes-specific follow-up
        if risks['diabetes']['score'] >= self.risk_thresholds['moderate']:
            followup.append("HbA1c testing every 3-6 months")
            followup.append("Annual diabetic eye examination")
            followup.append("Annual foot examination for diabetic complications")
            followup.append("Consider continuous glucose monitoring if diabetic")
        
        # Heart disease follow-up
        if risks['heart_disease']['score'] >= self.risk_thresholds['moderate']:
            followup.append("Lipid panel every 3-6 months until goals achieved, then annually")
            followup.append("Consider stress testing or cardiac imaging if symptoms develop")
            followup.append("Blood pressure monitoring at each medical visit")
        
        # Hypertension follow-up
        if risks['hypertension']['score'] >= self.risk_thresholds['moderate']:
            followup.append("Blood pressure monitoring every 2-4 weeks until controlled")
            followup.append("Home blood pressure monitoring with log")
            followup.append("Kidney function tests annually")
        
        # Preventive care
        followup.append("Age-appropriate cancer screenings (colonoscopy, mammography, etc.)")
        followup.append("Vaccination updates as recommended")
        followup.append("Bone density screening if indicated")
    
    def _add_monitoring_schedule(self, care_plan: Dict, patient_data: Dict, risks: Dict):
        """Add monitoring schedule based on risk levels"""
        
        schedule = []
        
        # Weight monitoring
        if patient_data['bmi'] >= 25:
            schedule.append({
                'Parameter': 'Weight',
                'Frequency': 'Weekly',
                'Target': f"Target BMI 18.5-24.9 (current: {patient_data['bmi']:.1f})",
                'Action': 'Track weight loss progress'
            })
        else:
            schedule.append({
                'Parameter': 'Weight',
                'Frequency': 'Monthly',
                'Target': 'Maintain current healthy weight',
                'Action': 'Monitor for changes'
            })
        
        # Blood pressure monitoring
        if risks['hypertension']['score'] >= self.risk_thresholds['moderate']:
            schedule.append({
                'Parameter': 'Blood Pressure',
                'Frequency': 'Daily (home monitoring)',
                'Target': '<130/80 mmHg',
                'Action': 'Log readings, report if consistently elevated'
            })
        else:
            schedule.append({
                'Parameter': 'Blood Pressure',
                'Frequency': 'Monthly',
                'Target': '<120/80 mmHg',
                'Action': 'Monitor for trends'
            })
        
        # Blood glucose monitoring
        if risks['diabetes']['score'] >= self.risk_thresholds['moderate']:
            schedule.append({
                'Parameter': 'Blood Glucose',
                'Frequency': 'Daily (if diabetic) or weekly (prediabetic)',
                'Target': 'Fasting: 80-130 mg/dL',
                'Action': 'Track patterns and report to physician'
            })
        
        # Cholesterol monitoring
        if patient_data['cholesterol'] >= 200 or risks['heart_disease']['score'] >= self.risk_thresholds['moderate']:
            schedule.append({
                'Parameter': 'Cholesterol Panel',
                'Frequency': 'Every 3-6 months',
                'Target': 'Total <200 mg/dL, LDL <100 mg/dL',
                'Action': 'Laboratory testing with physician review'
            })
        
        # Exercise tracking
        schedule.append({
            'Parameter': 'Physical Activity',
            'Frequency': 'Daily',
            'Target': '150+ minutes moderate activity/week',
            'Action': 'Log exercise duration and intensity'
        })
        
        # Medication adherence (if applicable)
        if patient_data['medications'].strip():
            schedule.append({
                'Parameter': 'Medication Adherence',
                'Frequency': 'Daily',
                'Target': '100% compliance',
                'Action': 'Use pill organizer, set reminders'
            })
        
        care_plan['monitoring_schedule'] = schedule
