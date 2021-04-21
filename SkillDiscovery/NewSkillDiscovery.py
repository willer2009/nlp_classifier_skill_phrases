from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
from flair.tokenization import SpacyTokenizer
import time

from DB_Manipulation.SkillDBManipulation import SkillDB


class SkillDiscovery:

    def __init__(self):
        # load the model you trained
        self.model = SequenceTagger.load('../training_result/best-model.pt')
        self.nlp = spacy.load("de_core_news_lg", disable=["ner"])
        self.db = SkillDB()
        self.sentenceID_to_sentence = self.db.get_map_of_value_to_key(2, 0, "SELECT * FROM Sentences")
        self.sentenceID_to_skill_pos = self.db.get_map_of_value_to_key(2, 1, "SELECT * FROM AnnotatedSentences")

    def get_extracted_skill(self, sentence_as_str):
        doc = self.nlp(sentence_as_str)

        skills_found = set()
        indexes = []
        for sent in doc.sents:
            sent = Sentence(str(sent), use_tokenizer=SpacyTokenizer("de_core_news_sm"), language_code='de')
            pos_to_idx = set()

            for token in sent:
                pos_to_idx.add((token.start_pos, token.end_pos, token.idx))
            self.model.predict(sent)
            for token in sent.get_spans():
                skills_found.add(token.text)
                for elt in pos_to_idx:
                    if elt[0] >= token.start_pos and elt[1] <= token.end_pos:
                        indexes.append(elt[2])

        return skills_found, sorted(indexes)

    def get_annotated_skills_from_sentence(self, sentenceID):
        id_s = self.sentenceID_to_skill_pos[sentenceID]
        array = id_s.replace('[', '').replace(']', '').split(',')
        array = id_s.replace('[', '').replace(']', '').split(',')
        skill_indexes = []
        [skill_indexes.append(int(idx)) for idx in array]

        doc = self.nlp(self.sentenceID_to_sentence[sentenceID])
        skill_set = set()
        i = 0
        skill = ''
        while i < len(skill_indexes):
            idx = skill_indexes[i]
            skill = doc[idx].text
            while i + 1 < len(skill_indexes) and skill_indexes[i + 1] == idx + 1:
                skill += ' ' + doc[idx + 1].text
                i += 1
                idx = skill_indexes[i]

            skill_set.add(skill.lower().strip())
            i += 1
        return skill_set


if __name__ == "__main__":
    skill_discovery = SkillDiscovery()
    skill_to_id = skill_discovery.db.get_map_of_skills_to_id()
    #print(skill_to_id.keys())
    skill_added = 0
    start = time.time()

    for i, sentenceID in enumerate(skill_discovery.sentenceID_to_skill_pos):
        #if i > 50:
            #break
        if i < 104:
            continue
        if i % 10 == 0:
            end = time.time()
            print(f' sentence {i} from {len(skill_discovery.sentenceID_to_skill_pos.keys())} ---> in {end-start} sec ')
            start = time.time()

        known_skill_set = skill_discovery.get_annotated_skills_from_sentence(sentenceID)
        sentence = skill_discovery.sentenceID_to_sentence[sentenceID]
        discovered_skill_set, indexes = skill_discovery.get_extracted_skill(sentence)
        for skill in discovered_skill_set:
            skill_low = skill.lower()
            if skill_low not in skill_to_id.keys():
                try:
                    skill_discovery.db.insert_skills(skill_low, -2)
                    skill_added += 1
                    print(f'New Skill: {skill} - {skill_added}')
                except Exception as e:
                    print(e)
                    pass
