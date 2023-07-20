import json
import jieba
import re
import gensim

file_name=[
     "highQualityTest",
     "highQualityTrain",
     "lowQualityTest",
     "lowQualityTrain"
]

pat= r'```(.|\n)*?```'   
replacement="codeBlock"

sentence=[]

def Process(str):
    replaced_string = re.sub(pattern=pat,repl= replacement, string=str)
    Str=[word for word in jieba.lcut(replaced_string) if word not in stopwords]
    for ele in Str:
        sentence.append(ele)
        

jieba.load_userdict('workspace/word2vec/user-defined')
stopwords=()
with open('workspace/word2vec/stopwords','r',encoding='utf-8') as f:
    stopwords={word.strip() for word in f}

for name in file_name:
    with open ('data/{}.jsonl'.format(name),'r',encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            ans=data["Answer"]
            question=data["Question"]
            tag=data["Tag"]
            try:
                point=data["Knowledge_Point"]
            except BaseException:
                point=data["Konwledge_Point"]
            Process(tag+point+question+ans)
    print(name)
            
            
# 根据需求配置 Word2Vec 参数并进行训练
model=gensim.models.Word2Vec(sentence,
                             vector_size=128,   # 词向量维度
                             window=25,          # 相关前后文的窗口大小
                             min_count=10,      # 词频
                             workers=4,         # 线程数
                             hs=1,              # 1: 采用hierarchical softmax训练模型; 0: 使用负采样
                             negative=0,        # 0: 使用负采样，设置多个负采样(通常在5-20之间)
                             epochs=20           # 迭代次数
                             )

model.save('new.model')