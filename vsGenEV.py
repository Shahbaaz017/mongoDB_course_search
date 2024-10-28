import pymongo
import json
from sentence_transformers import SentenceTransformer


# MongoDB connection
conn = pymongo.MongoClient("mongodb+srv://nitroshahbaaz:e0RgDgiKQiv26ssW@cluster0.uxdv3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = conn['education']
coll = db['courses']


# Load pre-trained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Path to the JSON file
# Path to the JSON file
file_path = "C:\\Users\\nitro\\OneDrive\\Pictures\\mongodb\\Archive\\medical_engineering_courses.json"



# Open JSON file and read
with open(file_path, "r") as file:
    documents = json.load(file)


for doc in documents:
    if 'fullplot' in doc:
        # Generate embedding and add it to the document
        doc['plot_embedding_hf'] = model.encode(doc['fullplot'], normalize_embeddings=True).tolist()
        
        # Insert or update document in MongoDB
        coll.update_one(
            {'_id': doc.get('_id')},  # Match document by _id if it exists
            {'$set': doc},            # Update the document
            upsert=True                # Insert if document does not exist
        )


print("Embeddings have been added/updated for documents in MongoDB.")
