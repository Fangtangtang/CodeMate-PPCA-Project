from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import jieba
import json
import numpy
from sentence_transformers import SentenceTransformer
from sentence_transformers import InputExample
from torch.utils.data import Dataset, DataLoader
from sentence_transformers import losses
import torch

    
file_name=[
     "highQualityTrain",
     "lowQualityTrain",
     "highQualityTest",
     "lowQualityTest"
]

y_value=[1,0,1,0]

model_name = "uer/roberta-base-chinese-extractive-qa"
    
jieba.load_userdict('user-defined')
stopwords=()
with open('stopwords','r',encoding='utf-8') as f:
    stopwords={word.strip() for word in f}


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
            # X_train.append(list(jieba.lcut(tag+point+question+ans)) )
            X_train.append(tag+point+question+ans)
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
            X_test.append(tag+point+question+ans)
            Y_test.append(y_value[i])

print("gotten str!")

# 创建自定义数据集对象
length=len(X_train)
dataset=[]
for i in range (0,length):
    dataset.append(InputExample(texts=[X_train[i]], label=Y_train[i]))

# 创建数据加载器（给模型喂数据）
# dataset=list(zip(X_train, Y_train))
batch_size = 64
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# 导入SentenceTransformer模型
sentence_transformer_model = SentenceTransformer(model_name)

print("gotten model!")

train_loss = losses.BatchAllTripletLoss(model=sentence_transformer_model)
print(train_loss)

sentence_transformer_model.fit(
    train_objectives=[(data_loader, train_loss)], 
    epochs=10
    )

print('fine-tuned!')

chunk_size = 1000

cnt=0
result = [X_train[i:i+chunk_size] for i in range(0, len(X_train), chunk_size)]
for words in result:
    converted=sentence_transformer_model.encode(words, convert_to_tensor=True)
    converted=converted.cpu().numpy()
    if(cnt==0):
        word_train=converted
    else:
        word_train=numpy.concatenate((word_train,converted))
    cnt+=1
    print("gotten word vec {}!".format(cnt))
print("gotten word vec!")

word_test = sentence_transformer_model.encode(X_test, convert_to_tensor=True)
word_test=word_test.cpu().numpy()
print("gotten word vec!")


rf_classifier = RandomForestClassifier()
rf_classifier.fit(word_train, Y_train)

print("trained!")
Y_pred = rf_classifier.predict(word_test)

accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy:", accuracy)

