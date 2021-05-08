import joblib
import numpy as np
import pandas as pd
from simpletransformers.classification import ClassificationModel
from sklearn import preprocessing


def load_data(paths):
    train_data = pd.read_csv(f'{paths["dataset"]}/hindi-cleaned-train.csv')
    train_data.columns = ["topic", "text"]
    test_data = pd.read_csv(f'{paths["dataset"]}/hindi-cleaned-test.csv')
    test_data.columns = ["topic", "text"]

    return train_data, test_data


def encode_classes(train_data, test_data):
    labeler = preprocessing.LabelEncoder()

    train_data_encoded = pd.DataFrame(train_data["text"])
    train_data_encoded = train_data_encoded.applymap(str)
    train_data_encoded["label"] = labeler.fit_transform(train_data["topic"])

    test_data_encoded = pd.DataFrame(test_data["text"])
    test_data_encoded = test_data_encoded.applymap(str)
    test_data_encoded["label"] = labeler.fit_transform(test_data["topic"])

    return train_data_encoded, test_data_encoded, labeler


def train_model(num_labels, use_cuda, output_dir, num_train_epochs, train_data):
    model = ClassificationModel(
        "electra",
        "monsoon-nlp/hindi-bert",
        num_labels=num_labels,
        use_cuda=use_cuda,
        args={
            "reprocess_input_data": True,
            "use_cached_eval_features": False,
            "output_dir": output_dir,
            "overwrite_output_dir": True,
            "num_train_epochs": num_train_epochs,
            "fp16": False,
        },
    )
    model.train_model(train_data)

    return model


def evaluate_model(model, test_data):
    eval_text = []
    eval_label = []
    eval_preds = []
    wrongpreds = 0

    for i in range(len(test_data)):
        eval_text.append(test_data["text"][i])
        eval_label.append(test_data["label"][i])

    preds = model.predict(eval_text)

    for i in range(len(preds[1])):
        eval_preds.append(np.argmax(preds[1][i]))

    for i in range(len(eval_label)):
        if eval_preds[i] != eval_label[i]:
            wrongpreds += 1

    accuracy = (len(test_data) - wrongpreds) / len(test_data)

    return accuracy


def main():
    # Variables
    paths = {
        "dataset": "../dataset/bbc_hindi_cleaned",
        "model_save_path": "../model/hindi_bert_model",
    }
    num_labels = 5
    use_cuda = False
    output_dir = paths["model_save_path"]
    num_train_epochs = 3

    # Loading the training and testing data
    train_data, test_data = load_data(paths)

    # Encoding the data with a labeler
    train_data_encoded, test_data_encoded, labeler = encode_classes(
        train_data, test_data
    )

    # Training the Hindi-Bert model
    model = train_model(num_labels, use_cuda, output_dir, num_train_epochs, train_data)

    # Evaluating the Hindi-Bert model
    accuracy = evaluate_model(model, test_data)


if __name__ == "__main__":
    main()
