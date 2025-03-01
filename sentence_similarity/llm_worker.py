from PyQt5.QtCore import QThread, pyqtSignal
from sentence_similarity.logging_tools import Logging_Tools

class ModelWorker(QThread):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal()

    def __init__(self, model, model_name, sentences, parent=None):
        super().__init__(parent)
        self.model = model
        self.model_name = model_name
        self.sentences = sentences
        self.logger = Logging_Tools()

    def run(self):
        # Create log and excel files
        print(f"Running {self.model_name} model worker")
        
        if self.model_name == "NLI":
            self.logger.create_csv_file(f"{self.model_name}_log.csv", "Results", {"Sentence1": [], "Sentence2": [], "label": [], "score": []})
        elif self.model_name == "Sentiment Analysis":
            self.logger.create_csv_file(f"{self.model_name}_log.csv", "Results", {"Sentence1": [], "Sentence2": [], "sentiment_1": [], "sentiment_2": []})
        else:
            self.logger.create_csv_file(f"{self.model_name}_log.csv", "Results", {"Sentence1": [], "Sentence2": [], "Result": []})
        
        # Compare the sentences
        results = []
        total_comparisons = len(self.sentences) * (len(self.sentences) - 1) // 2
        completed = 0
        
        for i, sentence1 in enumerate(self.sentences):
            for j, sentence2 in enumerate(self.sentences):
                if i < j:  # Only compare each pair once
                    # Calculate similarity
                    try:
                        result = self.model.calculate_similarity(sentence1, sentence2)
                        
                        # Create result dict based on model type
                        if self.model_name == "NLI":
                            result_dict = {
                                "Sentence1": sentence1,
                                "Sentence2": sentence2,
                                "label": result["label"],
                                "score": result["score"],
                                "Result": f"{result['label']}: {result['score']:.4f}"
                            }
                            self.logger.append_to_csv(f"{self.model_name}_log.csv", "Results", 
                                                     {"Sentence1": sentence1, "Sentence2": sentence2, 
                                                      "label": result["label"], "score": result["score"]})
                        elif self.model_name == "Sentiment Analysis":
                            result_dict = {
                                "Sentence1": sentence1,
                                "Sentence2": sentence2,
                                "sentiment_1": result[0],
                                "sentiment_2": result[1],
                                "Result": f"S1: {result[0]}, S2: {result[1]}"
                            }
                            self.logger.append_to_csv(f"{self.model_name}_log.csv", "Results", 
                                                     {"Sentence1": sentence1, "Sentence2": sentence2, 
                                                      "sentiment_1": result[0], "sentiment_2": result[1]})
                        else:
                            # For numeric results, format as float
                            if isinstance(result, (int, float)):
                                formatted_result = f"{float(result):.4f}"
                            else:
                                formatted_result = str(result)
                            
                            result_dict = {
                                "Sentence1": sentence1,
                                "Sentence2": sentence2,
                                "Result": formatted_result
                            }
                            self.logger.append_to_csv(f"{self.model_name}_log.csv", "Results", 
                                                     {"Sentence1": sentence1, "Sentence2": sentence2, "Result": result})
                        
                        results.append(result_dict)

                    except Exception as e:
                        result_dict = {
                            "Sentence1": sentence1,
                            "Sentence2": sentence2,
                            "Result": f"Error: {str(e)}"
                        }
                        results.append(result_dict)
                        
                    # Update progress
                    completed += 1
                    progress = int((completed / total_comparisons) * 100)
                    self.progress_signal.emit(progress)
                    
                    # Send result immediately for real-time updates
                    self.result_signal.emit(result_dict)
        
        self.finished_signal.emit()
