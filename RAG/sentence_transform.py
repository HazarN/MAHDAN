from sentence_transformers import SentenceTransformer
import pandas as pd

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
df = pd.read_csv("RAG/answers.csv")

df["student_emb"] = df["student_answer"].apply(lambda x: model.encode(x))
df["model_emb"] = df["model_answer"].apply(lambda x: model.encode(x))
df["question_emb"] = df["question_text"].apply(lambda x: model.encode(x))

# Save the embeddings to a new CSV file
df.to_csv("RAG/answers_with_embeddings.csv", index=False)
