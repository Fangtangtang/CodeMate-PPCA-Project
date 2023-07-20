from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import jieba
import json

file_name=[
     "highQualityTrain",
     "lowQualityTrain",
     "highQualityTest",
     "lowQualityTest"
]

y_value=[1,0,1,0]

jieba.load_userdict('user-defined')
stopwords=()
with open('stopwords','r',encoding='utf-8') as f:
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
rf_model = RandomForestClassifier()


# 定义要搜索的参数空间
param_grid = {
    'vectorizer__max_features': [None,500,1000,1500,2000],
    'rf_model__n_estimators': [60,90,110],
    'rf_model__max_depth': [None,40,80]
}

# 构建机器学习工作流
# 多个数据处理和模型训练步骤串联在一起，形成一个整体的机器学习流程
# 每个步骤都是一个二元元组，包含一个名称和一个实例
pipeline=Pipeline([
    ('vectorizer',vectorizer),
    ('rf_model', rf_model)
])

# 创建GridSearchCV对象，指定pipeline和参数空间
grid_search = GridSearchCV(pipeline, param_grid=param_grid, scoring='accuracy', cv=3, refit=True)

# 在训练集上执行网格搜索
# 在训练集上划分“训练集”和“测试集”，反复验证，获得结果较好的参数
grid_search.fit(X_train, Y_train)

# 查看每种参数组合的准确率
results = grid_search.cv_results_
for mean_score, params in zip(results['mean_test_score'], results['params']):
    print("参数组合: ", params)
    print("准确率: ", mean_score)
    print()

# 使用最佳参数组合的模型在测试集上进行预测
y_pred = grid_search.predict(X_test)

# 计算并输出正确率
accuracy = accuracy_score(Y_test, y_pred)
print("测试集正确率:", accuracy)
