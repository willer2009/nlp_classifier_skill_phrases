from flair.models import TextClassifier
from flair.data import Sentence

if __name__ == '__main__':

    lines = []
    with open('job1.txt', 'r') as f:
        lines = f.readlines()

    classifier = TextClassifier.load('data2/best-model.pt')

    for line in lines:
        line = line.replace('\n', '')
        if len(line) > 0:
            sentence = Sentence(line)
            classifier.predict(sentence)
            for label in sentence.labels:
                if label.score > 0.75 and label.value == '_label_potential_skill_phrase':
                    print(label.score, ' : ', line)
                else:
                    print(label.score, ' : ', label.value)

