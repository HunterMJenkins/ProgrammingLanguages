import json
import gensim.models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
from FunctionalProgrammingTest import get_collected_data 

# Load the identifiers and descriptions from the JSON file
with open('labels.json', 'r') as file:
    data = json.load(file)
    labels = [(key, value) for item in data['Items'] for key, value in item.items()]

def preprocess(doc):
    stop_words = set(stopwords.words('english'))
    return [token for token in simple_preprocess(doc) if token not in stop_words]

# Prepare documents for Doc2Vec, using only the labels
tagged_documents = [gensim.models.doc2vec.TaggedDocument(words=preprocess(title + ' ' + description), tags=[str(i)]) for i, (title, description) in enumerate(labels)]

# Train the Doc2Vec model
model = gensim.models.Doc2Vec(tagged_documents, vector_size=100, window=5, min_count=1, workers=4, epochs=40)

# Load the class imports and their descriptions (adjust the function to your implementation)
# Assuming you have a function `get_collected_data()` that returns a dictionary where keys are imports and values are descriptions
class_imports, class_descriptions = get_collected_data()

# Compare each class description to the labels and print the highest similarity
for imp, desc in class_descriptions.items():
    processed_desc = preprocess(desc)
    inferred_vector = model.infer_vector(processed_desc)
    sims = model.dv.most_similar([inferred_vector], topn=1)  # Updated to use 'dv' instead of 'docvecs'

    highest_label_index = int(sims[0][0])
    highest_similarity_score = sims[0][1]
    highest_label_title, highest_label_description = labels[highest_label_index]

    print(f"Highest similarity for import {imp} is '{highest_label_title}' with a score of {highest_similarity_score:.4f}")
