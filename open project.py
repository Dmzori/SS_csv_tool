import tkinter
from tkinter import filedialog
import pandas
from pathlib import Path
import os
#directory mode
#need buttons for directory mode to get the actual directory or somehow otherwise change the text/csv button functionality
#maybe have a check in the button behavior to check if the directory mode is toggled on then react accordingly

class GUI:
    def __init__(self):
        self.mainWin = tkinter.Tk()
        self.mainWin.title('text tool')

        #frames
        #txt file frame will take target strings and file address
        self.text_Frame = tkinter.Frame(self.mainWin)


        #button frame
        self.butt_Frame = tkinter.Frame(self.mainWin)


        #stringvars
        self.textDir_Str = tkinter.StringVar()
        self.csvDir_Str = tkinter.StringVar()
        self.targetTxt_Str = tkinter.StringVar()
        self.csvWrite_Str = tkinter.StringVar()
        self.csvCol_Str = tkinter.StringVar()

        #intvars
        self.cBox_Var1 = tkinter.IntVar()
        self.cBox_Var1.set(0)
        
        #checkbutton
        self.cb1 = tkinter.Checkbutton(self.text_Frame, text = 'directory mode', variable = self.cBox_Var1)

        #labels
        self.textDir_Label = tkinter.Label(self.text_Frame, text = 'Text File Directory', font = ('calibre',10,'normal'))
        self.csvDir_Label = tkinter.Label(self.text_Frame, text = 'CSV File Directory', font = ('calibre',10,'normal'))
        self.targetTxt_Label = tkinter.Label(self.text_Frame, text = 'Target Text String', font = ('calibre',10,'normal'))
        self.csvWrite_Label = tkinter.Label(self.text_Frame, text = 'CSV Write String', font = ('calibre',10,'normal'))
        self.csvCol_Label = tkinter.Label(self.text_Frame, text = 'CSV Column String', font = ('calibre', 10, 'normal'))
        

        #Entries
        self.textDir_Entry = tkinter.Entry(self.text_Frame, textvariable = self.textDir_Str, font = ('calibre',10,'normal'))
        self.csvDir_Entry = tkinter.Entry(self.text_Frame, textvariable = self.csvDir_Str, font = ('calibre',10,'normal'))
        self.targetTxt_Entry = tkinter.Entry(self.text_Frame, textvariable = self.targetTxt_Str, font = ('calibre',10,'normal'))
        self.csvWrite_Entry = tkinter.Entry(self.text_Frame, textvariable = self.csvWrite_Str, font = ('calibre',10,'normal'))
        self.csvCol_Entry = tkinter.Entry(self.text_Frame, textvariable = self.csvCol_Str, font = ('calibre' ,10, 'normal'))

        #pack labels
        self.textDir_Label.grid(row = 1, column = 1)
        self.csvDir_Label.grid(row = 2, column = 1)
        self.targetTxt_Label.grid(row = 3, column = 1)
        self.csvWrite_Label.grid(row = 4, column = 1)
        self.csvCol_Label.grid(row = 5, column = 1)

        #pack cbuttons
        self.cb1.grid(row = 6, column = 1)

        #pack entries
        self.textDir_Entry.grid(row = 1, column = 2)
        self.csvDir_Entry.grid(row = 2, column = 2)
        self.targetTxt_Entry.grid(row = 3, column = 2)
        self.csvWrite_Entry.grid(row = 4, column = 2)
        self.csvCol_Entry.grid(row = 5, column = 2)

        #buttons
        self.quit_Butt = tkinter.Button(self.butt_Frame, text = 'quit', command=self.mainWin.destroy)
        self.run_Butt = tkinter.Button(self.butt_Frame, text = 'run', command =self.run)
        self.textPath_Butt = tkinter.Button(self.text_Frame, text = 'text',  command =self.getTextPath)
        self.csvPath_Butt = tkinter.Button(self.text_Frame, text = 'csv', command =self.getCsvPath)

        #pack buttons
        self.quit_Butt.pack(side = tkinter.RIGHT)
        self.run_Butt.pack(side = tkinter.LEFT)
        self.textPath_Butt.grid(row = 1, column = 3)
        self.csvPath_Butt.grid(row = 2, column = 3)
        
        #pack frames
        self.text_Frame.pack()
        self.butt_Frame.pack()


        tkinter.mainloop()

        
    def getTextPath(self):
        path = tkinter.filedialog.askopenfilename()
        self.textDir_Str.set(path)
        

    def getCsvPath(self):
        path = tkinter.filedialog.askopenfilename()
        self.csvDir_Str.set(path)
    
    def run(self):
        self.textDir = self.textDir_Entry.get()
        self.csvDir = self.csvDir_Entry.get()
        self.targetTxt = self.targetTxt_Entry.get()
        self.csvWrite = self.csvWrite_Entry.get()
        self.csvCol = self.csvCol_Entry.get()
        self.csvRow = Path(self.textDir).stem
        if self.cBox_Var1.get() == 1:
            for file in Path(self.textDir).rglob('*.txt'):
                self.textFile = open(file, 'r')
                self.contents = self.textFile.read()
                self.textFile.close()
                self.df = pandas.read_csv(self.csvDir, index_col = [0])
                if 'FRIGATE' in self.contents:
                    #need to figure out how to get the col and row of the ship
                    self.df.loc[self.df['id']==Path(file).stem ,'supplies/mo'] = '1' 
                    self.df.to_csv(self.csvDir)
                if 'DESTROYER' in self.contents:
                    self.df.loc[self.df['id']==Path(file).stem ,'supplies/mo'] = '3' 
                    self.df.to_csv(self.csvDir)
                if 'CRUISER' in self.contents:
                    self.df.loc[self.df['id']==Path(file).stem ,'supplies/mo'] = '5' 
                    self.df.to_csv(self.csvDir)
                if 'CAPITAL_SHIP' in self.contents:
                    self.df.loc[self.df['id']==Path(file).stem ,'supplies/mo'] = '10' 
                    self.df.to_csv(self.csvDir)
            

        if self.cBox_Var1.get() == 0:
            self.textFile = open(self.textDir, 'r')
            self.contents = self.textFile.read()
            self.textFile.close()
            self.df = pandas.read_csv(self.csvDir, index_col = [0])   
            if self.targetTxt in self.contents: 
                self.df.loc[self.df['id']==self.csvRow ,self.csvCol] = self.csvWrite
                self.df.to_csv(self.csvDir)
                tkinter.messagebox.showinfo('it worked', message = 'write successful')
            else:
                tkinter.messagebox.showinfo('it failed', message = 'write failed')





if __name__ == '__main__':
    gui = GUI()
