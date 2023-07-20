from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from gensim.models import Word2Vec 
import jieba
import json

file_name=[
     "highQualityTrain",
     "lowQualityTrain",
     "highQualityTest",
     "lowQualityTest"
]

y_value=[1,0,1,0]

# word2vec
model=Word2Vec.load('new.model')
embedding_size = model.vector_size

# 获取词汇表
vocab = model.wv.index_to_key

# 计算词向量平均值
total_vectors = len(vocab)
embedding_size = model.vector_size
average_vector = []

for word in vocab:
    average_vector.append(model.wv[word])

average_vector = sum(average_vector) / total_vectors

jieba.load_userdict('workspace/word2vec/user-defined')
stopwords=()
with open('workspace/word2vec/stopwords','r',encoding='utf-8') as f:
    stopwords={word.strip() for word in f}


def get_sentence_vector(sentence):
    # 将句子用jieba分词
    word_list=[word for word in jieba.lcut(sentence) if word not in stopwords]
    # 所有能找到分词结果的词
    vectors = [model.wv[word] for word in word_list if word in model.wv]
    if vectors:
        return sum(vectors) / len(vectors)
    else:
        return average_vector


# 将文本数据转换为词向量表示
# 将整句处理成词向量

# 训练集
X_train=[]
Y_train=[]   
for i in range(0,2):             
    with open ('data/{}.jsonl'.format(file_name[i]),'r',encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            ans=data["Answer"]
            question=data["Question"]
            tag=data["Tag"]
            try:
                point=data["Knowledge_Point"]
            except BaseException:
                point=data["Konwledge_Point"]
            X_train.append(get_sentence_vector(tag+point+question+ans))
            Y_train.append(y_value[i])

# 测试集
X_test=[]
Y_test=[]   
for i in range(2,4):             
    with open ('data/{}.jsonl'.format(file_name[i]),'r',encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            ans=data["Answer"]
            question=data["Question"]
            tag=data["Tag"]
            try:
                point=data["Knowledge_Point"]
            except BaseException:
                point=data["Konwledge_Point"]
            X_test.append(get_sentence_vector(tag+point+question+ans))
            Y_test.append(y_value[i])

# for i in range(20,30):
rf_classifier = RandomForestClassifier(n_estimators=190,
                                        max_depth=27)
rf_classifier.fit(X_train, Y_train)

Y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy:", accuracy)

