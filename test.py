import pandas as pd
import math

people_df = pd.read_csv("input_2correct\\peoples_incorrect10km.txt", sep="\t",index_col=0)
temp=people_df[people_df['age']<9]
temp10=people_df[(people_df['age']>9) &(people_df['age']<20) ]
temp20=people_df[(people_df['age']>19) & (people_df['age']<30) ]
temp30=people_df[(people_df['age']>29) & (people_df['age']<40) ]
temp40=people_df[(people_df['age']>39) & (people_df['age']<50) ]
temp50=people_df[(people_df['age']>49) & (people_df['age']<60) ]
temp60=people_df[(people_df['age']>59) & (people_df['age']<70) ]
temp70=people_df[(people_df['age']>69) & (people_df['age']<80) ]
temp80=people_df[(people_df['age']>79) & (people_df['age']<90) ]
temp90=people_df[(people_df['age']>89) & (people_df['age']<100) ]
temp100=people_df[people_df['age']>99 ]
print(temp.shape[0]*100/people_df.shape[0])
print(temp10.shape[0]*100/people_df.shape[0])
print(temp20.shape[0]*100/people_df.shape[0])
print(temp30.shape[0]*100/people_df.shape[0])
print(temp40.shape[0]*100/people_df.shape[0])
print(temp50.shape[0]*100/people_df.shape[0])
print(temp60.shape[0]*100/people_df.shape[0])
print(temp70.shape[0]*100/people_df.shape[0])
print(temp80.shape[0]*100/people_df.shape[0])
print(temp90.shape[0]*100/people_df.shape[0])
print(temp100.shape[0]*100/people_df.shape[0])
t=people_df[(people_df['work_id']!='X')]
print(t.shape[0])