from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import json

file_name=[
     "highQualityTrain",
     "lowQualityTrain",
     "highQualityTest",
     "lowQualityTest"
]

y_value=[1,0,1,0]

jieba.load_userdict('workspace/word2vec/user-defined')
stopwords=()
with open('workspace/word2vec/stopwords','r',encoding='utf-8') as f:
    stopwords={word.strip() for word in f}


# 自定义划分依据
# 按划分返回一个list
def custom_tokenizer(text):
    return text.split("。") 

def get_sentence_token(sentence):
    # 将句子用jieba分词
    word_list=[word for word in jieba.lcut(sentence) if word not in stopwords]
    # 将词以特殊的划分依据链接为string，用于作为TfidfVectorizer的样本
    str=""
    for word in word_list:
        str=str+word+"。"
    return str


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
            X_train.append(get_sentence_token(tag+point+question+ans))
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
            X_test.append(get_sentence_token(tag+point+question+ans))
            Y_test.append(y_value[i])


# 指定划分工具
vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer)
# 先拟合全部数据，再转化
# vectorizer.fit(X_train+X_test)
X = vectorizer.fit_transform(X_train)

rf_classifier = RandomForestClassifier(n_estimators=70)
rf_classifier.fit(X, Y_train)

# 仅转化
X_=vectorizer.transform(X_test)
Y_pred = rf_classifier.predict(X_)

accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy:", accuracy)

