import sys
import json
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from datetime import datetime, time, date
from klients import Klients
from pakalpojums import Pakalpojums


class SpecialaisJSONKodetajs(json.JSONEncoder):
    def default(self, obj):
        return obj.strftime("%d.%m.%Y.") if isinstance(obj, date) else obj.strftime("%H:%M") if \
            isinstance(obj, time) else obj.__dict__


def eksportet(obj, eksporta_datnes_nosaukums):
    try:
        with open(eksporta_datnes_nosaukums, "w", encoding="utf-8") as eksporta_datne:
            json.dump(obj, eksporta_datne, ensure_ascii=False, cls=SpecialaisJSONKodetajs)
        return True
    except OSError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Kļūda")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Neizdevās izveidot datni datu eksportam!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    except Exception:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Kļūda")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Izvades kļūda!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def importet(importa_datnes_nosaukums):
    try:
        with open(importa_datnes_nosaukums, encoding="utf-8") as importa_datne:
            return json.load(importa_datne)
    except OSError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Kļūda")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Neizdevās atvērt datni datu importam!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    except json.decoder.JSONDecodeError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Kļūda")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Datnes satura formāts neatbilst JSON formātam!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    except Exception:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Kļūda")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Ievades kļūda!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    return list()


class KlientsWidget(QWidget):
    def __init__(self, izveletais_klients_index=-1, parent=None):
        super(KlientsWidget, self).__init__(parent)
        self.klients_index = izveletais_klients_index
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(500, 200)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.klienta_vards_line_edit = QLineEdit()
        self.klienta_uzvards_line_edit = QLineEdit()
        self.klienta_pers_kods_line_edit = QLineEdit()
        self.klienta_pers_kods_line_edit.setInputMask("999999-99999")
        self.klienta_talr_num_line_edit = QLineEdit()
        self.klienta_talr_num_line_edit.setInputMask("+99999999999")
        if self.klients_index == -1:
            self.setWindowTitle("Jaunais klients")
            self.klients_label = QLabel("Jaunais klients")
        else:
            self.setWindowTitle("Klients \"" + klienti[self.klients_index].klienta_vards + " " +
                                klienti[self.klients_index].klienta_uzvards + "\"")
            self.klients_label = QLabel("Klients \"" + klienti[self.klients_index].klienta_vards + " " +
                                        klienti[self.klients_index].klienta_uzvards + "\"")
            self.klienta_vards_line_edit.setText(klienti[self.klients_index].klienta_vards)
            self.klienta_uzvards_line_edit.setText(klienti[self.klients_index].klienta_uzvards)
            self.klienta_pers_kods_line_edit.setText(klienti[self.klients_index].klienta_pers_kods)
            self.klienta_talr_num_line_edit.setText(klienti[self.klients_index].klienta_talr_num)
        self.klients_label.setAlignment(Qt.AlignCenter)
        self.klients_label.setStyleSheet("font: 20px;")
        self.saglabat_klientu_button = QPushButton("Saglabāt")
        self.saglabat_klientu_button.setEnabled(False)
        self.aizvert_klientu_button = QPushButton("Aizvērt")
        self.klients_pogas_layout = QHBoxLayout()
        self.klients_pogas_layout.addWidget(self.saglabat_klientu_button)
        self.klients_pogas_layout.addWidget(self.aizvert_klientu_button)
        self.klients_form_layout = QFormLayout()
        self.klients_form_layout.addRow(self.klients_label)
        self.klients_form_layout.addRow("Vārds:", self.klienta_vards_line_edit)
        self.klients_form_layout.addRow("Uzvārds:", self.klienta_uzvards_line_edit)
        self.klients_form_layout.addRow("Personas kods:", self.klienta_pers_kods_line_edit)
        self.klients_form_layout.addRow("Tālruņa numurs:", self.klienta_talr_num_line_edit)
        self.klients_form_layout.addRow(self.klients_pogas_layout)
        self.setLayout(self.klients_form_layout)
        self.klienta_vards_line_edit.textChanged.connect(lambda: self.saglabat_klientu_button.setEnabled(True))
        self.klienta_uzvards_line_edit.textChanged.connect(lambda: self.saglabat_klientu_button.setEnabled(True))
        self.klienta_pers_kods_line_edit.textChanged.connect(lambda: self.saglabat_klientu_button.setEnabled(True))
        self.klienta_talr_num_line_edit.textChanged.connect(lambda: self.saglabat_klientu_button.setEnabled(True))
        self.saglabat_klientu_button.clicked.connect(self.saglabat_klientu)
        self.aizvert_klientu_button.clicked.connect(self.aizvert_klientu)

    def saglabat_klientu(self):
        if "" not in {self.klienta_vards_line_edit.text(), self.klienta_uzvards_line_edit.text()} and \
                len(self.klienta_pers_kods_line_edit.text()) == 12 and \
                len(self.klienta_talr_num_line_edit.text()) == 12:
            klients_list_widget_item = QListWidgetItem()
            if self.klients_index == -1:
                jaunais_klients = Klients(self.klienta_vards_line_edit.text(), self.klienta_uzvards_line_edit.text(),
                                          self.klienta_pers_kods_line_edit.text(),
                                          self.klienta_talr_num_line_edit.text())
                klienti.append(jaunais_klients)
                klients_list_widget_item.setText(jaunais_klients.klienta_vards + " " + jaunais_klients.klienta_uzvards)
                widget.klientu_saraksts_list_widget.addItem(klients_list_widget_item)
            else:
                klienti[self.klients_index].klienta_vards = self.klienta_vards_line_edit.text()
                klienti[self.klients_index].klienta_uzvards = self.klienta_uzvards_line_edit.text()
                klienti[self.klients_index].klienta_pers_kods = self.klienta_pers_kods_line_edit.text()
                klienti[self.klients_index].klienta_talr_num = self.klienta_talr_num_line_edit.text()
                klients_list_widget_item.setText(klienti[self.klients_index].klienta_vards + " " +
                                                 klienti[self.klients_index].klienta_uzvards)
                widget.klientu_saraksts_list_widget.takeItem(self.klients_index)
                widget.klientu_saraksts_list_widget.insertItem(self.klients_index, klients_list_widget_item)
                widget.klientu_saraksts_list_widget.setCurrentRow(self.klients_index)
            self.saglabat_klientu_button.setEnabled(False)
            widget.eksportet_klientu_sarakstu_button.setEnabled(True)
            return True
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Kļūda")
            msg.setWindowIcon(QIcon("logo.png"))
            msg.setText("Kāds no ievades laukiem ir tukšs vai tā vērtībai ir nepareizs formāts!\n" +
                        "Lūdzu, aizpildiet ar datiem visus laukus un pārbaudiet vērtības!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False

    def aizvert_klientu(self):
        if self.saglabat_klientu_button.isEnabled():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle("Izmaiņas nav saglabātas")
            msg.setWindowIcon(QIcon("logo.png"))
            msg.setText("Jums ir nesaglabātas izmaiņas!\nVai vēlaties vispirms saglabāt tās un tad aizvērt logu vai " +
                        "aizvērt logu, nesaglabājot izmaiņas?")
            vai_saglabat = msg.addButton("Saglabāt un aizvērt", QMessageBox.YesRole)
            msg.addButton("Aizvērt, nesaglabājot", QMessageBox.NoRole)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.exec_()
            if msg.clickedButton() == vai_saglabat:
                if not self.saglabat_klientu():
                    return
        self.close()


class PakalpojumsWidget(QWidget):
    def __init__(self, izveletais_pakalpojums_index=-1, parent=None):
        super(PakalpojumsWidget, self).__init__(parent)
        self.pakalpojums_index = izveletais_pakalpojums_index
        self.setWindowIcon(QIcon("logo.png"))
        self.setMinimumSize(500, 350)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.pakalpojuma_kategorija_line_edit = QLineEdit()
        self.pakalpojuma_nosaukums_line_edit = QLineEdit()
        self.pakalpojuma_atlaide_line_edit = QLineEdit()
        self.pakalpojuma_atlaide_line_edit.setInputMask("99.99")
        self.pakalpojuma_atlaide_line_edit.setText("00.00")
        self.pakalpojuma_cena_line_edit = QLineEdit()
        self.pakalpojuma_cena_double_validator = QDoubleValidator(bottom=0.00, decimals=2)
        self.pakalpojuma_cena_double_validator.setNotation(QDoubleValidator.StandardNotation)
        self.pakalpojuma_cena_line_edit.setValidator(self.pakalpojuma_cena_double_validator)
        self.pakalpojuma_datums_line_edit = QLineEdit()
        self.pakalpojuma_datums_line_edit.setInputMask("99.99.9999.")
        self.pakalpojuma_sakuma_laiks_line_edit = QLineEdit()
        self.pakalpojuma_sakuma_laiks_line_edit.setInputMask("99:99")
        self.pakalpojuma_beigu_laiks_line_edit = QLineEdit()
        self.pakalpojuma_beigu_laiks_line_edit.setInputMask("99:99")
        self.pakalpojuma_ilgums_line_edit = QLineEdit()
        self.pakalpojuma_ilgums_line_edit.setText("0")
        self.pakalpojuma_ilgums_line_edit.setReadOnly(True)
        self.pakalpojuma_kopsumma_line_edit = QLineEdit()
        self.pakalpojuma_kopsumma_line_edit.setText("00.00")
        self.pakalpojuma_kopsumma_line_edit.setReadOnly(True)
        if self.pakalpojums_index == -1:
            self.setWindowTitle("Jaunais pakalpojums")
            self.pakalpojums_label = QLabel("Jaunais pakalpojums")
        else:
            self.setWindowTitle("Pakalpojums \"" + pakalpojumi[self.pakalpojums_index].pakalpojuma_nosaukums + "\"")
            self.pakalpojums_label = QLabel("Pakalpojums \"" +
                                            pakalpojumi[self.pakalpojums_index].pakalpojuma_nosaukums + "\"")
            self.pakalpojuma_kategorija_line_edit.setText(pakalpojumi[self.pakalpojums_index].pakalpojuma_kategorija)
            self.pakalpojuma_nosaukums_line_edit.setText(pakalpojumi[self.pakalpojums_index].pakalpojuma_nosaukums)
            self.pakalpojuma_atlaide_line_edit.setText("{:.2f}".format(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_atlaide * 100).zfill(5))
            self.pakalpojuma_cena_line_edit.setText("{:.2f}".format(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_cena))
            self.pakalpojuma_datums_line_edit.setText(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_datums.strftime("%d.%m.%Y."))
            self.pakalpojuma_sakuma_laiks_line_edit.setText(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_sakuma_laiks.strftime("%H:%M"))
            self.pakalpojuma_beigu_laiks_line_edit.setText(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_beigu_laiks.strftime("%H:%M"))
            self.pakalpojuma_ilgums_line_edit.setText("{:.0f}".format(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_ilgums() / 60))
            self.pakalpojuma_kopsumma_line_edit.setText("{:.2f}".format(
                pakalpojumi[self.pakalpojums_index].pakalpojuma_kopsumma()))
        self.pakalpojums_label.setAlignment(Qt.AlignCenter)
        self.pakalpojums_label.setStyleSheet("font: 20px;")
        self.saglabat_pakalpojumu_button = QPushButton("Saglabāt")
        self.saglabat_pakalpojumu_button.setEnabled(False)
        self.aizvert_pakalpojumu_button = QPushButton("Aizvērt")
        self.pakalpojums_pogas_layout = QHBoxLayout()
        self.pakalpojums_pogas_layout.addWidget(self.saglabat_pakalpojumu_button)
        self.pakalpojums_pogas_layout.addWidget(self.aizvert_pakalpojumu_button)
        self.pakalpojums_form_layout = QFormLayout()
        self.pakalpojums_form_layout.addRow(self.pakalpojums_label)
        self.pakalpojums_form_layout.addRow("Kategorija:", self.pakalpojuma_kategorija_line_edit)
        self.pakalpojums_form_layout.addRow("Nosaukums:", self.pakalpojuma_nosaukums_line_edit)
        self.pakalpojums_form_layout.addRow("Atlaide, %:", self.pakalpojuma_atlaide_line_edit)
        self.pakalpojums_form_layout.addRow("Cena, EUR:", self.pakalpojuma_cena_line_edit)
        self.pakalpojums_form_layout.addRow("Datums:", self.pakalpojuma_datums_line_edit)
        self.pakalpojums_form_layout.addRow("Sākuma laiks:", self.pakalpojuma_sakuma_laiks_line_edit)
        self.pakalpojums_form_layout.addRow("Beigu laiks:", self.pakalpojuma_beigu_laiks_line_edit)
        self.pakalpojums_form_layout.addRow("Ilgums, min:", self.pakalpojuma_ilgums_line_edit)
        self.pakalpojums_form_layout.addRow("Kopsumma, EUR:", self.pakalpojuma_kopsumma_line_edit)
        self.pakalpojums_form_layout.addRow(self.pakalpojums_pogas_layout)
        self.setLayout(self.pakalpojums_form_layout)
        self.pakalpojuma_kategorija_line_edit.textChanged.connect(lambda:
                                                                  self.saglabat_pakalpojumu_button.setEnabled(True))
        self.pakalpojuma_nosaukums_line_edit.textChanged.connect(lambda:
                                                                 self.saglabat_pakalpojumu_button.setEnabled(True))
        self.pakalpojuma_atlaide_line_edit.textChanged.connect(lambda:
                                                               self.saglabat_pakalpojumu_button.setEnabled(True))
        self.pakalpojuma_cena_line_edit.textChanged.connect(lambda: self.saglabat_pakalpojumu_button.setEnabled(True))
        self.pakalpojuma_datums_line_edit.textChanged.connect(lambda: self.saglabat_pakalpojumu_button.setEnabled(True))
        self.pakalpojuma_sakuma_laiks_line_edit.textChanged.connect(lambda:
                                                                    self.saglabat_pakalpojumu_button.setEnabled(True))
        self.pakalpojuma_beigu_laiks_line_edit.textChanged.connect(lambda:
                                                                   self.saglabat_pakalpojumu_button.setEnabled(True))
        self.saglabat_pakalpojumu_button.clicked.connect(self.saglabat_pakalpojumu)
        self.aizvert_pakalpojumu_button.clicked.connect(self.aizvert_pakalpojumu)

    def saglabat_pakalpojumu(self):
        try:
            if "" not in {self.pakalpojuma_kategorija_line_edit.text(),
                          self.pakalpojuma_nosaukums_line_edit.text()} and \
                    datetime.strptime(self.pakalpojuma_sakuma_laiks_line_edit.text(), "%H:%M").time() < \
                    datetime.strptime(self.pakalpojuma_beigu_laiks_line_edit.text(), "%H:%M").time():
                pakalpojums_list_widget_item = QListWidgetItem()
                if self.pakalpojums_index == -1:
                    jaunais_pakalpojums = Pakalpojums(self.pakalpojuma_kategorija_line_edit.text(),
                                                      self.pakalpojuma_nosaukums_line_edit.text(),
                                                      float(self.pakalpojuma_atlaide_line_edit.text()) / 100,
                                                      float(self.pakalpojuma_cena_line_edit.text()),
                                                      datetime.strptime(self.pakalpojuma_datums_line_edit.text(),
                                                                        "%d.%m.%Y.").date(),
                                                      datetime.strptime(self.pakalpojuma_sakuma_laiks_line_edit.text(),
                                                                        "%H:%M").time(),
                                                      datetime.strptime(self.pakalpojuma_beigu_laiks_line_edit.text(),
                                                                        "%H:%M").time())
                    pakalpojumi.append(jaunais_pakalpojums)
                    pakalpojums_list_widget_item.setText(jaunais_pakalpojums.pakalpojuma_nosaukums)
                    widget.pakalpojumu_saraksts_list_widget.addItem(pakalpojums_list_widget_item)
                    self.pakalpojuma_ilgums_line_edit.setText("{:.0f}".format(
                        jaunais_pakalpojums.pakalpojuma_ilgums() / 60))
                    self.pakalpojuma_kopsumma_line_edit.setText("{:.2f}".format(
                        jaunais_pakalpojums.pakalpojuma_kopsumma()))
                else:
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_kategorija = \
                        self.pakalpojuma_kategorija_line_edit.text()
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_nosaukums = \
                        self.pakalpojuma_nosaukums_line_edit.text()
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_atlaide = \
                        float(self.pakalpojuma_atlaide_line_edit.text()) / 100
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_cena = float(self.pakalpojuma_cena_line_edit.text())
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_datums = \
                        datetime.strptime(self.pakalpojuma_datums_line_edit.text(), "%d.%m.%Y.").date()
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_sakuma_laiks = \
                        datetime.strptime(self.pakalpojuma_sakuma_laiks_line_edit.text(), "%H:%M").time()
                    pakalpojumi[self.pakalpojums_index].pakalpojuma_beigu_laiks = \
                        datetime.strptime(self.pakalpojuma_beigu_laiks_line_edit.text(), "%H:%M").time()
                    pakalpojums_list_widget_item.setText(pakalpojumi[self.pakalpojums_index].pakalpojuma_nosaukums)
                    widget.pakalpojumu_saraksts_list_widget.takeItem(self.pakalpojums_index)
                    widget.pakalpojumu_saraksts_list_widget.insertItem(self.pakalpojums_index,
                                                                       pakalpojums_list_widget_item)
                    widget.pakalpojumu_saraksts_list_widget.setCurrentRow(self.pakalpojums_index)
                    self.pakalpojuma_ilgums_line_edit.setText("{:.0f}".format(
                        pakalpojumi[self.pakalpojums_index].pakalpojuma_ilgums() / 60))
                    self.pakalpojuma_kopsumma_line_edit.setText("{:.2f}".format(
                        pakalpojumi[self.pakalpojums_index].pakalpojuma_kopsumma()))
                self.saglabat_pakalpojumu_button.setEnabled(False)
                widget.eksportet_pakalpojumu_sarakstu_button.setEnabled(True)
                return True
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Kāds no ievades laukiem ir tukšs vai tā vērtībai ir nepareizs formāts!\n" +
                            "Lūdzu, aizpildiet ar datiem visus laukus un pārbaudiet vērtības!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return False
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Kļūda")
            msg.setWindowIcon(QIcon("logo.png"))
            msg.setText("Kādai no ievades lauku vērtībām ir nepareizs formāts!\n" +
                        "Lūdzu, pārbaudiet visu ievades lauku vērtības!")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return False

    def aizvert_pakalpojumu(self):
        if self.saglabat_pakalpojumu_button.isEnabled():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setWindowTitle("Izmaiņas nav saglabātas")
            msg.setWindowIcon(QIcon("logo.png"))
            msg.setText("Jums ir nesaglabātas izmaiņas!\nVai vēlaties vispirms saglabāt tās un tad aizvērt logu vai " +
                        "aizvērt logu, nesaglabājot izmaiņas?")
            vai_saglabat = msg.addButton("Saglabāt un aizvērt", QMessageBox.YesRole)
            msg.addButton("Aizvērt, nesaglabājot", QMessageBox.NoRole)
            msg.setDefaultButton(QMessageBox.Yes)
            msg.exec_()
            if msg.clickedButton() == vai_saglabat:
                if not self.saglabat_pakalpojumu():
                    return
        self.close()


class GalvenaisWidget(QWidget):
    def __init__(self, parent=None):
        super(GalvenaisWidget, self).__init__(parent)
        self.klienti_label = QLabel("Klienti")
        self.klienti_label.setAlignment(Qt.AlignCenter)
        self.klienti_label.setStyleSheet("font: 20px;")
        self.izveidot_klientu_button = QPushButton("Izveidot jaunu")
        self.klientu_saraksts_list_widget = QListWidget()
        self.importet_klientu_sarakstu_button = QPushButton("Importēt")
        self.eksportet_klientu_sarakstu_button = QPushButton("Eksportēt")
        self.eksportet_klientu_sarakstu_button.setEnabled(False)
        self.klientu_pogas_layout = QHBoxLayout()
        self.klientu_pogas_layout.addWidget(self.importet_klientu_sarakstu_button)
        self.klientu_pogas_layout.addWidget(self.eksportet_klientu_sarakstu_button)
        self.klienti_layout = QVBoxLayout()
        self.klienti_layout.addWidget(self.klienti_label)
        self.klienti_layout.addWidget(self.izveidot_klientu_button)
        self.klienti_layout.addWidget(self.klientu_saraksts_list_widget)
        self.klienti_layout.addLayout(self.klientu_pogas_layout)
        self.pakalpojumi_label = QLabel("Pakalpojumi")
        self.pakalpojumi_label.setAlignment(Qt.AlignCenter)
        self.pakalpojumi_label.setStyleSheet("font: 20px;")
        self.izveidot_pakalpojumu_button = QPushButton("Izveidot jaunu")
        self.pakalpojumu_saraksts_list_widget = QListWidget()
        self.importet_pakalpojumu_sarakstu_button = QPushButton("Importēt")
        self.eksportet_pakalpojumu_sarakstu_button = QPushButton("Eksportēt")
        self.eksportet_pakalpojumu_sarakstu_button.setEnabled(False)
        self.pakalpojumu_pogas_layout = QHBoxLayout()
        self.pakalpojumu_pogas_layout.addWidget(self.importet_pakalpojumu_sarakstu_button)
        self.pakalpojumu_pogas_layout.addWidget(self.eksportet_pakalpojumu_sarakstu_button)
        self.pakalpojumi_layout = QVBoxLayout()
        self.pakalpojumi_layout.addWidget(self.pakalpojumi_label)
        self.pakalpojumi_layout.addWidget(self.izveidot_pakalpojumu_button)
        self.pakalpojumi_layout.addWidget(self.pakalpojumu_saraksts_list_widget)
        self.pakalpojumi_layout.addLayout(self.pakalpojumu_pogas_layout)
        self.galvenais_logs_layout = QHBoxLayout()
        self.galvenais_logs_layout.addLayout(self.klienti_layout)
        self.galvenais_logs_layout.addLayout(self.pakalpojumi_layout)
        self.setLayout(self.galvenais_logs_layout)
        self.izveidot_klientu_button.clicked.connect(self.izveidot_klientu)
        self.klientu_saraksts_list_widget.clicked.connect(self.apskatit_klientu)
        self.importet_klientu_sarakstu_button.clicked.connect(self.importet_klientu_sarakstu)
        self.eksportet_klientu_sarakstu_button.clicked.connect(self.eksportet_klientu_sarakstu)
        self.izveidot_pakalpojumu_button.clicked.connect(self.izveidot_pakalpojumu)
        self.pakalpojumu_saraksts_list_widget.clicked.connect(self.apskatit_pakalpojumu)
        self.importet_pakalpojumu_sarakstu_button.clicked.connect(self.importet_pakalpojumu_sarakstu)
        self.eksportet_pakalpojumu_sarakstu_button.clicked.connect(self.eksportet_pakalpojumu_sarakstu)

    def izveidot_klientu(self):
        klients_widget = KlientsWidget()
        klients_widget.show()

    def apskatit_klientu(self):
        klients_widget = KlientsWidget(self.klientu_saraksts_list_widget.selectedIndexes()[0].row())
        klients_widget.show()

    def importet_klientu_sarakstu(self):
        global klienti
        importa_datnes_nosaukums, ok = QInputDialog().getText(self, "Klientu datu imports",
                                                              "Lūdzu, ievadiet datnes nosaukumu datu importam!",
                                                              QLineEdit.Normal, "klienti.json")
        if importa_datnes_nosaukums and ok:
            datnes_saturs = importet(importa_datnes_nosaukums)
            if isinstance(datnes_saturs, list) and len(datnes_saturs) > 0:
                if all(i in datnes_saturs[0] for i in ("klienta_id", "klienta_vards", "klienta_uzvards",
                                                       "klienta_pers_kods", "klienta_talr_num")):
                    jaunie_klienti = list()
                    for item in datnes_saturs:
                        jaunie_klienti.append(Klients(item["klienta_vards"], item["klienta_uzvards"],
                                                      item["klienta_pers_kods"], item["klienta_talr_num"]))
                    if len(jaunie_klienti) != 0:
                        msg_text = "Tika veiksmīgi nolasīti dati par " + str(len(jaunie_klienti)) + " klient"
                        if len(jaunie_klienti) % 10 == 1:
                            msg_text += "u!"
                        else:
                            msg_text += "iem!"
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Imports ir veiksmīgs")
                        msg.setWindowIcon(QIcon("logo.png"))
                        msg.setText(msg_text)
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        for klients in jaunie_klienti:
                            klients_list_widget_item = QListWidgetItem()
                            klients_list_widget_item.setText(klients.klienta_vards + " " + klients.klienta_uzvards)
                            self.klientu_saraksts_list_widget.addItem(klients_list_widget_item)
                        klienti += jaunie_klienti
                        self.eksportet_klientu_sarakstu_button.setEnabled(True)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Kļūda")
                    msg.setWindowIcon(QIcon("logo.png"))
                    msg.setText("Nezināma objekta struktūra!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Nezināma datnes satura struktūra!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def eksportet_klientu_sarakstu(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Eksporta veida izvēle")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Vai vēlaties esportēt datus tikai par izvēlēto klientu vai par visiem klientiem?")
        vai_eksportet_izveleto_klientu = msg.addButton("Par izvēlēto klientu", QMessageBox.YesRole)
        msg.addButton("Par visiem klientiem", QMessageBox.NoRole)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.exec_()
        eksportejamie_klienti = list()
        if msg.clickedButton() == vai_eksportet_izveleto_klientu:
            if len(self.klientu_saraksts_list_widget.selectedIndexes()) > 0:
                eksportejamie_klienti.append(klienti[self.klientu_saraksts_list_widget.selectedIndexes()[0].row()])
                eksporta_datnes_nosaukuma_sakums = "klienta_" + str(eksportejamie_klienti[0].klienta_id)
                msg_text = "Tika veiksmīgi eksportēti dati par klientu \"" + \
                           eksportejamie_klienti[0].klienta_vards + " " + \
                           eksportejamie_klienti[0].klienta_uzvards + "\"!"
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Neviens klients nav izvēlēts!\nLūdzu, izvēlieties klientu!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
        else:
            if len(klienti) > 0:
                eksportejamie_klienti = klienti
                eksporta_datnes_nosaukuma_sakums = "klientu"
                msg_text = "Tika veiksmīgi eksportēti dati par visiem klientiem!"
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Neviens klients nav izveidots!\nLūdzu, vispirms izveidojiet vismaz vienu klientu!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
        eksporta_datnes_nosaukums, ok = QInputDialog().getText(self, "Klientu datu eksports",
                                                               "Lūdzu, ievadiet datnes nosaukumu datu eksportam!",
                                                               QLineEdit.Normal, eksporta_datnes_nosaukuma_sakums +
                                                               "_eksports_" +
                                                               datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json")
        if eksporta_datnes_nosaukums and ok:
            vai_eksports_ir_veiksmigs = eksportet(eksportejamie_klienti, eksporta_datnes_nosaukums)
            if vai_eksports_ir_veiksmigs:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Eksports ir veiksmīgs")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText(msg_text)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def izveidot_pakalpojumu(self):
        pakalpojums_widget = PakalpojumsWidget()
        pakalpojums_widget.show()

    def apskatit_pakalpojumu(self):
        pakalpojums_widget = PakalpojumsWidget(self.pakalpojumu_saraksts_list_widget.selectedIndexes()[0].row())
        pakalpojums_widget.show()

    def importet_pakalpojumu_sarakstu(self):
        global pakalpojumi
        importa_datnes_nosaukums, ok = QInputDialog().getText(self, "Pakalpojumu datu imports",
                                                              "Lūdzu, ievadiet datnes nosaukumu datu importam!",
                                                              QLineEdit.Normal, "pakalpojumi.json")
        if importa_datnes_nosaukums and ok:
            datnes_saturs = importet(importa_datnes_nosaukums)
            if isinstance(datnes_saturs, list) and len(datnes_saturs) > 0:
                if all(i in datnes_saturs[0] for i in ("pakalpojuma_id", "pakalpojuma_kategorija",
                                                       "pakalpojuma_nosaukums", "pakalpojuma_atlaide",
                                                       "pakalpojuma_cena", "pakalpojuma_datums",
                                                       "pakalpojuma_sakuma_laiks", "pakalpojuma_beigu_laiks")):
                    jaunie_pakalpojumi = list()
                    for item in datnes_saturs:
                        try:
                            jaunie_pakalpojumi.append(
                                Pakalpojums(item["pakalpojuma_kategorija"], item["pakalpojuma_nosaukums"],
                                            item["pakalpojuma_atlaide"], item["pakalpojuma_cena"],
                                            datetime.strptime(item["pakalpojuma_datums"],
                                                              "%d.%m.%Y.").date(),
                                            datetime.strptime(item["pakalpojuma_sakuma_laiks"],
                                                              "%H:%M").time(),
                                            datetime.strptime(item["pakalpojuma_beigu_laiks"],
                                                              "%H:%M").time()))
                        except ValueError:
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Critical)
                            msg.setWindowTitle("Kļūda")
                            msg.setWindowIcon(QIcon("logo.png"))
                            msg.setText("Pakalpojumam \"" + item["pakalpojuma_nosaukums"] +
                                        "\" ir nepareizs skaitļu formāts!")
                            msg.setStandardButtons(QMessageBox.Ok)
                            msg.exec_()
                    if len(jaunie_pakalpojumi) != 0:
                        msg_text = "Tika veiksmīgi nolasīti dati par " + str(len(jaunie_pakalpojumi)) + " pakalpojum"
                        if len(jaunie_pakalpojumi) % 10 == 1:
                            msg_text += "u!"
                        else:
                            msg_text += "iem!"
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Imports ir veiksmīgs")
                        msg.setWindowIcon(QIcon("logo.png"))
                        msg.setText(msg_text)
                        msg.setStandardButtons(QMessageBox.Ok)
                        msg.exec_()
                        for pakalpojums in jaunie_pakalpojumi:
                            pakalpojums_list_widget_item = QListWidgetItem()
                            pakalpojums_list_widget_item.setText(pakalpojums.pakalpojuma_nosaukums)
                            self.pakalpojumu_saraksts_list_widget.addItem(pakalpojums_list_widget_item)
                        pakalpojumi += jaunie_pakalpojumi
                        self.eksportet_pakalpojumu_sarakstu_button.setEnabled(True)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setWindowTitle("Kļūda")
                    msg.setWindowIcon(QIcon("logo.png"))
                    msg.setText("Nezināma objekta struktūra!")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Nezināma datnes satura struktūra!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def eksportet_pakalpojumu_sarakstu(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Eksporta veida izvēle")
        msg.setWindowIcon(QIcon("logo.png"))
        msg.setText("Vai vēlaties esportēt datus tikai par izvēlēto pakalpojumu vai par visiem pakalpojumiem?")
        vai_eksportet_izveleto_pakalpojumu = msg.addButton("Par izvēlēto pakalpojumu", QMessageBox.YesRole)
        msg.addButton("Par visiem pakalpojumiem", QMessageBox.NoRole)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.exec_()
        eksportejamie_pakalpojumi = list()
        if msg.clickedButton() == vai_eksportet_izveleto_pakalpojumu:
            if len(self.pakalpojumu_saraksts_list_widget.selectedIndexes()) > 0:
                eksportejamie_pakalpojumi.append(
                    pakalpojumi[self.pakalpojumu_saraksts_list_widget.selectedIndexes()[0].row()])
                eksporta_datnes_nosaukuma_sakums = "pakalpojuma_" + str(eksportejamie_pakalpojumi[0].pakalpojuma_id)
                msg_text = "Tika veiksmīgi eksportēti dati par pakalpojumu \"" + \
                           eksportejamie_pakalpojumi[0].pakalpojuma_nosaukums + "\"!"
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Neviens pakalpojums nav izvēlēts!\nLūdzu, izvēlieties pakalpojumu!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
        else:
            if len(pakalpojumi) > 0:
                eksportejamie_pakalpojumi = pakalpojumi
                eksporta_datnes_nosaukuma_sakums = "pakalpojumu"
                msg_text = "Tika veiksmīgi eksportēti dati par visiem pakalpojumiem!"
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Kļūda")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText("Neviens pakalpojums nav izveidots!\nLūdzu, vispirms izveidojiet vismaz vienu pakalpojumu!")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
        eksporta_datnes_nosaukums, ok = QInputDialog().getText(self, "Pakalpojumu datu eksports",
                                                               "Lūdzu, ievadiet datnes nosaukumu datu eksportam!",
                                                               QLineEdit.Normal, eksporta_datnes_nosaukuma_sakums +
                                                               "_eksports_" +
                                                               datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json")
        if eksporta_datnes_nosaukums and ok:
            vai_eksports_ir_veiksmigs = eksportet(eksportejamie_pakalpojumi, eksporta_datnes_nosaukums)
            if vai_eksports_ir_veiksmigs:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Eksports ir veiksmīgs")
                msg.setWindowIcon(QIcon("logo.png"))
                msg.setText(msg_text)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()


if __name__ == "__main__":
    klienti = list()
    pakalpojumi = list()
    app = QApplication(sys.argv)
    widget = GalvenaisWidget()
    win = QMainWindow()
    win.setWindowTitle("Skaistumkopšanas salona vadības sistēma")
    win.setWindowIcon(QIcon("logo.png"))
    win.setCentralWidget(widget)
    win.setMinimumSize(600, 550)
    win.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    win.show()
    sys.exit(app.exec_())
