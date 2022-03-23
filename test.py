# -*- coding:utf-8 -*-
import pprint
import re
from tqdm import tqdm
import pickle

class BPE_token_test:
    def __init__(self):
        self.vocabulary = []
        self.line_list = []

    def get_vocabulary(self, model_name):
        with open(model_name, 'rb') as f:
            vocab = pickle.load(f)
            self.vocabulary = [v[0] for v in vocab]
            f.close()

    def get_test_set(self, testfile):
        with open(testfile, 'r', encoding='utf-8') as f:
            self.line_list = f.readlines()
            f.close()

    def process(self):
        f = None
        try:
            self.get_vocabulary('vocab/vocabulary2')
            self.get_test_set('test_BPE.txt')
            f = open('test_out.txt', 'w')
            for i in tqdm(range(len(self.line_list))):
                temp = self.line_list[i]
                for v in self.vocabulary:
                    if len(v) > 1:
                        temp = re.sub(re.escape(' '.join((v[0], v[1:]))), v, temp)
                f.write(str(temp)[:-2] + ' </w>' + '\n')
        except Exception as e:
            print(e)
            f.close()
        finally:
            if f:
                f.close()

if __name__ == '__main__':
    example = BPE_token_test()
    example.process()