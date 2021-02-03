#   This is apliaction for getting promotions from nearby shops
#   Autor: Habas Paweł
#   
#   
#   Python 3.8
#   
#   Project on Slenium & PyQt5
#
#   Window build on PyQt5 
#   Combo box with Key Words, Button and text area
#
#   Scraping Rossmann page looking for Key Words. 
#   Then in all found items i'm looking for products from my list. 
#   Only products with promo price will be displayed

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QComboBox
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

class okno(QWidget):

    produkty_ross = {'Chusteczki':[],'Kot':[]}
    produkty_wybrane_ross = {'Chusteczki':[],'Kot':[]}
    lista_ross= {'Chusteczki' : ['BABYDREAM','ISANA KIDS','dla dzieci','kids','dzieci','NIVEA'],'Kot' : ['żwir','WINSTON']}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interfejs()

    def interfejs(self):
        self.but_ross = QPushButton("Rossmann",self)

        self.cbr = QComboBox()
        self.cbr.addItems(['Chusteczki','Kot'])
        
        self.ta_main = QPlainTextEdit(self)
        self.ta_main.zoomIn(4)

        ukladT = QGridLayout()
        ukladT.addWidget(self.cbr,0,0)
        ukladT.addWidget(self.but_ross,1,0)
        ukladT.addWidget(self.ta_main,0,1,10,1)

        self.setLayout(ukladT)
        self.setWindowTitle("Promocje")
        self.setGeometry(50,50,1000,600)

        self.but_ross.clicked.connect(self.akt_ross)

        self.show()
    
    def akt_ross(self):
        ktore = self.cbr.currentText()
        print(ktore)
        if ktore == 'Chusteczki':
            self.akt_szukaj_ross(ktore)
        elif ktore == 'Kot':
            self.akt_szukaj_ross(ktore)        
        
    def akt_szukaj_ross(self,ktore='Chusteczki'):
        txt = ''
        if len(self.produkty_wybrane_ross[ktore]) == 0:
            url = 'https://www.rossmann.pl/szukaj?Search='+ktore.lower()+'&Page=1&PageSize=100&PriceFrom=0&PriceTo=600'
            
            driver = webdriver.Chrome()
            driver.get(url)

            time.sleep(25)      #   TODO    # Here I have to insert selenium "wait for load"
            
            elem = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/section[2]/div[1]')

            elementy = elem.find_elements_by_class_name('tile-product')

            for e in elementy:
                try:
                    tytul = e.find_element_by_tag_name('strong').text
                    subtytul = e.find_element_by_tag_name('span').text
                    pln =   e.find_element_by_class_name('tile-product__promo-price').text
                    pln_old = e.find_element_by_class_name('tile-product__old-price').text
                    
                    cena = float(pln.split(' ')[0].replace(',','.'))
                    cena_old = float(pln_old .split(' ')[0].replace(',','.'))
                    self.produkty_ross[ktore].append({'t':tytul,'s':subtytul,'c':cena,'oc':cena_old})
                except:
                    print(e.find_element_by_tag_name('strong').text,'-',e.find_element_by_tag_name('span').text)

            driver.close()
            
            if len(self.produkty_wybrane_ross[ktore]) == 0 :
                for prod in self.produkty_ross[ktore]:
                    for key in self.lista_ross[ktore]:
                        if prod['t'].lower().find(key.lower()) >= 0 or prod['s'].lower().find(key.lower()) >= 0:
                            if self.produkty_wybrane_ross[ktore].count(prod) == 0:
                                self.produkty_wybrane_ross[ktore].append(prod)
        i=1
        for prod in self.produkty_wybrane_ross[ktore]:
            txt+=str(str(i)+' : '+str(prod['t'])+' '+str(prod['s'])+' - '+str(prod['oc'])+'->'+str(prod['c'])+' zł\n')
            i+=1

        self.ta_main.clear()
        self.ta_main.appendPlainText(str(txt))
        
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    okno = okno()
    sys.exit(app.exec_())
