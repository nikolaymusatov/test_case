import json
import datetime
import pandas as pd

def read_competitors2():
    with open(file="competitors2.json",encoding="utf-8") as read_file:
        data = json.load(read_file)
    Sportsmans=pd.DataFrame(columns=['Number','Name', 'Surname'])
    for i in data:
        temp=pd.DataFrame({'Number':[int(i)],'Name':[data[i]["Name"]],'Surname':[data[i]["Surname"]]})
        Sportsmans=pd.concat([Sportsmans,temp], ignore_index = True)
    return Sportsmans

def read_results():
    fileres=open("results_RUN.txt","r",encoding="utf-8-sig")
    data=fileres.readlines()
    times = pd.DataFrame(columns=['Number', 'Result'])
    for i in range(0, len(data), 2):
        temp1=data[i].split()
        temp2=data[i+1].split()
        if temp1[0]==temp2[0] and temp1[1]=='start' and temp2[1]=='finish':
            res=datetime.datetime.strptime(temp2[2], '%H:%M:%S,%f')-datetime.datetime.strptime(temp1[2], '%H:%M:%S,%f')
            temp = pd.DataFrame({'Number':[int(temp1[0])],'Result':[res]})
            times=pd.concat([times,temp], ignore_index = True)
    return times

def get_data():
    Sportsmans = read_competitors2()
    times=read_results()
    Sportsmans=Sportsmans.merge(times, left_on='Number', right_on='Number', suffixes=('_left', '_right'))
    Sportsmans=Sportsmans.sort_values(by=['Result'])
    Sportsmans=Sportsmans.reset_index(drop=True)
    return Sportsmans

def print_res():
    Sportamans=get_data()
    print("Занятое место   Нагрудный номер   Имя           Фамилия       Результат")
    for i in range(len(Sportamans)):
        temp=Sportamans.iloc[i]
        res=str(temp['Result'])
        res=res[10:-4]
        print(str(i+1).ljust(16)+str(temp['Number']).ljust(18)+temp['Surname'].ljust(14)+temp['Name'].ljust(14) +res)

if __name__ == '__main__':
    print_res()