from gensim.models import Word2Vec
from tabulate import tabulate
import time

model = Word2Vec.load("word2vec/w2v_.model")

#q = "barış"
#print(f"\n{q.capitalize()} kelimesine en yakın 10 kelime:\n")
# print(tabulate(model.wv.most_similar(positive=["geliyor","gitmek"],negative=["gelmek"]), headers=["Kelime", "Benzerlik Skoru"]))
#print(tabulate(model.wv.most_similar(q), headers=["Kelime", "Benzerlik Skoru"]))
model.wv.similarity("barış","savaş")