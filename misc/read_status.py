import json
import csv
import pickle
#train_list = pickle.load(open('train_list_MGS.p','rb'))
train_list = ['22308','13010','12307','12801','12802','14055']
for train_num in train_list:
    f=open('/home/zerone/python/ogd/train_running_status/Train'+str(train_num)+'.txt','r')
    f1=csv.writer(open('/home/zerone/python/ogd/train_running_status_csv/Train'+str(train_num)+'.csv','w')) #Everytime this file is run, it writes a new one
    f = f.readlines()
    f1.writerow(['actarr_date','day','station_code','station_name','scharr_date','scharr','actarr','latemin','status','schdep','actdep','distance','has_departed','has_arrived'])
    for line in f:
        run_stat = json.loads(line)
        run_stat = run_stat['route']
        for stat in run_stat:
            f1.writerow([stat['actarr_date'],stat['day'],stat['station_']['code'],stat['station_']['name'],stat['scharr_date'],stat['scharr'],stat['actarr'],stat['latemin'],stat['status'],stat['schdep'],stat['actdep'],stat['distance'],stat['has_departed'],stat['has_arrived']])
