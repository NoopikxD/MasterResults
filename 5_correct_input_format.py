import pandas as pd



#Deals with old-style data input removing index from people.txt and converting hh_income to float in
#households.txt

#schools_df = pd.read_csv("schools.txt", sep="\t")


hh_df = pd.read_csv("input_2correct\\households_SPbNew.txt", sep="\t")
people_df = pd.read_csv("input_2correct\\peoples_incorrect10km.txt", sep="\t",index_col=0)
workplaces_df = pd.read_csv("input_2correct\\workplaces_incorrect.txt", sep="\t")
print(people_df.shape[0])
people_df=people_df[people_df['sp_hh_id']!=1]
print(people_df.shape[0])
people_col_list = ['sp_id','sp_hh_id', 'age', 'race', 'relate', 'school_id', 'work_id']
hh_col_list = ['hh_income']
work_col_list = ['sp_id', 'size']
print(people_df)
#for col in people_col_list:
     #people_df[col] = people_df[col].astype('str')
     #people_df[col] = people_df[col].str.replace('\\.0', '')

for col in hh_col_list:
    hh_df[col] = hh_df[col].astype('str')
    hh_df[col] = hh_df[col].str.replace('\\.0', '')
#for col in work_col_list:
     #workplaces_df[col] = workplaces_df[col].astype('str')
     #workplaces_df[col] = workplaces_df[col].str.replace('\\.0', '')

hh_df = hh_df.round({'latitude': 6, 'longitude': 6})
hh_df = hh_df.drop(['hh_size'], axis=1)


people_df.to_csv("input_2correct\\people.txt", index=False, sep="\t") #removing index
hh_df.to_csv("input_2correct\\households.txt", index=False, sep="\t") #removing index
#workplaces_df.to_csv("input_2correct\\workplaces.txt", index=False, sep="\t") #removing index