import pandas as pd

#Checking the correctness of input before using it for FRED

def removeNonNumeric(series):
   return series.replace(to_replace='X', value=0)


def peopleStats(people_df):
    print("***People stats***")
    print("Total people: {}".format(people_df.shape[0]))
    print("Number of occupied households: {}".format(len(set(people_df['sp_hh_id'].tolist()))))
    print("Max occupied household number: {}".format(max(people_df['sp_hh_id'])))

    print("Number of filled workplaces: {}".format(len(set(people_df['work_id'].tolist()))))


    print("Max occupied workplace number: {}".format(max(pd.to_numeric(removeNonNumeric(people_df['work_id'])))))

def hhStats(hh_df):
    print("***Household stats***")
    print("Total households: {}".format(hh_df.shape[0]))

def workplacesStats (workplaces_df):
    print("***Workplaces stats***")
    print("Total workplaces: {}".format(workplaces_df.shape[0]))
    print("Total workplace capacity: {}".format(sum(workplaces_df['size'])))
def CalcAllWorkablePeoples(people_df):
    #temp = people_df[(people_df['age']>6) & (people_df['age']<65)]
    #print("Total workable people: {}".format(temp.shape[0]))
    #temp=people_df[(people_df['school_id']!='X')]
    #print(" learning peoples: {}".format(temp.shape[0]))
    #temp = people_df[((people_df['work_id'] !='X') | (people_df['school_id']!='X'))]
    #print("Working or learning people: {}".format(temp.shape[0]))
    temp=people_df[ (people_df['age'] >= 18) & (  ((people_df['sex'] == 'M') & (people_df['age'] <= 60)) | ((people_df['sex'] == 'F') & (people_df['age'] <= 55)))]
    print("Number of workable people: {}".format(temp.shape[0]))
    temp = people_df[((people_df['age'] >= 18) & (((people_df['sex'] == 'M') & (people_df['age'] <= 60)) | (
                (people_df['sex'] == 'F') & (people_df['age'] <= 55))) & (people_df['work_id']!='X'))]
    print("Number of working people: {}".format(temp.shape[0]))
    #temp = people_df[(people_df['age'] >= 18) & ( people_df['sex'] == 'F') & (people_df['age'] <= 55)]
    #print(temp.shape[0])

hh_df = pd.read_csv("input_2correct\\households.txt", sep="\t")
people_df = pd.read_csv("input_2correct\\peoples_IncorrectClosest.txt", sep="\t")
workplaces_df = pd.read_csv("input_2correct\\workplaces.txt", sep="\t")

workplacesStats(workplaces_df)
peopleStats(people_df)
hhStats(hh_df)
CalcAllWorkablePeoples(people_df)
