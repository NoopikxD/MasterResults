
import pandas as pd
import pickle
import matplotlib.pyplot as plt

#analyzing the input and generating the synthpop

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

def aggregateHouseholds(df):
    #Accumulates people by coordinates into households, leaving coords and quantities in df
    df = df.groupby(['latitude', 'longitude']).agg('sum')
    ages_list = list(df)
    df = df.reset_index()
    return df, ages_list

def findGender(str):

    if str == 'm':
        return 'M'
    else:
        return 'F'

def extractGenderAge(colname):
    return findGender(colname[:1]), int(colname[1:])

#def generatePeopleForHousehold(age):


def generateSynthpop(raw_df, ages_names_list):
    sp_id_cur = 1
    people_col_list = ['sp_id', 'sp_hh_id', 'age', 'sex', 'race', 'relate', 'school_id', 'work_id']
    hh_col_list = ['sp_id', 'stcotrbg', 'hh_race', 'hh_income', 'latitude',	'longitude']

    people_df = pd.DataFrame(columns=people_col_list)
    hh_df = pd.DataFrame(columns=hh_col_list) #Possible to decrease memory consumption by carving data from raw_df

    hh_num = raw_df.shape[0]

    for idx, row in raw_df.iterrows():
        print("Household {} out of {}".format(idx, hh_num))

        cur_hh = pd.Series({'sp_id': idx+1, 'stcotrbg': 194000, 'hh_race': 1, 'hh_income': 0, 'latitude': row['latitude'], 'longitude': row['longitude']})
        hh_df = hh_df.append(cur_hh, ignore_index=True)
        for col_name in ages_names_list:

            if int(row[col_name])>0: #generating people
                for i in range(int(row[col_name])):

                    gender, age = extractGenderAge(col_name)

                    cur_indiv = pd.Series( {'sp_id': sp_id_cur, 'sp_hh_id': idx+1, 'age': age, 'sex': gender,
                                          'race': '1', 'relate': 0, 'school_id': 'X', 'work_id': 'X'} )

                    people_df = people_df.append(cur_indiv, ignore_index=True)
                    sp_id_cur+=1


    people_dtype_list = ['int64', 'int64', 'int64', 'category', 'int64', 'int64', 'object', 'object']

    for col, type in zip(people_col_list, people_dtype_list):
        people_df[col] = people_df[col].astype(type)

    hh_dtype_list = ['int64', 'int64', 'int64', 'float64', 'float64']

    for col, type in zip(hh_col_list, hh_dtype_list):
        hh_df[col] = hh_df[col].astype(type)


    people_df.to_csv('People_SPb.txt', index=False, sep='\t')
    hh_df.to_csv('Households_SPb.txt', index=False, sep='\t')

    ##HH_INDEX + 1 !!!


if __name__ == '__main__':

    raw_df = pd.read_pickle(r'output\database.p') #_cleant
    raw_df, ages_list = aggregateHouseholds(raw_df)

    generateSynthpop(raw_df, ages_list)



