import joblib
import numpy as np
from simpletransformers.classification import ClassificationModel


class Classify:
    def __init__(self):
        # Defining paths and loading the model and the labeler
        self.paths = {
            "model": "../model/hindi_bert_model/model_joblib",
            "labeler": "../model/hindi_bert_model/labeler_joblib",
        }
        self.model = joblib.load(f'{self.paths["model"]}')
        self.labeler = joblib.load(f'{self.paths["labeler"]}')
        print("Loaded assets")

    def predictor(self, text):
        # Predicting the category from the input hindi text

        prediction = self.model.predict(text)
        category = self.labeler.inverse_transform(prediction[0])
        print("made prediction")

        return category[0]
