# README

## 任务内容

BPE 编程作业：基于 BPE 的汉语 tokenization 



要求： 采用 BPE 算法对汉语进行子词切割，算法采用 Python (3.0 以上版本)编码实现，自行编制代

码完成算法，不直接用 subword-nmt 等已有模块。 



数据： 

训练语料 train_BPE：进行算法训练，本作业发布时同时提供。 

测试语料 test_BPE：进行算法测试，在本作业提交日前三天发布。 

所有提供的数据均为 Unicode(UTF-8)编码，作业程序的输出文本也务必采用 UTF-8 编码。 



算法的初始词表：建议可以从训练语料 train_BPE 中获取的汉字、字母、标点符号以及其他

基本符号(如_、$等)。 



## 环境信息

Macbook Pro(Apple Silicon), macOS Monterey 12.3

Pycharm, Python 3.9.5

调用库：tqdm, re, collections, pickle



## 算法说明

### train.py

在训练程序中，所有变量和函数均被封装入BPE_token_learner类中。

#### 成员变量

```python
def __init__(self, len):
    self.file = None  # 读入训练文件的指针
    self.vocabulary = collections.defaultdict(int)  # 词汇字典，value为对应的出现频率
    self.line_list = []  # 从文件直接读入的语料行
    self.book = []  # 经过处理后的语料行
    self.book_freq = []  # 对应处理后的语料行 每行所对应的频率
    self.max_len = len  # 最大词汇字典的长度，由用户设定
```

1. 其中book和book_freq在相同的索引值下是对应的，用列表而不是字典来存储的原因是在python下列表检索更快，尤其是在庞大的数据量和循环结构内。

2. 词汇字典中记录出现频率的目的是：给词汇排序，在对文本进行分词的时候优先选择出现概率更高的词。



#### 成员函数

1. **从文件中获得训练数据**

```python
def set_train_data(self, filename)
```

从给定的文件名中获取训练数据集，使用readlines方法读入self.line_list中。



2. **初始化语料行和词汇词典**

```python
def basic_init(self)
```

首先，将self.line_list中的所有内容经过逐行处理（去除末尾的换行符，并换成'</w>'符号）导入self.book中，同时计算对应语料行的频率，存放之相同索引值下的self.book_freq列表中。

然后，从self.book语料行列表中初始化词典，初始化内容为单个汉字，并计算对应的频率，存放至self.vocabulary中。

全程使用tqdm进度条显示初始化进度以及预计剩余时间。



3. **获得词对词典和词对索引词典**

```python
def get_pairs(self)
```

从self.book和self.book_freq中获取词对词典以及词对索引词典。

词对词典的key - value值为：词对 - 对应出现的频率，词对索引词典：词对 - 对应在语料行self.book中出现的索引号。这样做的目的是在后续更新词对词典时，可以直接利用索引寻找其所来源的语料行，不需要将全部语料遍历。



4. **更新词对词典以及词对索引词典**

```python
def update_pairs(self, pairs, pairs_index, best)
```

传入的best参数为所选中的最高出现次数的词对，需要改变词对词典以及词对索引词典的内容。在词对索引词典的帮助下，程序可以精准地定位到其所在的所有语料行中，并遍历这些行的所有词对，修改词典。

修改方式：将best词对合并成为单个词，修改其在语料行中前后相邻的词对并增添在词典中。

最后，删除两个词典中原来被修改的词对以及best词对。



5. **更新语料行**

```python
def update_book(self, pairs_index, change)
```

在修改完词对后，需要对语料行进行分词更新。此时所新增的词对为传入的change，利用self.book_freq，准确定位到change所在语料行，进行分词。



6. **处理过程主程序**

```python
def process(self)
```

伪代码如下：

```
init train_data;
basic_init();
pairs，pairs_index <= get_pairs();

while len(vocabulary) < max_len:
		best <= most_freq(pairs)
		update_book(pairs_index, best)
		pairs，pairs_index <= update_pairs()
		best -> vocabulary
		
sorted(vocabulary, key=freq, sort_mode='decreasing')
dump_to_file(vocabulary)
```



#### 运行过程

设置词表最大长度为25000

<img src="/Users/pd_usr/Library/Application Support/typora-user-images/image-20220322195104310.png" alt="image-20220322195104310" style="zoom:50%;" />

<img src="/Users/pd_usr/Library/Application Support/typora-user-images/image-20220322195338190.png" alt="image-20220322195338190" style="zoom:50%;" />



### test.py

在测试程序中，所有变量和函数均被封装入BPE_token_test类中。

#### 成员变量

```python
self.vocabulary = []  # 词汇列表
self.line_list = []  # 测试语料行
```



#### 成员函数

1. 获取词汇表

```python
def get_vocabulary(self, model_name)
```

从pickle文件中恢复词表，并只取其中的词汇部分存入self.vocabulary中



2. 获取测试数据集

```python
def get_test_set(self, testfile)
```

从给定文件中获取测试数据集，以readlines方式读取并存入self.line_list中



3. 处理过程主程序

```python
def process(self)
```

贪婪匹配，遍历所有语料行以及词汇表，使用正则匹配实现分词。



#### 运行过程

<img src="/Users/pd_usr/Library/Application Support/typora-user-images/image-20220322200033952.png" alt="image-20220322200033952" style="zoom:50%;" />



## 文件目录

![image-20220322201743429](/Users/pd_usr/Library/Application Support/typora-user-images/image-20220322201743429.png)