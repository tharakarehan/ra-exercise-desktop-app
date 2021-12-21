import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from tkinter import *

def timefunc(t):
    year=t.year
    month=t.month
    day=t.day
    hour=t.hour
    minute=t.minute
    return str(year)+'-'+str(month)+'-'+str(day)+'-'+str(hour)+'-'+str(minute)

def Initialize():
    global db
    # Use a service account
    cred = credentials.Certificate('rheumatoid-arthritis-exercise-b577e2e23c56.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print('Connected to Firestore')

def Init():
    global db
    #############################################################
    pat_ref = db.collection(u'Users')
    udocs = pat_ref.stream()
    pDict1={}
    pDict2={}
    for pd in udocs:
        pDict1[pd.id]=pd.to_dict()['name']
        pDict2[pd.to_dict()['name']]=pd.id

    #print(pDict)
    ##############################################################
    doc_ref = db.collection(u'Doctors')
    docs=doc_ref.stream()
    dictMain={}
    for doc in docs:
        Dict={}
        name = doc.to_dict()['name']
        Dict['id'] = doc.id
        Dict['Pass']= doc.to_dict()['passcode']
        Stat1=len(doc_ref.document(doc.id).collection(u'Inspections').get())
        print('Stat1',Stat1)
        if Stat1>=1:
            p_docs=doc_ref.document(doc.id).collection(u'Inspections').stream()
            P_List=[]
            videoDict={}
            for d in p_docs:
                usr=d.to_dict()['user'].path
                #print(usr)
                t=d.to_dict()['timestamp']
                videoDict.setdefault(pDict1[usr.split('/')[1]], []).append({ timefunc(t): d.id})
                if usr not in P_List:
                    P_List.append(pDict1[usr.split('/')[1]])
            Dict['Patients']=list(set(P_List))
            Dict['Videos']=videoDict
        else:
            Dict['Patients']=['No One']
            Dict['Videos']=['No Videos']
        dictMain[name]=Dict

    return dictMain,pDict2

def downloadVd(gui,doctor,patient,video,docInfo):
    global db
    import requests
    #print(video)
    time = video.split()[-1]
    #print(time)
    doc_ref = db.collection(u'Doctors').document(docInfo[doctor]['id'])
    for t in docInfo[doctor]['Videos'][patient]:
        if list(t.keys())[0]==time:
            docT=t[time]
            break
    pat_ref = doc_ref.collection(u'Inspections').document(docT)
    url=pat_ref.get().to_dict()['url']
    FolList=os.listdir('Videos')
    if doctor+'-'+patient+'-'+time+'.mp4' in FolList:
        messagebox.showerror(title="Message", message=" This video is already downloaded ",icon='error')
        return 'Videos/'+doctor+'-'+patient+'-'+time+'.mp4'
    else:
        r = requests.get(url)
        with open('Videos/'+doctor+'-'+patient+'-'+time+'.mp4', 'wb') as outfile:
            outfile.write(r.content)
        messagebox.showinfo(title="Message", message="DOWNLOAD COMPLETED!",icon='info')
        return 'Videos/'+doctor+'-'+patient+'-'+time+'.mp4'

def review(gui,doctor,patient,video,docInfo,text,rating):
    global db
    #print(video)
    time = video.split()[-1]
    #print(time)
    doc_ref = db.collection(u'Doctors').document(docInfo[doctor]['id'])
    for t in docInfo[doctor]['Videos'][patient]:
        if list(t.keys())[0]==time:
            docT=t[time]
            break
    try:
        doc_ref.collection(u'Inspections').document(docT).update({'review':text})
        doc_ref.collection(u'Inspections').document(docT).update({'rating':rating})
        return True
    except:
        return False
    


    







