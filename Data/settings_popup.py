# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_OptionsDialog(object):
    def setupUi(self, OptionsDialog):
        OptionsDialog.setObjectName("OptionsDialog")
        OptionsDialog.resize(320, 240)
        self.gridLayout = QtWidgets.QGridLayout(OptionsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.cancel_button = QtWidgets.QPushButton(OptionsDialog)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 4, 1, 1, 1)
        self.apply_button = QtWidgets.QPushButton(OptionsDialog)
        self.apply_button.setObjectName("apply_button")
        self.gridLayout.addWidget(self.apply_button, 4, 0, 1, 1)
        self.batches_spin_box = QtWidgets.QSpinBox(OptionsDialog)
        self.batches_spin_box.setObjectName("batches_spin_box")
        self.gridLayout.addWidget(self.batches_spin_box, 0, 1, 1, 1)
        self.default_file_button = QtWidgets.QPushButton(OptionsDialog)
        self.default_file_button.setObjectName("default_file_button")
        self.gridLayout.addWidget(self.default_file_button, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.manifest_location_label = QtWidgets.QLabel(OptionsDialog)
        self.manifest_location_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.manifest_location_label.setObjectName("manifest_location_label")
        self.gridLayout.addWidget(self.manifest_location_label, 1, 0, 1, 1)
        self.batch_number_label = QtWidgets.QLabel(OptionsDialog)
        self.batch_number_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.batch_number_label.setObjectName("batch_number_label")
        self.gridLayout.addWidget(self.batch_number_label, 0, 0, 1, 1)
        self.file_path_label = QtWidgets.QLabel(OptionsDialog)
        self.file_path_label.setObjectName("file_path_label")
        self.gridLayout.addWidget(self.file_path_label, 2, 0, 1, 1)

        self.retranslateUi(OptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(OptionsDialog)

    def retranslateUi(self, OptionsDialog):
        _translate = QtCore.QCoreApplication.translate
        OptionsDialog.setWindowTitle(_translate("OptionsDialog", "Options"))
        self.cancel_button.setText(_translate("OptionsDialog", "Cancel"))
        self.apply_button.setText(_translate("OptionsDialog", "Apply"))
        self.default_file_button.setText(_translate("OptionsDialog", "Select File"))
        self.manifest_location_label.setText(_translate("OptionsDialog", "Manifest File Location:"))
        self.batch_number_label.setText(_translate("OptionsDialog", "Batches Per Container:"))
        self.file_path_label.setText(_translate("OptionsDialog", "No File Selected"))

