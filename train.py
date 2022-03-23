# -*- coding:utf-8 -*-
from tqdm import tqdm
import re
import collections
import pickle

class BPE_token_learner:
    def __init__(self, len):
        self.file = None
        self.vocabulary = collections.defaultdict(int)  # 词汇字典，value为对应的出现频率
        self.book = []  # 语料行
        self.line_list = []  # 从文件直接读入的语料行
        self.book_freq = []
        self.max_len = len

    def set_train_data(self, filename):
        """     从文件中获得训练数据      """
        self.file = open(filename, 'r', encoding='utf-8')
        self.line_list = self.file.readlines()
        self.file.close()

    def basic_init(self):
        """     初始化语料行和词汇词典    """
        temp_book = collections.defaultdict(int)
        print("Initializing book...")
        for i in tqdm(range(len(self.line_list))):
            sentence = self.line_list[i][:-1]  # 去除末端的换行符
            x = ''.join(list(sentence.strip())) + ' </w>'
            temp_book[x] += 1
            if temp_book[x] == 1:
                self.book.append(x)
                self.book_freq.append(1)
            elif temp_book[x] > 1:
                j = self.book.index(x)
                self.book_freq[j] += 1
        print(len(self.book))
        print(len(self.book_freq))
        print("Initialization of book is completed.")

        print("Initializing vocabulary...")
        for i in tqdm(range(len(self.book))):
            words = self.book[i].split()
            for word in words:
                self.vocabulary[word] += self.book_freq[i]
        print("Initialization of vocabulary is completed.")

    def get_pairs(self):
        """     获得词对词典和词对索引词典       """
        pairs = collections.defaultdict(int)
        pairs_index = collections.defaultdict(list)
        for i in range(len(self.book)):
            sentence = self.book[i].split()
            for j in range(len(sentence) - 1):
                pairs[sentence[j], sentence[j+1]] += self.book_freq[i]  # 词对频率
                pairs_index[sentence[j], sentence[j+1]].append(i)  # 词对所在行号
        return pairs, pairs_index

    def update_pairs(self, pairs, pairs_index, best):
        """     更新词对词典以及词对索引词典      """
        index = pairs_index[best]
        for i in index:
            words = self.book[i].split()
            for j in range(len(words) - 1):
                if (words[j], words[j+1]) == best:
                    if 0 < j < len(words)-1:
                        pairs[words[j-1], ''.join([words[j], best[0]])] += 1
                        pairs_index[words[j - 1], ''.join([words[j], best[0]])].append(i)
                        pairs[''.join([words[j], best[1]]), words[j+2]] += 1
                        pairs_index[''.join([words[j], best[1]]), words[j+2]].append(i)
                        del pairs[words[j-1], words[j]]
                        del pairs_index[words[j-1], words[j]]
                        del pairs[words[j], words[j+2]]
                        del pairs_index[words[j], words[j+2]]
                    elif j == 0:
                        pairs[''.join([words[j], best[1]]), words[j + 2]] += 1
                        pairs_index[''.join([words[j], best[1]]), words[j + 2]].append(i)
                        del pairs[words[j], words[j + 2]]
                        del pairs_index[words[j], words[j + 2]]
                    else:
                        pairs[words[j - 1], ''.join([words[j], best[0]])] += 1
                        pairs_index[words[j - 1], ''.join([words[j], best[0]])].append(i)
                        del pairs[words[j - 1], words[j]]
                        del pairs_index[words[j - 1], words[j]]

        del pairs[best]
        del pairs_index[best]
        return pairs, pairs_index


    def update_book(self, pairs_index, change):
        """     更新语料行       """
        word = re.escape(' '.join(change))
        for l in pairs_index[change]:  # 只搜寻change词对所在的所有行号
            self.book[l] = re.sub(word, ''.join(change), self.book[l])

    def process(self):
        print("Vocabulary initialization begins.")
        self.set_train_data('dataset/train_BPE.txt')
        self.basic_init()
        pairs, pairs_index = self.get_pairs()

        pbar = tqdm(total=(self.max_len - len(self.vocabulary)))
        while len(self.vocabulary) < self.max_len:
            k = len(self.vocabulary)
            best = max(pairs, key=pairs.get)
            self.update_book(pairs_index, best)
            pairs, pairs_index = self.update_pairs(pairs, pairs_index, best)
            self.vocabulary[''.join(best)] += 1
            if len(self.vocabulary) > k:  # 检测到有更新
                pbar.update(1)

        pbar.close()

        sorted_tokens_tuple = sorted(
            self.vocabulary.items(),
            key=lambda item: (len(item[0]), item[1]),
            reverse=True
        )
        F = open('vocab/vocabulary2', 'wb')
        pickle.dump(sorted_tokens_tuple, F)
        F.close()


if __name__ == '__main__':
    example = BPE_token_learner(25000)
    example.process()

