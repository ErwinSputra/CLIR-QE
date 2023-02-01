from query_expansion import QE
from preprocessing import Prapengolahan
from vector_space_model import VSM
from docs import Dokumen
from term_weighting import PembobotanKata
import sys
import re
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from deep_translator import GoogleTranslator
import subprocess


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("CLIR-QE.ui", self)
        pixmap = QPixmap('images/AIR&D.jpg')
        self.label.setPixmap(pixmap)
        pixmap = QPixmap('images/logo-unsri.png')
        self.label_2.setPixmap(pixmap)
        self.tabWidget.removeTab(1)
        self.tableWidget.setColumnWidth(1, 610)
        self.parm = 0
        self.tableWidget.move(0, 0)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.tabWidget.removeTab(index))
        self.tableWidget.doubleClicked.connect(self.read_more)
        self.searchBtn.clicked.connect(self.src)
        self.qeBtn.clicked.connect(self.search)
        self.resetBtn.clicked.connect(self.reset)
        self.manualBtn.clicked.connect(self.manual)
        self.exitBtn.clicked.connect(self.exit)

    def reset(self):
        print("Reset..")
        if len(self.tabWidget) > 1:
            for tab in range(len(self.tabWidget)-1):
                self.tabWidget.removeTab(1)
        self.qeSystem.setChecked(True)
        self.allres = []
        self.qe0 = []
        self.qe1 = []
        self.qe2 = []
        self.qe3 = []
        self.bool = False
        self.inside_qe = False
        self.allQuery.setChecked(True)
        self.inputQuery.setText("")
        self.sysResult.setPlainText(f"Kueri awal: -\n\nHasil kueri ekspansi teratas;\n1. -\n2. -\n3. -")
        self.label_1.setText("Hasil Pencarian dengan Kueri - : x artikel")
        self.tableWidget.setRowCount(0)

    def manual(self):
        print("Membuka pdf manual..")
        path = 'manual.pdf'
        subprocess.Popen([path], shell=True)

    def exit(self):
        print("Exiting..")
        sys.exit()

    def src(self):
        self.allres = []
        self.qe0 = []
        self.qe1 = []
        self.qe2 = []
        self.qe3 = []
        self.bool = False
        self.inside_qe = False
        if self.parm == 0:
            self.inv_idx = Dokumen().inverted_index()
            self.tf_idf_doc = PembobotanKata().create_tf_idf()
            self.parm += 1
        self.allQuery.setChecked(True)
        self.search()

    def search(self):
        query = ""
        if self.allQuery.isChecked():
            query = self.inputQuery.text()
            self.bool = True
        else:
            print("Memilih Kueri Ekspansi")
            self.inside_qe = True
            qe = self.sysResult.toPlainText()
            qe = qe.split("\n")
            new_qe = []
            if self.ogQuery.isChecked():
                self.bool = True
                que = qe[0]
                query = que[12:]

            for qe in qe[3:]:
                new_qe.append(qe[3:])

            if self.qeRes1.isChecked():
                query = new_qe[0]
                if len(self.qe1) != 0:
                    self.bool = True
                else:
                    self.bool = False
                    if new_qe[0] == "-":
                        query = "-"

            elif self.qeRes2.isChecked():
                query = new_qe[1]
                if len(self.qe2) != 0:
                    self.bool = True
                else:
                    self.bool = False
                    if new_qe[1] == "-":
                        query = "-"

            elif self.qeRes3.isChecked():
                query = new_qe[2]
                if len(self.qe3) != 0:
                    self.bool = True
                else:
                    self.bool = False
                    if new_qe[2] == "-":
                        query = "-"

        if query == "":
            msg = QtWidgets.QMessageBox()
            msg.setText("Kueri belum dimasukkan!")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()
        elif query == "-":
            msg = QtWidgets.QMessageBox()
            msg.setText("Kueri ekspansi tidak ada! Cek kueri pilihanmu")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.exec_()
        else:
            translated_query = GoogleTranslator(source='id', target='en').translate(query)
            print(translated_query)
            temp = False
            check_res = []
            if self.qeSystem.isChecked() & self.allQuery.isChecked() and len(self.allres) == 0:
                temp = True
                exp_query, rule = QE().expanding_query(translated_query)
                # exp_query;
                # [winter, wintertime, storm, violent_storm]
                # [pollution, befoulment, defilement, contamination]
                allterm = []
                for term in exp_query:
                    if "_" in term:
                        output = re.sub(r'_', ' ', term)
                        term = output
                    allterm.append(term)

                allquery = []
                arr1 = []
                arr2 = []
                arr3 = []
                k = 0
                if rule == 1:
                    altres = []
                    for item in allterm:
                        allquery.append(item)
                        q_terms = Prapengolahan().tokenize_and_extract(item)
                        print()
                        print(q_terms)
                        vec_space_model = VSM(self.inv_idx, self.tf_idf_doc)
                        res = vec_space_model.cos_sim(q_terms)

                        if res != -999:

                            for item in res:
                                if k == 0:
                                    self.qe0.append(item)
                                elif k == 1:
                                    self.qe1.append(item)
                                elif k == 2:
                                    self.qe2.append(item)
                                elif k == 3:
                                    self.qe3.append(item)

                                if item[0] not in altres:
                                    altres.append(item[0])
                                    self.allres.append(item)
                        k += 1
                    check_res = self.allres
                elif rule == 0:
                    arr1 = [allterm[0]]
                    arr2 = [allterm[1]]
                elif rule == 2:
                    arr1 = allterm[0:2]
                    arr2 = allterm[2:4]
                elif rule == 3:
                    arr1 = [allterm[0]]
                    arr2 = allterm[1:3]
                elif rule == 4:
                    arr1 = allterm[0:2]
                    arr2 = [allterm[2]]
                elif rule == 5:
                    arr1 = allterm[0:2]
                    arr2 = allterm[2:4]
                    arr3 = allterm[4:6]
                elif rule == 6:
                    arr1 = allterm[0:2]
                    arr2 = [allterm[2]]
                    arr3 = [allterm[3]]
                elif rule == 7:
                    arr1 = [allterm[0]]
                    arr2 = allterm[1:3]
                    arr3 = [allterm[3]]
                elif rule == 8:
                    arr1 = [allterm[0]]
                    arr2 = [allterm[1]]
                    arr3 = allterm[2:4]
                elif rule == 9:
                    arr1 = [allterm[0]]
                    arr2 = allterm[1:3]
                    arr3 = allterm[3:5]
                elif rule == 10:
                    arr1 = allterm[0:2]
                    arr2 = [allterm[2]]
                    arr3 = allterm[3:5]
                elif rule == 11:
                    arr1 = allterm[0:2]
                    arr2 = allterm[2:4]
                    arr3 = [allterm[4]]
                elif rule == 12:
                    arr1 = [allterm[0]]
                    arr2 = [allterm[1]]
                    arr3 = [allterm[2]]
                if rule == 2 or rule == 3 or rule == 4:
                    altres = []
                    for item1 in arr1:
                        for item2 in arr2:
                            # "winter storm", "winter violent storm", "wintertime storm", "wintertime violent storm"
                            que = item1 + " " + item2
                            allquery.append(que)
                            q_terms = Prapengolahan().tokenize_and_extract(que)
                            print()
                            print(q_terms)
                            # [winter storm], [winter violent storm], [wintertime storm], [wintertime violent storm]
                            vec_space_model = VSM(self.inv_idx, self.tf_idf_doc)
                            res = vec_space_model.cos_sim(q_terms)
                            # [23: 0.82, 45: 0.67] atau -999
                            if res != -999:
                                for item in res:
                                    if k == 0:
                                        self.qe0.append(item)
                                    elif k == 1:
                                        self.qe1.append(item)
                                    elif k == 2:
                                        self.qe2.append(item)
                                    elif k == 3:
                                        self.qe3.append(item)

                                    if item[0] not in altres:
                                        altres.append(item[0])
                                        self.allres.append(item)
                            k += 1
                    check_res = self.allres
                elif rule >= 5:
                    j = 0
                    altres = []
                    for item1 in arr1:
                        for item2 in arr2:
                            for item3 in arr3:
                                if j < 4:
                                    que = item1 + " " + item2 + " " + item3
                                    allquery.append(que)
                                    q_terms = Prapengolahan().tokenize_and_extract(que)
                                    print()
                                    print(q_terms)
                                    vec_space_model = VSM(self.inv_idx, self.tf_idf_doc)
                                    res = vec_space_model.cos_sim(q_terms)
                                    if res != -999:
                                        for item in res:
                                            if k == 0:
                                                self.qe0.append(item)
                                            elif k == 1:
                                                self.qe1.append(item)
                                            elif k == 2:
                                                self.qe2.append(item)
                                            elif k == 3:
                                                self.qe3.append(item)

                                            if item[0] not in altres:
                                                altres.append(item[0])
                                                self.allres.append(item)
                                    j += 1
                                    k += 1
                    check_res = self.allres
                if len(allquery) == 4:
                    self.sysResult.setPlainText(
                        f"Kueri awal: {allquery[0]}\n\nHasil kueri ekspansi teratas;\n1. {allquery[1]}\n2. {allquery[2]}\n3. {allquery[3]}")
                elif len(allquery) == 3:
                    self.sysResult.setPlainText(
                        f"Kueri awal: {allquery[0]}\n\nHasil kueri ekspansi teratas;\n1. {allquery[1]}\n2. {allquery[2]}\n3. -")
                elif len(allquery) == 2:
                    self.sysResult.setPlainText(
                        f"Kueri awal: {allquery[0]}\n\nHasil kueri ekspansi teratas;\n1. {allquery[1]}\n2. -\n3. -")
                else:
                    self.sysResult.setPlainText(
                        f"Kueri awal: {allquery[0]}\n\nHasil kueri ekspansi teratas;\n1. -\n2. -\n3. -")

            elif not self.qeSystem.isChecked() and len(self.allres) == 0:  # elif self.radioButton_2.isChecked():
                query_exp = Prapengolahan().tokenize_and_extract(translated_query)
                print()
                print(query_exp)
                vec_space_model = VSM(self.inv_idx, self.tf_idf_doc)
                res = vec_space_model.cos_sim(query_exp)
                #  [('4304', 1.0000000000000002), ('378', 1.0000000000000002), ('4935', 0.6283072553180628)]
                self.allres = res
                check_res = res
                self.qe0 = self.allres

                if res == -999:
                    check_res = []

                if not self.qeSystem.isChecked():
                    self.sysResult.setPlainText(
                        f"Kueri awal: {query}\n\nHasil kueri ekspansi teratas;\n1. -\n2. -\n3. -")
            elif self.bool:
                check_res = self.allres
            else:
                check_res = []

            if len(check_res) == 0:
                if self.allQuery.isChecked():
                    self.label_1.setText(
                        f"Hasil Pencarian dengan gabungan semua kueri: 0 artikel")  # docs_len / len(res)
                else:
                    self.label_1.setText(
                        f"Hasil Pencarian dengan Kueri ’{query}’: 0 artikel")  # docs_len / len(res)
                self.tableWidget.setRowCount(0)
                msg = QtWidgets.QMessageBox()
                msg.setText("Artikel Tidak Ditemukan!")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()
            else:
                docs_len = 0
                results = []
                qeres = self.allres
                if self.ogQuery.isChecked():
                    qeres = self.qe0
                elif self.qeRes1.isChecked():
                    qeres = self.qe1
                elif self.qeRes2.isChecked():
                    qeres = self.qe2
                elif self.qeRes3.isChecked():
                    qeres = self.qe3

                for item in qeres:
                    if item[1] >= 0.851:
                        results.append(item)
                        docs_len += 1
                if self.allQuery.isChecked():
                    self.label_1.setText(
                        f"Hasil Pencarian dengan gabungan semua kueri: {docs_len} artikel")  # docs_len / len(res)
                else:
                    self.label_1.setText(f"Hasil Pencarian dengan Kueri ’{query}’: {docs_len} artikel")  # docs_len / len(res)

                self.tableWidget.setRowCount(docs_len)

                corpus = Dokumen().document_retr()
                allcossim = []
                idx = 0
                if temp:
                    results = sorted(results, key=lambda x: x[1], reverse=True)

                self.id_doc = []
                self.allnews = []
                self.alltitle = []
                doc_list = []

                for item in results:
                    self.id_doc.append(item[0])
                    cossim = "%.2f" % item[1]
                    allcossim.append(cossim)
                    doc = corpus[str(item[0])]
                    j = 0
                    k = 0
                    n = 4000
                    doc_news = doc[1]
                    for i in range(0, len(doc_news), n):
                        if len(doc_news) > n and i + n < len(doc_news):
                            while doc_news[i + n + k] != " " and doc_news[i+n+k] != "." and doc_news[i+n+k] != "”" and doc_news[i+n+k] != "\"":  #
                                k += 1
                        doc_list.append(doc_news[i + j:i + n + k])
                        j = k

                    news = ""
                    for text in doc_list:
                        translated = GoogleTranslator(source='en', target='id').translate(text)
                        news += translated + " "

                    self.allnews.append(news)   # news

                    doc_title = GoogleTranslator(source='en', target='id').translate(doc[0])
                    self.alltitle.append(doc_title)

                    doc_list = []
                    idx += 1

                idx = 0
                for id in self.id_doc:
                    item = QTableWidgetItem(str(id))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(idx, 0, item)
                    idx += 1
                idx = 0
                for news in self.allnews:
                    self.tableWidget.setItem(idx, 1, QTableWidgetItem(news))
                    idx += 1
                idx = 0
                for cossim in allcossim:
                    cos = str(cossim)
                    item = QTableWidgetItem(cos[:6])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(idx, 2, item)
                    idx += 1
                print("Pencarian selesai..")

    @pyqtSlot()
    def read_more(self):
        self.new_tab = QtWidgets.QWidget()
        title = ""
        text = ""
        title_tab = ""
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            title = self.alltitle[currentQTableWidgetItem.row()]
            text = self.allnews[currentQTableWidgetItem.row()]
            title_tab = self.id_doc[currentQTableWidgetItem.row()]

        self.tabWidget.addTab(self.new_tab, f"Dok {title_tab}")
        self.new_layout = QtWidgets.QVBoxLayout(self.new_tab)
        self.new_label = QtWidgets.QLabel(self.new_tab)
        # title = "Kemungkinan penyebab di balik pemboman St. Petersburg"
        self.new_label.setText(title)
        self.new_label.setAlignment(Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.underline()
        self.new_label.setFont(font)
        self.new_textBrowser = QtWidgets.QTextBrowser(self.new_tab)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setReadOnly(True)
        font2 = QtGui.QFont()
        font2.setPointSize(10)
        self.new_textBrowser.setFont(font2)
        self.new_textBrowser.setAlignment(Qt.AlignBaseline)
        self.new_textBrowser.setText(text)
        self.new_layout.addWidget(self.new_label)
        self.new_layout.addWidget(self.new_textBrowser)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainWindow)
    widget.setFixedWidth(985)
    widget.setFixedHeight(770)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting..")