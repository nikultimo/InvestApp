from os import error
import sys
from typing import Type
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from apps import InvestApp as invApp
from openapi_client import openapi
from cryptography.fernet import Fernet
import cryptography


class ExampleApp(QtWidgets.QMainWindow, invApp.Ui_InvestApp):
    def __init__(self):
        # Init classs
        super().__init__()
        self.setupUi(self)  # Initialization of GUI Design
        self.getCostFromYFPushButton.clicked.connect(
            self.getRealCost)  # Get real cost of stock from Tinkoff Button
        self.calculateEarningPushButton.clicked.connect(
            self.calculateEarning)  # Calculate your earnings button
        self.setWindowIcon(QtGui.QIcon('images/logo.ico'))  # Set logo to app
        # Set logo to button for getting stocks names
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/download.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadStocksNamespushButton.setIcon(icon)
        # Get all names for stocks. Show it in drop down menu
        self.uploadStocksNamespushButton.clicked.connect(self.get_all_stocks)
        # Add triggered event to info button
        self.actionInfo.triggered.connect(self.openDialogBox)
        # Add triggered event to Export API Token button
        self.actionSave.triggered.connect(self.file_encrypt_save)
        # Add triggered event to Import API Token button
        self.actionLoad.triggered.connect(self.file_encrypt_load)
        # Add triggered event to Generate Encryption key button
        self.actionGenerate_Key.triggered.connect(self.generate_encrypt_key)

    def openDialogBox(self):
        # Dialog box for providing some information about this app
        QtWidgets.QMessageBox.about(self, 'Information',
                                    'With this App you can define your earnings based on your stock. \
        \r\nAlso all information about stocks are getting from Tinkoff Investment App. \
        \r\nFor better using you need to provide your Tinkoff API Token from this page: \
        \r\nhttps://www.tinkoff.ru/invest/settings/')

    def file_encrypt_save(self):
        # Write API Token to file and encrypt
        # with generated / saved key.
        try:
            # Get key
            fernet = self.get_key()
            # Write token to file
            self.write_token_to_file()
            # Encrypt
            self.encrypt_token(fernet)
        except FileNotFoundError:
            if name_file == 'encryption.key':
                self.customDialogBox(
                    "Error", "Encryption key must be in the working directory. Not found.")
            else:
                self.customDialogBox(
                    "Error", "File not found. Try different file")

    def file_encrypt_load(self):
        # Read API Token from encrypted file, decrypt it using
        # generated key and show in EditField
        try:
            # Get key
            fernet = self.get_key()
            # Decrypt token and shot it in EditField
            self.decrypt_token(fernet)
        except FileNotFoundError:
            if name_file == 'encryption.key':
                self.customDialogBox(
                    "Error", "Encryption key must be in the working directory. Not found.")
            else:
                self.customDialogBox(
                    "Error", "File not found. Try different file")
        except cryptography.fernet.InvalidToken:
            self.customDialogBox("Encryption error",
                                 "Invalid encryption key. Try different one")

    def get_key(self):
        # Generate encryption (decryption) key
        global name_file
        name_file = 'encryption.key'
        with open(name_file, 'rb') as filekey:
            key = filekey.read()
        # using the generated key
        fernet = Fernet(key)
        return fernet

    def write_token_to_file(self):
        # Write token from EditField to file
        global name_file
        name_file = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save API Token to file', "", "files TXT (*.txt)")
        file = open(name_file[0], 'w')
        text = self.apiTokenEditField.toPlainText()
        file.write(text)
        file.close()

    def encrypt_token(self, fernet):
        # Encrypt file with saved token
        global name_file
        with open(name_file[0], 'rb') as file:
            original = file.read()
            # encrypting the file
        encrypted = fernet.encrypt(original)
        # opening the file in write mode and
        # writing the encrypted data
        with open(name_file[0], 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def decrypt_token(self, fernet):
        # Decrypt file with saved token and show it at apiTokenEditField
        name_file = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Load API Token from file', "", "files TXT (*.txt)")
        file = open(name_file[0], 'rb')
        with file:
            text = file.read()
            decrypted = fernet.decrypt(text)
            self.apiTokenEditField.setText(decrypted.decode("utf-8"))

    def generate_encrypt_key(self):
        # Generate encryption key and show dialog box
        key = Fernet.generate_key()
        # string the key in a file
        with open('encryption.key', 'wb') as filekey:
            filekey.write(key)
        self.customDialogBox("Encryption", "Encryption key was successfuly generated in the working directory. \
            \r\nSave and move it to secure place for further use.")

    def customDialogBox(self, title, text):
        # Custom dialog box
        QtWidgets.QMessageBox.about(self, title, text)

    def getRealCost(self):
        # Get real cost of stock
        try:
            stock_name = self.stockNameTextEdit.currentText()
            earn, average, lots, _ = self.parser_stock(stock_name)
            itog = earn / lots + average
            itog = round(itog, 6)
            self.stockRealCostTextEdit.setPlainText("{0}".format(str(itog)))
            self.stockAmountTextEdit.setPlainText("{0}".format(str(lots)))
            self.stockAverageTextEdit.setPlainText("{0}".format(str(average)))
            return itog
        except TypeError:
            self.customDialogBox('Error', 'Not the right Token API')
        except IndexError:
            self.customDialogBox('Error', 'Not the right stock name')
        except:
            self.customDialogBox(
                'Error', 'Not the right stock name or Token API')

    def usdToRub(self):
        # Convert usd to rub
        earn, average, lots, _ = self.parser_stock('USD000UTSTOM')
        gain = earn / lots + average
        return gain

    def get_all_stocks(self):
        try:
            _translate = QtCore.QCoreApplication.translate
            # Grab all stocks to drop down box
            token = self.apiTokenEditField.toPlainText()
            client = openapi.api_client(token)
            pf = client.portfolio.portfolio_get()
            k = 0
            index = 0
            for i in range(self.stockNameTextEdit.count(), -1, -1):
                self.stockNameTextEdit.removeItem(i)
            while k <= len(pf.payload.positions) - 1:
                self.stockNameTextEdit.addItem("")
                name = pf.payload.positions[k].ticker
                self.stockNameTextEdit.setItemText(k, name)
                k += 1
        except:
            self.customDialogBox('Error', 'Not the right Token API')

    def parser_stock(self, stock_name):
        # Get stock info from Tinkoff API Token
        token = self.apiTokenEditField.toPlainText()
        client = openapi.api_client(token)
        pf = client.portfolio.portfolio_get()
        state = False
        k = 0
        index = 0
        earn = 0
        average = 0
        lots = 0
        currency = ''
        while state != True and k <= len(pf.payload.positions) - 1:
            if pf.payload.positions[k].ticker == stock_name:
                index = k
                state = True
            else:
                k += 1
        if pf.payload.positions[k].ticker != stock_name:
            self.customDialogBox('Error', 'Not the right stock name')
            exit()
        else:
            earn = pf.payload.positions[index].expected_yield.value
            average = pf.payload.positions[index].average_position_price.value
            lots = pf.payload.positions[index].balance
            currency = pf.payload.positions[index].average_position_price.currency
        return float(earn), float(average), float(lots), currency

    def calculateEarning(self):
        # Calculate your earning
        try:
            stock_name = self.stockNameTextEdit.currentText()
            _, average, lots, currency = self.parser_stock(stock_name)
            stock_price_now = float(self.stockRealCostTextEdit.toPlainText())
            print(currency)
            if currency == 'USD':
                res = (lots*(stock_price_now - average))*self.usdToRub()
            else:
                res = lots*(stock_price_now - average)
            self.earningTextEdit.setPlainText("{0}".format(str(res)))
        except TypeError:
            self.customDialogBox('Error', 'Not the right Token API')
        except IndexError:
            self.customDialogBox('Error', 'Not the right stock name')
        except:
            self.customDialogBox(
                'Error', 'Not the right stock name or Token API')


def main():
    app = QtWidgets.QApplication(sys.argv)  # New sample of QApplication
    window = ExampleApp()  # Create object of class ExampleApp
    window.show()  # Show the window
    app.exec_()  # Launch the app


if __name__ == '__main__':  # If launch the file forwardly, not importing
    main()  # then run function main()
