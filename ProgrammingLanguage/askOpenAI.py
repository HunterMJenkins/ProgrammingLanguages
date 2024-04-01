import json
import fitz  # PyMuPDF
from openai import OpenAI
import gensim.models
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

# Initialize the OpenAI client
OpenAI.api_key = 'YOUR_API_KEY'  # Replace with your actual API key
client = OpenAI()

def get_context(pdf_path, start_page=1, end_page=1):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(start_page - 1, end_page):
            page = pdf.load_page(page_num)
            text += page.get_text()
    return text

def ask_question(question, context):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"{question}. Here is the context: {context}"}
        ]
    )
    return completion.choices[0].message.content

def askOpenAI(info):
    pdf_path = 'Tag_that_issue_Applying_API-domain_labels_in_issue.pdf'
    pdf_text = get_context(pdf_path, 19, 19)  # Adjust the page numbers as needed

    question = f"Given the information on the imported class decide what is the most optimal classifier of the 31 different labels, In your answer just state the label of the most optimal classifier (example: Big Data, Cloud, logic, Parser ...) dependent on the descriptions. Here is the information on the imports: {info}"
    answer = ask_question(question, pdf_text)
    #print(f"Question: {question}")
    #print(answer)

    # Return the answer for further processing if needed
    return answer

def preprocess(doc):
    stop_words = set(stopwords.words('english'))
    return [token for token in simple_preprocess(doc) if token not in stop_words]

def train_doc2vec_model(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        labels = [(key, value) for item in data['Items'] for key, value in item.items()]

    tagged_documents = [gensim.models.doc2vec.TaggedDocument(words=preprocess(title + ' ' + description), tags=[str(i)]) for i, (title, description) in enumerate(labels)]
    model = gensim.models.Doc2Vec(tagged_documents, vector_size=100, window=5, min_count=1, workers=4, epochs=40)
    return model, labels

def analyze_similarities(model, labels, class_descriptions):
    for imp, desc in class_descriptions.items():
        processed_desc = preprocess(desc)
        inferred_vector = model.infer_vector(processed_desc)
        sims = model.dv.most_similar([inferred_vector], topn=1)
        highest_label_index = int(sims[0][0])
        highest_similarity_score = sims[0][1]
        highest_label_title, highest_label_description = labels[highest_label_index]
        #print(f"Highest similarity for '{imp}' is '{highest_label_title}' with a score of {highest_similarity_score:.4f}")

    return highest_label_title

def main(info_text, import_text):

    # Create a dictionary with import_text as the key and info_text as the value
    class_descriptions = {import_text: info_text}

    print("Import: " , import_text)
    # Call askOpenAI or perform some analysis with info_text
    print("AI: " , askOpenAI(info_text))
    # Continue with the rest of the processing
    json_file_path = 'labels.json'
    model, labels = train_doc2vec_model(json_file_path)

    # Make sure class_descriptions is correctly formatted as a dictionary for analyze_similarities
    print("SimScore: " , analyze_similarities(model, labels, class_descriptions), "\n----------------------------------")




if __name__ == '__main__':
    main()
