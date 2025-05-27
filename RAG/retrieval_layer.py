# -*- coding: utf-8 -*-
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

# Benzer cevapları getir
MODEL = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
def get_similar_answers(new_answer, top_k=3):
    new_emb = MODEL.encode(new_answer)
    D, I = index.search(np.array([new_emb]), top_k)
    return df.iloc[I[0]], new_emb

# Prompt üret
def generate_feedback_prompt(question, new_answer, previous_answer ):
    context = f"Student Answer: {previous_answer['student_answer']} - Score: {previous_answer['score']}"
    
    prompt = f"""
        Sen bir hukuk sınavı değerlendiricisisin.

        Soru:
        \"{question}\"

        Benzer geçmiş öğrenci cevabı:
        \"{context}\"

        Yeni öğrenci cevabı:
        \"{new_answer}\"


        Bu yeni cevaba 100 üzerinden kaç puan verirdin ve neden? Cevabın şu formatta olmalı 'Puan': X, 'Açıklama': Y]
        Cevap:"""
    return prompt

# Function to call Gemma via Ollama
def call_gemma_with_ollama(prompt, model_name="gemma3:12b"):
    response = ollama.chat(model=model_name, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content'].strip()

if __name__ == "__main__":

    # CSV'yi oku ve embedding'leri dönüştür
    df = pd.read_csv("RAG/answers_with_embeddings.csv")
    df["student_emb"] = df["student_emb"].apply(load_embeddings)

    # FAISS index
    student_embeddings = np.vstack(df["student_emb"].values)
    index = faiss.IndexFlatL2(student_embeddings.shape[1])
    index.add(student_embeddings)
    
    # Create new answer dict "answer": , "question":
    new_answers = [
        {"question": "Savaş’ın pişmanlık ve tahrik durumları ceza hukukunda nasıl değerlendirilmektedir? Bu durumların ceza indirimi üzerindeki etkilerini açıklayınız.", "answer":  "Savaş’ın pişmanlık ve tahrik durumları ceza hukukunda önemli bir yere sahiptir. Bu durumlar, failin eylemi gerçekleştirdiği sırada içinde bulunduğu psikolojik durumu yansıtır ve ceza indirimi açısından dikkate alınır. Pișmanlık, failin eyleminden duyduğu üzüntü ve pişmanlıktır. Tahrik ise, failin eylemi gerçekleştirmesine neden olan dışsal bir etken veya olaydır. Ceza hukukunda, bu durumlar failin cezalandırılmasında hafifletici sebep olarak değerlendirilir. Örneğin, savaş sırasında yaşanan travmalar ve psikolojik etkiler, failin eylemini daha az cezalandırılabilir hale getirebilir. Ancak, bu durumların ceza indirimi üzerindeki etkisi, her olayın özel koşullarına bağlı olarak değişir."},
        {"question": "Barış’ın tartışma sırasında Savaş’a yönelik hakaret veya küçük düşürücü ifadeler kullanıp kullanmadığını değerlendiriniz. İfade özgürlüğünün sınırları ve hakaret suçunun nasıl hukuki bir çerçevede ele alınacağını açıklayınız.", "answer": "Barış’ın Savaş’a yönelik hakaret veya küçük düşürücü ifadeler kullanması, ifade özgürlüğünün sınırlarını aşan bir durum olarak değerlendirilebilir. İfade özgürlüğü, demokratik toplumlarda önemli bir haktır, ancak bu hak, başkalarının onurunu ve saygınlığını ihlal etmemelidir. Hakaret suçu, bir kişinin onuruna saldırıda bulunmayı içeren bir eylemdir ve hukuki olarak cezalandırılabilir. Bu nedenle, Barış’ın Savaş’a yönelik ifadeleri, hakaret suçu kapsamında değerlendirilebilir ve hukuki bir çerçevede ele alınmalıdır."},
    ]

    # Loop df questions
    for i, row in df.iterrows():
        question = row["question_text"]

        # Find the new answer for the question
        new_answer = False
        for item in new_answers:
            if item["question"] == question:
                new_answer = item["answer"]
                break
        if not new_answer:
            print(f"New answer not found for question: {question}")
            continue

        # Get similar answers
        similar_answers, new_emb = get_similar_answers(new_answer)

        # Generate feedback prompt
        prompt = generate_feedback_prompt(question, new_answer, row)

        # Call Gemma via Ollama
        response = call_gemma_with_ollama(prompt)

        print(f"Question: {question}")
        print(f"New Answer: {new_answer}")
        print(f"Response: {response}\n")
        