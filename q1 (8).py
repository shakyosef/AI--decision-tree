from copy import copy
import random
import numpy as np
import math
import pandas as pd
from datetime import  date, datetime, timedelta
from pptree import *
from scipy.stats import chi2

class Tree:
#Data structure - the decision tree.
#If it is a root - there are boys - branches -
#If he asked - there is no industry name
#If it is a branch - there is a branch
#If he rose - no boys have a definitive answer
        def __init__(self, examples,parent_examples, attributes_arr, father,entropy,name_attributes,branches_name,branches,name_example):
            self.examples = examples
            self.father = father
            self.branches_value = []
            self.boys=dict()
            self.branches_name=branches_name
            self.entropy = entropy
            self.name_attributes = name_attributes
            self.attributes_arr = attributes_arr
            self.branches=branches
            self.anser=' '
            self.name_example=name_example
        def get_anser(self):
            return self.anser
        def get_if_have_anser(self):
            if  self.anser!=' ':
                return True
            else:
                return False
        def get_all_boys(self):
            return  self.boys
        def add_boy(self,boy,index):
            self.boys[index]=boy
        def get_boy(self,index):
            return self.boys[index]
        def get_branches(self):
           return self.branches
        def get_name_example(self):
            return self.name_example
        def get_examples(self):
            return self.examples
        def get_father(self):
            return self.father
        def set_branches_value(self,v):
            self.branches_value.remove(v)
        def set_anser(self,a):
            if a=='True':
               self.anser='busy'
            else:
                if  a=='False':
                  self.anser = 'not busy'
        def get_attributes_arr(self):
            return self.attributes_arr
        def add_branches_value(self,v):
             self.branches_value.append(v)
        def get_branches_value(self):
            return  self.branches_value
        def get_branches_name(self):
            return self.branches_name
        def get_name_attributes(self):
            return self.name_attributes
        def set_name_attributes(self):
            self.name_attributes=' '
            self.branches_value=[]
      #Print function
        def  __str__(self):
            if len(self.branches_value)==0:
                t = self.branches + " ----> " + self.anser
            else:
                if self.branches_value is str:
                    t= self.branches + " ----> " + self.anser
                else:
                    if self.branches=='':
                        t=self.name_attributes
                    else:
                       t = self.branches + " ----> " + self.name_attributes
            return t

#Range division functions - for data obtained in Excel
def date_groups_func(series):
    date=datetime.strptime(series,  '%d/%m/%Y')
    month = date.month
    if month < 4:
        return  1
    elif 4<= month < 7:
        return 2
    elif 7 <= month <10:
        return 3
    elif 10 <= month < 13:
        return 4
def Temperature_groups_func(series):
   # print(float(series))
    if int(series) < 0:
        return  1
    elif 0<=  int(series) < 15:
        return 2
    elif 15 <=  int(series):
        return 3
def Humidity_groups_func(series):
    if int(series) < 25:
        return  1
    elif 25<=  int(series) < 50:
        return 2
    elif 50 <=  int(series)<75:
        return 3
    elif 75 <= int(series) :
        return 4

def Wind_speed_groups_func(series):
        if int(series) < 2:
            return 1
        elif 2 <= int(series) < 4.4:
            return 2
        elif 4.4 <= int(series):
            return 3

def Visibility_groups_func(series):
    if int(series) < 500:
        return 1
    elif 500 <= int(series) < 1000:
        return 2
    elif 1000 <= int(series)<1500:
        return 3
    elif 1500 <= int(series):
        return 4

def Dew_point_temperature_groups_func(series):
    if int(series) < -10:
        return 1
    elif -10 <= int(series) < 10:
        return 2
    elif 10 <= int(series):
        return 3


def Solar_Radiation_groups_func(series):
    if int(series) < 1.2:
        return 1
    elif 1.2 <= int(series) < 2.4:
        return 2
    elif 2.4 <= int(series):
        return 3

def Rainfall_groups_func(series):
    if int(series) < 4:
        return 1
    elif 4 <= int(series) <10:
        return 2
    elif 10 <= int(series)< 20:
        return 3
    elif 20 <= int(series):
        return 4


def Snowfall_groups_func(series):
    if int(series) < 2.6:
        return 1
    elif 2.6 <= int(series) <5.2:
        return 2
    elif 5.2 <= int(series):
        return 3


def Seasons_groups_func(series):
    if series== 'Winter':
        return 1
    if series == 'Spring':
        return 2
    if series == 'Summer':
        return 3
    if series == 'Autumn':
        return 4
def Holiday_groups_func(series):
    if series== 'No Holiday':
        return 1
    if series == 'Holiday':
        return 2
def Functioning_Day_groups_func(series):
    if series== 'No':
        return 1
    if series == 'Yes':
        return 2
def Rented_Bike_Count_groups_func(series):

        if int( series )> 650:
           return 'True'
        else:
          return  'False'
def Hour_groups_func(series):
    if int(series) < 6:
        return 1
    elif 6 <= int(series) < 12:
        return 2
    elif 12 <= int(series)<18:
        return 3
    elif 18 <= int(series):
        return 4
#Reading data from an Excel file - division into ranges and adding range columns to a matrix
def part_all_data():
    df = pd.read_csv('SeoulBikeData.csv', encoding='unicode_escape')
    my_data =pd.DataFrame(data=df)
    my_data['busy'] = my_data['Rented Bike Count'].apply(Rented_Bike_Count_groups_func)
    my_data['Date_num'] = my_data.Date.apply(date_groups_func)
    my_data['Hour_num'] = my_data.Hour.apply(Hour_groups_func)
    my_data['Temperature_num'] = my_data['Temperature(°C)'].apply(Temperature_groups_func)
    my_data['Humidity_num'] = my_data['Humidity(%)'].apply(Humidity_groups_func)
    my_data['Wind_speed_num'] = my_data['Wind speed (m/s)'].apply(Wind_speed_groups_func)
    my_data['Visibility_num'] = my_data['Visibility (10m)'].apply(Visibility_groups_func)
    my_data['Dew_point_temperature_num'] = my_data['Dew point temperature(°C)'].apply(
        Dew_point_temperature_groups_func)
    my_data['Solar_Radiation_num'] = my_data['Solar Radiation (MJ/m2)'].apply(Solar_Radiation_groups_func)
    my_data['Rainfall_num'] = my_data['Rainfall(mm)'].apply(Rainfall_groups_func)
    my_data['Snowfall_num'] =my_data['Snowfall (cm)'].apply(Snowfall_groups_func)
    my_data['Seasons_num'] = my_data['Seasons'].apply(Seasons_groups_func)
    my_data['Holiday_num'] = my_data['Holiday'].apply(Holiday_groups_func)
    my_data['Functioning_Day_num'] =my_data['Functioning Day'].apply(Functioning_Day_groups_func)
    return my_data

#Dividing the data table by the ranges of a particular attribute. Returns a vector of data tables of a
# particular attribute, where each member of the vector is of a different range of the attribute
def get_divisions(examples,index):
    divisions=[]
    if index==0:
        i = 1
        while i < 5:
            p = examples[examples['Date_num'] == i]
            if len(p)!=0:
              divisions.append(p)
            i = i + 1
        return   divisions

    if index == 1:
        i = 1
        while i < 5:
            p = examples[examples['Hour_num'] == i]
            if len(p) != 0:
              divisions.append(p)
            i = i + 1
        return divisions

    if index == 2:
        i = 1
        while i < 4:
            p = examples[examples['Temperature_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions
    if index== 3:
        i = 1
        while i < 5:
            p = examples[examples['Humidity_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions
    if index==4:
        i = 1
        while i < 4:
            p = examples[examples['Wind_speed_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions

    if index == 5:
        i = 1
        while i < 5:
            p = examples[examples['Visibility_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions

    if index == 6:
        i = 1
        while i < 4:
            p =  examples[ examples['Dew_point_temperature_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions

    if  index ==7:
        i = 1
        while i < 4:
            p =  examples[ examples['Solar_Radiation_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions

    if index == 8:
        i = 1
        while i < 5:
            p = examples[examples['Rainfall_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions

    if index == 9:
        i = 1
        while i < 4:
            p = examples[examples['Snowfall_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions

    if index == 10:
        i = 1
        while i < 5:
            p = examples[examples['Seasons_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions
    if index == 11:
        i = 1
        while i < 3:
            p = examples[ examples['Holiday_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions
    if index == 12:
        i = 1
        while i < 3:
            p =examples[examples['Functioning_Day_num'] == i]
            if len(p) != 0:
                divisions.append(p)
            i = i + 1
        return divisions
#Gets the total number of shows and the amount in which the show is busy or not busy and returns the entropy for it
def entropy_func(c, n):

    return -(c*1.0/n)*math.log(c*1.0/n, 2)
#Gets the amount of times it is loaded and the amount of times it is not loaded and
# returns the entropy of the industry. Given both cases
def entropy_cal(c1, c2):
    if c1== 0 or c2 == 0:  # when there is only one class in the group, entropy is 0
        return 0
    return entropy_func(c1, c1+c2) + entropy_func(c2, c1+c2)
#Gets a vector of data, where each vector member is a data table of another domain in the same attribute.
# Returns a total entropy of the entire trait,
# including consideration of the probability of each domain
def entropy_of_all_division(division):
    s = 0
    n = 0
    for i in range(len(division)):
        examples = division[i]
        n=n+len(examples)
    for c in range(len(division) ):
        examples=division[c]
        n_c = len(examples)
        positive= examples[ examples['busy']=='True'].shape[0]
        negative=examples[ examples['busy']=='False'].shape[0]
        e = n_c*1.0/n * entropy_cal(positive, negative)
        s += e
    return s, n
#Gets a data table of only one domain of a particular attribute.
# And calculates the entropy. Returns entropy to a single branch.
def entropy_of_one_division(division):
    s = 0
    positive= division[ division['busy']=='True'].shape[0]
    negative=division[ division['busy']=='False'].shape[0]
    e =  entropy_cal(positive, negative)
    s += e
    return s
#Gets the entire data table and location of a particular attribute.
#Uses a function to get the vector divided into domains and returns the total entropy.
def get_entropy(examples,index):
    division=get_divisions(examples, index)
    s,n=entropy_of_all_division(division)
    return s
#Gets the vector features, the data table and the entropy before.
#If the entropy before is not determined returns the attribute - the split - for it the smallest entropy.
#Otherwise returns the attribute — the split — for which the subtraction of the previous lesser entropy is the greatest new.
def best_split(attributes_arr,examples,a_befor):
    max=None
    indexMax=None
    if a_befor==None:
        for i in range(len(attributes_arr)):
          if attributes_arr[i] == 0:
            entropy=get_entropy(examples,i)
            if max==None:
               max=entropy
               indexMax = i
            else:
               if  entropy<max:
                   max = entropy
                   indexMax = i
    else:
      for i in range(len(attributes_arr)):
            if attributes_arr[i] == 0:
                entropy = get_entropy(examples, i)
                if indexMax == None or max == None:
                    indexMax = i
                    max = a_befor - entropy
                else:
                    if a_befor -  entropy>max:
                        indexMax = i
                        max = a_befor -  entropy
    return indexMax, max

#Gets a data table and returns the answer that is the majority.
def PLURALITY_VALUE(examples):
    max=None
    if max==None:
            max =examples['busy'].value_counts().idxmax()
    return  str(max)
#Gets a position of an attribute - and for it returns the name of the question,
# the names of all the branches, and the name of the attribute.
def name_tree(index):
    name_q=''
    branches=[]
    name_exmple=''
    if index == 0:
        name_q = 'What is the month?'
        branches = ['month: 1, 2, 3', 'month: 4, 5, 6', 'month: 7, 8, 9', 'month: 10, 11,12']
        name_exmple='Date_num'
    if index == 1:
        name_q = 'what''s the time?'
        branches = ['Hour: 00:00-5:00', 'Hour: 6:00-11:00', 'Hour: 12:00-17:00', 'Hour: 18:00-23:00']
        name_exmple = 'Hour_num'
    if index == 2:
        name_q = 'What is the Temperature(°C)?'
        branches = ['temp<0', '0<temp<15', '15<temp']
        name_exmple ='Temperature_num'
    if index == 3:
        name_q = 'what is the Humidity(%)?'
        branches = ['Humidity<25', '25< Humidity<50', '50< Humidity<75','75< Humidity']
        name_exmple ='Humidity_num'
    if index == 4:
        name_q = 'what is the Wind speed (m/s)?'
        branches = ['Wind speed<2','2<Wind speed<4.4','4.4<Wind speed']
        name_exmple ='Wind_speed_num'
    if index == 5:
        name_q = 'what is the Visibility (10m)?'
        branches = ['Visibility<500','500< Visibility<1000','1000<Visibility<1500','1500< Visibility']
        name_exmple ='Visibility_num'
    if index == 6:
        name_q = 'what is the Dew point temperature(°C)?'
        branches = ['Dew point temperature< -10', '-10<Dew point temperature<10','10<Dew point temperature']
        name_exmple ='Dew_point_temperature_num'
    if index == 7:
        name_q = 'what is the Solar Radiation (MJ/m2)?'
        branches = ['Solar Radiation< 1.2','1.2<Solar Radiation<2.4','2.4<Solar Radiation']
        name_exmple ='Solar_Radiation_num'
    if index == 8:
        name_q = 'what is the Rainfall(mm)?'
        branches = ['Rainfall<4','4<Rainfall<10','10< Rainfall<20','20<Rainfall']
        name_exmple ='Rainfall_num'
    if index == 9:
        name_q = 'what is the Snowfall (cm)?'
        branches = ['Snowfall< 2.6','2.6<Snowfall<5.2','5.2<Snowfall']
        name_exmple ='Snowfall_num'
    if index == 10:
        name_q = 'what is the Seasons?'
        branches = ['Seasons: Winter', 'Seasons: Spring', 'Seasons: Summer', 'Seasons:Autumn']
        name_exmple ='Seasons_num'
    if index == 11:
        name_q = ' is  Holiday?'
        branches = ['No Holiday', 'Holiday']
        name_exmple ='Holiday_num'
    if index == 12:
        name_q = ' is Functioning Day?'
        branches = ['No Functioning Day', 'Functioning Day']
        name_exmple ='Functioning_Day_num'
    return name_q, branches, name_exmple
#Gets a comprehensive data table of a particular attribute- Dad-.
# And receives a vector in which each limb is a domain of a particular trait
def cut_TREE( examples,examples_fader):
    # If there are examples of industries. That is, we are in a split and not a husband. Calculate the critical value by alpha == 0.05
    # And degrees of freedom that are- amount of cluttered data and more amount of unloaded data less 1 of the father- of the overall table
    if len(examples)!=0:
           true_fader= examples_fader[ examples_fader['busy']=='True'].shape[0]
           false_fader = examples_fader[examples_fader['busy'] == 'False'].shape[0]
           ratio_true_fader=(true_fader/(true_fader+ false_fader))
           ratio_false_fader = ( false_fader / (true_fader + false_fader))
           free = true_fader + false_fader -1
           crit = chi2.ppf(q=0.05, df=free)
    sum_p_boys=None
    for i in  examples:
      flog=True
      examples_boy= i
      true_boy = examples_boy[examples_boy['busy'] == 'True'].shape[0]
      false_boy = examples_boy[examples_boy['busy'] == 'False'].shape[0]
      if  true_boy==0 and false_boy==0:
             flog=False
      if flog==True:
          # Calculate the amount of items I would expect to receive from the child if he were to split up like his father
       p_true_boy = (ratio_true_fader * (true_boy + false_boy))
       p_false_boy = (ratio_false_fader * (true_boy + false_boy))
       if  sum_p_boys==None:
          if p_true_boy!=0 and p_false_boy!=0:
               sum_p_boys=(((pow((true_boy- p_true_boy),2))/p_true_boy) +((pow((false_boy-p_false_boy),2))/p_false_boy))
          elif  p_true_boy!=0 and  p_false_boy==0:
              sum_p_boys = ((pow((true_boy- p_true_boy),2))/p_true_boy)
          elif  p_true_boy==0 and  p_false_boy!=0:
              sum_p_boys =  ((pow((false_boy - p_false_boy), 2)) / p_false_boy)
       else:
          if p_true_boy != 0 and p_false_boy != 0:
                sum_p_boys= sum_p_boys+(((pow((true_boy- p_true_boy),2))/p_true_boy) +((pow((false_boy-p_false_boy),2))/p_false_boy))
          elif  p_true_boy!=0 and  p_false_boy==0:
              sum_p_boys =sum_p_boys+ ((pow((true_boy- p_true_boy),2))/p_true_boy)
          elif  p_true_boy==0 and  p_false_boy!=0:
              sum_p_boys = sum_p_boys + ((pow((false_boy - p_false_boy), 2)) / p_false_boy)
    if sum_p_boys==None:
        return False
    # With the statistical value less than the critical value we will not reject the null hypothesis.
    # That is, all the sons are divided like their father.
    # That is, the question is meaningless. Therefore we will return truth. Otherwise we will return a lie.
    if  sum_p_boys < crit:
         return True
    else:
        return  False
#Get a tree and cut it if necessary
def to_cut_tree(t):
  if t is not str :
      #Takes the list of sons of the root-branches
    d=t.get_branches_value()
    mona=0
    boys_examples=[]
    for i in d:
        #For each branch checks if it has not risen -
        # then sends back to function with this branch - i.e. with the sub-tree
        if i.get_if_have_anser()==False:
            to_cut_tree(i)
        else:
            #If he went up - adds his data table to the list
            exc=i.get_examples()
            boys_examples.append(exc)
            mona=mona+1
    # If like the leaves is equal to the amount of the boys - the branches then I have reached the end of the tree
    if mona==len(d):
        parent_examples=t.get_examples()
        if_cut = cut_TREE(boys_examples, parent_examples)
        #If the function returns true - cut the tree.
        #I change to Dad - the industry from which the split came -
        # the answer to most of Dads.# And sends the whole function with the new tree after I downloaded the sub-tree i.e. with the father.
        if if_cut==True:
          f=t.get_father()
          if f!=None:
           examples=t.get_examples()
           anser= PLURALITY_VALUE( examples)
           t.set_anser(anser)
           t.set_name_attributes()
           to_cut_tree(f)



def DECISION_TREE_LEARNING(examples, parent_examples,attributes_arr, father,entropy,branches):
    if len(examples)== 0:
        # If my examples are blank - that is, no data
        return PLURALITY_VALUE(parent_examples)
    else:
        same=True
        anser=None
        k = examples['busy'].value_counts().to_numpy()
        #If all my examples give the same results (result - busy or not busy)
        if len(k) > 1:
                same=False
        else:
              if len(k)==1:
                  anser =examples[ 'busy'].value_counts().idxmax()
        if same==True and anser!=None:
             return str(anser)
        else:
            mona=0
            for i in range(len(attributes_arr)):
                if attributes_arr[i]==0:
                    mona=mona+1
            #If there are no more features - that means I can not ask any more questions
            if mona==0:
                return PLURALITY_VALUE(examples)
            else:
                #If my examples are not empty, and my examples are not identical in the result, and I also have more features, there is more to ask
                index_a,entropy=best_split(attributes_arr,examples,entropy)
                attributes_arr[index_a]=1
                name_attributes ,branches_name,name_example=name_tree(index_a)
                t=Tree(examples, parent_examples, attributes_arr, father, entropy,name_attributes,branches_name,branches,name_example)
                attributes_arr = copy(t.get_attributes_arr())
                for i in range(len(branches_name)):
                    exs=examples[examples[name_example]== i +1]
                    branches=branches_name[i]
                    entropy=entropy_of_one_division(exs)
                    subtree=DECISION_TREE_LEARNING(exs, examples,attributes_arr,t,entropy,branches)
                    if type(subtree) is str:
                        #If an absolute answer comes out - that is, busy or not busy.
                       #I create a tree that has no sons. Just the name of the branch and the
                        # final answer and add this branch to the sons of the father.
                        b = Tree(exs, examples, attributes_arr,t, entropy, '',
                                [], branches, name_example)
                        b.set_anser(subtree)
                        t.add_branches_value(b)
                        t.add_boy(subtree, i + 1)
                    else:
                        #Otherwise - if a sub-tree is returned I add the tree
                        # that was returned to the father's sons.
                        t.add_branches_value(subtree)
                        t.add_boy(subtree, i + 1)
                return t




def chake_tree(chake_data,t):
#Receives a table of data for testing
  x=chake_data.shape[0]
  mis=0
# For each row in the table checks whether its result is the same as the result in the decision tree
  for i in range(x):
    row = chake_data.iloc[i, :]
    if type(t) is not str:
     clum_name= t.get_name_example()
     # Gets the domain where the test data is for a feature - question - of the tree root
     clm= row[clum_name]
     next=t.get_boy(clm)
     #As long as the branch - the son - of a tree root - a feature - of some kind is not finite -
     # busy or not busy performs the same process explained above
     while type(next) is not str :
         clum_name = next.get_name_example()
         clm = row[clum_name]
         next = next.get_boy(clm)
     if next!=row['busy']:
         mis=mis+1
# Returns the mean error of the test data table
  return (mis/x)

def part_to_k(x,my_data):
    indices = my_data.index.tolist()
    test_indices = random.sample(population=indices, k=x)
    traning_data= my_data.loc[test_indices]
    leran_data = my_data.drop(test_indices)
    return leran_data, traning_data
#Gets an integer, divides the data into k parts and trains on K-1 and checks on k
def tree_error(k):
    attributes_arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    all_miss=0
    #Divide all data into attributes and domains by attributes
    my_data = part_all_data()
    #Calculate the number of parts to be divided by the data table
    x=len(my_data )/k
    mona=0
    while mona<k:
        #For the first time k-1 divides parts for testing and k for training
        if mona==0:
          leran_data,chake_data =part_to_k(int(x), my_data)
        else:
            #Make sure you do not re-select the same data for testing and training.
            # And therefore divides the remaining part each time!
             sam_leran=chake_data
             leran_data, chake_data = part_to_k(int(x), my_data)
             e = [ sam_leran,  leran_data ]
             leran_data = pd.concat(e)
        branches = ''
        # Creating a decision tree
        t = DECISION_TREE_LEARNING( leran_data,  leran_data, attributes_arr, None, None, branches)
        # Checking the decision tree and calculating the errors
        all_miss= all_miss+chake_tree(chake_data, t)
        my_data=leran_data
        mona=mona+1
        # The percentage of errors calculated by a weighted average
    print('Error rate:',((all_miss/k)*100),'%')

#Distributes only the data obtained from the array! To domains by attributes
def date_groups_func2(series):
    date=datetime.strptime(series,  '%d/%m/%Y')
    month = date.month
    if month < 4:
        return  1
    elif 4<= month < 7:
        return 2
    elif 7 <= month <10:
        return 3
    elif 10 <= month < 13:
        return 4
def Temperature_groups_func2(series):
    if float(series) < 0:
        return  1
    elif 0<=  float(series) < 15:
        return 2
    elif 15 <=  float(series):
        return 3
def Humidity_groups_func2(series):
    if float(series) < 25:
        return  1
    elif 25<=  float(series) < 50:
        return 2
    elif 50 <= float(series)<75:
        return 3
    elif 75 <= float(series) :
        return 4

def Wind_speed_groups_func2(series):
        if float(series) < 2:
            return 1
        elif 2 <= float(series) < 4.4:
            return 2
        elif 4.4 <= float(series):
            return 3

def Visibility_groups_func2(series):
    if float(series) < 500:
        return 1
    elif 500 <= float(series) < 1000:
        return 2
    elif 1000 <= float(series)<1500:
        return 3
    elif 1500 <= float(series):
        return 4

def Dew_point_temperature_groups_func2(series):
    if float(series) < -10:
        return 1
    elif -10 <= float(series) < 10:
        return 2
    elif 10 <= float(series):
        return 3


def Solar_Radiation_groups_func2(series):
    if float(series) < 1.2:
        return 1
    elif 1.2 <= float(series) < 2.4:
        return 2
    elif 2.4 <=float(series):
        return 3

def Rainfall_groups_func2(series):
    if float(series) < 4:
        return 1
    elif 4 <= float(series) <10:
        return 2
    elif 10 <= float(series)< 20:
        return 3
    elif 20 <= float(series):
        return 4


def Snowfall_groups_func2(series):
    if float(series) < 2.6:
        return 1
    elif 2.6 <= float(series) <5.2:
        return 2
    elif 5.2 <= float(series):
        return 3


def Seasons_groups_func2(series):
    if series== 'Winter':
        return 1
    if series == 'Spring':
        return 2
    if series == 'Summer':
        return 3
    if series == 'Autumn':
        return 4
def Holiday_groups_func2(series):
    if series== 'No Holiday':
        return 1
    if series == 'Holiday':
        return 2
def Functioning_Day_groups_func2(series):
    if series== 'No':
        return 1
    if series == 'Yes':
        return 2

def Hour_groups_func2(series):
    if int(series) < 6:
        return 1
    elif 6 <= int(series) < 12:
        return 2
    elif 12 <= int(series)<18:
        return 3
    elif 18 <= int(series):
        return 4

def part_data(my_data):
    #Distributes only the data obtained from the array!
    my_data['Date_num'] =  my_data['Date'].apply(date_groups_func2)
    my_data['Hour_num'] = my_data.Hour.apply(Hour_groups_func2)
    my_data['Temperature_num'] = my_data['Temperature(°C)'].apply(Temperature_groups_func2)
    my_data['Humidity_num'] = my_data['Humidity(%)'].apply(Humidity_groups_func2)
    my_data['Wind_speed_num'] = my_data['Wind speed (m/s)'].apply(Wind_speed_groups_func2)
    my_data['Visibility_num'] = my_data['Visibility (10m)'].apply(Visibility_groups_func2)
    my_data['Dew_point_temperature_num'] = my_data['Dew point temperature(°C)'].apply(
        Dew_point_temperature_groups_func2)
    my_data['Solar_Radiation_num'] = my_data['Solar Radiation (MJ/m2)'].apply(Solar_Radiation_groups_func2)
    my_data['Rainfall_num'] = my_data['Rainfall(mm)'].apply(Rainfall_groups_func2)
    my_data['Snowfall_num'] = my_data['Snowfall (cm)'].apply(Snowfall_groups_func2)
    my_data['Seasons_num'] = my_data['Seasons'].apply(Seasons_groups_func2)
    my_data['Holiday_num'] = my_data['Holiday'].apply(Holiday_groups_func2)
    my_data['Functioning_Day_num'] = my_data['Functioning Day'].apply(Functioning_Day_groups_func2)
    return my_data
# Receives an array that contains numbers and strings
def is_busy(row_inpot):
    data=[{'Date':row_inpot[0],'Hour':row_inpot[1],'Temperature(°C)':row_inpot[2],'Humidity(%)':row_inpot[3],
           'Wind speed (m/s)':row_inpot[4], 'Visibility (10m)':row_inpot[5],'Dew point temperature(°C)':row_inpot[6],
           'Solar Radiation (MJ/m2)':row_inpot[7],'Rainfall(mm)':row_inpot[8],'Snowfall (cm)':row_inpot[9],
           'Seasons' :row_inpot[10],'Holiday':row_inpot[11],'Functioning Day':row_inpot[12]}]
    #Note the array data to the DataFrame and divide the data by domains.
    row=pd.DataFrame(data)
    row_inpot=part_data(row)
    attributes_arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #Divide all data into domains
    my_data = part_all_data()
    branches = ''
    t=DECISION_TREE_LEARNING(my_data, my_data, attributes_arr, None,None,branches)
    #Construction of a decision tree and its examination using the array data inpout
    clum_name = t.get_name_example()
    # By the attribute name of the tree root - returns the data from the array
    clm = row_inpot[clum_name][0]
    # Returns the branch - (sub-tree) of the tree in the area where the data is in the array
    next = t.get_boy(clm)
    # As long as there is no definitive answer - busy or not busy - perform the actions we explained above
    while type(next) is not str :
         clum_name = next.get_name_example()
         clm = row_inpot[clum_name][0]
         next = next.get_boy(clm)
        # Returns and prints 1 if otherwise loaded - prints and returns 0
    if next=='True':
        print('1')
        return 1
    else:
        print('0')
        return 0
#According to a number of data - divides all the data into test data and learning data
def traning_chake(  my_data, num_leran_data):
    indices=my_data.index.tolist()
    test_indices = random.sample(population=indices, k=num_leran_data)
    leran_data=my_data.loc[test_indices]
    traning_data= my_data.drop(test_indices)
    return  leran_data, traning_data
#Receives a percentage of data to be tested.
#Divides all data by domains.
#Divides data into test data and learning data.
#Creates a decision tree.
#Decision cutter.
#Prints a decision tree.
#Computer error on test data and prints error percentage
def build_tree(ration):
    attributes_arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    my_data = part_all_data()
    num_leran_data = int(len(my_data) * ration)
    examples,chake_data = traning_chake(  my_data, num_leran_data)
    branches=''
    t=DECISION_TREE_LEARNING(examples, examples, attributes_arr, None,None,branches)
    to_cut_tree(t)
    print_tree(t, "branches_value", horizontal=True)
    miss= chake_tree(chake_data, t)*100
    print('Error rate:',miss,'%')












