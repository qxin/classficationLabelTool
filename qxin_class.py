import tkinter as tk

from tkinter import *

import numpy as np
from PIL import Image, ImageTk
import tkinter.ttk as ttk
import os
import glob
import random
import sys
# qxin set for win7
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

from collections import OrderedDict
# colors for the bounding boxes
COLORS = {}


class LabelTool:
    def __init__(self, window,imgpaths,cnt):
        self.parent = window
        self.imgpaths = imgpaths
        self.cnt = cnt
        self.totals = {}
        for x in self.imgpaths:
            self.totals[x] = -1

        # set up the main frame

        self.parent.title("LabelTool")
        self.parent.resizable(width=True, height=True)
        self.parent.geometry("1200x500")
        self.parent.bind("<space>", self.press_space)
        self.parent.bind("<Return>", self.press_return)
        self.parent.bind("<BackSpace>", self.press_BackSpace)
        self.parent.bind("<Left>", self.hit_prev)
        self.parent.bind("<Right>", self.hit_next)



        self.parent.bind("c", self.press_clear)
        self.parent.bind("s", self.press_save)
        for x in range(10):
            self.parent.bind("{}".format(x), lambda event, a=x: self.qxin_prees_num_clsLabel(a))

        self.left_frame = Frame(self.parent)
        # self.left_frame.pack(fill=BOTH, expand=1)
        # self.left_frame.grid(row=0, column=0,rowspan=2, sticky=W + N,highlightbackground="green")
        # self.left_frame.pack()
        self.left_frame.place(bordermode=OUTSIDE,x=10, y=10, height=500, width=500)
        self.mainPanel = Canvas(self.left_frame, cursor='tcross')
        self.mainPanel.config(width=400, height=400)
        self.mainPanel.pack()
        self.savedInfo = tk.Label(self.left_frame, bg='yellow', width=50, text='empty')
        self.savedInfo.pack()
        # self.mainPanel.grid(row=0, column=0, rowspan=30, sticky=W + N)
        self.top_frame = Frame(self.parent)
        self.top_frame.place(x=520, y=10, height=300, width=600)

        self.bot_frame = Frame(self.parent)
        self.bot_frame.place(x=520, y=320,height=300, width=600)




        # main button
        button_row = 0
        self.bt_save = tk.Button(self.top_frame,
                                 text="Save",
                                 width=15, height=2,
                                 command=self.hit_save
                                 )
        self.bt_save.grid(row=button_row, column=0, sticky=W + N)

        self.bt_prev = tk.Button(self.top_frame,
                                 text="Prev",
                                 width=15, height=2,
                                 command=self.hit_prev
                                 )
        self.bt_prev.grid(row=button_row, column=1, sticky=W + N)

        self.bt_next = tk.Button(self.top_frame,
                                 text="Next",
                                 width=15, height=2,
                                 command=self.hit_next
                                 )
        self.bt_next.grid(row=button_row, column=2, sticky=W + N)

        # clsnames
        self._labelVar = tk.StringVar()
        self.l1Clsnames,self.l2Clsnames = self.initClsnames()
        self.l1Radios,self.rowcnt = self.place_radio(self.l1Clsnames.keys(), self.top_frame,
                                                     func_withArg = self.select_l1_cls,
                                                     firstrow=1)
        self.l2Radios = []

        # labelInfo
        row_label = self.rowcnt+2

        self.labelInfo = tk.Label(self.top_frame, bg='green', width=25, text='empty',font = "Verdana 20")
        self.labelInfo.grid(row=row_label, column=0,columnspan=10, sticky=W + N)

        ##
        self.entry1 = tk.Label(self.top_frame, bg='white', width=20, text='')
        self.entry1.grid(row=self.rowcnt + 1, column=0,columnspan=10, sticky=W + N)
        self.entry2 = tk.Label(self.top_frame, bg='white', width=20, text='')
        self.entry2.grid(row=self.rowcnt + 3, column=0,columnspan=10, sticky=W + N)
        #
        self.activeI = 0
        self.activeEntry = self.entry1
        self.activeRadios = self.l1Radios
        self.activeClsnames = list(self.l1Clsnames.keys())
        #
        self.loadImg()

    def reset_state(self):
        self.activeI = 0
        self.activeEntry = self.entry1
        self.activeRadios = self.l1Radios
        self.activeClsnames = list(self.l1Clsnames.keys())

        self.labelInfo.config(text="")
        self.entry1.config(text="")
        self.entry2.config(text="")

        self.tryDelRadio(self.l2Radios)
    def press_BackSpace(self,event =None):
        txt = self.activeEntry["text"][:-1]
        self.activeEntry.config(text=txt)
        self.showlist(txt)
        #
        # if len(txt)==0:
        #     labelinfo = ""
        # else:
        #     labelinfo = self.activeClsnames[int(txt)]
        #
        # self.labelInfo.config(text=labelinfo)
        # self._labelVar.set(labelinfo)

    def showlist(self, stringNum):
        if len(stringNum)>2:
            l1clsId = int(stringNum[:2])
            l2clsId = int(stringNum[2:])
            labelinfo = self.activeClsnames[l2clsId]
            self.labelInfo.config(text=labelinfo)
            self._labelVar.set(labelinfo)
        else:
            self.tryDelRadio(self.l2Radios)

            if len(stringNum) == 0:
                labelinfo = ""
                self.activeClsnames = None
                self.labelInfo.config(text=labelinfo)
                self._labelVar.set(labelinfo)

            else:
                l1clsId = int(stringNum)
                labelinfo = list(self.l1Clsnames.keys())[l1clsId]

                self.labelInfo.config(text=labelinfo)
                self._labelVar.set(labelinfo)
                self.activeClsnames = self.l1Clsnames[labelinfo]

                self.l2Radios, _ = self.place_radio(self.activeClsnames, self.bot_frame,
                                                    func_withArg=self.updateLabelInfo,
                                                    firstrow=0, everyn=3)





    def qxin_prees_num_clsLabel(self,a):
        # import ipdb
        # ipdb.set_trace()
        txt = "{}{}".format(self.activeEntry["text"],a)
        self.activeEntry.config(text = txt)
        self.showlist(txt)

    #
    # def qxin_prees_num_clsLabel(self,a):
    #     # import ipdb
    #     # ipdb.set_trace()
    #     txt = "{}{}".format(self.activeEntry["text"],a)
    #     self.activeEntry.config(text = txt)
    #
    #     labelinfo = self.activeClsnames[int(txt)]
    #     self.labelInfo.config(text=labelinfo)
    #     self._labelVar.set(labelinfo)
    #
    #     print("Pressed, {}, {}".format(txt,self.activeClsnames[int(txt)]))
    #     sys.stdout.flush()

    def press_save(self, event = None):
        self.hit_save()


    def press_clear(self,event = None):
        self.activeEntry.config(text="")

    def press_space(self,event=None):
        self.activeI = (self.activeI + 1) % 2
        self.activeEntry.config(text="")

        if self.activeI == 0:
            self.activeEntry = self.entry1
            self.activeRadios = self.l1Radios
            self.activeClsnames = list(self.l1Clsnames.keys())
            self.tryDelRadio(self.l2Radios)
        else:
            # self.select_l1_cls()
            self.tryDelRadio(self.l2Radios)
            txt = self.labelInfo['text']
            if txt in self.l1Clsnames:
                self.activeClsnames = self.l1Clsnames[txt]
                self.l2Radios, _ = self.place_radio(self.activeClsnames, self.bot_frame,
                                                    func_withArg=self.updateLabelInfo,
                                                    firstrow=0, everyn=3)

    def select_l1_cls(self,event=None):

        self.tryDelRadio(self.l2Radios)
        # txt = self.labelInfo['text']
        txt = self.updateLabelInfo()
        if txt in self.l1Clsnames:
            self.activeClsnames = self.l1Clsnames[txt]
            self.l2Radios, _ = self.place_radio(self.activeClsnames,self.bot_frame,
                                                 func_withArg= self.updateLabelInfo,
                                                 firstrow = 0,everyn=3)


    def press_return(self,x):
        # self.updateLabelInfo()
        self.hit_save()
        self.hit_next()

    def hit_next(self,event = None):
        self.cnt += 1
        self.press_clear()
        self.loadImg()


    def hit_prev(self,event = None):
        self.cnt -= 1
        self.loadImg()

    def place_radio(self, keys, frame, func_withArg = None, firstrow=0, firstcol=0, everyn=5):
        radios = []
        nextcol = firstcol
        for i,x in enumerate(keys):
            radio = tk.Radiobutton(frame, text="{:02d}:".format(i) + x,
                                   variable=self._labelVar, value=x,
                                   command=lambda a=x: func_withArg(a))
            radios.append(radio)
            # radio.pack()
            radio.grid(row=firstrow, column=nextcol, sticky=W + N)
            nextcol += 1
            if (i+1) % everyn == 0:
                firstrow += 1
                nextcol = firstcol
        return radios,firstrow

    def loadlabel(self):
        txt = "None"
        if os.path.exists(self.imagePath+".txt"):
            with open(self.imagePath+".txt") as f:
                for line in f:
                    txt = line
                    break
        self.savedInfo.config(text="{}/{},{}".format(self.cnt,len(self.imgpaths),txt))


    def loadImg(self):
        self.imagePath = self.imgpaths[self.cnt]
        maxLen = 400.
        with open(self.imagePath,'rb') as qxin_fp:
            self.img = Image.open(qxin_fp)
            self.img.load()
        scale = maxLen / max(self.img.size)
        self.img = self.img.resize([int(scale * s) for s in self.img.size])
        # self.img = self.img.resize((400,400))
        w,h = self.img.size
        x1,y1 = int((maxLen-w)/2.),int((maxLen-h)/2.)
        self.tkImg = ImageTk.PhotoImage(self.img)
        self.mainPanel.create_image(x1, y1, image=self.tkImg, anchor=NW)

        #
        self.loadlabel()
        self.reset_state()

        labelinfo = list(self.l1Clsnames.keys())[0]
        self.labelInfo.config(text=labelinfo)
        self._labelVar.set(labelinfo)

    def initClsnames(self):
        clsnamefile = "D:/d1024/cls5names.chs.txt"
        l1_clsnames = OrderedDict()
        l2_clsnames = OrderedDict()

        with open(clsnamefile) as f:
            for line in f:
                cn,en = line.strip().split("\t")
                supercls = cn[:cn.index("_")]
                if supercls not in l1_clsnames:
                    l1_clsnames[supercls] = [cn]
                else:
                    l1_clsnames[supercls].append(cn)

                l2_clsnames[cn] = en

        return l1_clsnames,l2_clsnames
    def tryDelRadio(self,radios):
        if len(radios) > 0:
            for x in radios:
                x.destroy()
            radios.clear()




    def updateLabelInfo(self,event=None):
        txt = self._labelVar.get()
        self.labelInfo.config(text=txt)
        # txt = self.labelInfo['text']
        return txt

    def hit_save(self,event=None):
        txt = self.labelInfo['text']
        # if txt == "对":
        #     self.totals[self.imagePath] = 1
        # else:
        #     self.totals[self.imagePath] = 0
        # totals = 0
        # rights = 0
        # for k,v in self.totals.items():
        #     if v == -1:
        #         continue
        #     totals += 1
        #     if v == 1:
        #         rights += 1
        #
        # print("Total: {},Right: {},ACC: {}".format(totals,rights,float(rights)/totals))

        if len(txt) > 0:
            with open(self.imagePath+".txt",'w') as f:
                f.write(txt)
            print("Saved: " + txt)
        else:
            print("Not Change.")
        sys.stdout.flush()

        self.loadlabel()


import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument('-d', type=str, default='cfg/coco.data', help='img dir path')
parser.add_argument('-i', type=int, default=0, help='from img')
opt = parser.parse_args()
print(opt)
if __name__ == '__main__':
    # imgpaths = np.random.permutation(sorted(glob.glob(opt.d+"/*.jpg")))

    imgpaths = [x for x in sorted(glob.glob(opt.d + "/*.jpg")) if not os.path.exists(x+".txt")]

    root = Tk()
    tool = LabelTool(root,imgpaths,opt.i)
    # tool.loadDir(dbg=False,in_imgdir=opt.d,in_cur=opt.i)
    # root.resizable(width=True, height=True)
    root.mainloop()