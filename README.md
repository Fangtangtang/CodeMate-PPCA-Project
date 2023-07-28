# CodeMate-PPCA-Project
2023小学期ppca课程codemate项目，基于大语言模型的数据挖掘任务。

## crawler
爬虫任务，爬取了CSDN、Wikipedia、Stackoverflow数据结构相关信息，以问答对形式存储在jsonl文件。

- CSDN
  - `crawler.py`：使用`request`爬取
  - `essence_link.py`：使用`selenium.webdriver`爬取CSDN精华区关于数据结构与算法模块链接
  - `essence_thread_ver.py`：使用`selenium.webdriver`和多线程爬取链接网页
  - `essence.py`：使用`selenium.webdriver`和协程爬取链接网页
- csdnSpider：使用scrapy架构的CSDN爬虫
- Stackoverflow
  - `get_detail.py`：使用`selenium.webdriver`和多线程爬取链接网页
  - `essence.py`：使用`selenium.webdriver`爬取tag为`data_structure`下的链接
- Wikipedia
  - `body.py`：使用`request`爬取带有目录的词条信息
  - `introduction.py`：使用`request`爬取词条简介
  - `other.py`：使用`request`爬取不带有目录的词条信息



## classifier

实现⼀个随机森林分类器，分类高质量（1）和低质量（0）的数据。

- jieba_
  - `cut_word1.py`：使用`jieba`分词
  - `cut_word2.py`：使用`jieba`分词，将标识为代码块（用```包裹）部分，替换为codeBlock
  - `stopwords`：停用词
  - `user-defined`：用户定义的词汇
- sentence_bert_
  - `bert_finetuned.py`：使用sentence_bert模型词向量化
- TfidfVectorize_
  - `grid_search.py`：使用网格搜索，寻找TfidfVectorizer和RandomForestClassifier较优参数组合
  - `use_tfidf.py`：使用TfidfVectorizer词向量化
- word2vec_
  - `train.py`：训练word2vec
  - `use_word2vec.py`：用训练得到的word2vec词向量化

## 使用bert分类任务
使用bert预训练模型，连接下游文本二分类任务。
- 模型训练代码：https://www.kaggle.com/code/fangtangtang/bert-based-binary-classification

将在测试集上表现较好的模型作为基座做集成学习的投票。
- 投票分类器代码：https://www.kaggle.com/code/fangtangtang/bert-based-votingclassifier