# Import modules
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import pyperclip, math, csv, os

# Pyinstaller setting
def path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Import data
data=list(csv.reader(open(path("pdf.csv"))))
pdf=[float(data[i][0]) for i in range(len(data))]

data=list(csv.reader(open(path("pre_prob.csv"))))
chunk_x=[int(data[i][0]) for i in range(len(data))]
chunk_z=[int(data[i][1]) for i in range(len(data))]
prob=[float(data[i][2]) for i in range(len(data))]
cand_x=[chunk_x[i]*16+2 for i in range(len(data))]
cand_z=[chunk_z[i]*16+2 for i in range(len(data))]
stair_x=[chunk_x[i]*16+4 for i in range(len(data))]
stair_z=[chunk_z[i]*16+4 for i in range(len(data))]
net_x=[chunk_x[i]*2 for i in range(len(data))]
net_z=[chunk_z[i]*2 for i in range(len(data))]
lencand=len(data)

prob_dis=sorted([[prob[i],i] for i in range(len(cand_x))],reverse=True)
rec_x=round(sum(stair_x[i]*prob[i] for i in range(len(cand_x))))
rec_z=round(sum(stair_z[i]*prob[i] for i in range(len(cand_x))))
dist=[(rec_x-stair_x[j])**2+(rec_z-stair_z[j])**2 for j in range(len(cand_x))]
prob_in=sum([prob[j] for j in range(len(cand_x)) if dist[j]<16384])
rec_net_x=rec_x//8
rec_net_z=rec_z//8

pt=[]
pt_mode=[]
pt_prec=[]
pt_err=[]

# Functions
def PDF(x):
    if x>40:
        return(0)
    else:
        return(pdf[round(x*1000)])
def disprob(x):
    a=100*x
    return(f'{a:.2f}'+"%")
def disprob2(x):
    a=100*x
    return(f'{a:.1f}'+"%")
def cal_angle(x1,x2,z1,z2):
    xvec=x2-x1
    zvec=z2-z1
    diagvec=((zvec**2)+(xvec**2))**0.5
    if zvec>0:
        return(math.acos(xvec/diagvec))
    else:
        return(2*math.pi-math.acos(xvec/diagvec))
def rgb_to_hex(r, g, b):
  return '#{:02X}{:02X}{:02X}'.format(r, g, b)

# Window
win=tk.Tk()
win.title("/StroCate v1.1 (LHS1219)")
win.geometry("400x340+0+100")
win.resizable(False,False)
win.attributes("-topmost",True)
win.iconbitmap(path("icon.ico"))
ft=font.Font(family="Malgun Gothic",size=10)
ft2=font.Font(family="Malgun Gothic",size=10,underline=True)
win.option_add("*Font",ft)

# Accuracy setting
acc_dis=tk.Label(win,text="Allign Error")
acc_dis.place(x=55,y=11,anchor=tk.CENTER)
acc_list=[0.03,0.05,0.075,0.1,0.2,0.3,0.4,0.5,0.75,1,1.5,2,4]
acc_set=ttk.Combobox(win,values=acc_list,width=6,state="readonly")
acc_set.bind('<<ComboboxSelected>>')
acc_set.set("0.3")
acc_set.place(x=55,y=35,anchor=tk.CENTER)

# Mode setting
def set_mode(event):
    global x1, z1, x2, z2
    if mode_set.get()=="Coord+Coord":
        x2,z2=0,0
        c2_dis.config(text="Coord 2: ("+f'{x2:.2f}'+","+f'{z2:.2f}'+")")
        c2_but.place(x=200,y=93)
        facing_dir.place_forget()
        pixel_inp.place_forget()
    else:
        c2_dis.config(text="Direction:")
        c2_but.place_forget()
        facing_dir.set("Facing")
        facing_dir.place(x=90,y=95)
        pixel_inp.delete(0,tk.END)
        pixel_inp.insert(0,"Pixel")
        pixel_inp.place(x=175,y=96)
        if round(x1%1,1) not in [0.3,0.7] or round(z1%1,1) not in [0.3,0.7]:
            x1,z1=0,0
            c1_dis.config(text="Coord 1: ("+f'{x1:.2f}'+","+f'{z1:.2f}'+")")

mode_dis=tk.Label(win,text="Input Mode")
mode_dis.place(x=228,y=11,anchor=tk.CENTER)
mode_list=["Coord+Coord","Corner+Facing"]
mode_set=ttk.Combobox(win,values=mode_list,width=10,state="readonly")
mode_set.bind('<<ComboboxSelected>>',set_mode)
mode_set.set(mode_list[0])
mode_set.place(x=228,y=35,anchor=tk.CENTER)

pc=12
# Prob chunk setting
def set_pc(event):
    global pc
    ind=pc_list.index(pc_set.get())
    pc=pc_list_num[ind]
    pc_lab.config(text="<"+str(pc)+"C")
    update()
pc_dis=tk.Label(win,text="Prob Within")
pc_dis.place(x=330,y=11,anchor=tk.CENTER)
pc_list=[str(i)+" Chunks" for i in [6,8,10,12,14,16,18,20]]
pc_list_num=[6,8,10,12,14,16,18,20]
pc_set=ttk.Combobox(win,values=pc_list,width=9,state="readonly")
pc_set.bind('<<ComboboxSelected>>',set_pc)
pc_set.set(pc_list[3])
pc_set.place(x=330,y=35,anchor=tk.CENTER)

# Precision setting
pre_dis=tk.Label(win,text="Pixel Error")
pre_dis.place(x=135,y=11,anchor=tk.CENTER)
prec_inp=ttk.Combobox(win,values=["0.01","0.025","0.05","0.075","0.1","0.15","0.2","0.25","0.3"],width=6,state="readonly")
prec_inp.set("0.25")
prec_inp.place(x=135,y=35,anchor=tk.CENTER)

# Add coordinate
x1,z1,x2,z2=0,0,0,0

def set_c1():
    global x1, z1
    try:
        inp=pyperclip.paste()
        inp=inp.split(" ")
        x1=float(inp[0])
        z1=float(inp[2])
        if mode_set.get()=="Corner+Facing":
            if round(x1%1,1) not in [0.3,0.7] or round(z1%1,1) not in [0.3,0.7]:
                x1,z1=0,0
    except:
        pass
    c1_dis.config(text="Coord 1: ("+f'{x1:.2f}'+","+f'{z1:.2f}'+")")

def set_c2():
    global x2, z2
    try:
        inp=pyperclip.paste()
        inp=inp.split(" ")
        x2=float(inp[0])
        z2=float(inp[2])
    except:
        pass
    c2_dis.config(text="Coord 2: ("+f'{x2:.2f}'+","+f'{z2:.2f}'+")")

def add_point():
    global pt, x1, x2, z1, z2, pt_mode, pt_prec, pt_err
    if mode_set.get()==mode_list[0]:
        if (x1,z1)!=(x2,z2):
            pt.insert(0,[x1,z1,x2,z2])
            pt_mode.insert(0,mode_set.get())
            pt_err.insert(0,float(acc_set.get()))
            pt_prec.insert(0,0)
            listdata.insert(0,acc_set.get()+'/'+f'{x1:.0f}'+","+f'{z1:.0f}'+"/"+f'{x2:.0f}'+","+f'{z2:.0f}')
            x1,x2,z1,z2=0,0,0,0
            c1_dis.config(text="Coord 1: ("+f'{x1:.2f}'+","+f'{z1:.2f}'+")")
            c2_dis.config(text="Coord 2: ("+f'{x2:.2f}'+","+f'{z2:.2f}'+")")
            update()
    else:
        mode1=round(x1%1,2)
        mode2=round(z1%1,2)
        facing=facing_dir.get()
        if (mode1==0.3 or mode1==0.7) and (mode2==0.3 or mode2==0.7) and (facing=="X" or facing=="Z") and prec_inp.get()!="Prec":
            valid=True
            try:
                dir_pixel=float(pixel_inp.get())
                if dir_pixel>=0 and dir_pixel<=16:
                    valid=True
                else:
                    valid=False
            except:
                valid=False
            if valid:
                if mode1==0.7 and mode2==0.7:
                    if facing=="X":
                        x2=x1+0.3
                        z2=z1+0.3-dir_pixel/16
                    else:
                        x2=x1+0.3-dir_pixel/16
                        z2=z1+0.3
                elif mode1==0.7 and mode2==0.3:
                    if facing=="X":
                        x2=x1+0.3
                        z2=z1-0.3+dir_pixel/16
                    else:
                        x2=x1+0.3-dir_pixel/16
                        z2=z1-0.3
                elif mode1==0.3 and mode2==0.7:
                    if facing=="X":
                        x2=x1-0.3
                        z2=z1+0.3-dir_pixel/16
                    else:
                        x2=x1-0.3+dir_pixel/16
                        z2=z1+0.3
                else:
                    if facing=="X":
                        x2=x1-0.3
                        z2=z1-0.3+dir_pixel/16
                    else:
                        x2=x1-0.3+dir_pixel/16
                        z2=z1-0.3
                    
                pt.insert(0,[x1,z1,x2,z2])
                pt_mode.insert(0,mode_set.get())
                pt_err.insert(0,float(acc_set.get()))
                listdata.insert(0,acc_set.get()+'/'+f'{x1:.0f}'+","+f'{z1:.0f}'+"/"+f'{x2-x1:.2f}'+"/"+f'{z2-z1:.2f}')
                facing_dir.set("Facing")
                pixel_inp.delete(0,tk.END)
                pixel_inp.insert(0,"Pixel")
                pt_prec.insert(0,float(prec_inp.get()))
                x1,x2,z1,z2=0,0,0,0
                c1_dis.config(text="Coord 1: ("+f'{x1:.2f}'+","+f'{z1:.2f}'+")")
                update()
        
def del_point():
    global pt, pt_mode, pt_prec, pt_err
    try:
        ind=listdata.curselection()[0]
        listdata.delete(ind)
        pt.pop(ind)
        pt_prec.pop(ind)
        pt_mode.pop(ind)
        pt_err.pop(ind)
        update()
    except:
        pass

def error_plus():
    global pt_err
    try:
        ind=listdata.curselection()[0]
        acc_ind=acc_list.index(pt_err[ind])
        if acc_ind<(len(acc_list)-1):
            acc_ind=acc_ind+1
            pt_err[ind]=acc_list[acc_ind]
            listdata.delete(ind)
            if pt_mode=="Coord+Coord":
                listdata.insert(ind,str(pt_err[ind])+'/'+f'{pt[ind][0]:.0f}'+","+f'{pt[ind][1]:.0f}'+"/"+f'{pt[ind][2]:.0f}'+","+f'{pt[ind][3]:.0f}')
            else:
                listdata.insert(ind,str(pt_err[ind])+'/'+f'{pt[ind][0]:.0f}'+","+f'{pt[ind][1]:.0f}'+"/"+f'{pt[ind][2]-pt[ind][0]:.2f}'+"/"+f'{pt[ind][3]-pt[ind][1]:.2f}')
            update()
            listdata.select_set(ind)
    except:
        pass

def error_minus():
    global pt_err
    try:
        ind=listdata.curselection()[0]
        acc_ind=acc_list.index(pt_err[ind])
        if acc_ind>0:
            acc_ind=acc_ind-1
            pt_err[ind]=acc_list[acc_ind]
            listdata.delete(ind)
            if pt_mode=="Coord+Coord":
                listdata.insert(ind,str(pt_err[ind])+'/'+f'{pt[ind][0]:.0f}'+","+f'{pt[ind][1]:.0f}'+"/"+f'{pt[ind][2]:.0f}'+","+f'{pt[ind][3]:.0f}')
            else:
                listdata.insert(ind,str(pt_err[ind])+'/'+f'{pt[ind][0]:.0f}'+","+f'{pt[ind][1]:.0f}'+"/"+f'{pt[ind][2]-pt[ind][0]:.2f}'+"/"+f'{pt[ind][3]-pt[ind][1]:.2f}')
            update()
            listdata.select_set(ind)
    except:
        pass

def clear():
    global pt, pt_mode, pt_prec, pt_err
    pt=[]
    pt_mode=[]
    pt_prec=[]
    pt_err=[]
    listdata.delete(0,tk.END)
    update()

def clear_inp(event):
    pixel_inp.delete(0,tk.END)

c1_dis=tk.Label(win,text="Coord 1: ("+f'{x1:.2f}'+","+f'{z1:.2f}'+")")
c1_dis.place(x=5,y=65)
c1_but=tk.Button(win,text="PASTE",command=set_c1,padx=5,pady=1)
c1_but.place(x=200,y=63)

c2_dis=tk.Label(win,text="Coord 2: ("+f'{x2:.2f}'+","+f'{z2:.2f}'+")")
c2_dis.place(x=5,y=95)
facing_dir=ttk.Combobox(win,values=["X","Z"],width=6,state="readonly")
facing_dir.set("Facing")
pixel_inp=tk.Entry(win,width=6)
pixel_inp.insert(0,"Pixels")
pixel_inp.bind("<Button-1>",clear_inp)
if mode_set.get()=="Coord+Coord":
    c2_but=tk.Button(win,text="PASTE",command=set_c2,padx=5,pady=1)
    c2_but.place(x=200,y=93)

add_but=tk.Button(win,text="ADD",command=add_point,padx=8,pady=3)
add_but.place(x=265,y=77)

# Datas
tk.Label(win,text="DATA").place(x=5,y=130)
listdata=tk.Listbox(win,height=8,width=15)
listdata.place(x=5,y=152)

del_but=tk.Button(win,text="DELETE",command=del_point,padx=2,pady=1)
del_but.place(x=5,y=302)
clear_but=tk.Button(win,text="CLEAR",command=clear,padx=2,pady=1)
clear_but.place(x=63,y=302)
pl_but=tk.Button(win,text="ER+",command=error_plus,padx=2,pady=1)
# pl_but.place(x=42,y=304)
mn_but=tk.Button(win,text="ER-",command=error_minus,padx=2,pady=1)
# mn_but.place(x=81,y=304)

# Visualization
labels=[[] for i in range(10)]
for i in range(10):
    R=tk.Label(win,text="")
    R.place(x=160,y=160+20*i,anchor=tk.CENTER)
    labels[i].append(R)
    R=tk.Label(win,text="")
    R.place(x=240,y=160+20*i,anchor=tk.CENTER)
    labels[i].append(R)
    R=tk.Label(win,text="")
    R.place(x=308,y=160+20*i,anchor=tk.CENTER)
    labels[i].append(R)
    R=tk.Label(win,text="")
    R.place(x=360,y=160+20*i,anchor=tk.CENTER)
    labels[i].append(R)

# Calculate
def update():
    global prob, prob_dis, rec_x, rec_z, rec_net_x, rec_net_z
    prob=[float(data[i][2]) for i in range(len(data))]
    for iteration in range(len(pt)):
        x1=pt[iteration][0]
        z1=pt[iteration][1]
        x2=pt[iteration][2]
        z2=pt[iteration][3]

        dist=((x1-x2)**2+(z1-z2)**2)**0.5
        error_angle=math.tan(pt_err[iteration]/12/16)
        if pt_mode[iteration]==mode_list[1]:
            error_precision=math.atan(0.01/2*2*math.sqrt(2)/dist)*0.3
        else:
            error_precision=math.atan(pt_prec[iteration]/16/0.3)*0.5
        error_combine=(error_angle**2+error_precision**2)**0.5
        
        a=x1+0.5
        b=z1+0.5
        p=(z2-z1)/(x2-x1)
        q=z1-p*x1
        r=12

        denom1=-1*a*a*p*p+2*a*b*p-2*a*p*q-b*b+2*b*q+p*p*r*r-q*q+r*r
        denom2=a+b*p-p*q
        nom=p*p+1
        xeye1=(denom1**0.5+denom2)/nom
        xeye2=(-1*denom1**0.5+denom2)/nom
        zeye1=p*xeye1+q
        zeye2=p*xeye2+q

        dir_vec=(x2-x1,z2-z1)
        vec1=(xeye1-a,zeye1-b)
        vec2=(xeye2-a,zeye2-b)
        cos1=dir_vec[0]*vec1[0]+dir_vec[1]*vec1[1]
        cos2=dir_vec[0]*vec2[0]+dir_vec[1]*vec2[1]
        if cos1>cos2:
            xeye=xeye1
            zeye=zeye1
        else:
            xeye=xeye2
            zeye=zeye2

        angle=cal_angle(a,xeye,b,zeye)
        cand_angle=[cal_angle(a,cand_x[i],b,cand_z[i]) for i in range(len(cand_x))]
        angle_dif=[min(abs(cand_angle[i]-angle),abs(cand_angle[i]-angle+2*math.pi),abs(cand_angle[i]-angle-2*math.pi)) for i in range(len(cand_x))]
        prob_mult=[PDF(angle_dif[i]/(error_precision+error_angle)) for i in range(len(cand_x))]
        prob=[prob[i]*prob_mult[i] for i in range(len(cand_x))]
        sumprob=sum(prob)
        if sumprob>0:
            prob=[prob[i]/sumprob for i in range(len(cand_x))]
        else:
            prob=[1/lencand for i in range(len(cand_x))]

    prob_dis=sorted([[prob[i],i] for i in range(len(cand_x))],reverse=True)
    rec_x=round(sum(stair_x[i]*prob[i] for i in range(len(cand_x))))
    rec_z=round(sum(stair_z[i]*prob[i] for i in range(len(cand_x))))
    dist=[(rec_x-stair_x[j])**2+(rec_z-stair_z[j])**2 for j in range(len(cand_x))]
    prob_in=sum([prob[j] for j in range(len(cand_x)) if dist[j]<36864])
    rec_net_x=rec_x//8
    rec_net_z=rec_z//8

    pc2=(pc*16)**2

    prob2=[]
    for i in range(9):
        j=prob_dis[i][1]
        p2=sum(prob[l] for l in range(len(cand_x)) if (stair_x[l]-stair_x[j])**2+(stair_z[l]-stair_z[j])**2<pc2)
        prob2.append(p2)
        
    for i in range(9):
        j=prob_dis[i][1]
        labels[i][0].config(text="("+str(stair_x[j])+","+str(stair_z[j])+")")
        labels[i][1].config(text="("+str(net_x[j])+","+str(net_z[j])+")")
        k=prob_dis[i][0]
        if k<0.05:
            k2=k*(1/0.05)
            col_code=(math.floor(k2*127),0,0)
        else:
            k2=(k-0.05)*(1/0.95)
            col_code=(math.floor(127+k2*127),0,0)
        if i==0 and prob_dis[i][0]>2/lencand:
            labels[i][2].config(text=disprob2(prob_dis[i][0]),fg=rgb_to_hex(col_code[0],col_code[1],col_code[2]),font=ft2)
        else:
            labels[i][2].config(text=disprob2(prob_dis[i][0]),fg=rgb_to_hex(col_code[0],col_code[1],col_code[2]),font=ft)
        
        col_code=(math.floor(255*prob2[i]),0,0)
        if max(prob2)==prob2[i] and prob2[i]>0.1:
            labels[i][3].config(text=disprob2(prob2[i]),fg=rgb_to_hex(col_code[0],col_code[1],col_code[2]),font=ft2)
        else:
            labels[i][3].config(text=disprob2(prob2[i]),fg=rgb_to_hex(col_code[0],col_code[1],col_code[2]),font=ft)

# Result
tk.Label(win,text="OVERWORLD").place(x=160,y=140,anchor=tk.CENTER)
tk.Label(win,text="NETHER").place(x=240,y=140,anchor=tk.CENTER)
tk.Label(win,text="PROB").place(x=308,y=140,anchor=tk.CENTER)
pc_lab=tk.Label(win,text="<"+str(pc)+"C")
pc_lab.place(x=360,y=140,anchor=tk.CENTER)
update()

# Display
win.mainloop()
