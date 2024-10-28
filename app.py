from flask import Flask, render_template, request
import pymongo
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
app = Flask(__name__)


def generate_embedding(text: str) -> list[float]:
    return model.encode(text, normalize_embeddings=True).tolist()


conn = pymongo.MongoClient(
    "mongodb+srv://root:root@cluster0.0vqp1sc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = conn['education']
coll = db['courses']


@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    if request.method == 'POST':
        query = request.form['search_term']
        pipeline = [
            {"$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "plot_embedding_hf",
                "numCandidates": 100,
                "limit": 10,
                "index": "vector_index",
            }}
        ]
        result = list(coll.aggregate(pipeline))

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True,port=2610)