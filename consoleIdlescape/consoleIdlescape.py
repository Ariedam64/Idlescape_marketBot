from typing import List
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
import random
from selenium.webdriver import ActionChains
from datetime import datetime
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import sys
import time

from selenium.webdriver.remote.webelement import WebElement

class Telegram:

    def __init__(self, m_wd):
            self.token = '5328440960:AAH-OtrbLtk7eOf0fjLhSb5Gjex3lE-Rbps'
            self.methodSendMessage = 'sendMessage'
            self.methodGetMessage = 'getUpdates'
            self.myuserid = 5202661069
            self.lastUpdate = 0
            self.currentUpdate = 0
            self.messInit()
            self.threadMess = Thread(target=self.checkCommandsBot, daemon=True)
            self.wd = m_wd

    def start(self):
        self.threadMess.start()
        return self

    def sendMess(self, content):
        requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(self.token, self.methodSendMessage),
            data={'chat_id': self.myuserid, 'text': content}
        ).json()

    def messInit(self):
        result = requests.get(url='https://api.telegram.org/bot{0}/{1}'.format(self.token, self.methodGetMessage)).json()
        num_updates = len(result["result"])
        self.lastUpdate = num_updates - 1
        self.currentUpdate = num_updates

    def getUpdate(self):
        result = requests.get(url='https://api.telegram.org/bot{0}/{1}'.format(self.token, self.methodGetMessage)).json()
        num_updates = len(result["result"])
        self.lastUpdate = num_updates - 1

    def getLastMess(self):
         result = requests.get(url='https://api.telegram.org/bot{0}/{1}'.format(self.token, self.methodGetMessage)).json()
         text = result["result"][self.lastUpdate]["message"]["text"]
         return (text)

    def incrementCurrentUpdate(self):
        self.currentUpdate += 1

    def cmdQte(self):
        self.sendMess('Total acheté: x' + self.wd.getTotalQte())
        self.incrementCurrentUpdate()

    def cmdPrice(self):
        self.sendMess('Total depensé: ' + self.wd.getTotalPrice() + ' gold')
        self.incrementCurrentUpdate()

    def cmdTime(self):
        self.sendMess('Bot actif depuis: ' + self.wd.getTotalTime())
        self.incrementCurrentUpdate()

    def cmdPutOnMarket(self):
        self.sendMess("Items mis en vente: x" + self.wd.getTotalPutOnMarket())
        self.incrementCurrentUpdate()

    def cmdItemPrice(self):
        self.sendMess("Prix minimum de vente: " + self.wd.getItemPrice() + ' gold')
        self.incrementCurrentUpdate()

    def cmdRefreshTime(self):
        self.sendMess("Temps refresh du market: \n" + self.wd.getRefreshTimeMin() + ' - ' + self.wd.getRefreshTimeMax())
        self.incrementCurrentUpdate()

    def cmdSoldTime(self):
        self.sendMess("Temps de remise en vente: \n" + self.wd.getSoldTimeMin() + ' - ' + self.wd.getSoldTimeMax())
        self.incrementCurrentUpdate()

    def cmdNotifBuy(self):
        self.wd.updateNotifBuyState()
        self.sendMess("Notification d'achat: " + self.wd.isNotifBuy())
        self.incrementCurrentUpdate()

    def cmdNotifSold(self):
        self.wd.updateNotifSoldState()
        self.sendMess("Notification de vente: " + self.wd.isNotifSold())
        self.incrementCurrentUpdate()

    def cmdNotifPutOnMarket(self):
        self.wd.updateNotifPutOnMarketState()
        self.sendMess("Notification de remise en vente: " + self.wd.isNotifPutOnMarket())
        self.incrementCurrentUpdate()

    def cmdIsActif(self):
        self.wd.updateIsActif()
        self.sendMess("Etat du bot: " + self.wd.getIsActif())
        self.incrementCurrentUpdate()

    def cmdCheckingChat(self):
        self.wd.updateCheckingChatState()
        self.sendMess("Vérification du chat: " + self.wd.isCheckingChat())
        self.incrementCurrentUpdate()

    def cmdSetRefreshTime(self):
        self.wd.limitPrice = self.getLastMess().split(' ', 1)[1]

        self.sendMess("Prix minimum de vente: " + self.wd.getItemPrice() + ' gold')

    def cmdSetPrice(self):
        if (len(self.getLastMess().split(' ', 1)) != 2):
            self.sendMess("Erreur: Veuillez saisir une valeur (ex: /setPrice 1029)")
        else:
            try:
                self.wd.limitPrice = int(self.getLastMess().split(' ', 1)[1])
                self.sendMess("M.A.J du prix minimum de vente: " + self.wd.getItemPrice() + ' gold')
            except ValueError:
                self.sendMess("Erreur: La valeur donner doit être un nombre entier")
        self.incrementCurrentUpdate()

    def cmdSetRefreshTime(self):
        if (len(self.getLastMess().split(' ', 2)) != 3):
            self.sendMess("Erreur: Veuillez saisir deux valeurs (ex: /setRefreshTime 10 20)")
        else:
            try:
                self.wd.minRefreshMarketTime = int(self.getLastMess().split(' ', 2)[1])
                self.wd.maxRefreshMarketTime = int(self.getLastMess().split(' ', 2)[2])
                self.sendMess("M.A.J du temps de refresh du market: \n" + self.wd.getRefreshTimeMin() + ' - ' + self.wd.getRefreshTimeMax())
            except ValueError:
                self.sendMess("Erreur: Les valeurs donner doit être des nombres entiers")
        self.incrementCurrentUpdate()

    def cmdSetPutTime(self):
        if (len(self.getLastMess().split(' ', 2)) != 3):
            self.sendMess("Erreur: Veuillez saisir deux valeurs (ex: /setPutTime 20 250)")
        else:
            try:
                self.wd.minRefreshSoldTime = int(self.getLastMess().split(' ', 2)[1])
                self.wd.maxRefreshSoldTime = int(self.getLastMess().split(' ', 2)[2])
                self.sendMess("M.A.J du temps de remise en vente: \n" + self.wd.getSoldTimeMin() + ' - ' + self.wd.getSoldTimeMax())
            except ValueError:
                self.sendMess("Erreur: Les valeurs donner doit être des nombres entiers")
        self.incrementCurrentUpdate()

    def cmdSetItem(self):
        if (len(self.getLastMess().split(' ', 1)) != 2):
            self.sendMess("Erreur: Veuillez saisir un nom d'item (ex: /setItem Mithril Ore)")
        else:
            self.wd.isActif = False
            self.wd.browser.find_element(By.CLASS_NAME, 'marketplace-back-button').click()
            self.wd.browser.implicitly_wait(2)
            try:
                newItem = str(self.getLastMess().split('/setItem ', 1)[1])            
                if (self.wd.isItemImg(newItem) != ''):
                    self.wd.setItemImg(newItem)
                    self.wd.itemName = newItem
                    self.wd.actions.move_to_element(self.wd.browser.find_element(By.XPATH, "//img[contains(@src, '" + self.wd.itemImg + "')]")).click().perform()
                    self.sendMess("M.A.J de l'item mis en vente")
            except:
                self.wd.actions.move_to_element(self.wd.browser.find_element(By.XPATH, "//img[contains(@src, '" + self.wd.itemImg + "')]")).click().perform()
                self.sendMess("Erreur: L'item que vous avez saisi n'existe pas")
        self.wd.isActif = True
        self.incrementCurrentUpdate()

    def checkCommandsBot(self):       
        while True:
            time.sleep(2)
            self.getUpdate()
            if (self.currentUpdate == self.lastUpdate):
                if(self.getLastMess() == '/help'):
                   self.sendMess("""
Liste de commandes: \n
------------------------Récupération------------------------- \n
/info - Renvoi toutes les informations concernant le bot \n
-------------------------Paramétrage-------------------------\n
/setItem {item} - Définis un nouveau item 
/setPrice {prix} - Définis un nouveau prix minimum de mise en vente
/setRefreshTime {min} {max} - Définis le temps de rafraichissement du market en secondes
/setPutTime {min} {max} - Définis le temps de remise en vente en secondes
/setActif - Rend actif ou inactif le bot
/setCheckingChat - Rend actif ou inactif la vérification du chat \n
------------------------Notifications------------------------ \n
/notifBuy - Active/Désactive les notifications d'achats
/notifSold - Active/Désactive les notifications l'orsque l'item n'est plus en vente  
/notifPutOnMarket - Active/Désactive les notifications lors de la remise en vente
                   """)
                   self.incrementCurrentUpdate()
                elif(self.getLastMess() == '/info'):
                   self.sendMess("Etat du bot: " + self.wd.getIsActif() + "\nVérification du chat: " + self.wd.isCheckingChat() + "\nTemps d'activité: " + self.wd.getTotalTime() + "\nItem: " + self.wd.itemName + "\nTotal récupérés: x" +  self.wd.getTotalQte() + "\nTotal dépensé: " + self.wd.getTotalPrice() + ' gold'+ "\nTotal mis en vente : x" + self.wd.getTotalPutOnMarket() + "\nPrix de vente minimal: " + self.wd.getItemPrice() + ' gold \nTemps de rafraichissement du market:\n' + self.wd.getRefreshTimeMin() + ' - ' + self.wd.getRefreshTimeMax() + "\nTemps de rafraichissement de vente:\n" + self.wd.getSoldTimeMin() + ' - ' + self.wd.getSoldTimeMax() + "\nNotification d'achat: " + self.wd.isNotifBuy() + "\nNotification de vente: " + self.wd.isNotifSold() + "\nNotification de remise en vente: " + self.wd.isNotifPutOnMarket())
                   self.incrementCurrentUpdate()
                elif(self.getLastMess() == '/setCheckingChat'):
                    self.cmdCheckingChat()
                elif(self.getLastMess() == '/setActif'):
                    self.cmdIsActif()
                elif(self.getLastMess() == '/notifBuy'):
                    self.cmdNotifBuy()
                elif(self.getLastMess() == '/notifSold'):
                    self.cmdNotifSold()
                elif(self.getLastMess() == '/notifPutOnMarket'):
                    self.cmdNotifPutOnMarket()
                elif(self.getLastMess().split(' ', 1)[0] == '/setPrice'):
                    self.cmdSetPrice()
                elif(self.getLastMess().split(' ', 1)[0] == '/setRefreshTime'):
                    self.cmdSetRefreshTime()
                elif(self.getLastMess().split(' ', 1)[0] == '/setPutTime'):
                    self.cmdSetPutTime()
                elif(self.getLastMess().split(' ', 1)[0] == '/setItem'):
                    self.cmdSetItem()
                else:
                    self.incrementCurrentUpdate()
                
        pass

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):

        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()

        pass

class WebDriver:
    def __init__(self, m_limitPrice, m_time):
        self.limitPrice = m_limitPrice
        self.time = m_time
        self.isCheckChat = True
        self.listFoundMessage = set()
        self.sellTime = datetime.now().strftime("%H:%M:%S")
        self.itemName = "Mithril Ore"
        self.itemImg = ''
        self.lastItem = ""
        self.foundList = {''}
        self.listMessage = set()
        self.PATH = Service('C:\chromedriver.exe')
        self.urlJeu = 'https://idlescape.com/game'
        self.browser = None
        self.found = True
        self.notifBuy = True
        self.notifSold = False
        self.notifPutOnMarket = False
        self.isActif = True
        self.randomPrice = 0
        self.nbPassage = 1
        self.totalQte = 0
        self.totalPrice = 0
        self.totalTime = 0
        self.totalPutOnMarket = 0
        self.minRefreshMarketTime = 30
        self.maxRefreshMarketTime = 500
        self.minRefreshSoldTime = 40
        self.maxRefreshSoldTime = 300
        self.actions = 0
        self.telBot = Telegram(self)
        self.startDate = datetime.now()
        self.options = webdriver.ChromeOptions()

    def wdOptionsInjection(self):
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("user-data-dir=C:\\Users\\Romann\\AppData\\Local\\Google\\Chrome\\nv")
        #self.options.add_argument("--headless")
 
    def start(self):
        try:
            wd0 = Loader("Initialisation du bot Telegram ", "Initialisation du bot Telegram : OK").start()
            self.telBot.start()
            wd0.stop()

            wd1 = Loader("Initialisation des options du webDriver ", "Initialisation des options du webDriver : OK").start()
            self.wdOptionsInjection()
            wd1.stop()

            wd2 = Loader("Implémentation des options dans le webDriver ", "Implémentations des options du webDriver : OK").start()
            self.browser = webdriver.Chrome(service=self.PATH, options=self.options)
            self.actions = ActionChains(self.browser)
            wd2.stop()

            wd3 = Loader("Connection à Idlescape ", "Connection à Idlescape : OK").start()
            self.browser.get(self.urlJeu) #On se connecte au site
            wd3.stop()
            
        except:
            print('Impossible de lancer le webDriver')

    def connectToMarket(self):
        try:
             wd4 = Loader("Accès au market en cours ", "Accès au market : OK").start()
             self.browser.find_element(By.CLASS_NAME, 'character-select-container').click()
             self.browser.implicitly_wait(4)
             self.browser.find_element(By.CLASS_NAME, 'close-dialog-button').click()       
             self.browser.implicitly_wait(2)
             self.browser.find_element(By.CLASS_NAME, 'navbar1-box').click()
             self.browser.implicitly_wait(2)
             self.browser.find_element(By.XPATH, '//*[text()="Marketplace"]').click()  
             self.browser.implicitly_wait(2)
             self.setItemImg(self.itemName)
             threadCheckChat = Thread(target=self.checkChat, daemon=True)
             threadCheckChat.start()
             self.actions.move_to_element(self.browser.find_element(By.XPATH, "//img[contains(@src, '" + self.itemImg + "')]")).click().perform()
   
        except:
            print("Impossible d'acceder au market")
        
        wd4.stop()

    def checkChat(self):

        while True:
           if self.isCheckChat == True and self.isActif:
               htmlMarket2 = self.browser.page_source #Récupère le code HTML du site chargé
               soupMarket2 = BeautifulSoup(htmlMarket2, 'html.parser') #On définie notre hasher
               for chatMessage in soupMarket2.find_all('div',{"class": "chat-message"}):           
                
                        if len(chatMessage.find_all("span")) > 2:
                            message = str(chatMessage.find_all("span")[3].text)
                            heure = str(chatMessage.find_all("span")[0].text)
                            pseudo = str(chatMessage.find_all("span")[1].text)
                    
                        if (message.find('style="position: absolute; top: 0px; left: 0px; width: 100%; height: 100%;">')) == -1:
                            messToSend = heure + pseudo + ": " + message
                            self.listMessage.add(messToSend)

               time.sleep(5)
               if len(self.listMessage) > 0:
                    for mess in self.listMessage:
                        message = mess.lower()
                        if message.find(" mith ".lower()) != -1 or message.find("mithril".lower()) != -1 or message.find("market manipulation".lower()) != -1:
                            if (mess not in self.listFoundMessage):
                                self.listFoundMessage.add(mess)
                                self.telBot.sendMess("Désactivation automatique du bot suite au message suivant: \n" + mess)
                                self.updateIsActif()

    def checkMarket(self):

        wd5 = Loader("Vérification des valeurs en cours ").start()
        self.telBot.sendMess('Vérification des valeurs en cours')
        while True:

            if self.isActif == True:
                self.browser.implicitly_wait(2)
                self.browser.find_element(By.XPATH, '//*[@id="marketplace-refresh-button"]').click()
                time.sleep(3) 

                htmlMarket = self.browser.page_source #Récupère le code HTML du site chargé
                soupMarket = BeautifulSoup(htmlMarket, 'html.parser') #On définie notre hasher
                soupMarket.find_all("table", {"class": "crafting-table marketplace-table"})

                item = soupMarket.find_all('tr')[1]
                quantite = item.find_all('td')[2].text
                prix = item.find_all('td')[3].text
                prix = prix.replace(" ", "")
                quantite = quantite.replace(" ", "")
                self.lastItem = item.find_all('td')[0].text + '| x' + quantite + ', ' + prix
            
                prix = int(prix)
                if prix < self.randomPrice and self.lastItem not in self.foundList:
                    self.foundList.add(self.lastItem)             
                    self.buyMaxItem()
                    self.totalPrice += int(prix) * int(quantite)
                    self.totalQte += int(quantite)
                    if self.notifBuy:
                        self.telBot.sendMess(datetime.now().strftime("%H:%M:%S") + ': Achat de ' + str(self.lastItem))
                elif prix > self.randomPrice:
                    if self.notifSold:
                        self.telBot.sendMess(datetime.now().strftime("%H:%M:%S") + ': Votre ' + self.itemName + ' a été vendu')
                    self.foundList = {''}
                    self.found = False
                    time.sleep(random.randint(self.minRefreshSoldTime, self.maxRefreshSoldTime))
                    self.sellNewItem()
                    if self.notifPutOnMarket:
                        self.telBot.sendMess(datetime.now().strftime("%H:%M:%S") + ': Mise en vente x1 ' + self.itemName + ' a ' + str(self.limitPrice))
                    self.totalPutOnMarket += 1
                time.sleep(random.randint(self.minRefreshMarketTime, self.maxRefreshMarketTime))         
                self.nbPassage += 1

        wd5.stop()

    def getLastItem(self):
        return str(self.lastItem)

    def isFound(self):
        return str(self.found)

    def getTotalQte(self):
        return str("{:,}".format(self.totalQte))

    def getTotalPrice(self):
        return str("{:,}".format(self.totalPrice))

    def getItemPrice(self):
        return str("{:,}".format(self.limitPrice))

    def setItemImg(self, item):
        self.itemImg = self.browser.find_element(By.XPATH, "//img[contains(@alt, '" + item + "')]").get_attribute("src").replace("https://idlescape.com", "")

    def isItemImg(self, item):
        return self.browser.find_element(By.XPATH, "//img[contains(@alt, '" + item + "')]").get_attribute("src").replace("https://idlescape.com", "")

    def isNotifBuy(self):
        if(self.notifBuy):
            return 'Activé'
        return 'Désactivé'

    def updateNotifBuyState(self):
        self.notifBuy = not self.notifBuy

    def isCheckingChat(self):
        if(self.isCheckChat):
            return 'Activé'
        return 'Désactivé'

    def updateCheckingChatState(self):
        self.isCheckChat = not self.isCheckChat

    def isNotifSold(self):
        if(self.notifSold):
            return 'Activé'
        return 'Désactivé'

    def updateNotifSoldState(self):
        self.notifSold = not self.notifSold

    def isNotifPutOnMarket(self):
        if(self.notifPutOnMarket):
            return 'Activé'
        return 'Désactivé'

    def updateNotifPutOnMarketState(self):
        self.notifPutOnMarket = not self.notifPutOnMarket

    def getIsActif(self):
        if(self.isActif):
            return 'Actif'
        return 'Inactif' 

    def updateIsActif(self):
        self.isActif = not self.isActif

    def getRefreshTimeMin(self):
        sec = self.minRefreshMarketTime % (24 * 3600)
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02ds" % (min, sec)

    def getRefreshTimeMax(self):
        sec = self.maxRefreshMarketTime % (24 * 3600)
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02ds" % (min, sec)

    def getSoldTimeMin(self):
        sec = self.minRefreshSoldTime % (24 * 3600)
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02ds" % (min, sec)

    def getSoldTimeMax(self):
        sec = self.maxRefreshSoldTime % (24 * 3600)
        sec %= 3600
        min = sec // 60
        sec %= 60
        return "%02d:%02ds" % (min, sec)

    def getTotalTime(self):
        totalTime = str(datetime.now() - self.startDate)
        totalTime = totalTime.split('.', 1)[0]
        totalTime = totalTime + 's'
        return str(totalTime)

    def getTotalPutOnMarket(self):
        return str(self.totalPutOnMarket) + ' ' + self.itemName

    def buyMaxItem(self):
        try:
            self.browser.implicitly_wait(1)
            self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div[4]/div[2]/div[2]/div[1]/div[2]/div/table/tbody/tr[1]').click()
            self.browser.implicitly_wait(2)
            self.browser.find_element(By.XPATH, '//*[text()="Buy Max"]').click()
            self.browser.implicitly_wait(2)
            self.browser.find_element(By.XPATH, '//*[text()="Buy"]').click()
        except:
            self.telBot.sendMess("Erreur lors de l'achat du mithril \nPassage du bot dans l'état inactif")
            self.isActif = False

    def sellNewItem(self):
        try:
            self.browser.implicitly_wait(2)
            self.browser.find_element(By.CLASS_NAME, 'marketplace-back-button').click()
            self.browser.implicitly_wait(2)
            self.browser.find_element(By.XPATH, '//*[text()="Sell"]').click()
            self.browser.implicitly_wait(2)
            try:
                self.actions.move_to_element(self.browser.find_element(By.XPATH, "//img[contains(@src, '" + self.itemImg + "')]")).click().perform()
                self.browser.implicitly_wait(2)
                self.randomPrice = random.randint(self.limitPrice-5, self.limitPrice+5)
                self.browser.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/input').send_keys(self.randomPrice)
                self.browser.implicitly_wait(2)
                self.browser.find_element(By.XPATH, '//*[text()="Sell"]').click()
                self.browser.implicitly_wait(2)
            except:
                self.telBot.sendMess("Vous n'avez plus de " + self.itemName + "\nPassage du bot dans l'état inactif")
                self.isActif = False
            self.browser.find_element(By.XPATH, '//*[text()="Buy"]').click()
            self.browser.implicitly_wait(2)
            self.actions.move_to_element(self.browser.find_element(By.XPATH, "//img[contains(@src, '" + self.itemImg + "')]")).click().perform()
        except:
            self.telBot.sendMess("Erreur lors de la vente du mithril \nPassage du bot dans l'état inactif")
            self.isActif = False

        pass


print('-----------------------------------------------------DEBUT DU PROGRAMME'+ "\n"+ "\n"+ "\n")

wd = WebDriver(1712, random.randint(35, 254))
wd.start()
wd.connectToMarket()
wd.checkMarket()

print('-------------------------------------------------------FIN DU PROGRAMME')



