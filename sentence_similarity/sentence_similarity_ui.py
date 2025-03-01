import sys
import os
import json
sys.path.append(os.getcwd())

import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QPushButton, QTextEdit, QTabWidget, 
                            QTableWidget, QTableWidgetItem, QSplitter, QFileDialog,
                            QGroupBox, QLineEdit, QMessageBox, QProgressBar, QScrollArea,
                            QSizePolicy, QListWidget, QInputDialog)

from sentence_similarity.sentence_similarity_comperators import (
    SentenceComparator_Word2Vec,
    SentenceComparator_Ollama,
    SentenceComparator_semantic,
    SentenceComparator_bert_cosine,
    SentenceComparator_SBERT,
    SentenceComparator_NLI,
    SentenceComparator_sentiment_analysis
)

from sentence_similarity.model_worker import ModelWorker

class SentenceSimilarityUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentence Similarity Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Storage file path
        self.storage_file = "sentence_similarity/utils/pyqt_app_storage.json"
        
        # Initialize models dictionary
        self.models = {}
        self.current_model = None
        self.current_model_name = ""
        self.default_sentences = [
            "C'nin dikkat ve özen yükümlülüğüne aykırı davranmış olması nedeniyle kusurlu olduğu değerlendirilebilir.",
            "C'nin dikkat ve özen yükümlülüğüne aykırı davranmış olması nedeniyle kusurlu olduğu değerlendirilemez.",
            "C kişisi marketten alışveriş yapmıştır ve kasada ödeme yapmadan çıkmıştır.",
            "C kişisi kasada ödeme yapmadan marketten çıkmıştır.",
            "C kasaya ödeme yapması gerekirken yapmamıştır."
        ]
        
        # Create the main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create the tab widget
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.setup_tab = QWidget()
        self.results_tab = QWidget()
        
        self.tabs.addTab(self.setup_tab, "Setup & Run")
        self.tabs.addTab(self.results_tab, "Results")
        
        # Load saved sentences
        self.sentences = self.load_sentences()
        
        # Setup the tabs
        self.init_setup_tab()
        self.init_results_tab()
        
        # Current results
        self.current_results = []
        
        # Create log directory if it doesn't exist
        if not os.path.exists("log"):
            os.makedirs("log")
    
    def load_sentences(self):
        # Load sentences from the JSON file if it exists
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('sentences', self.default_sentences)
            except Exception as e:
                print(f"Error loading sentences: {e}")
                return self.default_sentences
        else:
            return self.default_sentences
    
    def save_sentences(self):
        # Save the current sentences to the JSON file
        try:
            sentences = [self.sentences_list.item(i).text() for i in range(self.sentences_list.count())]
            data = {'sentences': sentences}
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Failed to save sentences: {str(e)}")
    
    def init_setup_tab(self):
        layout = QVBoxLayout(self.setup_tab)
        
        # Model selection
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout(model_group)
        
        model_selector_layout = QHBoxLayout()
        model_selector_layout.addWidget(QLabel("Select Model:"))
        
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "Word2Vec", 
            "Semantic", 
            "BERT Cosine", 
            "SBERT", 
            "NLI", 
            "Sentiment Analysis", 
            "Ollama"
        ])
        model_selector_layout.addWidget(self.model_combo)
        
        self.load_model_btn = QPushButton("Load Model")
        self.load_model_btn.clicked.connect(self.load_model)
        model_selector_layout.addWidget(self.load_model_btn)
        
        model_layout.addLayout(model_selector_layout)
        
        # Additional parameters for Ollama
        self.ollama_params_group = QGroupBox("Ollama Parameters")
        ollama_params_layout = QHBoxLayout(self.ollama_params_group)
        
        ollama_params_layout.addWidget(QLabel("System Prompt:"))
        self.system_prompt_input = QLineEdit("You are an assistant that evaluates the similarity between two sentences. Don't explain only give the result. Your response have to be in the format of: 'Result': <Result>.")
        ollama_params_layout.addWidget(self.system_prompt_input)
        
        ollama_params_layout.addWidget(QLabel("Llama Version:"))
        self.llama_version_input = QLineEdit("phi4:latest")
        ollama_params_layout.addWidget(self.llama_version_input)
        
        ollama_params_layout.addWidget(QLabel("Temperature:"))
        self.temperature_input = QLineEdit("0.4")
        ollama_params_layout.addWidget(self.temperature_input)
        
        model_layout.addWidget(self.ollama_params_group)
        self.ollama_params_group.setVisible(False)
        
        self.model_combo.currentTextChanged.connect(self.update_model_params_visibility)
        
        layout.addWidget(model_group)
        
        # Test sentences with list appearance
        sentences_group = QGroupBox("Test Sentences")
        sentences_layout = QVBoxLayout(sentences_group)
        
        # List widget for sentences
        self.sentences_list = QListWidget()
        sentences_layout.addWidget(self.sentences_list)
        
        # Add the default or loaded sentences to the list
        for sentence in self.sentences:
            self.sentences_list.addItem(sentence)
        
        # Buttons for managing sentences
        btn_layout = QHBoxLayout()
        
        self.add_sentence_btn = QPushButton("Add Sentence")
        self.add_sentence_btn.clicked.connect(self.add_sentence)
        btn_layout.addWidget(self.add_sentence_btn)
        
        self.remove_sentence_btn = QPushButton("Remove Selected")
        self.remove_sentence_btn.clicked.connect(self.remove_selected_sentence)
        btn_layout.addWidget(self.remove_sentence_btn)
        
        sentences_layout.addLayout(btn_layout)
        
        layout.addWidget(sentences_group)
        
        # Run section
        run_group = QGroupBox("Run Test")
        run_layout = QVBoxLayout(run_group)
        
        self.progress_bar = QProgressBar()
        run_layout.addWidget(self.progress_bar)
        
        self.run_btn = QPushButton("Run Test")
        self.run_btn.clicked.connect(self.run_test)
        self.run_btn.setEnabled(False)  # Disable until model is loaded
        run_layout.addWidget(self.run_btn)
        
        layout.addWidget(run_group)
    
    def add_sentence(self):
        # Open an input dialog to get a new sentence
        sentence, ok = QInputDialog.getText(self, "Add Sentence", "Enter a new sentence:")
        if ok and sentence:
            self.sentences_list.addItem(sentence)
            self.save_sentences()  # Save after adding a new sentence
    
    def remove_selected_sentence(self):
        # Remove the selected sentence from the list
        selected_items = self.sentences_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a sentence to remove.")
            return
        
        for item in selected_items:
            row = self.sentences_list.row(item)
            self.sentences_list.takeItem(row)
        
        self.save_sentences()  # Save after removing a sentence
    
    def init_results_tab(self):
        layout = QVBoxLayout(self.results_tab)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["Sentence 1", "Sentence 2", "Result"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.results_table)
    
    def update_model_params_visibility(self):
        # Show Ollama parameters only when Ollama is selected
        self.ollama_params_group.setVisible(self.model_combo.currentText() == "Ollama")
    
    def load_model(self):
        model_name = self.model_combo.currentText()
        self.current_model_name = model_name
        
        try:
            if model_name == "Word2Vec":
                self.current_model = SentenceComparator_Word2Vec()
            elif model_name == "Semantic":
                self.current_model = SentenceComparator_semantic()
            elif model_name == "BERT Cosine":
                self.current_model = SentenceComparator_bert_cosine()
            elif model_name == "SBERT":
                self.current_model = SentenceComparator_SBERT()
            elif model_name == "NLI":
                self.current_model = SentenceComparator_NLI()
            elif model_name == "Sentiment Analysis":
                self.current_model = SentenceComparator_sentiment_analysis()
            elif model_name == "Ollama":
                system_prompt = self.system_prompt_input.text()
                llama_version = self.llama_version_input.text()
                temperature = float(self.temperature_input.text())
                self.current_model = SentenceComparator_Ollama(system_prompt, llama_version, temperature)
            
            self.models[model_name] = self.current_model
            self.run_btn.setEnabled(True)
            
            QMessageBox.information(self, "Model Loaded", f"{model_name} model loaded successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error Loading Model", f"Failed to load {model_name} model: {str(e)}")
    
    def run_test(self):
        if not self.current_model:
            QMessageBox.warning(self, "No Model Selected", "Please load a model first.")
            return
        
        # Get sentences from the list widget
        sentences = [self.sentences_list.item(i).text() for i in range(self.sentences_list.count())]
        
        if len(sentences) < 2:
            QMessageBox.warning(self, "Not Enough Sentences", "Please enter at least two sentences for comparison.")
            return
        
        # Disable UI during test
        self.run_btn.setEnabled(False)
        self.load_model_btn.setEnabled(False)
        
        # Clear previous results
        self.results_table.setRowCount(0)
        self.current_results = []
        
        # Create and start worker thread
        self.worker = ModelWorker(self.current_model, self.current_model_name, sentences)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.result_signal.connect(self.add_result)
        self.worker.finished_signal.connect(self.finish_test)
        self.worker.start()
        
        # Switch to results tab
        self.tabs.setCurrentIndex(1)
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def add_result(self, result):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        self.results_table.setItem(row, 0, QTableWidgetItem(result["Sentence1"]))
        self.results_table.setItem(row, 1, QTableWidgetItem(result["Sentence2"]))
        self.results_table.setItem(row, 2, QTableWidgetItem(str(result["Result"])))
        
        # Store the result for visualization
        self.current_results.append(result)
    
    def finish_test(self):
        # Re-enable UI
        self.run_btn.setEnabled(True)
        self.load_model_btn.setEnabled(True)
        
        # Update the progress bar to 100%
        self.progress_bar.setValue(100)
        
        QMessageBox.information(self, "Test Complete", "Sentence comparison test completed successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SentenceSimilarityUI()
    window.show()
    sys.exit(app.exec_())