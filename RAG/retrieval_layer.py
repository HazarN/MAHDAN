import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import ast
import ollama # Import the ollama library

def load_embeddings(embedding_str):
    try:
        # Remove any leading/trailing whitespace
        fixed = embedding_str.strip()

        # Remove outer brackets if they exist
        if fixed.startswith('[') and fixed.endswith(']'):
            fixed = fixed[1:-1] # Remove the first and last character

        # Replace any sequence of one or more spaces with a single comma
        # This handles cases like " 0.1  0.2" -> "0.1,0.2"
        fixed = ','.join(fixed.split())

        # Re-add the outer brackets to form a valid list literal
        fixed = f"[{fixed}]"

        return np.array(ast.literal_eval(fixed))
    except Exception as e:
        print("Hatalı satır:", embedding_str)
        raise e

# CSV'yi oku ve embedding'leri dönüştür
df = pd.read_csv("RAG/answers_with_embeddings.csv")
df["student_emb"] = df["student_emb"].apply(load_embeddings)

# Embedding modeli
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

# FAISS index
student_embeddings = np.vstack(df["student_emb"].values)
index = faiss.IndexFlatL2(student_embeddings.shape[1])
index.add(student_embeddings)

# Benzer cevapları getir
def get_similar_answers(new_answer, top_k=3):
    new_emb = model.encode(new_answer)
    D, I = index.search(np.array([new_emb]), top_k)
    return df.iloc[I[0]], new_emb

# Prompt üret
def generate_feedback_prompt(new_answer, similar_answers_df):
    context = "\n\n".join([
        f"Öğrenci Cevabı: {row.student_answer}\nPuan: {row.score}" for _, row in similar_answers_df.iterrows()
    ])
    prompt = f"""
Sen bir hukuk sınavı değerlendiricisisin.
Yeni öğrenci cevabını aşağıda verdim:
\"{new_answer}\"

Benzer geçmiş öğrenci cevapları ve puanları şunlardır:
{context}

Bu yeni cevaba 100 üzerinden kaç puan verirdin ve neden?
Cevap:"""
    return prompt

# Function to call Gemma via Ollama
def call_gemma_with_ollama(prompt, model_name="gemma3:12b"):
    """
    Sends a prompt to the specified Gemma model running via Ollama.
    """
    try:
        # Ensure Ollama server is running (it usually runs in the background after installation)
        response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Error calling Ollama with Gemma ({model_name}): {e}")
        print("Please ensure Ollama is running and the model is downloaded ('ollama run gemma3:12b' in terminal).")
        return "Error generating feedback."

# Yeni öğrenci cevapları (örnek)
new_answers = [
    "Failin kastı yoktur çünkü hata haksızlığı ortadan kaldırır.",
    "İştirak halinde işlenen suçlarda ceza sorumluluğu herkes için farklı değerlendirilir.",
    "Kusur yeteneği olmayan bir kişi ceza sorumluluğu taşımaz."
]

# Prompt'ları üretip kaydet
results = []
for i, ans in enumerate(new_answers):
    print(f"Processing new answer {i+1}/{len(new_answers)}: \"{ans}\"")
    similar_df, new_emb = get_similar_answers(ans, top_k=3)
    prompt = generate_feedback_prompt(ans, similar_df)

    # Call Gemma via Ollama to get feedback
    generated_feedback = call_gemma_with_ollama(prompt, model_name="gemma3:12b") # Use "gemma:2b" if you pulled the 2b model

    results.append({
        "id": i,
        "new_student_answer": ans,
        "prompt": prompt,
        "generated_feedback": generated_feedback # Store the generated feedback
    })

output_df = pd.DataFrame(results)
output_df.to_csv("RAG/generated_prompts_and_feedback.csv", index=False)
print("✅ Prompts and generated feedback saved to: RAG/generated_prompts_and_feedback.csv")