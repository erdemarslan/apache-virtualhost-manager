# -*- coding: utf-8 -*-

import json
import os
import psutil
import glob
import time
import sys
import traceback
import types
import subprocess

from PyQt5 import QtCore, QtGui, QtWinExtras
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLineEdit, QLabel, QPushButton, QGroupBox, \
    QComboBox, QPlainTextEdit, QFileDialog, QSystemTrayIcon



class Pencere(QWidget):

    def __init__(self):

        super().__init__()
        # Tanımlamalar burada olacak!
        self.groupBox1 = QGroupBox(self)
        self.groupBox2 = QGroupBox(self)
        self.groupBox3 = QGroupBox(self)
        self.groupBox4 = QGroupBox(self)

        self.label_info = QLabel(self)

        self.event_log = QPlainTextEdit(self.groupBox1)

        self.button_apache_start = QPushButton(self.groupBox2)
        self.button_apache_stop = QPushButton(self.groupBox2)
        self.button_apache_restart = QPushButton(self.groupBox2)
        self.button_apache_conf = QPushButton(self.groupBox2)

        self.comboBox_virtual_hosts = QComboBox(self.groupBox3)
        self.button_virtual_delete = QPushButton(self.groupBox3)
        self.button_virtual_errlog = QPushButton(self.groupBox3)
        self.button_virtual_acclog = QPushButton(self.groupBox3)
        self.button_virtual_path = QPushButton(self.groupBox3)

        self.text_virtual = QLineEdit(self.groupBox4)
        self.button_virtual_add = QPushButton(self.groupBox4)

        self.config = {}

        self.set_ui()
        self.first_run()

    def set_ui(self):
        self.resize(450, 340)
        self.setFixedSize(self.size())
        self.setWindowTitle("Sanal Sunucu Yönetimi")
        app_icon = QtGui.QIcon()
        app_icon.addFile('assets/logo16.png', QtCore.QSize(16, 16))
        app_icon.addFile('assets/logo24.png', QtCore.QSize(24, 24))
        app_icon.addFile('assets/logo32.png', QtCore.QSize(32, 32))
        app_icon.addFile('assets/logo48.png', QtCore.QSize(48, 48))
        app_icon.addFile('assets/logo128.png', QtCore.QSize(128, 128))
        app_icon.addFile('assets/logo256.png', QtCore.QSize(256, 256))
        app_icon.addFile('assets/logo512.png', QtCore.QSize(512, 512))
        app_icon.addFile('assets/icon.ico')
        self.setWindowIcon(app_icon)


        # GroupBox'un Fontu
        fontGroupBox = QtGui.QFont()
        fontGroupBox.setFamily("Segoe UI")
        fontGroupBox.setPointSize(8)

        # GroupBox1
        self.groupBox1.setFont(fontGroupBox)
        self.groupBox1.setObjectName("groupBox1")
        self.groupBox1.setGeometry(QtCore.QRect(10, 10, 251, 291))
        self.groupBox1.setTitle("Olay Günlüğü")
        self.groupBox1.setStyleSheet("color: rgb(255, 0, 0);")

        # GroupBox2
        self.groupBox2.setFont(fontGroupBox)
        self.groupBox2.setObjectName("groupBox2")
        self.groupBox2.setGeometry(QtCore.QRect(270, 10, 171, 81))
        self.groupBox2.setTitle("Apache Sunucu")
        self.groupBox2.setStyleSheet("color: rgb(255, 0, 0);")

        # GroupBox3
        self.groupBox3.setFont(fontGroupBox)
        self.groupBox3.setObjectName("groupBox3")
        self.groupBox3.setGeometry(QtCore.QRect(270, 100, 171, 111))
        self.groupBox3.setTitle("Sanal Sunucu Listesi")
        self.groupBox3.setStyleSheet("color: rgb(255, 0, 0);")

        # GroupBox4
        self.groupBox4.setFont(fontGroupBox)
        self.groupBox4.setObjectName("groupBox4")
        self.groupBox4.setGeometry(QtCore.QRect(270, 220, 171, 81))
        self.groupBox4.setTitle("Yeni Sanal Sunucu Oluştur")
        self.groupBox4.setStyleSheet("color: rgb(255, 0, 0);")

        # Information
        self.label_info.setObjectName("label_info")
        self.label_info.setGeometry(QtCore.QRect(10, 320, 431, 16))
        self.label_info.setText("Son işlem bilgisi...")

        # Event Log (groupBox1)
        self.event_log.setObjectName("event_log")
        self.event_log.setGeometry(QtCore.QRect(10, 20, 231, 261))
        self.event_log.setReadOnly(True)
        self.event_log.setStyleSheet("color: rgb(0, 0, 0);")

        # Apache Button Start
        self.button_apache_start.setObjectName("button_apache_start")
        self.button_apache_start.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.button_apache_start.setText("Başlat")
        self.button_apache_start.setStyleSheet("color: rgb(0, 0, 0);")

        # Apache Button Stop
        self.button_apache_stop.setObjectName("button_apache_stop")
        self.button_apache_stop.setGeometry(QtCore.QRect(90, 20, 75, 23))
        self.button_apache_stop.setText("Durdur")
        self.button_apache_stop.setStyleSheet("color: rgb(0, 0, 0);")

        # Apache Button Restart
        self.button_apache_restart.setObjectName("button_apache_restart")
        self.button_apache_restart.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.button_apache_restart.setText("Y. Başlat")
        self.button_apache_restart.setStyleSheet("color: rgb(0, 0, 0);")

        # Apache Button Conf
        self.button_apache_conf.setObjectName("button_apache_conf")
        self.button_apache_conf.setGeometry(QtCore.QRect(90, 50, 75, 23))
        self.button_apache_conf.setText("Conf Dosyası")
        self.button_apache_conf.setStyleSheet("color: rgb(0, 0, 0);")

        # Virtual Host List ComboBox
        self.comboBox_virtual_hosts.setObjectName("comboBox_virtual_hosts")
        self.comboBox_virtual_hosts.setGeometry(QtCore.QRect(10, 20, 151, 22))
        self.comboBox_virtual_hosts.setEditable(False)
        self.comboBox_virtual_hosts.setStyleSheet("color: rgb(0, 0, 0);")

        # Virtual Host Delete Button
        self.button_virtual_delete.setObjectName("button_virtual_delete")
        self.button_virtual_delete.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.button_virtual_delete.setText("Sil")
        self.button_virtual_delete.setStyleSheet("color: rgb(0, 0, 0);")

        # Virtual Host Error Log Button
        self.button_virtual_errlog.setObjectName("button_virtual_errlog")
        self.button_virtual_errlog.setGeometry(QtCore.QRect(90, 50, 75, 23))
        self.button_virtual_errlog.setText("Error Log")
        self.button_virtual_errlog.setStyleSheet("color: rgb(0, 0, 0);")

        # Virtual Host Access Log Button
        self.button_virtual_acclog.setObjectName("button_virtual_acclog")
        self.button_virtual_acclog.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.button_virtual_acclog.setText("Access Log")
        self.button_virtual_acclog.setStyleSheet("color: rgb(0, 0, 0);")

        # Virtual Host Path Button
        self.button_virtual_path.setObjectName("button_virtual_path")
        self.button_virtual_path.setGeometry(QtCore.QRect(90, 80, 75, 23))
        self.button_virtual_path.setText("Dosya Yolu")
        self.button_virtual_path.setStyleSheet("color: rgb(0, 0, 0);")

        # TextBox New Virtual Host
        self.text_virtual.setObjectName("text_virtual")
        self.text_virtual.setGeometry(QtCore.QRect(10, 20, 151, 20))
        self.text_virtual.setPlaceholderText("Sanal Sunucu Adı")
        self.text_virtual.setStyleSheet("color: rgb(0, 0, 0);")
        self.text_virtual.setAlignment(QtCore.Qt.AlignCenter)

        # Virtual Host Path Button
        self.button_virtual_add.setObjectName("button_virtual_add")
        self.button_virtual_add.setGeometry(QtCore.QRect(50, 50, 75, 23))
        self.button_virtual_add.setText("Oluştur")
        self.button_virtual_add.setStyleSheet("color: rgb(0, 0, 0);")

    def first_run(self):

        apache_service = getService("Apache2.4")

        if not apache_service:
            cevap = QMessageBox.question(self, "Uygulama Kapatılıyor",
                                         "Apache Sunucusu bilgisayarınızda kurulu olmadığı için program sonlandırılacak.",
                                         QMessageBox.Ok)
            if cevap == QMessageBox.Ok:
                exit()

        self.label_info.setText(apache_service["description"] + " (" + getStatus(apache_service["status"]) + ")")
        self.label_info.update()

        if apache_service["status"] == "running":
            self.printEventLog("Apache sunucu çalışıyor")
            self.button_apache_start.setEnabled(False)
        else:
            self.printEventLog("Apache sunucu durduruldu")
            self.button_apache_restart.setEnabled(False)
            self.button_apache_stop.setEnabled(False)

        # Json dosyasını ara! Yok ise oluştur. Bu json dosyasında ne olacak dersen. Apache Yolu, htdocs yolu vb
        if not os.path.exists("config.json"):

            QMessageBox.question(self, "İlk Kurulum",
                                 "Bu programı çalıştırabilmeniz için Apache sunucusu ile ilgili bazı bilgileri vermeniz gerekiyor.",
                                 QMessageBox.Ok)
            devam = False
            apache_folder = None
            vhost_folder = None

            while not devam:
                apache_folder = QFileDialog.getExistingDirectory(self, "Apache Klasörünü Seçin")

                apache_folder = os.path.normpath(apache_folder)

                apache_bin_path = apache_folder + "\\bin\\httpd.exe"

                if os.path.exists(apache_folder + "\\bin\\httpd.exe") \
                        and apache_service["binpath"] == "\"" + apache_bin_path + "\" -k runservice":
                    devam = True
                else:

                    cvp = QMessageBox.question(self, "HATA",
                                               "Seçtiğiniz klasör Apache Sunucusuna aitmiş gibi durmuyor. Lütfen sisteminizde kurulu olan Apache Sunucusunun yolunu seçiniz!",
                                               QMessageBox.Ok)
                    if cvp == QMessageBox.Ok:
                        pass

            devam = False

            while not devam:
                vhost_folder = QFileDialog.getExistingDirectory(self, "Döküman Klasörünü Seçin", apache_folder)

                vhost_folder = os.path.normpath(vhost_folder)

                if os.path.exists(vhost_folder) and vhost_folder != ".":
                    devam = True
                else:
                    cvp = QMessageBox.question(self, "HATA",
                                               "Sanal sunucuların bulunduğu klasörü seçmediniz. Lütfen tekrar deneyiniz...",
                                               QMessageBox.Ok)
                    if cvp == QMessageBox.Ok:
                        pass

            self.config["apache_folder"] = apache_folder
            self.config["vhost_folder"] = vhost_folder

            with open("config.json", "w", encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False)
        else:
            with open("config.json") as json_file:
                self.config = json.load(json_file)

        self.load_vhosts()

        self.printEventLog("Program başlatıldı")

        # Butonlara Action ekleyelim!
        self.button_apache_start.clicked.connect(self.doApacheStart)
        self.button_apache_stop.clicked.connect(self.doApacheStop)
        self.button_apache_restart.clicked.connect(self.doApacheRestart)
        self.button_apache_conf.clicked.connect(self.doApacheConfOpen)
        self.button_virtual_delete.clicked.connect(self.doVirtualDelete)
        self.button_virtual_errlog.clicked.connect(self.doVirtualErrLog)
        self.button_virtual_acclog.clicked.connect(self.doVirtualAccLog)
        self.button_virtual_path.clicked.connect(self.doVirtualFolder)
        self.button_virtual_add.clicked.connect(self.doVirtualAdd)

    def load_vhosts(self):
        v_hosts = [host.split(".conf")[0] for host in [liste.split("\\")[-1] for liste in [f for f in glob.glob(
            self.config["apache_folder"] + "\\conf\\virtualhosts\\*.conf")]]]

        self.comboBox_virtual_hosts.clear()
        self.comboBox_virtual_hosts.addItems(v_hosts)

    def printEventLog(self, message):
        self.event_log.appendPlainText("[" + time.strftime("%H:%M") + "] " + message)

    def doApacheStart(self):
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        run = subprocess.Popen(self.config["apache_folder"] + "\\bin\\httpd.exe -k start", shell=True, stdin=None,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err, out = run.communicate()
        run.stdout.close()

        service = getService("Apache2.4")

        if service["status"] == "running":
            self.button_apache_start.setEnabled(False)
            self.button_apache_stop.setEnabled(True)
            self.button_apache_restart.setEnabled(True)
            self.printEventLog("Apache sunucusu başlatıldı")
        else:
            self.printEventLog("Apache sunucusu başlatılırken hata oluştu")

        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def doApacheStop(self):
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        run = subprocess.Popen(self.config["apache_folder"] + "\\bin\\httpd.exe -k stop", shell=True, stdin=None,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        err, out = run.communicate()
        run.stdout.close()

        if "The 'Apache2.4' service has stopped." in str(out):
            self.button_apache_stop.setEnabled(False)
            self.button_apache_start.setEnabled(True)
            self.button_apache_restart.setEnabled(False)
            self.printEventLog("Apache sunucu durduruldu")
        else:
            self.printEventLog("Apache sunucu durdurulurken hata meydana geldi")

        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def doApacheRestart(self):
        self.button_apache_restart.setEnabled(False)

        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        run = subprocess.Popen(self.config["apache_folder"] + "\\bin\\httpd.exe -k restart", shell=True, stdin=None,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err, out = run.communicate()
        run.stdout.close()

        service = getService("Apache2.4")

        if service["status"] == "running":
            self.button_apache_start.setEnabled(False)
            self.button_apache_stop.setEnabled(True)
            self.button_apache_restart.setEnabled(True)
            self.printEventLog("Apache sunucusu yeniden başlatıldı")
        else:
            self.printEventLog("Apache sunucusu yeniden başlatılırken hata oluştu")

        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def doApacheConfOpen(self):
        notepad = "notepad.exe"
        conffile = self.config["apache_folder"] + "\\conf\\httpd.conf"
        subprocess.Popen([notepad, conffile])
        self.printEventLog("httpd.conf dosyası açıldı")

    def doVirtualDelete(self):
        if self.comboBox_virtual_hosts.currentIndex() >= 0:
            name = self.comboBox_virtual_hosts.currentText()
            self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

            conffile = self.config["apache_folder"] + "\\conf\\virtualhosts\\" + name + ".conf"
            documentfolder = self.config["vhost_folder"] + "\\" + name

            self.doApacheStop()
            self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

            try:
                os.remove(conffile)
            except:
                pass
            try:
                os.rename(documentfolder, self.config["vhost_folder"] + "\\removed_" + name)
            except:
                pass

            hosts = os.path.join(os.environ["SYSTEMROOT"], "System32", "drivers", "etc", "hosts")

            satirlar = []
            with open(hosts, "r", encoding="utf-8") as rh:
                for line in rh:
                    if line == "# Virtual Host " + name + "\n":
                        pass
                    elif line == "127.0.0.1 " + name + "\n":
                        pass
                    elif line == "127.0.0.1 www." + name + "\n":
                        pass
                    else:
                        satirlar.append(line)

            with open(hosts, "w+", encoding="utf-8") as wh:
                wh.writelines(satirlar)

            self.doApacheStart()

            self.load_vhosts()

            self.printEventLog(name + " sanal sunucusu silindi")

        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def doVirtualErrLog(self):
        if self.comboBox_virtual_hosts.currentIndex() >= 0:
            vhost = self.comboBox_virtual_hosts.currentText()
            notepad = "notepad.exe"
            file = self.config["apache_folder"] + "\\logs\\" + vhost + "-error.log"
            if os.path.isfile(file):
                subprocess.Popen([notepad, file])
                self.printEventLog(vhost + "-error.log dosyası açıldı")
            else:
                self.printEventLog(vhost + "-error.log dosyası bulunamadı")

    def doVirtualAccLog(self):
        if self.comboBox_virtual_hosts.currentIndex() >= 0:
            vhost = self.comboBox_virtual_hosts.currentText()
            notepad = "notepad.exe"
            file = self.config["apache_folder"] + "\\logs\\" + vhost + "-access.log"
            if os.path.isfile(file):
                subprocess.Popen([notepad, file])
                self.printEventLog(vhost + "-access.log dosyası açıldı")
            else:
                self.printEventLog(vhost + "-access.log dosyası bulunamadı")

    def doVirtualFolder(self):
        if self.comboBox_virtual_hosts.currentIndex() >= 0:
            vhost = self.comboBox_virtual_hosts.currentText()
            explorer = "explorer.exe"
            folder = self.config["vhost_folder"] + "\\" + vhost
            if os.path.isdir(folder):
                subprocess.Popen([explorer, folder])
                self.printEventLog(folder + " yolu açıldı")
            else:
                self.printEventLog(folder + " yolu bulunamadı")

    def doVirtualAdd(self):

        name = self.text_virtual.text()
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        if not name == "":
            # dosya yollarını belirtelim
            conffile = self.config["apache_folder"] + "\\conf\\virtualhosts\\" + name + ".conf"
            documentfolder = self.config["vhost_folder"] + "\\" + name

            if not os.path.isfile(conffile):

                if not os.path.exists(documentfolder):
                    os.mkdir(documentfolder)

                with open(conffile, "w+", encoding="utf-8") as file:
                    file.write("<virtualhost *:80>\n")
                    file.write("\tDocumentRoot \"" + str(documentfolder).replace("\\", "/") + "\"\n")
                    file.write("\tServerName " + name + "\n")
                    file.write("\tServerAlias www." + name + "\n")
                    file.write("\tErrorLog \"logs/" + name + "-error.log\"\n")
                    file.write("\tCustomLog \"logs/" + name + "-access.log\" common\n")
                    file.write("\t<directory \"" + str(documentfolder).replace("\\", "/") + "\">\n")
                    file.write("\t\tAllowOverride All\n")
                    file.write("\t\tOptions Indexes FollowSymLinks\n")
                    file.write("\t\tOrder allow,deny\n")
                    file.write("\t\tAllow from all\n")
                    file.write("\t</directory>\n")
                    file.write("</virtualhost>")

                # hosts dosyasına da yaz
                hosts = os.path.join(os.environ["SYSTEMROOT"], "System32", "drivers", "etc", "hosts")

                with open(hosts, "a", encoding="utf-8") as h:
                    h.write("# Virtual Host " + name + "\n")
                    h.write("127.0.0.1 " + name + "\n")
                    h.write("127.0.0.1 www." + name + "\n")

                self.doApacheStop()
                self.doApacheStart()

                self.load_vhosts()

                self.text_virtual.setText("")

                self.printEventLog("Sanal sunucu \"" + name + "\" eklendi")
            else:
                self.printEventLog("HATA: Bu isimde bir sanal sunucu zaten var")
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


def getService(name):
    service = None
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception as ex:
        print(str(ex))

    return service


def isUserAdmin():
    if os.name == 'nt':
        import ctypes
        # WARNING: requires Windows XP SP2 or higher!
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False
    elif os.name == 'posix':
        # Check for root on Posix
        return os.getuid() == 0
    else:
        raise RuntimeError("Unsupported operating system for this module: %s" % (os.name,))


def runAsAdmin(cmdLine=None, wait=True):
    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32api
    import win32con
    import win32event
    import win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType, types.ListType):
        raise ValueError("cmdLine is not a sequence.")
    cmd = '"%s"' % (cmdLine[0],)

    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    showCmd = win32con.SW_SHOWNORMAL
    lpVerb = 'runas'  # causes UAC elevation prompt.

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)
    rcx = None

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rcx = win32process.GetExitCodeProcess(procHandle)

    return rcx


def getStatus(status):
    if status == "running":
        return "Çalışıyor"
    else:
        return "Durduruldu"


def main(args):
    if not isUserAdmin():
        rc = runAsAdmin()
    else:
        rc = 0
        app = QApplication([])
        pencere = Pencere()
        pencere.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv[1:])
