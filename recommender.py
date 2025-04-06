import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AssessmentRecommender:
    """
    Recommendation engine for SHL assessments using TF-IDF and cosine similarity
    """

    def __init__(self, data_path='shl_assessments.csv'):
        """
        Initialize the recommender with assessment data

        Args:
            data_path: Path to CSV file containing assessment data
        """
        # Load assessment data
        self.assessments_df = pd.read_csv(data_path)

        # Create a combined text field for better matching
        self.assessments_df['combined_text'] = (
                self.assessments_df['name'] + ' ' +
                self.assessments_df['test_type'] + ' ' +
                self.assessments_df['description']
        )

        # Initialize and fit the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            analyzer='word',
            ngram_range=(1, 2),  # Use both unigrams and bigrams
            stop_words='english',
            max_features=5000
        )

        # Create the TF-IDF matrix for assessments
        self.tfidf_matrix = self.vectorizer.fit_transform(self.assessments_df['combined_text'])
        print(f"Loaded {len(self.assessments_df)} assessments and created TF-IDF matrix")

    def _extract_duration_limit(self, query):
        """Extract duration limit from query if specified"""
        duration_patterns = [
            r'(\d+)\s*minutes',
            r'(\d+)\s*mins',
            r'(\d+)\s*min',
            r'less than (\d+)',
            r'under (\d+)',
            r'max.*?(\d+)',
            r'maximum.*?(\d+)',
            r'completed in (\d+)'
        ]

        for pattern in duration_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return None

    def _extract_skills(self, query):
        """Extract technical skills mentioned in the query"""
        # Common programming languages and technical skills
        skills = [
            'java', 'python', 'javascript', 'js', 'sql', 'c#', 'c++',
            'typescript', 'php', 'ruby', 'scala', 'golang', 'html', 'css',
            'react', 'angular', 'vue', 'node', 'aws', 'azure', 'cloud',
            'data science', 'machine learning', 'ml', 'ai', 'data analysis',
            'devops', 'agile', 'scrum', 'leadership', 'management',
            'communication', 'collaboration', 'problem solving'
        ]

        found_skills = []
        for skill in skills:
            # Use word boundary to match whole words
            if re.search(r'\b' + re.escape(skill) + r'\b', query.lower()):
                found_skills.append(skill)

        return found_skills

    def _extract_test_types(self, query):
        """Extract test types mentioned in the query"""
        test_types = {
            'cognitive': ['cognitive', 'reasoning', 'aptitude', 'ability'],
            'personality': ['personality', 'behavior', 'behavioural'],
            'technical': ['technical', 'coding', 'programming'],
            'situational': ['situational', 'judgement', 'judgment'],
        }

        found_types = []
        for test_type, keywords in test_types.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', query.lower()):
                    found_types.append(test_type)
                    break

        return found_types

    def recommend(self, query, max_recommendations=10):
        """
        Recommend assessments based on a text query

        Args:
            query: Natural language query or job description
            max_recommendations: Maximum number of recommendations to return

        Returns:
            DataFrame with recommended assessments
        """
        print(f"Processing query: {query[:100]}...")

        # Extract constraints from query
        duration_limit = self._extract_duration_limit(query)
        skills = self._extract_skills(query)
        test_types = self._extract_test_types(query)

        # Print extracted information for debugging
        if duration_limit:
            print(f"Detected duration limit: {duration_limit} minutes")
        if skills:
            print(f"Detected skills: {', '.join(skills)}")
        if test_types:
            print(f"Detected test types: {', '.join(test_types)}")

        # Transform the query using the same vectorizer
        query_vector = self.vectorizer.transform([query])

        # Calculate cosine similarities
        cosine_similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Add similarities to a copy of the dataframe
        results = self.assessments_df.copy()
        results['similarity'] = cosine_similarities

        # Apply filters based on extracted information
        if duration_limit:
            # Convert duration to numeric, coercing errors to NaN
            results['duration_num'] = pd.to_numeric(results['duration'], errors='coerce')
            # Filter by duration limit
            results = results[results['duration_num'] <= duration_limit]

        if test_types:
            # Filter by test types if specified
            test_type_pattern = '|'.join(test_types)
            results = results[results['test_type'].str.lower().str.contains(test_type_pattern, case=False, na=False)]

        # Add bonus score for skills match if technical assessments are sought
        if 'technical' in test_types and skills:
            # Check if any of the skills are in the assessment name or description
            for skill in skills:
                results['similarity'] = np.where(
                    results['name'].str.contains(skill, case=False, na=False) |
                    results['description'].str.contains(skill, case=False, na=False),
                    results['similarity'] + 0.2,  # Boost the score
                    results['similarity']
                )

        # Sort by similarity score and take top N
        results = results.sort_values('similarity', ascending=False).head(max_recommendations)

        # Return the recommendations without the similarity score and combined_text
        return results[['name', 'url', 'remote_testing', 'adaptive_support', 'duration', 'test_type']]


if __name__ == "__main__":
    # Test the recommender
    recommender = AssessmentRecommender()

    # Example queries from the assignment
    test_queries = [
        "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes.",
        "Hiring for an analyst position. Need cognitive and personality tests under 30 minutes."
    ]

    # Test each query
    for query in test_queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        recommendations = recommender.recommend(query, max_recommendations=5)
        print("\nRECOMMENDATIONS:")
        print(recommendations.to_string(index=False))
        print("-" * 80)