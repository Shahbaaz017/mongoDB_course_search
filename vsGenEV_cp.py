# import requests, time
# import pymongo
# import sys
# hf_token = "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"
# embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


# def generate_embedding(text: str) -> list[float]:
# 	response = requests.post(
# 		embedding_url,
# 		headers={"Authorization": f"Bearer {hf_token}"},
# 		json={"inputs": text})
# 	if response.status_code != 200:
# 		raise ValueError(
# 		    f"Request failed with status code {response.status_code}: {response.text}")
# 	print(response.json())
# 	return response.json()


# conn = pymongo.MongoClient(
#     "mongodb+srv://root:root@cluster0.0vqp1sc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# db = conn['education']
# coll = db['courses']
# print(coll)

# for doc in coll.find({"plot_embedding_hf":{"$exists": False}}).limit(100):
# 	#doc['plot_embedding_hf'] = generate_embedding(doc['fullplot'])
# 	#print(doc)
# 	coll.update_one({'_id':doc['_id']},{'$set':{'plot_embedding_hf':generate_embedding(doc['fullplot'])}})
# 	time.sleep(0.05)

import json
import random
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

# Unique course details for Arts and Commerce branches
unique_course_details = {
    "Arts": {
        "Fine Arts": "The Fine Arts program encourages creativity and self-expression through various artistic mediums. Students explore painting, sculpture, and digital art while developing a unique artistic voice.",
        "History": "The History course examines the events, cultures, and societies that have shaped our world. Students analyze historical texts and artifacts to gain insights into past human experiences and their relevance today.",
        "Psychology": "The Psychology program explores human behavior and mental processes. Students study theories of psychology, research methods, and therapeutic practices, preparing them for careers in counseling and mental health.",
        "Literature": "The Literature course immerses students in the study of various literary works and genres. Through critical analysis and interpretation, students develop a deeper understanding of cultural narratives and human experiences.",
        "Sociology": "The Sociology program examines social structures, relationships, and cultural norms. Students analyze societal issues and trends, equipping them to contribute to social change and community development.",
        "Philosophy": "The Philosophy course challenges students to explore fundamental questions about existence, knowledge, and ethics. Through rigorous analysis and debate, students develop critical thinking and reasoning skills.",
        "Political Science": "The Political Science program investigates political systems, theories, and behaviors. Students study governance, policy-making, and international relations, preparing them for careers in public service and diplomacy.",
        "Theatre": "The Theatre course combines performance, production, and theory. Students engage in acting, directing, and stagecraft, developing skills to bring stories to life on stage."
    },
    "Commerce": {
        "Accounting": "The Accounting program covers financial principles, reporting, and auditing. Students learn to analyze financial statements and manage budgets, preparing them for roles in finance and business management.",
        "Finance": "The Finance course focuses on investment strategies, risk management, and financial analysis. Students gain insights into capital markets and corporate finance, equipping them for careers in banking and investment.",
        "Marketing": "The Marketing program explores consumer behavior, market research, and digital marketing strategies. Students develop skills to create effective marketing campaigns and build brand awareness.",
        "Business Administration": "The Business Administration course provides a broad understanding of business operations, leadership, and management practices. Students prepare for diverse roles in various industries, from startups to large corporations.",
        "Economics": "The Economics program analyzes production, distribution, and consumption of goods and services. Students study economic theories and policies, equipping them to understand and address economic challenges.",
        "Entrepreneurship": "The Entrepreneurship course nurtures innovation and business development skills. Students learn to identify opportunities, create business plans, and launch startups, fostering an entrepreneurial mindset.",
        "Human Resources": "The Human Resources program focuses on talent management, organizational behavior, and labor relations. Students learn to develop effective workforce strategies and promote a positive workplace culture."
    }
}

# Course levels and counts for Arts and Commerce
course_levels = {
    "Undergraduate": 150,
    "Postgraduate": 100,
    "PhD": 50
}

# Sample universities for each course
universities = [
    {
        "university_name": "University of Arts",
        "fees": "INR 600000",
        "city": "London",
        "country": "UK",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a6/University_of_Arts_London_logo.png"
    },
    {
        "university_name": "Commerce College",
        "fees": "INR 500000",
        "city": "New York",
        "country": "USA",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Columbia_University_seal.png"
    },
    {
        "university_name": "Global University",
        "fees": "INR 450000",
        "city": "Sydney",
        "country": "Australia",
        "image": "https://upload.wikimedia.org/wikipedia/en/b/b5/University_of_Sydney_logo.svg"
    },
    {
        "university_name": "Metropolitan University",
        "fees": "INR 700000",
        "city": "Toronto",
        "country": "Canada",
        "image": "https://upload.wikimedia.org/wikipedia/en/c/c5/University_of_Toronto_logo.svg"
    }
]

# Generate documents for Arts and Commerce courses
documents = []

for level, count in course_levels.items():
    for _ in range(count):
        field = random.choice(list(unique_course_details.keys()))
        branch = random.choice(list(unique_course_details[field].keys()))
        
        # Course details specific to the branch
        course_name = f"{branch} in {field}"
        course_duration = "3 years" if level == "Undergraduate" else "2 years" if level == "Postgraduate" else "5 years"
        course_description = unique_course_details[field][branch]

        # Randomly select a university detail
        university = random.choice(universities)
        
        # Create the document
        document = {
            "course_name": course_name,
            "course_duration": course_duration,
            "course_details": course_description,
            "course_approximate_fees": university["fees"],
            "course_type": [level],
            "fullplot": f"The course '{course_name}' spans {course_duration} and provides in-depth knowledge about {branch}. {course_description} The approximate fees for this course are {university['fees']}.",
            "university_details": {
                "name": university["university_name"],
                "city": university["city"],
                "country": university["country"],
                "image": university["image"]
            }
        }
        document['plot_embedding_hf']=model.encode(document['fullplot'],normalize_embeddings=True).tolist()
        documents.append(document)

# Save to JSON file
file_path_arts_commerce = 'arts_commerce_courses.json'
with open(file_path_arts_commerce, 'w') as file:
    json.dump(documents, file, indent=4)

file_path_arts_commerce

