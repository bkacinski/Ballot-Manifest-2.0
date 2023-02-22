import sys
import pandas as pd
from Data.manifest_form import *
from Data import settings_popup
from PyQt5 import QtWidgets
import json

with open('settings.json', 'r') as f:
    settings = json.load(f)
    county_name = settings["County Name"]
    batches_per_container = settings["Batches Per Container"]
    column_names = settings["Column Names"]
    file_name = settings["File Name"]


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        pd.options.display.float_format = '{:,.0f}'.format
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.pop_up = SettingsPopup()

        # Button Functions
        self.submit_form_button.clicked.connect(self.submit_form)
        self.submit_form_button.setAutoDefault(True)
        self.submit_label_button.clicked.connect(self.submit_label)
        self.action_open.triggered.connect(self.open_file)
        self.action_new.triggered.connect(self.create_from_template)
        self.actionOptions.triggered.connect(self.options_window)

        # Class Variables
        self.df = None
        self.filename = file_name
        if self.filename == '':
            self.file_loaded = False
        else:
            self.file_loaded = True
        self.batch_loaded = False
        self.batch_labels = []
        self.batch_entries = []
        self.container_info = []
        self.current_location = 1
        self.container_label = QtWidgets.QLabel('')
        self.form_frame.addWidget(self.container_label, 2, 4)
        self.scanner_label = QtWidgets.QLabel('')
        self.form_frame.addWidget(self.scanner_label, 1, 4)
        if self.file_loaded:
            self.load_file()
        else:
            self.populate_batches()

    # Populate batch numbers on screen dynamically
    def populate_batches(self, start=1, scanner='', container=''):
        for widget in self.batch_labels + self.batch_entries:
            self.form_frame.removeWidget(widget)
            widget.deleteLater()
            widget = None
        self.current_location = start
        self.scanner_label.setText(scanner)
        self.container_label.setText(container)
        self.batch_labels = []
        self.batch_entries = []
        for i in range(start, start + batches_per_container):
            self.batch_labels.append(QtWidgets.QLabel('Batch ' + str(i) + ':'))
            self.batch_entries.append(QtWidgets.QLineEdit(self.centralwidget))
        for index, label in enumerate(self.batch_labels, start=3):
            self.form_frame.addWidget(label, index, 3)
        for index, line_edit in enumerate(self.batch_entries, start=3):
            self.form_frame.addWidget(line_edit, index, 4)
            if index != len(self.batch_entries) + 2:
                line_edit.returnPressed.connect(self.batch_entries[index - 2].setFocus)
            else:
                line_edit.returnPressed.connect(self.submit_form_button.setFocus)
        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.form_frame.addItem(spacer_item, batches_per_container + 3, 4)
        self.set_disable_form()

    def submit_form(self):
        # Check if any fields between first and last are blank
        entries = [entry.text() for entry in self.batch_entries] 

        def check_valid(iterable):
            last_value = 0
            for index, value in enumerate(reversed(iterable)):
                if value != "":
                    last_value = -index + -1
                    break

            # Check for contiguous value error
            for value in iterable[:last_value]:
                if value == "":
                    return False
            else:
                for value in iterable[:last_value + 1]:
                    try:
                        number_checker = int(value)
                    except ValueError:
                        return False
                else:
                    return True

        valid_form = check_valid(entries)

        if valid_form:
            new_data = pd.DataFrame(columns=column_names)
            new_data[column_names[0]] = [county_name for i in range(batches_per_container)]
            new_data[column_names[1]] = [self.container_info[0] for i in range(batches_per_container)]
            new_data[column_names[2]] = [self.container_info[1] + i for i in range(batches_per_container)]
            new_data[column_names[3]] = [entry.text() for entry in self.batch_entries]
            new_data[column_names[4]] = [self.container_info[2] for i in range(batches_per_container)]
            mask = new_data[column_names[3]] != ''
            new_data = new_data[mask]
            new_data.set_index(keys=column_names[:3], inplace=True)
            self.df = self.df.append(new_data)
            self.df.sort_index(inplace=True)
            self.df.to_csv(self.filename)
            self.toggle_batch_loaded()
            self.populate_batches()
            self.label_line_edit.setFocus()
        else:
            # print("Invalid Form")
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Error: All consecutive batches must be filled in. And all values must be numbers")
            error_dialog.exec_()

    def submit_label(self):
        text = self.label_line_edit.text().split('.')
        if len(text) != 3:
            self.populate_batches()
        else:
            scanner = text[0]
            start = int(text[1])
            container = text[2]
            self.container_info = [int(scanner), start, container]
            self.label_line_edit.clear()
            self.toggle_batch_loaded()
            self.populate_batches(start, scanner, container)
            if (county_name, float(scanner), float(start)) in self.df.index:
                mask = self.df[column_names[4]] == container
                ballot_counts = self.df[mask][column_names[3]].tolist()
                for index, line_edit in enumerate(self.batch_entries[:len(ballot_counts)]):
                    line_edit.setText(str(int(ballot_counts[index])))
                for i in range(len(ballot_counts)):
                    try:
                        self.df.drop((county_name, float(scanner), float(start) + i), inplace=True)
                    except KeyError:
                        continue
            self.batch_entries[0].setFocus()

    def toggle_batch_loaded(self):
        self.batch_loaded = not self.batch_loaded

    def set_disable_form(self):
        if self.file_loaded and not self.batch_loaded:
            for line_edit in self.batch_entries:
                line_edit.setDisabled(True)
            self.label_line_edit.setDisabled(False)
            self.submit_label_button.setDisabled(False)
            self.submit_form_button.setDisabled(True)
        elif self.file_loaded is False:
            for line_edit in self.batch_entries:
                line_edit.setDisabled(True)
            self.label_line_edit.setDisabled(True)
            self.submit_label_button.setDisabled(True)
            self.submit_form_button.setDisabled(True)
        elif self.file_loaded and self.batch_loaded:
            for line_edit in self.batch_entries:
                line_edit.setDisabled(False)
            self.label_line_edit.setDisabled(True)
            self.submit_label_button.setDisabled(True)
            self.submit_form_button.setDisabled(False)

    def open_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', 'CSV Files (*.csv)')
        if file[0]:
            self.filename = file[0]
            self.load_file()

    def create_from_template(self):
        directory = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '.', 'CSV Files (*.csv)')
        new_from_template = pd.DataFrame(columns=column_names)
        new_from_template.to_csv(directory[0], index=False)
        self.df = new_from_template.set_index(keys=column_names[:3])
        self.filename = directory[0]
        self.load_file()

    def load_file(self):
        try:
            self.df = pd.read_csv(self.filename, index_col=column_names[:3])
            self.df.sort_index(inplace=True)
            self.file_loaded = True
            self.populate_batches()
        except:
            self.filename = None
            self.file_loaded = False
            self.populate_batches()
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('File Unable to load. Check that file path is correct, or assign a new file')
            error_dialog.exec_()

    def options_window(self):
        self.pop_up.show()


class SettingsPopup(QtWidgets.QWidget, settings_popup.Ui_OptionsDialog):
    def __init__(self):
        super(SettingsPopup, self).__init__()
        self.setupUi(self)

        self.batches_spin_box.setValue(batches_per_container)
        self.file = file_name
        if file_name == '':
            self.file_path_label.setText('No File Selected')
        else:
            self.file_path_label.setText(file_name)
        self.apply_button.clicked.connect(self.change_settings)
        self.default_file_button.clicked.connect(self.select_default_path)
        self.cancel_button.clicked.connect(self.close)

    def select_default_path(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '.', 'CSV Files (*.csv)')
        if file[0]:
            self.file = file[0]
            self.file_path_label.setText(self.file)

    def change_settings(self):
        with open("settings.json", "r") as f:
            new_settings = {
                "County Name": "Arapahoe",
                "Batches Per Container": self.batches_spin_box.value(),
                "File Name": self.file,
                "Column Names": [
                    'County',
                    'Device ID',
                    'Batch',
                    '# of Ballots',
                    'Location',
                ]
            }

        window.filename = self.file
        global batches_per_container
        batches_per_container = self.batches_spin_box.value()
        window.load_file()

        with open("settings.json", "w") as f:
            json.dump(new_settings, f)

        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
