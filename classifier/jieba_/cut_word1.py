import json
import jieba
import re
file_name=[
     "highQualityTest",
    #  "highQualityTrain",
    #  "lowQualityTest",
    #  "lowQualityTrain"
]

def Process(str,name):
    # str=re.sub(r'[^\w]','',str)
    Str=[word for word in jieba.lcut(str) if word not in stopwords]
    string=""
    for ele in Str:
         string+=(ele+' ')
    with open('jieba_sample.txt','a',encoding='utf-8') as file:
            file.write(string+'\n')
        

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
            Process(tag,name)
            Process(point,name)
            Process(question,name)
            Process(ans,name)
            

