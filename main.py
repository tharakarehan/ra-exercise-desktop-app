from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image 
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from time import sleep
import numpy as np
import cv2
import math
import os
from utils import VideoROIExtractor
from firestore import Init,downloadVd,review,Initialize
#change the path according to your location
# bklocation='/Users/tharakarehan/Desktop/RA Exercise App/code/background1.jpg'
global IMAGE
bklocation='background1.jpg'
Key=None

def DOWNLOAD():
    global Key
    global v5
    if VR == FALSE:
        messagebox.showerror(title="Message", message="Please verify your account ",icon='error')
    elif v4.get()=='Select a Patient':
        messagebox.showerror(title="Message", message=" Select a Patient ",icon='error')
    elif v4.get()=='No One':
        messagebox.showerror(title="Message", message=" No Patient Available ",icon='error')
    elif v5.get()=='' or v5.get()=='Select a Video':
        messagebox.showerror(title="Message", message=" Select a Video ",icon='error')
    else:
        print('v5',type(v5.get()))
        path=downloadVd(gui,v3.get(),v4.get(),v5.get(),docInfo)
        Key = path
       
def PLAY():
    global Key
    global v
    if resolution_field.get()=='':
        size=400
    else:
        size=int(resolution_field.get())
    if Key == None or Key=='':
        messagebox.showerror(title="Message", message="No video Detected",icon='error')
    else:
        V=VideoROIExtractor(verbose=True, sFactor=v1.get(), zFactor=v2.get() , outputSize=size ,path=Key)
        if v.get()==1:
            V.HandExtractor(save=False , handSide='L' ,fillMiss=False,handVisual=False,P=0.1)
        elif v.get()==2:
            V.HandExtractor(save=False , handSide='L' ,fillMiss=False,handVisual=True,P=0.1)
        elif v.get()==3:
            V.FootExtractor(save=False , footSide='L' ,fillMiss=False)
        elif v.get()==4:
            V.HeadExtractor(save=False ,fillMiss=False)
        elif v.get()==5:
            V.HandExtractor(save=False , handSide='R' ,fillMiss=False,handVisual=False,P=0.1)
        elif v.get()==6:
            V.HandExtractor(save=False , handSide='R' ,fillMiss=False,handVisual=True,P=0.1)
        elif v.get()==7:
            V.FootExtractor(save=False , footSide='R' ,fillMiss=False)
        elif v.get()==8:
            V.OriginalVideo()
        else:
            messagebox.showerror(title="Message", message="Please choose an option",icon='error')

def SAVE():
    global Key
    global v
    if resolution_field.get()=='':
        size=400
    else:
        size=int(resolution_field.get())
    if Key == None or Key=='':
        messagebox.showerror(title="Message", message="No video Detected",icon='error')
    else:
        V=VideoROIExtractor(verbose=True, sFactor=v1.get(), zFactor=v2.get() , outputSize=size ,path=Key)
        if v.get()==1:
            V.HandExtractor(save=True , handSide='L' ,fillMiss=False,handVisual=False,P=0.1)
        elif v.get()==2:
            V.HandExtractor(save=True , handSide='L' ,fillMiss=False,handVisual=True,P=0.1)
        elif v.get()==3:
            V.FootExtractor(save=True , footSide='L' ,fillMiss=False)
        elif v.get()==4:
            V.HeadExtractor(save=True ,fillMiss=False)
        elif v.get()==5:
            V.HandExtractor(save=True , handSide='R' ,fillMiss=False,handVisual=False,P=0.1)
        elif v.get()==6:
            V.HandExtractor(save=True , handSide='R' ,fillMiss=False,handVisual=True,P=0.1)
        elif v.get()==7:
            V.FootExtractor(save=True , footSide='R' ,fillMiss=False)
        elif v.get()==8:
            messagebox.showerror(title="Message", message="Original video is already saved",icon='error')
        else:
            messagebox.showerror(title="Message", message="Please choose an option",icon='error')

def OPEN():
    global Key
    x = askopenfilename()
    Key=x
    print(x)

def CHECK():
    global PatList
    global patOpt
    global VR
    global v4
    if v3.get()=='' or security_field.get()=='':
        messagebox.showerror(title="Message", message="Please fill the Credentials",icon='error')
    
    elif docInfo[v3.get()]['Pass']==security_field.get():
        PatList=docInfo[v3.get()]['Patients']
        patOpt.destroy()
        patOpt = OptionMenu(gui, v4, *PatList)
        patOpt.place(x=162, y=105,anchor='c')
        messagebox.showinfo(title="Message", message="Account Verified",icon='info')
        VR = TRUE
    else:
        messagebox.showerror(title="Message", message="Wrong Username and Password Combination",icon='error')

def SEARCH():
    global v5
    global Key
    global VidList
    global vidOpt
    global docInfo
    global patInfo
    if VR == FALSE:
        messagebox.showerror(title="Message", message="Please verify your account ",icon='error')
    elif v4.get()=='Select a Patient':
        messagebox.showerror(title="Message", message=" Select a Patient ",icon='error')
    elif v4.get()=='No One':
        messagebox.showerror(title="Message", message=" No Video Available ",icon='error')
    else:
        docInfo,patInfo=Init()
        VidList=list(map(lambda x:v4.get()+': '+str(list(x.keys())[0]), docInfo[v3.get()]['Videos'][v4.get()]))
        vidOpt.destroy()
        vidOpt = OptionMenu(gui, v5, *VidList)
        vidOpt.place(x=210, y=150,anchor='c')
        messagebox.showinfo(title="Message", message="Videos Found!",icon='info')

def REVIEW():

    def close_window_TL(): 
        popup.destroy()

    def SUBMIT():
        stat=review(popup,v3.get(),v4.get(),v5.get(),docInfo,review_text.get('1.0',END),v6.get())
        if stat:
            messagebox.showinfo(title="Message", message="Successfully Submitted",icon='info')
        else:
            messagebox.showerror(title="Message", message="Submission Failed",icon='error')

    v6 = IntVar()
    if VR == FALSE:
        messagebox.showerror(title="Message", message="Please verify your account ",icon='error')
    elif v4.get()=='Select a Patient':
        messagebox.showerror(title="Message", message=" Select a Patient ",icon='error')
    elif v4.get()=='No One':
        messagebox.showerror(title="Message", message=" No Patient Available ",icon='error')
    elif v5.get()=='' or v5.get()=='Select a Video':
        messagebox.showerror(title="Message", message=" Select a Video ",icon='error')
    else:
        popup = Toplevel()
        popup.configure(background='#e5e5a3')
        popup.geometry("500x450")
        popup.title('Doctor Review Panel')
        label1=Label(popup,bg='#e5e5a3',fg='black',text="Doctor Review Panel", font=("TkDefaultFont", 30))
        label1.place(x=250, y=25,anchor='c')
        label2=Label(popup,bg='#e5e5a3',fg='black',text="Write the review", font=("TkDefaultFont", 13))
        label2.place(x=90, y=75,anchor='c')
        review_text = Text(popup,width=54,height=12,bg='white',font=("TkDefaultFont", 11))
        review_text.place(x=250, y=175,anchor='c')
        label3=Label(popup,bg='#e5e5a3',fg='black',text="Rating", font=("TkDefaultFont", 13))
        label3.place(x=60, y=277,anchor='c')
        scaleStab = Scale( popup, variable = v6, from_ = 0, to = 5, orient = HORIZONTAL,length=250,width=20,tickinterval=1
                        ,resolution=1)
        scaleStab.place(x=250, y=320,anchor='c')

        #submit button
        buttonSB = Button(popup, text='Submit', fg='black',command=SUBMIT, height=2, width=12,highlightbackground='#3E4149') 
        buttonSB.place(x=140, y=400,anchor='c')

        #quit button
        buttonQR = Button(popup, text='Quit', fg='red',command=close_window_TL, height=2, width=12,highlightbackground='red') 
        buttonQR.place(x=360, y=400,anchor='c')


def close_window(): 
    gui.destroy()

###########################################################
Initialize()
docInfo,patInfo=Init()
print('doc',docInfo)
print('pat',patInfo)
###########################################################
gui = Tk() 
gui.title("RA Exercise App")    
gui.geometry("350x745") 
###########################################################
#Background image of the window
I=Image.open(bklocation)
I=I.resize((350,745))
background_image=ImageTk.PhotoImage(I)
background_label =Label(gui, image=background_image)
background_label.image=background_image
background_label.place(x=0, y=0, relwidth=1, relheight=1)
###########################################################
#Variables and parameters
v = IntVar()
v1 = DoubleVar()
v2 = DoubleVar()
v3 = StringVar(gui)
v4 = StringVar(gui)
v5 = StringVar(gui)
v3.set('Select a Doctor')
v4.set('Select a Patient')
v5.set('Select a Video')
VR = FALSE
DocList=docInfo.keys()
PatList=['Select a Patient']
VidList=['Select a Video']
Colour='#e5e5a3'
############################################################
#doctor label
doctor = Label(gui, text="Doctor :", bg='#2f319f',font=("TkDefaultFont", 16),fg='white')
doctor.place(x=85, y=25,anchor='c')

#doctor drop-down menu
docOpt = OptionMenu(gui, v3, *DocList)
docOpt.place(x=85, y=60,anchor='c')

#Passkey label
security = Label(gui, text="Pass Key :", bg='#2e40b3',font=("TkDefaultFont", 16),fg='white')
security.place(x=210, y=25,anchor='c')

#passkey entry
security_field = Entry(gui,width=8)
security_field.place(x=210, y=60,anchor='c')

#verify button
styleV = ttk.Style()
styleV.theme_use('default')
styleV.configure('my.TButton', font =('TkDefaultFont', 10, 'bold', 'underline'),foreground = 'red',bordercolor="red")
buttonV=ttk.Button(gui, text='Verify' ,command=CHECK, style='my.TButton',width=5)
buttonV.place(x=295, y=60,anchor='c')

#patient label
patient = Label(gui, text="Patient :", bg='#2f34a2',font=("TkDefaultFont", 16),fg='white')
patient.place(x=55, y=105,anchor='c')

#patient drop-down menu
patOpt = OptionMenu(gui, v4, *PatList)
patOpt.place(x=162, y=105,anchor='c')

#search button
buttonSr = Button(gui, text='Search', fg='black',command=SEARCH,  height=1, width=5,highlightbackground='#2d49be') 
buttonSr.place(x=282, y=105, anchor="c")

#video label
patient = Label(gui, text="Video :", bg='#2f37a6',font=("TkDefaultFont", 16),fg='white')
patient.place(x=55, y=150,anchor='c')

#video drop-down menu
vidOpt = OptionMenu(gui, v5, *VidList)
vidOpt.place(x=210, y=150,anchor='c')

#download button
buttonD = Button(gui, text='Download', fg='black',command=DOWNLOAD,  height=2, width=12,highlightbackground='#3E4149') 
buttonD.place(x=257, y=210, anchor="c")

#open button
buttonO = Button(gui, text='Open', fg='black',command=OPEN,  height=2, width=12,highlightbackground='#3E4149') 
buttonO.place(x=93, y=210, anchor="c")

#play button
buttonP = Button(gui, text='Play Video', fg='black',command=PLAY, height=2, width=12,highlightbackground='#3E4149') 
buttonP.place(x=257, y=645,anchor='c')

#save button
buttonS = Button(gui, text='Save Video', fg='black',command=SAVE, height=2, width=12,highlightbackground='#3E4149') 
buttonS.place(x=93, y=645,anchor='c')

#review button
buttonR = Button(gui, text='Review', fg='black',command=REVIEW, height=2, width=12,highlightbackground='#3E4149') 
buttonR.place(x=93, y=705,anchor='c')

#quit button
buttonQ = Button(gui, text='Quit', fg='red',command=close_window, height=2, width=12,highlightbackground='red') 
buttonQ.place(x=257, y=705,anchor='c')

#canvas
w = Canvas(gui, width=290,height=350,bg=Colour)
w.place(x=175,y=430,anchor='c')

#radio buttons (left side)
RbuttonLH=Radiobutton(gui, text="Left Hand            ", variable=v, value=1,width=14,bg=Colour)
RbuttonLH.place(x=100, y=280,anchor='c')
RbuttonLHP=Radiobutton(gui, text="Left Hand (Pose)", variable=v, value=2,width=14,bg=Colour)
RbuttonLHP.place(x=100, y=310,anchor='c')
RbuttonLF=Radiobutton(gui, text="Left Foot             ", variable=v, value=3,width=14,bg=Colour)
RbuttonLF.place(x=100, y=340,anchor='c')
RbuttonH=Radiobutton(gui, text="Head                   ", variable=v, value=4,width=14,bg=Colour)
RbuttonH.place(x=100, y=370,anchor='c')

#radio buttons (right side) 
RbuttonLH=Radiobutton(gui, text="Right Hand            ", variable=v, value=5,width=15,bg=Colour)
RbuttonLH.place(x=248, y=280,anchor='c')
RbuttonLHP=Radiobutton(gui, text="Right Hand (Pose)", variable=v, value=6,width=15,bg=Colour)
RbuttonLHP.place(x=248, y=310,anchor='c')
RbuttonLF=Radiobutton(gui, text="Right Foot             ", variable=v, value=7,width=15,bg=Colour)
RbuttonLF.place(x=248, y=340,anchor='c')
RbuttonH=Radiobutton(gui, text="Original                 ", variable=v, value=8,width=15,bg=Colour)
RbuttonH.place(x=248, y=370,anchor='c')

#scale for stabilization
scaleStab = Scale( gui, variable = v1, from_ = 0, to = 0.7, orient = HORIZONTAL,length=250,width=20,tickinterval=0.1
                        ,resolution=0.01,bg=Colour,label='Stability Factor')
scaleStab.place(x=175, y=430,anchor='c')

#scale for zooming
scaleZoom = Scale( gui, variable = v2, from_ = 0.5, to = 1.5, orient = HORIZONTAL,length=250,width=20,tickinterval=0.1
                        ,resolution=0.01,bg=Colour,label='Zooming Factor')
scaleZoom.place(x=175, y=515,anchor='c')

#resolution entry
resolution_field = Entry(gui,width=10)
resolution_field.place(x=200, y=580,anchor='c')

#resolution label
resolution = Label(gui, text="Resolution :", bg=Colour,font=("TkDefaultFont", 16))
resolution.place(x=95, y=580,anchor='c')

gui.mainloop()