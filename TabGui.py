from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QApplication, QCheckBox, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTabWidget, QWidget
from web3 import exceptions as ex
from eth_account import Account
import secrets
import json
import web3
import time
import sys

from web3.types import GasPriceStrategy

mainnet = web3.HTTPProvider('http://85.214.94.10:8545') #Mainnet (ChainID 1)
testnet = web3.HTTPProvider('http://85.214.95.88:8545') #Goerli Testnet (Chain ID 5)

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('Web3 Application')
        self.setFixedSize(412, 355)
        winlay = QGridLayout()
        self.setLayout(winlay)

        self.TabWidget = QTabWidget()
        winlay.addWidget(self.TabWidget, 0, 0)

        
        self.w3 = web3.Web3(mainnet)
        self.cid = 1
        self.loop = True

        #Tab 1 Check Balance, create all Widgets in GridLayout
        self.tab1 = QWidget()
        blclay = QGridLayout()
        self.tab1.setLayout(blclay)

        blclabel1 = QLabel('Input Address:')
        self.blclabel2 = QLabel('Balance:')
        self.blctext = QLineEdit('')
        blcbtn = QPushButton('Check Balance')

        blcbtn.clicked.connect(self.checkBalance)

        blclay.addWidget(blclabel1, 0, 0)
        blclay.addWidget(self.blctext, 1, 0)
        blclay.addWidget(self.blclabel2, 2, 0)
        blclay.addWidget(blcbtn, 3, 0)
        self.tab1.setFixedHeight(120)

        #Tab 2 send Transactions, create all Widgets in GridLayout
        self.tab2 = QWidget()
        txnlay = QGridLayout()
        self.tab2.setLayout(txnlay)

        txnlabel1 = QLabel('Your secret Key:')
        txnlabel2 = QLabel('Amount:')
        txnlabel3 = QLabel('To(public Address):')
        self.txnlabel4 = QLabel('All Transactions will use the current Gas Fee.\nIf you choose send all, you will have an blank Wallet after that Transaction.')
        self.txntext1 = QLineEdit() #secret key
        self.txntext2 = QLineEdit() #Amount
        self.txntext3 = QLineEdit() #Public Address from receiver
        self.txncb = QCheckBox('Send all')
        txnbtn = QPushButton('send ETH')

        txnbtn.clicked.connect(self.createTxn)

        txnlay.addWidget(txnlabel1, 0, 0)
        txnlay.addWidget(txnlabel2, 2, 0)
        txnlay.addWidget(txnlabel3, 4, 0)
        txnlay.addWidget(self.txnlabel4, 8, 0)
        txnlay.addWidget(self.txntext1, 1, 0)
        txnlay.addWidget(self.txntext2, 3, 0)
        txnlay.addWidget(self.txntext3, 5, 0)
        txnlay.addWidget(self.txncb, 7, 0)
        txnlay.addWidget(txnbtn, 6, 0)


        #Tab 3 Create new ETH Wallets, create all Widgets in GridLayout
        self.tab3 = QWidget()
        crelay = QGridLayout()
        self.tab3.setLayout(crelay)
        

        crelabel1 = QLabel('Public address:')
        crelabel2 = QLabel('Secret address:')
        self.crelabel3 = QLabel()
        self.cretext1 = QLineEdit() #public address
        self.cretext2 = QLineEdit() #secret address
        crebtn1 = QPushButton('Create new address')
        crebtn2 = QPushButton('Save data')

        crebtn1.clicked.connect(self.create)
        crebtn2.clicked.connect(self.saveData)

        crelay.addWidget(crelabel1, 0, 0)
        crelay.addWidget(crelabel2, 3, 0)
        crelay.addWidget(self.cretext1, 2, 0)
        crelay.addWidget(self.cretext2, 4, 0)
        crelay.addWidget(crebtn1, 5, 0)
        crelay.addWidget(crebtn2, 6, 0)
        crelay.addWidget(self.crelabel3, 7, 0)
        self.tab3.setFixedHeight(180)

        #Tab 4 show some Blockchain statistics, create all Widgets in GridLayout
        self.tab4 = QWidget()
        stalay = QGridLayout()
        self.tab4.setLayout(stalay)

        self.stalabel1 = QLabel('Blockchain: ')
        self.stalabel2 = QLabel('Blockcount: ')
        self.stalabel3 = QLabel('avg. Blocktime: ')
        self.stalabel4 = QLabel('Latest Block Hash: ')
        self.stalabel5 = QLabel('Latest Block Miner: ')
        self.stalabel6 = QLabel('Latest Block Time: ')
        self.stabtn = QPushButton('Get latest Stats')

        stalay.addWidget(self.stalabel1, 0, 0)
        stalay.addWidget(self.stalabel2, 1, 0)
        stalay.addWidget(self.stalabel3, 2, 0)
        stalay.addWidget(self.stalabel4, 3, 0)
        stalay.addWidget(self.stalabel5, 4, 0)
        stalay.addWidget(self.stalabel6, 5, 0)
        stalay.addWidget(self.stabtn, 6, 0)

        self.stabtn.clicked.connect(self.getStatistics)

        #Add all Tabs to TabWidget
        self.TabWidget.addTab(self.tab1, 'Check Balance')
        self.TabWidget.addTab(self.tab2, 'Transaction')
        self.TabWidget.addTab(self.tab3, 'Create Address')
        self.TabWidget.addTab(self.tab4, 'Blockchain statistics')

        #Note Label
        notelabel = QLabel('If the Görli Testnet Checkbox isn`t checked, all Tools will use the Ethereum \nMainnet!')
        self.netcb = QCheckBox('Görli Testnet')
        winlay.addWidget(notelabel, 1, 0)
        winlay.addWidget(self.netcb, 2, 0)

    #Alle needed Functions
    def netSelect(self):
        if self.netcb.isChecked():
            self.w3 = web3.Web3(testnet)
            self.cid = 5
        else:
            self.w3 = web3.Web3(mainnet)
            self.cid = 1

    def checkBalance(self):
        self.netSelect()

        if self.blctext.text() == '':
            self.blclabel2.setText('Add an Address!')
        else: 
            try:
                blc = self.w3.eth.get_balance(self.blctext.text())
                self.blclabel2.setText('Balance: ' + str(self.w3.fromWei(blc, 'ether')) + ' ETH')
            except ex.InvalidAddress:
                self.blclabel2.setText('Add an Valid Address')
            except ValueError:
                self.showError('Node Error!')

    def create(self):
        sec = secrets.token_hex(32)
        pub = Account.from_key(sec)

        self.cretext1.setText(str(pub.address))
        self.cretext2.setText(str(sec))

    def saveData(self):
        if self.cretext1.text() == '':
            self.crelabel3.setText('Create an Address before you save!')
        else:
            file_name = self.cretext1.text() + '.json'
            string = {"Secrete address: ": self.cretext2.text(), 
                      "Public address": self.cretext1.text()}
            file = open(file_name, "w")
            file.write(json.dumps(string))
            file.close()
            self.crelabel3.setText('Data saved')

    def createTxn(self):
        self.netSelect()

        if self.w3.isConnected():
            if self.txntext1.text() != '':
                if self.validateSecretKey(self.txntext1.text()):
                    if self.validateAddress(self.txntext3.text()):
                        if self.txncb.isChecked():
                            blc = self.w3.eth.get_balance(Account.from_key(self.txntext1.text()).address)
                            gas = self.w3.eth.gasPrice * 21000
                            value = blc - gas
                            if value > 0:
                                self.sendTransaction(self.txntext1.text(), self.cid, self.w3.fromWei(value, 'ether'), self.txntext3.text())
                            else:
                                self.txnlabel4.setText('Your ETH is lower than the actual GasFee!')
                        else:
                            if self.txntext2.text() != '':
                                if self.validateAmount(self.txntext2.text()):
                                    blc = self.w3.eth.get_balance(Account.from_key(self.txntext1.text()).address)
                                    amount = float(self.txntext2.text())
                                    if amount < blc:
                                        gas = self.w3.eth.gasPrice * 21000
                                        blcgas = self.w3.toWei(amount, 'ether') + gas
                                        if blcgas < blc:
                                            self.sendTransaction(self.txntext1.text(), self.cid, amount, self.txntext3.text())
                                        else:
                                            self.txnlabel4.setText('Your Amount + GasFee is higher then your actual balance!\nPlease adjust your amount!')
                                    else:
                                        self.txnlabel4.setText('Your Amount is higher than your actual balance!')
                                else: 
                                    self.txnlabel4.setText('Please enter an valid amount of ETH like 0.00!')
                            else:
                                self.txnlabel4.setText('Use Send all or send an specific Amount of ETH!')
                    else:
                        self.txnlabel4.setText('Please enter an valid receiving address!')
                else:
                    self.txnlabel4.setText('Please enter an valid Secret Key!')
            else: 
                self.txnlabel4.setText('Please enter your Secret Key!')
        else:
            self.txnlabel4.setText('No Blockchain connection!')
        
    def sendTransaction(self, secret_key, cid, value, to):
        tx = self.w3.eth.account.sign_transaction({
            'chainId': cid,
            'nonce': self.w3.eth.getTransactionCount(Account.from_key(secret_key).address),
            'to': to, 
            'value': self.w3.toWei(value, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gasPrice
        }, secret_key)
        try:
            self.w3.eth.send_raw_transaction(tx.rawTransaction)
            self.txnlabel4.setText('Transaction send.')
        except:
            self.txnlabel4.setText('Error occured while sending your Transaction.\nPlease check your Secret Key, your available ETH and the recieving address!')

    def validateAddress(self, acc):
        if self.w3.isConnected:
            try: 
                blc = self.w3.eth.get_balance(acc)
                return True
            except ex.InvalidAddress:
                return False
        else:
            return False

    def validateSecretKey(self, key):
        try:
            acc = Account.from_key(key)
            return True
        except:
            return False

    def validateAmount(self, str):
        try:
            value = float(str)
            return True
        except:
            return False

    def testOtherFunctions(self):
        print(self.validateAmount(self.txntext2.text()))

    def getStatistics(self):
        self.netSelect()
        self.stalabel2.setText('Blockcount: ' + str(self.w3.eth.get_block_number()))

    def showError(self, error_msg):
        msg = QMessageBox()
        msg.setText(error_msg)
        msg.setWindowTitle('Error')
        msg.exec_()

#create Window
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()