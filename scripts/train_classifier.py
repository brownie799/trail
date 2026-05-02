"""Template script to fine-tune BERT for misinformation classification.

Replace dataset loading and trainer config as needed.
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "bert-base-uncased"

if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=3)
    print("Loaded model/tokenizer. Add Trainer pipeline to fine-tune and export.")
