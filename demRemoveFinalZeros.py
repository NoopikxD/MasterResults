import pandas as pd


t1=pd.read_pickle(r'testdata\schoolmates10km.p')
t2=pd.read_pickle(r'testdata\workmates10km.p')
t3=pd.read_pickle(r'testdata\unworkmates.p')
rework=pd.concat([t1,t2,t3])

#rework = pd.read_csv('workplaces.txt', sep='\t',index_col=None)
#rework=rework.drop(columns='Unnamed: 0')
print(rework)
rework.to_pickle(r'testdata\peoplesIncorrect.p')
rework.to_csv(r'testdata\peoples_Incorrect10km.txt',sep='\t')
#rework.to_csv('workplaces1.txt',sep='\t',index=False)



#print(rework.shape[0])
#test = rework.iloc[:-2, :-3]
# print(test.shape[1])
#sumofall = test.sum(axis=1)
#sumsum = sumofall.sum()
#print(sumsum)
#rework=rework[(rework['longitude']!=0) & (rework['latitude']!=0)]
#print(rework.shape[0])
#test = rework.iloc[:-2, :-3]
#rework.to_pickle(r'output\database_cleantTEST.p')
#rework.to_excel(r'output\database_cleantTEST.xlsx')