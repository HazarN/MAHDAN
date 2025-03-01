import sys;import os;sys.path.append(os.getcwd())

import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QPushButton, QTextEdit, QTabWidget, 
                            QTableWidget, QTableWidgetItem, QSplitter, QFileDialog,
                            QGroupBox, QLineEdit, QMessageBox, QProgressBar, QScrollArea,
                            QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from sentence_similarity.sentence_similarity_comperators import (
    SentenceComparator_Word2Vec,
    SentenceComparator_Ollama,
    SentenceComparator_semantic,
    SentenceComparator_bert_cosine,
    SentenceComparator_SBERT,
    SentenceComparator_NLI,
    SentenceComparator_sentiment_analysis
)

from sentence_similarity.llm_worker import ModelWorker

class SentenceSimilarityUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sentence Similarity Analyzer")
        self.setGeometry(100, 100, 1200, 800)
        
        
        # Initialize models dictionary
        self.models = {}
        self.current_model = None
        self.current_model_name = ""
        self.default_sentences = [
            "C'nin dikkat ve özen yükümlülüğüne aykırı davranmış olması nedeniyle kusurlu olduğu değerlendirilebilir.",
            "C'nin dikkat ve özen yükümlülüğüne aykırı davranmış olması nedeniyle kusurlu olduğu değerlendrilemez.",
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
        
        # Setup the tabs
        self.init_setup_tab()
        self.init_results_tab()
        
        # Current results
        self.current_results = []
        
        # Create log directory if it doesn't exist
        if not os.path.exists("log"):
            os.makedirs("log")
    
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
        
        # Test sentences
        sentences_group = QGroupBox("Test Sentences")
        sentences_layout = QVBoxLayout(sentences_group)
        
        self.sentences_text = QTextEdit()
        self.sentences_text.setPlaceholderText("Enter one sentence per line. These sentences will be compared against each other.")
        self.sentences_text.setText("\n".join(self.default_sentences))
        sentences_layout.addWidget(self.sentences_text)
        
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
        
        # Get sentences from text edit
        sentences_text = self.sentences_text.toPlainText()
        sentences = [line.strip() for line in sentences_text.split('\n') if line.strip()]
        
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