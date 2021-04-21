import pandas as pd

data = pd.read_csv("./training_classificator.csv", encoding='utf-8').sample(frac=1).drop_duplicates()
#data = data[['v1', 'v2']].rename(columns={"v1": "label", "v2": "text"})

#data['label'] = '__label__' + data['label'].astype(str)
data.iloc[0:int(len(data) * 0.03)].to_csv('data2/train.csv', sep='\t', index=False, header=False)
data.iloc[int(len(data) * 0.03):int(len(data) * 0.035)].to_csv('data2/test.csv', sep='\t', index=False, header=False)
data.iloc[int(len(data) * 0.03):int(len(data) * 0.035)].to_csv('data2/dev.csv', sep='\t', index=False, header=False)