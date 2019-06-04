import pandas as pd
import pickle
import numpy as np


#analyzing the input and generating the synthpop

def formAgeColumnsNames():
    list_names = []

    for gender in ['m', 'g']:
        for i in range(0,101):
            list_names.append(gender+str(i))

    return list_names

def calcSumDwellers(df, age_names):
    sum = 0
    for name in age_names:
        sum+= df[name].sum()

    return sum


def popStructure(hh_df):
    m_num = 0
    f_num = 0
    for i in range(0,100):
        mname = 'm'+str(i)
        fname = 'g'+str(i)

        mcol = hh_df[mname].astype('float64')
        fcol = hh_df[fname].astype('float64')

        print('Males, {}:  {}'.format(mname, mcol.sum()))
        print('Females, {}:  {}'.format(fname, fcol.sum()))
        m_num = m_num + mcol.sum()
        f_num = f_num + fcol.sum()
    print("Males, total: {}".format(m_num))
    print("Females, total: {}".format(f_num))
    print("Total: {}".format(m_num+f_num))

def calcHHSize(row):
    #print(row)
    size = 0
    for gender_age in formAgeColumnsNames():
        size+= int(row[gender_age])

    return size

def aggregateHouseholds(df):
    #Accumulates people by coordinates into households, leaving coords and quantities in df

    df = df[['latitude', 'longitude']+formAgeColumnsNames()]


    # for item in formAgeColumnsNames():
    #     df[item] = df[item].astype('float64')

    df = df.apply(pd.to_numeric, errors='coerce')


    df = df.groupby(['latitude', 'longitude']).agg('sum')


    hh_sizes = df.apply(calcHHSize, axis = 1)
    df_add = pd.DataFrame(hh_sizes.tolist(), columns=['hh_size'], index=df.index)
    df = df.join(df_add)

    hh_size_col = df['hh_size']
    df.drop(labels=['hh_size'], axis=1, inplace=True)
    df.insert(0, 'hh_size', hh_size_col)

    print(df[:5])


    df = df.reset_index()
    return df

def findGender(str):

    if str == 'm':
        return 'M'
    else:
        return 'F'

def extractGenderAge(colname):
    return findGender(colname[:1]), int(colname[1:])

# def generateSynthpop(raw_df, ages_names_list):
#     sp_id_cur = 1
#     people_col_list = ['sp_id', 'sp_hh_id', 'age', 'sex', 'race', 'relate', 'school_id', 'work_id']
#     hh_col_list = ['sp_id', 'stcotrbg', 'hh_race', 'hh_income', 'latitude',	'longitude']
#
#     people_df = pd.DataFrame(columns=people_col_list)
#     hh_df = pd.DataFrame(columns=hh_col_list) #Possible to decrease memory consumption by carving data from raw_df
#
#     hh_num = raw_df.shape[0]
#
#     for idx, row in raw_df.iterrows():
#         print("Household {} out of {}".format(idx, hh_num))
#
#         cur_hh = pd.Series({'sp_id': idx+1, 'stcotrbg': 194000, 'hh_race': 1, 'hh_income': 0, 'latitude': row['latitude'], 'longitude': row['longitude']})
#         hh_df = hh_df.append(cur_hh, ignore_index=True)
#         for col_name in ages_names_list:
#             if int(row[col_name])>0: #generating people
#                 for i in range(int(row[col_name])):
#                     print("Person No. {} out of {}".format(i, int(row[col_name])))
#
#                     gender, age = extractGenderAge(col_name)
#
#                     cur_indiv = pd.Series( {'sp_id': sp_id_cur, 'sp_hh_id': idx+1, 'age': age, 'sex': gender,
#                                           'race': '1', 'relate': 0, 'school_id': 'X', 'work_id': 'X'} )
#
#                     people_df = people_df.append(cur_indiv, ignore_index=True)
#                     sp_id_cur+=1
#
#
#     people_dtype_list = ['int64', 'int64', 'int64', 'category', 'int64', 'int64', 'object', 'object']
#
#     for col, type in zip(people_col_list, people_dtype_list):
#         people_df[col] = people_df[col].astype(type)
#
#     hh_dtype_list = ['int64', 'int64', 'int64', 'float64', 'float64']
#
#     for col, type in zip(hh_col_list, hh_dtype_list):
#         hh_df[col] = hh_df[col].astype(type)
#
#     print(people_df.shape[0])
#
#
#     people_df.to_csv('People_SPb.txt', index=False, sep='\t')
#     hh_df.to_csv('Households_SPb.txt', index=False, sep='\t')


def generateSynthpop_v2(raw_df):
    #Optimized generation function
    sp_id_cur = 1

    hh_col_list = ['sp_id', 'stcotrbg', 'hh_size', 'hh_race', 'hh_income', 'latitude',	'longitude']

    hh_num = raw_df.shape[0]
    hh_ids = list(range(1,hh_num+1))
    hh_stcotrbg_list = [190000]*hh_num
    hh_race_list = [1]*hh_num
    hh_income = [0]* hh_num

    hh_add_df = pd.DataFrame(np.column_stack([hh_ids, hh_stcotrbg_list, hh_race_list, hh_income]), columns=['sp_id', 'stcotrbg', 'hh_race', 'hh_income'])

    hh_size_dic = {}

    people_gender = []
    people_age = []
    people_hh_id = []
    #print(raw_df[:5])
    #print(hh_add_df[:5])

    hh_df = hh_add_df.join(raw_df[['hh_size', 'latitude','longitude']])

    #print("Age group size: {}".format(calcSumDwellers(raw_df, ['m100'])))  # formAgeColumnsNames()

    #print(hh_df[:5])

    for col_name in formAgeColumnsNames():
        #print(col_name)
        gender, age = extractGenderAge(col_name)

        num_total = int(raw_df[col_name].sum())

        people_gender.extend([gender]*num_total)
        people_age.extend([age]*num_total)

        #Assigning household ids, starting from 1
        hh_id = 1
        for num_cur in raw_df[col_name]:
            if num_cur>0:
                people_hh_id.extend([hh_id]*int(num_cur))
            hh_id+=1


    #Constructing dataframes from the acquired data

    people_num = len(people_hh_id)

    print("Total population: {}".format(people_num))

    race_list = [1]*people_num
    relate_list = [0]*people_num
    work_id_list = school_id_list = ['X']*people_num
    sp_id_list = list(range(1, people_num+1))

    people_col_list = ['sp_id', 'sp_hh_id', 'age', 'sex', 'race', 'relate', 'school_id', 'work_id']

    people_df = pd.DataFrame(np.column_stack([sp_id_list, people_hh_id, people_age, people_gender, race_list, relate_list, school_id_list, work_id_list]), columns = people_col_list)

    #print(people_df[:5])

    people_dtype_list = ['int64', 'int64', 'int64', 'category', 'int64', 'int64', 'object', 'object', 'object']

    for col, type in zip(people_col_list, people_dtype_list):
        people_df[col] = people_df[col].astype(type)

    hh_dtype_list = ['int64', 'int64', 'int64', 'int64', 'float64', 'float64']

    for col, type in zip(hh_col_list, hh_dtype_list):
        hh_df[col] = hh_df[col].astype(type)

    people_df = people_df.sort_values('sp_hh_id')

    people_df.to_csv('People_SPbNew.txt', index=False, sep='\t')
    hh_df.to_csv('Households_SPbNew.txt', index=False, sep='\t')
    people_df.to_excel(r'People_SpbNew.xlsx')
    hh_df.to_excel(r'People_SpbNew.xlsx')



if __name__ == '__main__':

    raw_df = pd.read_pickle(r'output\databaseNewCleant.p') #_cleant , chunksize = 1000

    raw_df = aggregateHouseholds(raw_df)

    generateSynthpop_v2(raw_df)



