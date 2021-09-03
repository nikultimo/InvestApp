import sys
from typing import Type  # sys needs to transfer argv to QApplication
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from apps import InvestApp as invApp
from openapi_client import openapi

# pyuic5 InvestApp.ui -o InvestApp.py
# pip install auto-py-to-exe
# auto-py-to-exe


class ExampleApp(QtWidgets.QMainWindow, invApp.Ui_InvestApp):
    def __init__(self):
        # Init classs
        super().__init__()
        self.setupUi(self)  # Initialization of GUI Design
        oImage = QtGui.QImage('images/background.png')
        # resize Image to widgets size
        sImage = oImage.scaled(QSize(384, 235))
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(sImage))
        self.setPalette(palette)
        self.getCostFromYFPushButton.clicked.connect(
            self.getRealCost)  # Get real cost of stock from Tinkoff Button
        self.calculateEarningPushButton.clicked.connect(
            self.calculateEarning)  # Calculate your earnings button
        self.stockAverageTextEdit.setPlainText(
            ("{0}".format("5.31")))  # Default value for average stock price
        self.stockRealCostTextEdit.setPlainText(
            ("{0}".format("5.15")))  # Default value for real stock price
        self.earningTextEdit.setPlainText(
            ("{0}".format("0.0")))  # Default value for earnings
        self.setWindowIcon(QtGui.QIcon('images/logo.ico'))  # Set logo to app
        # Add triggered event to help button
        self.menuHelp.triggered.connect(self.openDialogBox)

    def openDialogBox(self):
        # Dialog box for providing some information about this app
        QtWidgets.QMessageBox.about(self, 'Information',
                                    'With this App you can define your earnings based on your stock. \
        \nAlso all information about stocks are getting from Tinkoff Investment App \
        For better using you need to provide your Tinkoff Token from this page: \
        https://www.tinkoff.ru/invest/settings/')

    def customDialogBox(self, title, text):
        # Custom dialog box
        QtWidgets.QMessageBox.about(self, title, text)

    def getRealCost(self):
        # Get real cost of stock
        try:
            stock_name = self.stockNameTextEdit.toPlainText()
            earn, average, lots = self.parser_stock(stock_name)
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
        earn, average, lots = self.parser_stock('USD000UTSTOM')
        gain = earn / lots + average
        return gain

    def parser_stock(self, stock_name):
        # Get stock info from Tinkoff API Token
        token = self.apiTokenEditField.toPlainText()
        client = openapi.api_client(token)
        pf = client.portfolio.portfolio_get()
        state = False
        k = 0
        index = 0
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
            return float(earn), float(average), float(lots)

    def calculateEarning(self):
        # Calculate your earning
        try:
            stock_name = self.stockNameTextEdit.toPlainText()
            earn, average, lots = self.parser_stock(stock_name)
            stock_price_now = float(self.stockRealCostTextEdit.toPlainText())
            res = (lots*(stock_price_now - average))*self.usdToRub()
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
