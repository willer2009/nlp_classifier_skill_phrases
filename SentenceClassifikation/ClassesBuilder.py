import json
import random

from spacy.lang.ja import separate_sentences


class ClassBuilder:

    def __init__(self):
        self.class2sentences = dict()
        self.buildClasses()
        self.create_classification_data()

    def buildClasses(self):
        with open('../full_jobs_20210416.json', 'r', encoding="utf8") as f:
            jobs = json.load(f)
            self.class2sentences['paragraph_separator'] = set()
            for job in jobs:
                for key in job.keys():
                    if key not in self.class2sentences.keys():
                        self.class2sentences[key] = set()
                    content = job[key].split('\n')
                    if len(content) > 0:
                        if key != 'task_block' and key != 'profile_block':
                            self.class2sentences['paragraph_separator'].add(content[0])
                        [self.class2sentences[key].add(sentence) for sentence in content if
                         len(sentence) > 0]
            for job_title in self.class2sentences['job_title']:
                self.class2sentences['id_block'].remove(job_title)
            for separator in self.class2sentences['paragraph_separator']:
                try:
                    self.class2sentences['id_block'].remove(separator)
                    self.class2sentences['job_title'].remove(separator)
                    self.class2sentences['task_block'].remove(separator)
                    self.class2sentences['profile_block'].remove(separator)
                except:
                    pass


    def create_classification_data(self):
        result = []
        for key in self.class2sentences.keys():
            prefix = '_label_' + self.getLabel(key)
            for sentence in self.class2sentences[key]:
                result.append(prefix + ',\"' + sentence.replace('\"', '') + '\"')
        random.shuffle(result)
        with open('training_classificator.csv', 'w', encoding='utf-8') as f:
            f.write('label, text\n')
            for line in result:
                f.write(line + '\n')

    def getLabel(self, key):
        if key == 'job_title' or key == 'paragraph_separator':
            return key
        if key == 'task_block' or key == 'profile_block':
            return 'potential_skill_phrase'
        return 'do_not_consider'


if __name__ == '__main__':
    cb = ClassBuilder()
