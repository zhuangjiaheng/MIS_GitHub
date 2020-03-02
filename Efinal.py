# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:04:49 2019

@author: zjh
"""

import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import re
import webbrowser
import time
import wordcloud
from PIL import Image,ImageTk

def originaltext():
    global text  #让此处的text被其他地方调用
    fd=tkinter.filedialog.askopenfilename()
    try:
        txt=open(fd,"r").read()
    except UnicodeDecodeError:
        txt=open(fd,"r",encodin  g="utf-8").read()
    textbox.insert(tk.INSERT,txt)
    text=getText(txt)   #读入文件后进行相应的处理
#文本输入及初步处理函数
def getText(txt):
    #txt=open(r"E:\大一下2019春\python\大作业 文本编辑器\样例3.txt","r",encoding='utf-8').read()#encoding一句在开样例三
    #txt=open(r"E:\大一下2019春\python\大作业 文本编辑器\样例2.txt","r").read()
    txt=txt.lower()
    for ch in '!"#$%()*+,-./:;<=>?@[\\]^_`{|}~\'–’“”0123456789':
        txt=txt.replace(ch,"")
    return txt
#text=getText(txt)
def save():
    global text
    txt=textbox.get(1.0,tk.END)
    text=getText(txt)
stopw=open(r"E:\大一下2019春\python\大作业 文本编辑器\停用词表.txt","r").read()
stopwords=stopw.split()
def modifiedtext(text):
    textbox.delete(1.0,tk.END)
    textbox.insert(tk.INSERT,text)  #INSERT表示光标位置加入
#清除函数
def clear():
    ans=tkinter.messagebox.askokcancel("Hint","Are you sure to clear?")
    if ans:
        textbox.delete(1.0,tk.END)
#词频统计函数
def frequency(text):
    words=text.split()
    counts={}
    for word in words:
        counts[word]=counts.get(word,0)+1
    items=list(counts.items())
    items.sort(key=lambda x:x[1],reverse=True)
    for i in range(len(items)):
        word,count=items[i]
        print("{0:<15}{1:>5}".format(word,count)) 
    print("英文单词的总数为:",len(words))
    #在GUI中输出
    cipin=tk.Tk()
    cipin.title("词频统计结果")
    cipin.geometry("400x300")
    textbox1 = tk.Text(cipin)
    textbox1.place(x=0,y=0,width=400,height=300)
    ybar=tk.Scrollbar(cipin,orient=tk.VERTICAL)
    ybar.config(command=textbox1.yview)
    textbox1.config(yscrollcommand=ybar.set) 
    ybar.pack(side=tk.RIGHT,fill=tk.Y)  #fill充满y轴
    #在IPython环境中输出
    for i in range(len(items)):
        word,count=items[i]
        ch1="{0:<15}{1:>5}".format(word,count)+"\n"
        textbox1.insert(tk.INSERT,ch1)
    ch2="英文单词的总数为:"+str(len(words))
    textbox1.insert(tk.INSERT,ch2)
#统计字符数
def strlong():
    printnum1=str(len(textbox.get(1.0,tk.END)))  #包括换行符
    #字数统计标签
    labelNum1=tk.Label(top,     
                      text="字符统计: "+printnum1,
                      justify=tk.RIGHT,
                      width=80) 
    labelNum1.place(x=10,y=550,width=125,height=20)
#统计单词数
def wordlong():
    caltxt=textbox.get(1.0,tk.END)
    words2=caltxt.split()
    rlt=len(words2)
    #字数统计标签
    labelNum2=tk.Label(top,     
                      text="词数统计: "+str(rlt),
                      justify=tk.RIGHT,
                      width=80) 
    labelNum2.place(x=10,y=575,width=125,height=20)
#绘制柱状图和云图
def draw(text,stopwords):
    words=text.split()
    counts={}
    for word in words:
        if word not in stopwords:
            counts[word]=counts.get(word,0)+1
    items=list(counts.items())
    items.sort(key=lambda x:x[1],reverse=True)
    drawords=[];nums=[]
    for i in range(6):
        word,count=items[i]
        drawords.append(word);nums.append(count)
        print("{0:<15}{1:>5}".format(word,count)) 
    color = tkinter.simpledialog.askstring('Hint','Please enter the graphic color')
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    ind = np.arange(1,7,1)
    width = 0.75
    plt.bar(ind, nums, width=width, color=color, label=u'关键词数目')
    plt.ylabel(u'nums')
    plt.xlabel(u'words')
    plt.title(u'词频统计表')
    plt.xticks(ind,drawords)
    plt.legend()
    plt.savefig(r"bar.jpg")
    plt.show()  #从哪蹦出来的orz Ipython中没了？？？
    '''
    root=tk.Tk()
    root.geometry("400x300")
    image =Image.open('bar.png')
    img =ImageTk.PhotoImage(image)
    canvas = tk.Canvas(root, width = image.width ,height = image.height, bg = 'white')
    canvas.create_image(0,0,image = img,anchor="nw")
    canvas.pack()
    '''
    #只能有一个tk()存在哦  
def drawcloud(text):
    w=wordcloud.WordCloud(font_path="msyh.ttc",
                          max_words=20,
                          width=1000,height=700,
                          background_color="white")
    w.generate(text)
    w.to_file("wordcloud.jpg")
    tkinter.messagebox.showinfo("Hint","Successfully generated!")
#文本高亮
def highlight():
    textbox.tag_add("highlight",tk.SEL_FIRST,tk.SEL_LAST)
    textbox.tag_config("highlight",background="yellow",foreground="red")
def cancellight():
    reprint=textbox.get("1.0",tk.END)
    textbox.delete("1.0",tk.END)
    textbox.insert(tk.INSERT,reprint)
    #textbox.tag_add("highlight",tk.SEL_FIRST,tk.SEL_LAST)
    #textbox.tag_config("highlight",background="white",foreground="black")
#一下三个函数共同完成查找功能
#将位置转换为元祖类型
def getindex(text,index):
    #print(textbox.index(index))
    return tuple(map(int,str.split(textbox.index(index),".")))
def wordlight(pos,speword,specolor):
    op='+'+str(len(speword))+'c'
    textbox.tag_add("highlight_word",pos,pos+op)
    textbox.tag_config("highlight_word",background=specolor,foreground="black")
def searchword():
    start="1.0"   
    speword = tkinter.simpledialog.askstring('Hint','Please enter the word')    
    specolor = tkinter.simpledialog.askstring('Hint','Please enter the color')
    while True:
        pos=textbox.search(speword,start,stopindex=tk.END)
        if not pos:  #返回起始位
            break
        #print("位置是:",getindex(textbox,pos))
        wordlight(pos,speword,specolor)
        start=pos+'+1c'
def searchword0():
    speword = tkinter.simpledialog.askstring('Hint','Please enter the word')
    it=re.finditer("[\s]*"+speword+"[^a-z]",text,re.I)
    #GUI前期绘制
    find=tk.Tk()
    find.title("查找结果")
    find.geometry("400x300")
    textbox2 = tk.Text(find)
    textbox2.place(x=0,y=0,width=400,height=300)
    ybar=tk.Scrollbar(find,orient=tk.VERTICAL)
    ybar.config(command=textbox2.yview)
    textbox2.config(yscrollcommand=ybar.set) 
    ybar.pack(side=tk.RIGHT,fill=tk.Y)  #fill充满y轴
    i=0
    for match in it:
        i+=1
        a=match.start()
        b=match.end()
        ch="第{}个{}的位置为:{}字符——{}字符".format(i,speword,a+1,b-1)+"\n"
        textbox2.insert(tk.INSERT,ch)
        print("第{}个{}的位置为:{}字符——{}字符".format(i,speword,a+1,b-1))
def change(text):
    text=" "+text[:-1]+" "
    old = tkinter.simpledialog.askstring('Hint','Please enter the old word')
    new = tkinter.simpledialog.askstring('Hint','Please enter the new word')
    #text=re.sub("[\s]*"+old+"[^a-z]"," "+new+" ",text,re.I)
    old=" "+old+" ";new=" "+new+" "
    text=text.replace(old,new)
    text=text.strip()
    textbox.delete(1.0,tk.END)
    textbox.insert(tk.INSERT,text)
    #注意：其他地方的text未被修改！用后若要保留文本要按保存
    #写写如何处理aaa aaasss的过程 考虑段落首尾
def click163(event):
    webbrowser.open("http://mail.163.com/")
def link163():
    textbox.insert("1.0","我使用163邮件服务器\n")
    textbox.tag_add("link163","1.3","1.6")
    textbox.tag_config("link163",foreground="blue",underline=True)
def click126(event):
    webbrowser.open("http://mail.126.com/")
def link126():
    textbox.insert("1.0","我使用126邮件服务器\n")
    textbox.tag_add("link126","1.3","1.6")
    textbox.tag_config("link126",foreground="blue",underline=True)
#定义键盘操作回调函数,绑定键盘操作
def key_callback(event):
    textbox.edit_separator()
#定义左击回调函数，绑定左击操作    
#def left_callback(event):
 #   textbox.edit_separator()
#撤回
def undo_callback():
    textbox.edit_undo()
#恢复
def redo_callback():
    textbox.edit_redo()
#与链接绑定
def show_hand_cursor(event):
    textbox.config(cursor="arrow")
def show_arrow_cursor(event):
    textbox.config(cursor="xterm")
#保存导出文件
def onSave():
    filename = tkinter.filedialog.asksaveasfilename()
    if filename:
      alltext=textbox.get(1.0,tk.END)           
      open(filename, 'w').write(alltext)
      tkinter.messagebox.showinfo("Hint","Successfully saved!")
def caltime():
    end=time.perf_counter()
    dtime=float(end-start)
    if dtime>=3600:
        q1=dtime//3600;r1=dtime%3600
        q2=int(r1//60);r2=int(r1%60)
        printtime=str(q1)+"(h):"+str(q2)+"(m):"+str(r2)+"(s)"
    elif dtime>=60:
        q1=int(dtime//60);r1=int(dtime%60)
        printtime=str(q1)+"(m):"+str(r1)+"(s)"
    else:
        printtime=str(round(dtime,2))+"(s)"  
    labelTime=tk.Label(top,     
                      text="时间统计: "+printtime,
                      justify=tk.RIGHT,
                      width=80) 
    labelTime.place(x=300,y=550,width=200,height=20)
#计时功能
start=time.perf_counter()
#主程序
top = tk.Tk()   #Toplevel
top.geometry("625x600")
top.resizable(False,False)
top.title("简易的文本编辑器")
#创建文本框
textbox = tk.Text(top,undo=True,maxundo=20)
textbox.place(x=5,y=50,width=600,height=500)

#插入一个分隔符到存放操作记录的栈中，用于表示已经完成一次完整的操作
textbox.edit_separator()
#将键盘鼠标操作事件“<Key><Button-1>”与回调函数***_callback绑定
textbox.bind("<Key>",key_callback)
#textbox.bind("<Button-1>",left_callback)
#链接效果163
textbox.tag_bind("link163","<Enter>",show_hand_cursor)
textbox.tag_bind("link163","<Button-1>",click163)
textbox.tag_bind("link163","<Leave>",show_arrow_cursor)
#链接效果126
textbox.tag_bind("link126","<Enter>",show_hand_cursor)
textbox.tag_bind("link126","<Button-1>",click126)
textbox.tag_bind("link126","<Leave>",show_arrow_cursor)

ybar=tk.Scrollbar(top,orient=tk.VERTICAL)
ybar.config(command=textbox.yview)
textbox.config(yscrollcommand=ybar.set) 
ybar.pack(side=tk.RIGHT,fill=tk.Y)

#创建导入文本按钮
ReadBtn=tk.Button(top,
                  text="导入文本",
                  command=originaltext)
ReadBtn.place(x=5,y=10,width=60,height=30)
#创建清除文本按钮
clearBtn=tk.Button(top,
                   text="标准模式",
                   command=lambda:modifiedtext(text))
clearBtn.place(x=80,y=10,width=60,height=30)
#创建词频统计按钮
wordfreBtn=tk.Button(top,
                     text="词频统计",
                     command=lambda:frequency(text))  #lambad传入参数是lambda
wordfreBtn.place(x=155,y=10,width=60,height=30)
#绘图按钮
drawBtn=tk.Button(top,
                  text="绘制图形",
                  command=lambda:draw(text,stopwords))
drawBtn.place(x=230,y=10,width=60,height=30)
#词云按钮
cloudBtn=tk.Button(top,
                   text="生成词云",
                   command=lambda:drawcloud(text))
cloudBtn.place(x=305,y=10,width=60,height=30)
#高亮按钮
lightBtn=tk.Button(top,
                   text="高亮文本",
                   command=highlight)
lightBtn.place(x=380,y=10,width=60,height=30)
#取消高亮按钮
cancellightBtn=tk.Button(top,
                         text="取消高亮",
                         command=cancellight)
cancellightBtn.place(x=455,y=10,width=60,height=30)
#查找按钮
searchBtn=tk.Button(top,
                    text="标记单词",
                    command=searchword)
searchBtn.place(x=530,y=10,width=60,height=30)
labelIntro=tk.Label(top,
                    text="注:除保存文本&导入文本,其余对文本内容的操作需先保存,后分析",
                    justify=tk.RIGHT,
                    width=1000) 
labelIntro.place(x=-125,y=575,width=1000,height=20)
#添加菜单功能
menubar = tk.Menu(top)  #创建一个顶级菜单
#filemenu1创建主菜单和子菜单
c1 = [originaltext,save,undo_callback,redo_callback,clear,lambda:modifiedtext(text),onSave]
i = 0
filemenu1 = tk.Menu(menubar,tearoff = 0)
for item in ['导入文本','文件保存','撤销操作','恢复操作','清空文本','标准模式','导出文本']:
    filemenu1.add_command(label = item,command = c1[i])
    filemenu1.add_separator()  #加分割线
    i = i + 1
#filemenu2创建主菜单和子菜单
c2 = [strlong,wordlong,lambda:frequency(text),lambda:draw(text,stopwords),lambda:drawcloud(text)]
i = 0
filemenu2 = tk.Menu(menubar,tearoff = 0)
for item in ['字符统计','词数统计','词频统计','绘柱状图','绘制云图']:
    filemenu2.add_command(label = item,command = c2[i])
    filemenu2.add_separator()  #加分割线
    i = i + 1
#filemenu3创建主菜单和子菜单
c3 = [highlight,cancellight,searchword,searchword0,lambda:change(text)]
i = 0
filemenu3 = tk.Menu(menubar,tearoff = 0)
for item in ['高亮文本','取消高亮','标记单词','查找单词','修改单词']:
    filemenu3.add_command(label = item,command = c3[i])
    filemenu3.add_separator()  #加分割线
    i = i + 1
#filemenu4创建主菜单和子菜单
c4 = [link163,link126]
i = 0
filemenu4 = tk.Menu(menubar,tearoff = 0)
for item in ['163邮箱','126邮箱']:
    filemenu4.add_command(label = item,command = c4[i])
    filemenu4.add_separator()  #加分割线
    i = i + 1
#filemenu5创建主菜单和子菜单
c5 = [caltime]
i = 0
filemenu5 = tk.Menu(menubar,tearoff = 0)
for item in ['时间统计']:
    filemenu5.add_command(label = item,command = c5[i])
    filemenu5.add_separator()  #加分割线
    i = i + 1
#指定主菜单和子子菜单的级联关系
#将menubar的menu属性指定为filemenu，即filemenu为menubar的下拉菜单
menubar.add_cascade(label = '文件编辑',menu = filemenu1)
menubar.add_cascade(label = '统计功能',menu = filemenu2)
menubar.add_cascade(label = '文件显示',menu = filemenu3)
menubar.add_cascade(label = '发送邮件',menu = filemenu4)
menubar.add_cascade(label = '时间管理',menu = filemenu5)
top['menu'] = menubar
tk.mainloop()
