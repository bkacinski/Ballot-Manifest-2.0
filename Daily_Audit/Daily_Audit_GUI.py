import pandas as pd
import warnings
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from Daily_Audit.settings import *

warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)


class AuditGUI:
    def __init__(self, master):
        # Establish base GUI settings.
        self.master = master
        self.master.title('Daily Audit')
        self.master.resizable(False, False)
        self.master.geometry('700x600+50+25')

        # Establish frame header settings.
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        self.title_text = ttk.Label(self.frame_header, font=('Arial', 18, 'bold'), wraplength=400,
                                    text='Daily Audit').grid(row=1, column=1, padx=25)

        # Establish load file settings.
        self.frame_load = ttk.Frame(master)
        self.cvr_file = None
        self.cvr_prompt = ttk.Label(self.frame_load, text='Select CVR File').grid(row=0, column=0,
                                                                                  columnspan=2, sticky='w')
        self.cvr_entry = ttk.Entry(self.frame_load, width=60)
        self.cvr_select_button = ttk.Button(self.frame_load, text='Select CVR',
                                            command=lambda: self.locate_file(self.cvr_entry, '.json'))
        self.manifest_file = None
        self.manifest_prompt = ttk.Label(self.frame_load, text='Select Manifest File').grid(row=3, column=0,
                                                                                            columnspan=2, sticky='w')
        self.manifest_entry = ttk.Entry(self.frame_load, width=60)
        self.manifest_select_button = ttk.Button(self.frame_load, text='Select Manifest',
                                                 command=lambda: self.locate_file(self.manifest_entry, '.csv'))
        self.load_button = ttk.Button(self.frame_load, text='Load Files', command=lambda: self.load_files())

        # Establish display difference settings.
        self.frame_table = ttk.Frame(master)
        self.cvr_table_label = ttk.Label(self.frame_table, text='CVR: ')
        self.manifest_table_label = ttk.Label(self.frame_table, text='Manifest: ')
        self.cvr_textbox = ScrolledText(self.frame_table, height=25, width=35, wrap='word')
        self.manifest_textbox = ScrolledText(self.frame_table, height=25, width=35, wrap='word')

        # Establish Menu Bar Settings
        self.master.option_add('*tearOff', False)
        self.menu_bar = Menu(master)
        self.master.config(menu=self.menu_bar)
        self.file = Menu(self.menu_bar)
        self.help_ = Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.file, label='File')
        self.menu_bar.add_cascade(menu=self.help_, label='Help')
        self.file.add_command(label='This is a label', command=lambda: print('there is a button here'))
        self.help_.add_command(label='How to use this software', command=lambda: print('how to use'))
        self.help_.add_command(label='About', command=lambda: print('About'))

        # Establish Pandas DataFrame Variables
        self.cvr = None
        self.manifest = None

        # Render Load View
        self.load_view()

    # Methods to render the Various Views
    def clear_view(self):
        self.frame_load.pack_forget()
        self.frame_table.pack_forget()

    def load_view(self):
        self.clear_view()
        self.cvr = None
        self.manifest = None
        self.frame_load.pack()
        self.cvr_entry.grid(row=1, column=0, columnspan=4, sticky='w', pady=5)
        self.cvr_entry.config(state='normal')
        self.cvr_entry.delete(0, END)
        self.cvr_entry.config(state='disabled')
        self.cvr_select_button.grid(row=2, column=0, sticky='w', pady=10)
        self.manifest_entry.grid(row=4, column=0, columnspan=4, sticky='w', pady=5)
        self.manifest_entry.config(state='normal')
        self.manifest_entry.delete(0, END)
        self.manifest_entry.config(state='disabled')
        self.manifest_select_button.grid(row=5, column=0, sticky='w', pady=10)
        self.load_button.grid(row=5, column=1)

    def table_view(self):
        self.clear_view()
        self.frame_table.pack()
        self.cvr_table_label.grid(row=0, column=0)
        self.manifest_table_label.grid(row=0, column=1)
        self.cvr_textbox.grid(row=1, column=0)
        self.manifest_textbox.grid(row=1, column=1)

    # Class Methods
    def locate_file(self, widget, ext):
        filename = filedialog.askopenfile()
        if filename is not None and filename.name[-len(ext):] == ext:
            filename = filename.name
            widget.config(state='normal')
            widget.insert(0, filename)
            widget.config(state='disabled')
        else:
            messagebox.showerror(title='Audit - Error', message='Please select a %s file' % ext)

    def load_files(self):
        # Establish Progressbar Settings
        popup = Toplevel(self.master)
        popup.title("Loading Files...")
        progress_bar = ttk.Progressbar(popup, orient='horizontal', length=200, mode='determinate')
        progress_bar.grid(column=0, row=0)
        progress_bar['value'] = 0

        self.manifest = pd.read_csv(self.manifest_entry.get())
        self.cvr = pd.read_json(self.cvr_entry.get())

        # set CVR
        self.cvr['Sessions'].to_dict()
        temp = pd.DataFrame(columns=['TabulatorId', 'BatchId'])
        progress_bar['maximum'] = len(self.cvr)
        for (i, r) in self.cvr.iterrows():
            progress_bar['value'] += 1
            progress_bar.update()
            row = r['Sessions']
            temp.loc[i] = [row['TabulatorId'], row['BatchId']]
        if progress_bar['value'] == progress_bar['maximum']:
            popup.destroy()

        self.cvr = temp

        temp = pd.DataFrame(columns=[COLUMN_NAMES['SCANNER_COL'], COLUMN_NAMES['BATCH_COL'], COLUMN_NAMES['COUNT_COL']])
        temp.set_index(keys=[COLUMN_NAMES['SCANNER_COL'], COLUMN_NAMES['BATCH_COL']], inplace=True)

        for scanner in self.cvr['TabulatorId'].value_counts().index:
            mask1 = self.cvr['TabulatorId'] == scanner
            for value in self.cvr[mask1]['BatchId'].unique():
                mask2 = self.cvr['BatchId'] == value
                count = len(self.cvr[mask1 & mask2])
                temp.loc[(scanner, value), COLUMN_NAMES['COUNT_COL']] = count

        temp.sort_index(inplace=True)
        temp[COLUMN_NAMES['COUNT_COL']] = temp[COLUMN_NAMES['COUNT_COL']].astype('int')

        self.cvr = temp

        # Set Manifest
        self.manifest.set_index(keys=[COLUMN_NAMES['SCANNER_COL'], COLUMN_NAMES['BATCH_COL']], inplace=True)
        for column in list(self.manifest.columns.values):
            if column != COLUMN_NAMES['COUNT_COL']:
                del self.manifest[column]
        self.manifest.fillna(0, inplace=True)
        self.manifest[COLUMN_NAMES['COUNT_COL']] = self.manifest[COLUMN_NAMES['COUNT_COL']].astype('int')

        # Do analysis
        if self.cvr.equals(self.manifest):
            self.cvr_textbox.insert(1.0, 'The CVR and Manifest Match')
            self.cvr_textbox.config(state='disabled')
            self.manifest_textbox.insert(1.0, 'The CVR and the Manifest Match')
            self.manifest_textbox.config(state='disabled')
        else:
            # Fill missing rows
            missing = self.cvr[~self.cvr.index.isin(self.manifest.index)]
            missing[COLUMN_NAMES['COUNT_COL']] = 0
            frames = [self.manifest, missing]
            result = pd.concat(frames)
            result.sort_index(inplace=True)
            self.manifest = result
            missing = self.manifest[~self.manifest.index.isin(self.cvr.index)]
            missing[COLUMN_NAMES['COUNT_COL']] = 0
            frames = [self.cvr, missing]
            result = pd.concat(frames)
            result.sort_index(inplace=True)
            self.cvr = result

            # find differences
            sum_cvr = self.cvr[COLUMN_NAMES['COUNT_COL']].sum()
            sum_manifest = self.manifest[COLUMN_NAMES['COUNT_COL']].sum()
            differences = (self.cvr != self.manifest).any(1)
            self.cvr_textbox.insert(1.0, 'Total: ' + str(sum_cvr) + '\n\n')
            self.cvr_textbox.insert(END, self.cvr[differences])
            self.cvr_textbox.config(state='disabled')
            self.manifest_textbox.insert(1.0, 'Total: ' + str(sum_manifest) + '\n\n')
            self.manifest_textbox.insert(END, self.manifest[differences])
            self.manifest_textbox.config(state='disabled')

            self.table_view()


def main():
    root = Tk()
    AuditGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
