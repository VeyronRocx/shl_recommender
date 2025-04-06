import pandas as pd

def create_sample_dataset():
    """Create a realistic sample dataset based on SHL catalog information"""
    
    assessments = [
        {
            "name": "Verify Interactive - Java",
            "url": "https://www.shl.com/solutions/products/verify-interactive-java/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "40",
            "test_type": "Technical",
            "description": "Assesses Java programming skills through interactive coding challenges that test practical implementation skills. Suitable for developers at all levels."
        },
        {
            "name": "Verify - Python",
            "url": "https://www.shl.com/solutions/products/verify-python/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "35",
            "test_type": "Technical",
            "description": "Evaluates Python coding skills and programming concepts. Ideal for developers and data scientists."
        },
        {
            "name": "Verify - SQL",
            "url": "https://www.shl.com/solutions/products/verify-sql/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "30",
            "test_type": "Technical",
            "description": "Tests SQL query writing skills, database concepts, and data manipulation capabilities."
        },
        {
            "name": "Verify - JavaScript",
            "url": "https://www.shl.com/solutions/products/verify-javascript/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "35",
            "test_type": "Technical",
            "description": "Assesses JavaScript programming skills including DOM manipulation, async operations, and modern ES6+ concepts."
        },
        {
            "name": "Verify G+ Cognitive Ability",
            "url": "https://www.shl.com/solutions/products/verify-gplus/",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "duration": "25",
            "test_type": "Cognitive",
            "description": "Measures critical thinking and problem-solving skills with adaptive testing that adjusts difficulty based on performance."
        },
        {
            "name": "Occupational Personality Questionnaire (OPQ)",
            "url": "https://www.shl.com/solutions/products/opq/", 
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "45",
            "test_type": "Personality",
            "description": "Comprehensive personality assessment measuring 32 dimensions of workplace behavior and preferences."
        },
        {
            "name": "SHL Behavioral Assessment",
            "url": "https://www.shl.com/solutions/products/behavioral-assessment/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "20",
            "test_type": "Behavioral", 
            "description": "Evaluates workplace behaviors and competencies through situational questions and scenarios."
        },
        {
            "name": "Situational Judgement Test",
            "url": "https://www.shl.com/solutions/products/situational-judgement/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "30",
            "test_type": "Situational Judgement",
            "description": "Presents realistic workplace scenarios to evaluate decision-making and judgment in professional contexts."
        },
        {
            "name": "ADEPT-15 Personality Assessment",
            "url": "https://www.shl.com/solutions/products/adept15/",
            "remote_testing": "Yes", 
            "adaptive_support": "Yes",
            "duration": "25",
            "test_type": "Personality",
            "description": "Adaptive personality assessment measuring 15 key workplace traits with high predictive validity."
        },
        {
            "name": "Verify Numerical Reasoning",
            "url": "https://www.shl.com/solutions/products/verify-numerical/",
            "remote_testing": "Yes",
            "adaptive_support": "Yes", 
            "duration": "25",
            "test_type": "Cognitive",
            "description": "Tests ability to analyze and interpret numerical data and make sound decisions based on that analysis."
        },
        {
            "name": "Verify Verbal Reasoning", 
            "url": "https://www.shl.com/solutions/products/verify-verbal/",
            "remote_testing": "Yes",
            "adaptive_support": "Yes",
            "duration": "20",
            "test_type": "Cognitive",
            "description": "Assesses ability to understand and evaluate written information to draw accurate conclusions."
        },
        {
            "name": "Remote Interview Solution",
            "url": "https://www.shl.com/solutions/products/remote-interview/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "30",
            "test_type": "Behavioral",
            "description": "Structured video interview platform with AI-powered insights and standardized evaluation criteria."
        },
        {
            "name": "Leadership Assessment",
            "url": "https://www.shl.com/solutions/products/leadership-assessment/",
            "remote_testing": "Yes",
            "adaptive_support": "No",
            "duration": "60",
            "test_type": "Personality",
            "description": "Comprehensive evaluation of leadership potential, styles, and competencies for selection and development."
        },
        {
            "name": "Verify Spatial Reasoning",
            "url": "https://www.shl.com/solutions/products/verify-spatial/",
            "remote_testing": "Yes", 
            "adaptive_support": "No",
            "duration": "20",
            "test_type": "Cognitive",
            "description": "Measures ability to visualize, manipulate and reason with 2D and 3D objects and patterns."
        },
        {
            "name": "Digital Skills Assessment",
            "url": "https://www.shl.com/solutions/products/digital-skills/",
            "remote_testing": "Yes",
            "adaptive_support": "No", 
            "duration": "35",
            "test_type": "Technical",
            "description": "Evaluates proficiency with digital tools, data literacy, and technology adaptation capabilities."
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(assessments)
    
    # Save to CSV
    df.to_csv("shl_assessments.csv", index=False)
    print(f"Created sample dataset with {len(df)} assessments")
    return df

if __name__ == "__main__":
    create_sample_dataset()
