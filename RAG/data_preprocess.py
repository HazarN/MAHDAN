import json
import pandas as pd

with open("RAG/answers.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for question in data["questions"]:
    question_id = question["question_id"]
    scenario = data["scenario"]
    question_text = question["text"]
    model_answer = question["model_answer"]
    for student in question["students_answers"]:
        student_id = student["student_id"]
        student_answer = student["answer"]
        score = data["scores"][question_id][student_id]
        rows.append({
            "question_id": question_id,
            "scenario": scenario,
            "question_text": question_text,
            "model_answer": model_answer,
            "student_id": student_id,
            "student_answer": student_answer,
            "score": score
        })

df = pd.DataFrame(rows)
df.to_csv("RAG/answers.csv", index=False)
