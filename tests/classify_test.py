import os
import sys
import unittest
import simpletransformers
import sklearn

sys.path.append(os.path.abspath("../"))

from hindibert.classify import Classify


class ClassifyTest(unittest.TestCase):
    def test_load_assets(self):
        inst = Classify()

        self.assertIsInstance(
            inst.model,
            simpletransformers.classification.classification_model.ClassificationModel,
        )
        self.assertIsInstance(inst.labeler, sklearn.preprocessing._label.LabelEncoder)

    def test_predictor(self):
        inst = Classify()
        text = [
            "इंडियन प्रीमियर लीग (IPL) में रविवार को खेले गए मुकाबले में दिल्ली कैपिटल्स ने पंजाब किंग्स को 7 विकेट से हरा दिया। दिल्ली में खेले गए मुकाबले में कप्तान ऋषभ पंत की टीम शुरू से ही हावी रही। पंजाब के कप्तान मयंक को छोड़कर टीम का कोई भी बल्लेबाज दिल्ली के बॉलर्स के आगे टिक नहीं सका। इसके बाद शिखर धवन और पृथ्वी शॉ की ताबड़तोड़ शुरुआत ने दिल्ली की जीत सुनिश्चित कर दी। आइए जानते हैं वो 5 पॉइंट जिसकी वजह से दिल्ली ने पंजाब के खिलाफ जीत दर्ज की।"
        ]
        category = inst.predictor(text=text)
        print(category)

        self.assertIsInstance(category, str)
        self.assertEqual(category, "sport", "Should be sport")


if __name__ == "__main__":
    unittest.main()
