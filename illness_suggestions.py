# illness_suggestions.py

illness_suggestions = {
    "Metabolic Syndrome": {
        "description": (
            "Metabolic syndrome is characterized by insulin resistance, dyslipidemia, hypertension, "
            "and central obesity. It increases the risk for type 2 diabetes and cardiovascular disease."
        ),
        "tests": [
            {"category": "Blood_Chemistry", "test": "FBS"},
            {"category": "Lipid_Profile", "test": "Triglycerides"},
            {"category": "Lipid_Profile", "test": "HDL"},
            {"category": "Vital_Signs", "test": "BP"}
        ]
    },
    "Diabetes": {
        "description": (
            "Diabetes is marked by elevated blood sugar levels and insulin resistance, typically evaluated "
            "using blood glucose tests and related metabolic markers."
        ),
        "tests": [
            {"category": "Blood_Chemistry", "test": "FBS"},
            {"category": "Blood_Chemistry", "test": "Creatinine"}
        ]
    },
    "Cardiovascular Disease": {
        "description": (
            "Cardiovascular disease encompasses disorders of the heart and blood vessels, often associated with "
            "dyslipidemia and hypertension."
        ),
        "tests": [
            {"category": "Lipid_Profile", "test": "LDL"},
            {"category": "Vital_Signs", "test": "BP"},
            {"category": "Cardiac_Markers", "test": "Troponin"}
        ]
    },
    "Thyroid Disorder": {
        "description": (
            "Thyroid disorders affect metabolism, weight regulation, and energy levels. Evaluation typically includes "
            "assays for thyroid hormones."
        ),
        "tests": [
            {"category": "Thyroid_Function", "test": "TSH"},
            {"category": "Thyroid_Function", "test": "Free_T4"}
        ]
    },
    "Liver Dysfunction": {
        "description": (
            "Liver dysfunction may be indicated by abnormal liver enzymes and protein levels. Evaluation often involves "
            "tests for ALT, AST, bilirubin, and albumin."
        ),
        "tests": [
            {"category": "Liver_Function", "test": "SGPT_ALT"},
            {"category": "Liver_Function", "test": "SGOT_AST"}
        ]
    },
    "Kidney Disease": {
        "description": (
            "Kidney disease is suggested by impaired filtration, leading to elevated BUN and creatinine, often accompanied by "
            "electrolyte imbalances and proteinuria."
        ),
        "tests": [
            {"category": "Blood_Chemistry", "test": "Creatinine"},
            {"category": "Blood_Chemistry", "test": "BUN"},
            {"category": "Urinalysis", "test": "Urine_Protein"}
        ]
    },
    "Anemia": {
        "description": (
            "Anemia is characterized by low hemoglobin and hematocrit levels, resulting in reduced oxygen delivery to tissues."
        ),
        "tests": [
            {"category": "Hematology", "test": "Hemoglobin"},
            {"category": "Hematology", "test": "Hematocrit"},
            {"category": "Hematology", "test": "RBC"}
        ]
    },
    "Pancreatitis": {
        "description": (
            "Pancreatitis is inflammation of the pancreas, typically indicated by elevated pancreatic enzymes."
        ),
        "tests": [
            {"category": "Pancreatic", "test": "Amylase"},
            {"category": "Pancreatic", "test": "Lipase"}
        ]
    },
    "Rheumatoid Arthritis": {
        "description": (
            "Rheumatoid arthritis is an autoimmune condition characterized by joint inflammation, often accompanied by a positive "
            "rheumatoid factor and anti-CCP antibodies."
        ),
        "tests": [
            {"category": "Immunology", "test": "RF"},
            {"category": "Immunology", "test": "Anti_CCP"}
        ]
    },
    "Cancer Screening": {
        "description": (
            "Tumor markers may prompt further investigation for malignancies as part of a comprehensive cancer screening strategy."
        ),
        "tests": [
            {"category": "Tumor_Markers", "test": "CEA"},
            {"category": "Tumor_Markers", "test": "AFP"},
            {"category": "Tumor_Markers", "test": "CA_19-9"},
            {"category": "Tumor_Markers", "test": "CA_125"}
        ]
    },
    "Coagulation Disorder": {
        "description": (
            "Abnormalities in coagulation tests may indicate bleeding or clotting disorders that require further evaluation."
        ),
        "tests": [
            {"category": "Coagulation", "test": "Prothrombin_Time"},
            {"category": "Coagulation", "test": "INR"},
            {"category": "Coagulation", "test": "D_Dimer"}
        ]
    },
    "Infectious Disease": {
        "description": (
            "Infections can be detected using specific antigen and antibody tests, screening for common agents such as HIV, "
            "hepatitis B and C, and syphilis."
        ),
        "tests": [
            {"category": "Infectious_Disease", "test": "HIV"},
            {"category": "Infectious_Disease", "test": "HBsAg"},
            {"category": "Infectious_Disease", "test": "Anti_HCV"},
            {"category": "Infectious_Disease", "test": "RPR"}
        ]
    },
    "HIV/AIDS": {
        "description": (
            "HIV/AIDS is caused by the human immunodeficiency virus, which progressively weakens the immune system. "
            "Evaluation typically includes HIV antigen/antibody tests, CD4 counts, and viral load measurements."
        ),
        "tests": [
            {"category": "Infectious_Disease", "test": "HIV"},
            {"category": "Infectious_Disease", "test": "HIV_CD4"},
            {"category": "Infectious_Disease", "test": "HIV_Viral_Load"}
        ]
    },
    "Electrolyte Imbalance": {
        "description": (
            "Electrolyte imbalances may indicate dehydration, renal dysfunction, or hormonal disturbances. Evaluating multiple "
            "electrolyte parameters provides a comprehensive picture."
        ),
        "tests": [
            {"category": "Electrolytes", "test": "Sodium"},
            {"category": "Electrolytes", "test": "Potassium"},
            {"category": "Electrolytes", "test": "Calcium"},
            {"category": "Electrolytes", "test": "Magnesium"},
            {"category": "Electrolytes", "test": "Phosphorus"}
        ]
    },
    "Vitamin D Deficiency": {
        "description": (
            "Low vitamin D levels can affect bone health and immune function. Screening with vitamin D and calcium tests helps assess "
            "related metabolic changes."
        ),
        "tests": [
            {"category": "Other_Markers", "test": "Vitamin_D"},
            {"category": "Electrolytes", "test": "Calcium"}
        ]
    },
    "Prostate Disorder": {
        "description": (
            "Prostate disorders, including benign prostatic hyperplasia and prostate cancer, are primarily evaluated using PSA levels."
        ),
        "tests": [
            {"category": "Prostate", "test": "PSA"}
        ]
    },
    "Autoimmune Disorder (Lupus)": {
        "description": (
            "Systemic lupus erythematosus (SLE) is an autoimmune disease that is often initially screened using antinuclear antibody (ANA) tests."
        ),
        "tests": [
            {"category": "Immunology", "test": "ANA"}
        ]
    },
    "Systemic Inflammation": {
        "description": (
            "Elevated inflammatory markers such as CRP and ESR may indicate systemic inflammation from infection, autoimmune conditions, "
            "or other chronic processes."
        ),
        "tests": [
            {"category": "Inflammatory", "test": "CRP"},
            {"category": "Inflammatory", "test": "ESR"}
        ]
    },
    "Urinary Tract Infection": {
        "description": (
            "A urinary tract infection is commonly detected by abnormalities in urinalysis, including the presence of nitrites, "
            "leukocyte esterase, and blood."
        ),
        "tests": [
            {"category": "Urinalysis", "test": "Urine_Nitrites"},
            {"category": "Urinalysis", "test": "Leukocyte_Esterase"},
            {"category": "Urinalysis", "test": "Urine_Blood"}
        ]
    },
    "Iron Deficiency Anemia": {
        "description": (
            "Iron deficiency anemia results from inadequate iron levels, leading to decreased hemoglobin production and a reduced red blood cell count."
        ),
        "tests": [
            {"category": "Other_Markers", "test": "Ferritin"},
            {"category": "Other_Markers", "test": "Iron"},
            {"category": "Hematology", "test": "Hemoglobin"}
        ]
    },
    "Gout": {
        "description": (
            "Gout is an inflammatory arthritis characterized by elevated uric acid levels and deposition of urate crystals in joints."
        ),
        "tests": [
            {"category": "Blood_Chemistry", "test": "Uric_Acid"}
        ]
    },
    "Heart Failure": {
        "description": (
            "Heart failure occurs when the heart is unable to pump blood effectively, often evaluated using markers such as BNP and oxygen saturation."
        ),
        "tests": [
            {"category": "Cardiac_Markers", "test": "BNP"},
            {"category": "Vital_Signs", "test": "Oxygen"}
        ]
    },
    "Acute Coronary Syndrome": {
        "description": (
            "Acute coronary syndrome refers to conditions with sudden, reduced blood flow to the heart, commonly evaluated by troponin levels."
        ),
        "tests": [
            {"category": "Cardiac_Markers", "test": "Troponin"}
        ]
    },
    "Hyperlipidemia": {
        "description": (
            "Hyperlipidemia is characterized by elevated lipid levels in the blood, increasing the risk for cardiovascular disease. "
            "It is typically evaluated using a comprehensive lipid panel."
        ),
        "tests": [
            {"category": "Lipid_Profile", "test": "Cholesterol"},
            {"category": "Lipid_Profile", "test": "LDL"},
            {"category": "Lipid_Profile", "test": "HDL"},
            {"category": "Lipid_Profile", "test": "Triglycerides"}
        ]
    },
    "Tuberculosis": {
        "description": (
            "Tuberculosis is a bacterial infection primarily affecting the lungs. Diagnosis is often supported by an interferon gamma release assay (IGRA) "
            "to detect immune reactivity to Mycobacterium tuberculosis antigens."
        ),
        "tests": [
            {"category": "Infectious_Disease", "test": "IGRA_TB"}
        ]
    },
    "Dengue Fever": {
        "description": (
            "Dengue fever is a mosquito-borne viral infection characterized by high fever, severe headache, joint and muscle pain, and sometimes a drop in "
            "platelet count, increasing the risk of bleeding."
        ),
        "tests": [
            {"category": "Infectious_Disease", "test": "Dengue_NS1"},
            {"category": "Hematology", "test": "Platelet_Count"}
        ]
    },
    "Malaria": {
        "description": (
            "Malaria is a parasitic infection transmitted by mosquitoes, causing cyclical fevers, chills, and anemia. Diagnosis is most often made by detecting "
            "parasites in a blood smear."
        ),
        "tests": [
            {"category": "Infectious_Disease", "test": "Malaria_Smear"}
        ]
    },
    "COVID-19": {
        "description": (
            "COVID-19 is caused by the SARS-CoV-2 virus and can range from mild respiratory symptoms to severe illness. While PCR remains the gold standard for diagnosis, "
            "supportive evaluation may include temperature monitoring and white blood cell counts."
        ),
        "tests": [
            {"category": "Vital_Signs", "test": "Temperature"},
            {"category": "Hematology", "test": "WBC"}
        ]
    },
    "Influenza": {
        "description": (
            "Influenza is a contagious respiratory illness caused by influenza viruses, typically presenting with high fever, cough, body aches, and fatigue."
        ),
        "tests": [
            {"category": "Vital_Signs", "test": "Temperature"},
            {"category": "Hematology", "test": "WBC"}
        ]
    },
    "Common Cold": {
        "description": (
            "The common cold is a mild viral upper respiratory infection characterized by a runny nose, sneezing, and sometimes low-grade fever."
        ),
        "tests": [
            {"category": "Vital_Signs", "test": "Temperature"}
        ]
    },
    "Gastroenteritis": {
        "description": (
            "Gastroenteritis, which presents with diarrhea and abdominal cramps, is usually due to viral or bacterial infections and may lead to dehydration "
            "and electrolyte imbalances."
        ),
        "tests": [
            {"category": "Gastrointestinal_Assessments", "test": "Diarrheas"},
            {"category": "Electrolytes", "test": "Sodium"},
            {"category": "Urinalysis", "test": "Specific_Gravity"},
            {"category": "Hematology", "test": "WBC"}
        ]
    },
    "Acute Hepatitis": {
        "description": (
            "Acute hepatitis refers to liver inflammation, most commonly caused by viral infections (e.g., hepatitis A, B, or C), and is evaluated using specific viral markers "
            "and liver function tests."
        ),
        "tests": [
            {"category": "Infectious_Disease", "test": "HBsAg"},
            {"category": "Infectious_Disease", "test": "Anti_HCV"},
            {"category": "Infectious_Disease", "test": "HBcIgM"},
            {"category": "Infectious_Disease", "test": "Hepatitis_A_IgM"}
        ]
    },
    "Stroke": {
        "description": (
            "Stroke is a medical emergency caused by an interruption of blood flow to the brain, potentially leading to permanent neurological damage. Rapid evaluation is critical."
        ),
        "tests": [
            {"category": "Neurological_Assessments", "test": "Stroke"}
        ]
    },
    "Mild Stroke": {
        "description": (
            "A mild stroke, often synonymous with a transient ischemic attack (TIA), presents with temporary neurological deficits. Evaluation is essential to prevent future events."
        ),
        "tests": [
            {"category": "Neurological_Assessments", "test": "Mild_Stroke"}
        ]
    },
    "Low Body Mass": {
        "description": (
            "Low body mass may indicate malnutrition, chronic disease, or metabolic disturbances. Evaluation typically includes nutritional assessment and blood tests for metabolic markers."
        ),
        "tests": [
            {"category": "Liver_Function", "test": "Albumin"}
        ]
    }
}

if __name__ == "__main__":
    import json
    print(json.dumps(illness_suggestions, indent=2))
