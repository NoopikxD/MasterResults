import pandas as pd
from shapely.geometry import Point
from geopy.distance import great_circle
import numpy as np
import time
from multiprocessing import Pool
from functools import partial
import random
#Distributing people among schools and workplaces

def isSchoolAge(row):
    return row['age']>=7 and row['age']<=17

def isWorkingAge(row):
    return row['age'] >= 18 and (row['sex']=='M' and row['age'] <= 60 or row['sex']=='F' and row['age'] <= 55)

def rowPointLocation(row):
    return Point(float(row['latitude']), float(row['longitude']))
def rowPointLocationForWorkspace(row):
    return Point(float(row['longitude']), float(row['latitude']))

def findDistToObj(row, point):
    #finds distances from the selected point to the object represented by DataFrame row
    obj_point = rowPointLocation(row)
    dist = great_circle((point.x, point.y), (obj_point.x, obj_point.y)).km
    return dist
def findDistToObjForWorkspace(row, point):
    #finds distances from the selected point to the object represented by DataFrame row
    obj_point = rowPointLocationForWorkspace(row)
    dist = great_circle((point.x, point.y), (obj_point.x, obj_point.y)).km
    return dist
def findDistTest(row, *args):
    point=args[0]

    obj_point = rowPointLocationForWorkspace(row)
    dist = great_circle((point.x, point.y), (obj_point.x, obj_point.y)).km
    return dist<5




def assignSchools(df_orig, hh_points_dic, schools_df_orig):

    close_schools_ids = []

    df = df_orig[df_orig.apply(isSchoolAge, axis=1)]

    students_num = {} #Counting students assigned to each school

    print("Schools, total: {}".format(schools_df_orig.shape[0]))
    print("Schoolchildren, total: {}".format(df.shape[0]))

    df_add = pd.DataFrame(list(np.zeros(schools_df_orig.shape[0])), columns=['distances'], index=schools_df_orig.index)
    #print(df_add)
    schools_df = schools_df_orig.join(df_add)
    print(schools_df)
    df=df[(df['age']>=7) & (df['age']<=17)]
    allSchoolsFilled = False
    size=df.shape[0]

    for idx, person_row in df.iterrows():
        #print(person_row)
            #print("Student {} ({})".format(idx, size))
        print("Student {}({})".format(idx,df.shape[0]))
        person_point = hh_points_dic[person_row['sp_hh_id']]
        series_distance = schools_df.apply(findDistToObj, args=(person_point, ), axis = 1)
        print(series_distance)
        df_add = pd.DataFrame(series_distance.tolist(), columns=['distances'], index=schools_df.index)
        schools_df.update(df_add)

        isStudentAssigned = False
        while not isStudentAssigned:
            #print("Schools: \n", schools_df)
            #print("School distances: \n", schools_df['distances'])
            min_index = schools_df['distances'].idxmin()

            #print(min_index)
            close_school = schools_df.loc[min_index]

            if not (close_school['sp_id'] in students_num.keys()): #checking capacity
                students_num[close_school['sp_id']] = 1
            else:
                students_num[close_school['sp_id']] = students_num[close_school['sp_id']] + 1

            #print('Success!')
            #print("Student distribution ", students_num)

            if students_num[close_school['sp_id']] == close_school['capacity']: #school filled to capacity
                #print("Before: {}".format(schools_df.shape[0]))
                schools_df = schools_df.drop(min_index) #(schools_df.index[min_index])
                #print("After: {}".format(schools_df.shape[0]))

                if schools_df.shape[0] == 0:
                    allSchoolsFilled = True

            isStudentAssigned = True

        close_schools_ids.append(close_school['sp_id'])
        if allSchoolsFilled:
            print("All schools filled to capacity!")
            break



    #print(pd.Series(close_schools_ids, name="school_id", index = df.index[:len(close_schools_ids)]))
    #print(close_schools_ids)
    df_orig.update(pd.DataFrame(close_schools_ids, columns=['school_id'], index = df.index[:len(close_schools_ids)]))

    return df_orig


def testworkplaces(orig_df, schools_df, hh,req_dist=0):
    #delta=0.02
    #reqdist=0.1
    delta=0.1
    reqdist=0
    if req_dist==0:
        reqdist=0.3
    else:
        reqdist=req_dist

    summin=0
    nummin=0
    minid=-1
    lasttime=time.time()
    #
    #add = np.zeros(orig_df.shape[0])
    #orig_df.update(pd.DataFrame(add, columns=['school_id']))
    #add = np.zeros(school_df.shape[0])
    #school_df.update(pd.DataFrame(add,columns=['tcap']))
    #schools_df['tcap']=schools_df['capacity']
    school_df=schools_df.copy()
    school_df['tcap']=school_df['capacity'].copy()
    #school_df['tcap']=school_df['size'].copy()
    df = orig_df[(orig_df['age'] >= 7) & (orig_df['age'] <= 17)].copy()

    #df=orig_df[ (orig_df['age'] >= 18) & (  ((orig_df['sex'] == 'M') & (orig_df['age'] <= 60)) | ((orig_df['sex'] == 'F') & (orig_df['age'] <= 55)))]
    df=df[1:].copy()


    fullschools=[]
    i = 0

    #print(df)
   # print(school_df)

    print("All schoolmates: {} ".format(df.shape[0]))

    for idx, row in df.iterrows():
        point = hh[row['sp_hh_id']]
        dist = []
        temp = pd.DataFrame()
        if(req_dist==0):
            while (temp.shape[0] == 0):
                temp = school_df[
                ((np.sqrt((point.x - school_df['latitude']) ** 2 + (point.y - school_df['longitude']) ** 2) < reqdist))]

                if(temp.shape[0]==0):
                    reqdist += delta
                if(temp.shape[0]>30):
                    reqdist -= delta / 4

                while(temp.shape[0]>80):
                    reqdist-=delta/2
                    newtemp = school_df[
                        ((np.sqrt((point.x - school_df['latitude']) ** 2 + (
                                    point.y - school_df['longitude']) ** 2) < reqdist))]
                    if(newtemp.shape[0]!=0):
                        temp=newtemp
                    else:
                        break
        else:
            temp= school_df[
                ((np.sqrt((point.x - school_df['latitude']) ** 2 + (point.y - school_df['longitude']) ** 2) < reqdist))]

        idschool = -1
        if(req_dist==0):
            min = 9999
            minid = -1

            iter = 0
            for idx1, schrow in temp.iterrows():
            # dist.append(findDistToObj(schrow, point))
                distbtw = findDistToObj(schrow, point)
                if (distbtw < min):
                    min = distbtw
                    minid = idx1
                    idschool = schrow['sp_id']

            summin+=min
            nummin+=1
        #idschool=school_df.loc[minid]['sp_id']
        else:
            if(temp.shape[0]!=0):
                n=random.randint(0,temp.shape[0]-1)
                j=0
                for idx1, schrow in temp.iterrows():
                    if(j==n):
                        distbtw=findDistToObj(schrow,point)
                        minid=idx1
                        idschool=schrow['sp_id']
                        summin+=distbtw
                        nummin+=1
                        break
                    j+=1
            else:
                minid=-1
                print("{}: school not in radius".format(idx))

        if(temp.shape[0]!=0):
            #df.set_value(idx,'school_id',idschool)
            if(minid!=-1):
                df.set_value(idx,'work_id',idschool)
                school_df.loc[minid,'tcap']-=1
                #print(school_df.shape[0])
                var = school_df.loc[minid,'tcap']
                #print(var)

                if(int(var)<=0):
                    school_df = school_df[(school_df['tcap']>0)]
                    if(school_df.shape[0]==0):
                        df.to_pickle(r'testdata\schoolmates.p')
                        df.to_csv('testdata\schoolmates.txt')
                        break
                    #print(school_df)
                    print("DROPPED {} ROW ".format(idschool))




        #print(temp)


        #minloc=np.argmin(dist)
        #range=np.sqrt((school_df.iloc[minloc]['latitude']-point.x)**2 + (school_df.iloc[minloc]['longitude']-point.y)**2)
        #range=np.sqrt((school_df.iloc[minloc]['latitude']-point.y)**2 + (school_df.iloc[minloc]['longitude']-point.x)**2)
        #if(range>0.1):
            #diffcounter+=1

        #print(str(dist[minloc]) +". " + str(diffcounter) + ". All: " + str(i))
        if(i%1000==0):
            newtime=time.time()
            print("i: {}/{}. Time passed: {}. AvgDistance:{} ".format(i,df.shape[0],(newtime-lasttime),(summin*1.0/(nummin+1))))
            lasttime=newtime

        #print(str(i) +" " + str(df.shape[0]))
        i+=1
    #print(orig_df)
        #print(dist)
        #print(distfree)
    df.to_pickle(r'testdata\schoolmates10km.p')
    df.to_csv('testdata\schoolmates10km.txt')
    #print(df)
    #print(school_df)








if __name__=='__main__':

    schools_df = pd.read_csv("schools.txt", sep="\t")
    workplaces_df = pd.read_csv("workplaces.txt", sep="\t")
    #workplaces_df=workplaces_df.rename(columns={'latitude':'longitude', 'longitude':'latitude'})

    hh_df = pd.read_csv("Households_SPbNew.txt", sep="\t")

    hh_points_dic = {}

    list_keys = hh_df['sp_id'].tolist()
    list_values = [Point([row['latitude'], row['longitude']]) for idx,row in hh_df.iterrows()]


    for key, value in zip(list_keys, list_values):
        hh_points_dic[key] = value


    people_df_orig = pd.read_csv("People_SPbNew.txt", sep="\t") #REMOVE NROWS , nrows=100000

    testworkplaces(people_df_orig,schools_df, hh_points_dic,req_dist=0.07)#Для школьников
    #testworkplaces(people_df_orig,workplaces_df,hh_points_dic,req_dist=0.1)#для рабочего класса
#people_df = assignSchools(people_df_orig, hh_points_dic, schools_df)
#people_df.to_excel("TESTASSIGNATION.txt")

#people_df = assignWorkplaces(people_df_orig, hh_points_dic, workplaces_df)

#people_df.to_csv("People_SPb_assigned.txt", index=False, sep="\t")
