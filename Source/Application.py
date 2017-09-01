# -*- coding: utf-8 -*-

"""
==============================================================================
GUI for Xml Report File merging for BMW ACSM5 Project
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: BMW ACSM5 $
$Source: Application.py
$Revision: 1.3 $
$Author: David Szurovecz $
$Date: 2017/07/14 16:20:32CEST $
============================================================================
"""
from lxml import etree
from easygui import fileopenbox, diropenbox
from LogHandler import Logger
from PIL import Image, ImageTk
import Tkinter as tk
import ttk as ttk
import tkMessageBox
import sys
import threading
import subprocess as sp
from Report_Parser import Parser


class MainApplication(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        '''INIT Objects'''
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = tk.Frame(parent)
        self.parent.pack()
        root.title('TestList Creator')
        self.resetInputs()
        self.initUI()

    def resetInputs(self):
        self.file_one = u''
        self.file_two = u''
        self.save_list = u''
        try:
            self.openreport_var.set(False)
        except AttributeError:
            pass

    def initUI(self):
        #=======================================================================
        # Create Container For MainFrame
        #=======================================================================
        self.hintone = tk.LabelFrame(self.parent, text=" 1. Enter File Details: ")
        self.hintone.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        #=======================================================================
        # Create Container For Settings
        #=======================================================================
        self.hintsettings = tk.LabelFrame(self.parent, text=" 2. Settings: ")
        self.hintsettings.grid(row=3, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        #=======================================================================
        # Create Container for Picture
        #=======================================================================
        self.hintpic = tk.LabelFrame(self.parent, bd=0)
        self.hintpic.grid(row=3, columnspan=7, sticky='E', padx=5, pady=5, ipadx=5, ipady=5)
        #=======================================================================
        # Create Buttons
        #=======================================================================
        self.ok_button = tk.Button(self.parent, text="OK", command=self.OKButton)
        self.ok_button.grid(row=4, column=0, sticky='W' + 'E', padx=5, pady=5, ipadx=1, ipady=1)
        self.exit_button = tk.Button(self.parent, text="Exit", command=self.cancelbutton)
        self.exit_button.grid(row=4, column=1, sticky='W', padx=5, pady=5, ipadx=30, ipady=1)
        browseBtnone = tk.Button(self.hintone, text="Browse ...", command=self.browseFirst)
        browseBtnone.grid(row=0, column=8, sticky='W', padx=5, pady=2)
        browseBtntwo = tk.Button(self.hintone, text="Browse ...", command=self.browseSecond)
        browseBtntwo.grid(row=1, column=8, sticky='W', padx=5, pady=2)
        browseBtnthree = tk.Button(self.hintone, text="Browse ...", command=self.savebutton)
        browseBtnthree.grid(row=2, column=8, sticky='W', padx=5, pady=2)
        self.openreport_var = tk.BooleanVar()
        checkopnrep = tk.Checkbutton(
            self.hintsettings,
            text="Open Log After Process Finished",
            variable=self.openreport_var)
        checkopnrep.grid(row=5)
        #=======================================================================
        # Draw the Labels
        #=======================================================================
        labelone = tk.Label(self.hintone, text="Select the Main Report File: ")
        labelone.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        labeltwo = tk.Label(self.hintone, text="Select the Empty Tetlist: ")
        labeltwo.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        labelthree = tk.Label(self.hintone, text="Select the Output Path: ")
        labelthree.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        #=======================================================================
        # File Selection Entry
        #=======================================================================
        self.labelent_one = tk.Entry(self.hintone)
        self.labelent_one.grid(row=0, column=1, columnspan=7, sticky="W", pady=3)
        self.labelent_two = tk.Entry(self.hintone)
        self.labelent_two.grid(row=1, column=1, columnspan=7, sticky="WE", pady=2)
        self.labelent_three = tk.Entry(self.hintone)
        self.labelent_three.grid(row=2, column=1, columnspan=7, sticky="WE", pady=2)
        self.image('logo.jpg')
        self.get_centercoordinate(root)
        root.attributes('-alpha', 1.0)

    def browseFirst(self):
        '''Select the files to Edit'''
        current_entry = self.labelent_one
        self.file_one = fileopenbox(filetypes=['*.xml'])
        if self.file_one.encode('utf-8') == '.':
            pass
        elif self.file_one:
            current_entry.insert(0, str(self.file_one.encode('utf-8')))

    def browseSecond(self):
        '''Select the files to Edit'''
        current_entry = self.labelent_two
        self.file_two = fileopenbox(filetypes=['*.xml'])
        if self.file_two.encode('utf-8') == '.':
            pass
        elif self.file_two:
            current_entry.insert(0, str(self.file_two.encode('utf-8')))

    def savebutton(self):
        '''Select the files save path'''
        current_entry = self.labelent_three
        self.save_list = diropenbox()
        if self.save_list:
            current_entry.insert(0, self.save_list.encode('utf-8') + '\Example.tl')

    def OKButton(self):
        '''Input Verification and start the process'''
        self.get_inputs()
        if self.file_one and self.file_two and self.save_list:
            self.t1 = threading.Thread(target=self.parse, name='controller')
            self.t1.start()
            self.disablebuttons()
            self.progress()
        elif not self.file_one or self.file_two or self.save_list:
            self.errormessage()
        elif not self.t1.is_alive():
            self.pb.stop()
            self.pbar.destroy()
            self.enablebuttons()

    def queue_event(self, message):
        '''This is a thread handler what checks that worker thread is alive'''
        if self.t1.is_alive():
            self.master.after(100, self.queue_event, message)
        elif message == 'Parsing error':
            tkMessageBox.showinfo(
                'Error',
                'Unable to Parse Data.')
            self.pb.stop()
            self.pbar.destroy()
            self.enablebuttons()
        elif message == 'Success':
            self.pb.stop()
            self.pbar.destroy()
            self.enablebuttons()
            tkMessageBox.showinfo(
                'Finished',
                'Process has been finished. See Log File in the Log directory.')
            openlog = Logger.Logger.logging(self.listofFailed, self.file_one)
            if self.openreport_var.get():
                sp.Popen(["notepad.exe", openlog])

    def cancelbutton(self):
        sys.exit()

    def errormessage(self):
        '''Show an Error window'''
        tkMessageBox.showinfo("Error", "Missing Data")

    def parserrormessage(self):
        tkMessageBox.showinfo("Error", "Unable to Parse Data. Not a valid Input Files")

    def parse(self):
        self.source = etree.parse(self.file_one)
        self.source_root = self.source.getroot()
        self.destination = etree.parse(self.file_two)
        Parser.XmlParser(self.source).get_failedtestnames()
        self.listofFailed = Parser.XmlParser.XML_ATTRS['failed']
        self.output = self.save_list
        Parser.ListCreator().testlist_creator(self.listofFailed, self.output, self.destination)
        self.queue_event('Success')

    def progress(self):
        self.pbar = tk.Tk()
        self.pbar.overrideredirect(1)
        self.pbar.title('Processing')
        self.pb = ttk.Progressbar(
            self.pbar,
            orient="horizontal",
            length=210,
            mode="indeterminate")
        self.pb.place(relx=.5, rely=.5, anchor="c")
        self.pb.pack()
        self.get_centercoordinate(self.pbar)
        self.pb.start()

    def disablebuttons(self):
        self.ok_button.config(state='disabled')

    def enablebuttons(self):
        self.ok_button.config(state='normal')

    def image(self, nameofpic):
        image = Image.open(nameofpic)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.hintpic, image=photo)
        label.image = photo
        label.grid()

    def get_inputs(self):
        self.file_one = self.labelent_one.get()
        self.file_two = self.labelent_two.get()
        self.save_list = self.labelent_three.get()

    def get_centercoordinate(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()


if __name__ == "__main__":

    root = tk.Tk()
    root.attributes('-alpha', 0.0)  # Transparent GUI until Initialization
    root.iconbitmap(r'.\Icon.ico')
    run = MainApplication(root)
    root.mainloop()
