import ollama

class SentenceComparator:
    def __init__(self,model_name):
        self.model_name = model_name
    
    def calculate_similarity(self,sentence_1,sentence_2):
        raise NotImplementedError

class SentenceComparator_Ollama( SentenceComparator ):
    """
    SentenceComparator_Ollama is a class that uses Ollama API to calculate the similarity between two sentences.
    
    Args:
        system_prompt (str): The prompt that is used to generate the model.
        llama_version (str): The version of the llama model.
        temperature (float): The temperature parameter of the model.
        model_name (str): The name of the model.
    """

    def __init__(self,system_prompt, llama_version="llama3.1", temperature=0.4):

        super().__init__(llama_version)

        # Ollama model parameters
        self.system_prompt = system_prompt
        self.llama_version = llama_version
        self.temperature = temperature

        # Fake role messages to support the model
        self.role_messages = [
                {
                    'role': 'user',
                    'content': 'İlk cümle: C kişisi kasada ödeme yapmadan marketten çıkmıştır, İkinci cümle: C kişisi marketten alışveriş yapmıştır ve kasada ödeme yapmadan çıkmıştır'
                },
                {
                    'role': 'assistant',
                    'content': "değerlendirme: 0"
                },
                {
                    'role': 'user',
                    'content': 'İlk cümle: Havalar güzelken denize gitmek çok iyi olur., İkinci cümle: Bir insan ev almadan önce araba parası biriktirmeli.'
                },
                {
                    'role': 'assistant',
                    'content': "değerlendirme: 1"
                }
            ]
        self.generate_model()
    
    def generate_model(self):
        modelfile = f'''
        FROM {self.llama_version}
        SYSTEM {self.system_prompt} 
        PARAMETER temperature {self.temperature}
        '''
        ollama.create(model=f'MAHDAN_{self.llama_version}', modelfile=modelfile)

    def calculate_similarity(self,sentence_1,sentence_2):
        sentence_in = 'İlk Cümle: ' + sentence_1 + ' ,\n İkinci Cümle: ' + sentence_2        

        # Concat messages and sentence
        messages_temp = self.role_messages.copy()

        messages_temp.append({
            'role': 'user',
            'content': sentence_in
        })

        response = ollama.chat(model=f'MAHDAN_{self.llama_version}', messages= messages_temp)

        return response['message']['content']

# Semantic Similarity
from sentence_transformers import SentenceTransformer, util

#model_name = 'paraphrase-MiniLM-L6-v2'
# Class of Semantic Similarity
class SentenceComparator_semantic(SentenceComparator):
    """
    SentenceComparator_semantic is a class that uses SentenceTransformer to calculate the similarity between two sentences.

    Args:
        model_name (str): The name of the model.
    """
    
    def __init__(self, model_name='paraphrase-MiniLM-L6-v2'):
        super().__init__(model_name)

        # Load the model
        self.model_name = model_name
        self.model = self.generate_model()

    def generate_model(self):
        return SentenceTransformer(self.model_name)
    
    def get_embeddings(self, sentences):
        return self.model.encode(sentences)

    def calculate_similarity(self, sentence_1, sentence_2):
        embeddings = self.get_embeddings([sentence_1, sentence_2])
        return util.cos_sim(embeddings[0], embeddings[1])


import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

#model_name = 'bert-base-multilingual-cased'
# Calculate cosine similarity between two sentences with BERT
class SentenceComparator_bert_cosine(SentenceComparator):
    """
    SentenceComparator_bert_cosine is a class that uses BERT to calculate the similarity between two sentences.

    Args:
        model_name (str): The name of the model.
    """
    
    
    def __init__(self, model_name='bert-base-multilingual-cased'):
        super().__init__(model_name)

        # Load the model
        self.model_name = model_name
        self.model = self.generate_model()

    def generate_model(self):
        return BertModel.from_pretrained(self.model_name)
    
    def get_embeddings(self, sentence):

        tokenizer = BertTokenizer.from_pretrained(self.model_name)
        inputs = tokenizer(sentence, return_tensors='pt')

        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)

        return embeddings
    
    def calculate_similarity(self, sentence_1, sentence_2):
        embeddings1 = self.get_embeddings(sentence_1)
        embeddings2 = self.get_embeddings(sentence_2)
        
        return cosine_similarity(embeddings1, embeddings2)
    

from sentence_transformers import SentenceTransformer, util
import torch
# Load the pre-trained SBERT model
#model_name = 'paraphrase-multilingual-mpnet-base-v2'
# Class of SBERT Similarity
class SentenceComparator_SBERT(SentenceComparator):
    """
    SentenceComparator_SBERT is a class that uses SentenceTransformer to calculate the similarity between two sentences.

    Args:
        model_name (str): The name of the model.
    """
    
    def __init__(self, model_name='paraphrase-multilingual-mpnet-base-v2'):
        super().__init__(model_name)

        # Load the model
        self.model_name = model_name
        self.model = self.generate_model()
        
    def generate_model(self):
        return SentenceTransformer(self.model_name)
    
    def get_embeddings(self, sentences):
        return self.model.encode(sentences, convert_to_tensor=True)
    
    def calculate_similarity(self, sentence_1, sentence_2):
        embeddings = self.get_embeddings([sentence_1, sentence_2])
        return util.pytorch_cos_sim(embeddings[0], embeddings[1])
    

from transformers import pipeline
# NLI pipeline oluşturma (Türkçe destekleyen model kullanılabilir)
#nli_model = pipeline("text-classification", model="microsoft/deberta-large-mnli")
class SentenceComparator_NLI(SentenceComparator):
    """
    SentenceComparator_NLI is a class that uses Hugging Face's NLI pipeline to calculate the similarity between two sentences.
    It requires internet connection to run.
    
    Args:
        model_name (str): The name of the model.
    """

    def __init__(self, model_name="microsoft/deberta-large-mnli"):
        super().__init__(model_name)
        self.model_name = model_name
        self.model = self.generate_model()

    def generate_model(self):
        return pipeline("text-classification", model=self.model_name)
    
    def calculate_similarity(self, sentence_1, sentence_2):
        input_sentence = sentence_1 + ' [SEP] ' + sentence_2
        result = self.model(input_sentence)
        return result[0]
    

# Sentiment Analysis class
class SentenceComparator_sentiment_analysis(SentenceComparator):
    """
    SentenceComparator_sentiment_analysis is a class that uses Hugging Face's sentiment analysis pipeline to calculate the similarity between two sentences.

    Args:
        model_name (str): The name of the model.
    """
    def __init__(self,model_name="saribasmetehan/bert-base-turkish-sentiment-analysis"):
        super().__init__(model_name)
        
        # Load the model
        model_id = model_name
        self.classifer = pipeline("text-classification",model = model_id)
    
    def clearify_sentence(self, sentence):
        return sentence.lower().replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace("(", "").replace(")", "")

    def calculate_similarity(self, sentence_1, sentence_2):
        sentence_1 = self.clearify_sentence(sentence_1)
        sentence_2 = self.clearify_sentence(sentence_2)

        pred1 = self.classifer(sentence_1)
        pred2 = self.classifer(sentence_2)

        #is_similar = pred1[0]["label"] == pred2[0]["label"]
        
        return (pred1[0]["label"], pred2[0]["label"])
    
# Word2Vec Similarity
from gensim.models import Word2Vec
class SentenceComparator_Word2Vec(SentenceComparator):
    """
    SentenceComparator_Word2Vec is a class that uses Word2Vec to calculate the similarity between two sentences.

    Args:
        model_name (str): The name of the model.
    """
    def __init__(self, model_name="utils/word2vec/w2v_.model"):
        super().__init__(model_name)

        self.model = self.generate_model(model_name)

    def generate_model(self, model_name):
        return Word2Vec.load(model_name)
    
    def clean_sentence(self, sentence):
        return sentence.lower().replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace("(", "").replace(")", "")
    
    def extract_key_features(self, words_1, words_2):
        
        # Nested iteration to compare each word in the sentences
        #Dict: {word_1:{word_comp1:score, word_comp2:score, ...}, word_2:{word_comp1:score, word_comp2:score, ...}}
        searched_pairs = [];similarity_dict = {}

        for word_1 in words_1:
            if word_1 not in similarity_dict:
                similarity_dict.update({word_1:{}})
            for word_2 in words_2:
                if (word_1, word_2) in searched_pairs or (word_2, word_1) in searched_pairs:
                    continue
                try:
                    searched_pairs.append((word_1, word_2))
                    # Calculate the similarity between the words
                    similarity_dict[word_1].update({word_2:self.model.wv.similarity(word_1, word_2)})
                except:
                    pass
        return similarity_dict
    
    def calculate_similarity(self, sentence_1, sentence_2):
        # Clean the sentences and split them into words
        sentence_1 = self.clean_sentence(sentence_1); words_1 = sentence_1.split()
        sentence_2 = self.clean_sentence(sentence_2); words_2 = sentence_2.split()

        # Extract key features
        similarity_dict = self.extract_key_features(words_1, words_2)
            
        # Extract informations from the similarity_dict
        key_features = []
        for key, value in similarity_dict.items():
            if len(value) > 0:
                # Sort and get the best match
                sorted_dict = sorted(value.items(), key=lambda x:x[1], reverse=True)
                max_score = sorted_dict[0][1]
                best_key = sorted_dict[0][0]

                key_features.append({"key":key, "score":max_score,"best_match":best_key})

        # Calculate the average score
        avg_score = sum([x["score"] for x in key_features]) / len(key_features)

        return avg_score#,key_features


import jpype
import os
import atexit

#ZEMBEREK https://github.com/ahmetaa/zemberek-nlp : Bakılacak
class SentenceComparator_jpype(SentenceComparator):
    """
    SentenceComparator_jpype is a class that uses Zemberek to calculate the similarity between two sentences.

    Args:
        model_name (str): The name of the model.
    """
    
    def __init__(self):
        super().__init__("Zemberek")

        # JVM'i başlat
        if not jpype.isJVMStarted():
            jpype.startJVM("C:/Program Files/Java/jdk-22/bin/server/jvm.dll", 
                           "-Djava.class.path=utils/zemberek-full.jar")
        
        # Zemberek sınıfını başlat
        TurkishMorphology = jpype.JClass('zemberek.morphology.TurkishMorphology')
        self.morphology = TurkishMorphology.createWithDefaults()

        # JVM'i kapatmayı atexit ile garanti altına al
        atexit.register(self.shutdown_jvm)
    
    def calculate_similarity(self, sentence_1, sentence_2):
        # Cümlelerin analizini yap
        analysis1 = self.morphology.analyzeSentence(sentence_1)
        analysis2 = self.morphology.analyzeSentence(sentence_2)
        return analysis1, analysis2
    
    def shutdown_jvm(self):
        # JVM'i kapat
        if jpype.isJVMStarted():
            jpype.shutdownJVM()

# Örnek kullanım

#print(jpype.isJVMStarted())
#jvm = SentenceComparator_jpype()
#test_sentence = "Bu güzel bir gün."
#print(jvm.calculate_similarity("keşke hemen şurada ölsen ve gebersen.", test_sentence))

if __name__ == "__main__":
    # Create a SentenceComparator object
    pass