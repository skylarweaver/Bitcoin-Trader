# Skylar Weaver
#112 Term Project
# Bitcoin Trading Application

import MtGoxAPI
import EmailAlert
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import re
import json
import json_ascii
import urllib
import urllib2
import urlparse
import simplejson
import webbrowser
import lxml.html
API = MtGoxAPI.Client()


# ** THIS PROGRAM IS ONLY AS RELIABLE AS YOUR INTERNET CONNECTION AND
# ** MT.GOX'S SERVER **

#create all functions for the portfolio page to use
class Portfolio(object):
	def __init__(self,initialInvestment = 0, sendAddress=None, sendAmount = None,
				 fee_int="", no_instant=False, green = False):
		self.initialInvestment = initialInvestment
		self.sendAddress = sendAddress
		self.sendAmount_int = sendAmount
		self.fee_int = fee_int
		self.no_instant = no_instant
		self.green = green
	def initialInvestment(self):
		pass
	#Returns the amount of bitcoins in one's mtGox wallet
	def bitcoinsInWallet(self):
		return API.get_balance()["btcs"]
	# returns the amount of USD in one's MtGox wallet
	def USDInWallet(self):
		return API.get_balance()["usds"]
	#displays percent change in initialInvestment
	def percentChange(self):
		return (float(self.USDInWallet()) / initialInvestment) *100
	def profit(self):
		return ((float(self.USDInWallet()) + 
			float(self.bitcoinsInWallet())*API.get_ticker()["last"]) - 
		self.initialInvestment)
	def withdrawbitcoins(self):
		API.bitcoin_withdraw(self,self.sendAddress,self.sendAmount_int,
						self.fee_int,self.no_instant,self.green)
portfolio = Portfolio()






#class for the investment button
class InvestmentPopup(tkSimpleDialog.Dialog):
	def body(self, master):
		self.investmentData = None
		Label(master, text="USD").grid(row=0)
		Label(master, text="BTCS").grid(row=1)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		return self.e1 # initial focus
	def apply(self):
		USD = self.e1.get()
		BTCS= self.e2.get()
		global InputInitialInvestmentVariable 
		InputInitialInvestmentVariable = (USD,BTCS)

#for the buy button
class BuyPopup(tkSimpleDialog.Dialog):
	def body(self, master):
		self.buyInfo = None
		Label(master, text="Num BTCs").grid(row=0)
		Label(master, text="Price").grid(row=1)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		return self.e1 # initial focus
	def apply(self):
		numBTCS = self.e1.get()
		price= self.e2.get()
		global buyData
		buyData = (numBTCS,price)
#for the sell button
class SellPopup(tkSimpleDialog.Dialog):
	def body(self, master):
		self.sellData = None
		Label(master, text="Num BTCS").grid(row=0)
		Label(master, text="Price").grid(row=1)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		return self.e1 # initial focus
	def apply(self):
		bitcoinsToSell = self.e1.get()
		sellPrice= self.e2.get()
		global sellData
		sellData = (bitcoinsToSell,sellPrice)

#for the set text alert button
class SetTextAlert(tkSimpleDialog.Dialog):
	def body(self, master):
		self.sellData = None
		Label(master, text="Alert Price").grid(row=0)
		self.e1 = Entry(master)
		self.e1.grid(row=0, column=1)
		return self.e1 # initial focus
	def apply(self):
		alertPrice = None
		alertPrice = self.e1.get()
		global textAlertData
		textAlertData = None
		textAlertFile = open("textAlertData.txt", "r")
		if alertPrice not in textAlertFile:
			textAlertData = (alertPrice)
		textAlertFile.close()
#for the delete text alert button
class DeleteTextAlert(tkSimpleDialog.Dialog):
	def body(self, master):
		Label(master, text="Delete Price:").grid(row=0)
		self.e1 = Entry(master)
		self.e1.grid(row=0, column=1)
		return self.e1 # initial focus
	def apply(self):
		global priceToDelete
		priceToDelete = None
		if self.e1.get().isdigit():
			priceToDelete= self.e1.get()

class SetupPhone(tkSimpleDialog.Dialog):
	def body(self, master):
		self.sellData = None
		Label(master, text="Phone Number").grid(row=0)
		Label(master, text="Phone Carrier").grid(row=1)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		return self.e1 # initial focus
	def apply(self):
		phoneNumber = self.e1.get()
		phoneCarrier= self.e2.get()
		global phoneData
		try:
			#use reg expression to ensure correct input fo phone number
			newPhoneNumber=re.match("^[0-9]?([0-9]{3}).?([0-9]{3}).?([0-9]{4})$"
									, phoneNumber)
			newPhoneNumber = ( "".join([newPhoneNumber.group(i) 
								for i in xrange(1,4)]))
			phoneData = (newPhoneNumber,phoneCarrier)
		except:
			pass

#class for buying and selling
#For my own account security, the secret key I use for the API is set to only
#be allowed to retrieve account info and deposit. If this project were real,
#I could easiy set my key allow trading, and that would make this class fully 
#functional.
class Trade(object):
	def __init__(self, tradeType, bitcoins=None, price=None, amount=None):
		self.type = tradeType
		self.tradebitcoins= bitcoins
		self.tradePrice = price
		self.tradeAmount = amount
	#connects to API to buy and sell
	#for demo and testing pruposes, trading is temp disabled
	def buy(self):
		self.type = "bid"
		API.order_new(self.type, self.tradeAmount, 
						self.tradePrice, protection)
	def sell(self):
		self.type = "ask"
		API.order_new(self.type, self.tradeAmount, 
						self.tradePrice, protection)






#draw the application
class GUI(object):
	#initialize everything, calling the API prefferably only once
	#and at the beginning because it is slow and unreliable
	def init(self):
		self.width = self.canvas.winfo_reqwidth() - 4
		self.height = self.canvas.winfo_reqheight() - 4
		self.image = PhotoImage(file="sms2.gif")
		self.smallImage = self.image.subsample(1,1)
		self.imageWidth = 60
		self.imageHeight = 60
		self.tickerHeight = 50
		self.showPortfolio = True
		self.showTrade = False
		self.showNews = False
		self.showTicker =True
		self.showBuy = True
		self.showSell = False
		self.showAlert = False
		self.headerHeight = 0.135 * self.height
		self.tabWidth = (self.width/3)
		#open files for reading
		self.textAlertFile = open("textAlertData.txt", "r+")
		self.phoneDataFile = open("phoneData.txt", "r")
		self.dataFileUSD = open("termDataUSD.txt","r")
		self.dataFileBTC = open("termDataBTC.txt","r")
		self.initialInvestmentUSD = float(self.dataFileUSD.readline())
		self.initialInvestmentBTC = float(self.dataFileBTC.readline())
		self.phoneNumber= (self.phoneDataFile.readline())[0:10]
		self.phoneDataFile.seek(0)
		self.phoneCarrier= (self.phoneDataFile.readline())[11:]
		self.bitcoinsToBuy = 0
		self.buyPrice = 0
		self.bitcoinsToSell = 0
		self.sellPrice = 0
		self.USDSpent = 0
		self.profit = 0
		self.bitcoinsInWallet = 0
		self.USDInWallet = 0
		self.urls=["","",""]
		#set up buttons
		self.investmentButton  = Button(self.canvas,
								text="Input Initial Investment",
								command= self.inputInitialInvestment)
		self.buyButton= Button(self.canvas,text="Buy bitcoins", 
								command = self.buyBitcoins)
		self.sellButton = Button(self.canvas, text = "Sell Bitcoins", 
								command = self.sellBitcoins)
		self.setupPhone = Button(self.canvas, text = "Setup New Phone Number",
								 command = self.setupPhone)
		self.textAlertButton = Button(self.canvas, text = "Set Alert",
									 command  = self.setTextAlert)
		self.deleteAlertButton= Button(self.canvas, text = "Delete Alert",
										 command  = self.deleteTextAlert)
		self.urlButton1= Button(self.canvas, text = "Visit Site",
							 command  = lambda: self.openWebPage(self.urls[0]),bg="#0030CF")
		self.urlButton2= Button(self.canvas, text = "Visit Site",
						 command  = lambda: self.openWebPage(self.urls[1]),bg="#0030CF")
		self.urlButton3= Button(self.canvas, text = "Visit Site",
						 command  = lambda: self.openWebPage(self.urls[2]), bg="#0030CF")
		self.profitPortfolio = Portfolio(initialInvestment = 
										self.initialInvestmentUSD)
		#make calls to profit class and API
		self.profit = self.profitPortfolio.profit()
		self.ticker = API.get_ticker()
		self.bitcoinsInWallet = portfolio.bitcoinsInWallet()
		self.USDInWallet = portfolio.USDInWallet()
		self.revenue = float(self.ticker["last"])*float(self.bitcoinsInWallet)
		self.getNews()
		self.redrawAll()
	def redrawAll(self):
		self.canvas.delete(ALL)
		self.textAlertFile = open("textAlertData.txt","r")
		self.textAlertFile.seek(0)
		#draw appropriate screen
		if (self.showPortfolio == True):
			self.drawPortfolio()
		if (self.showTrade == True):
			self.drawTrade()
		if (self.showNews == True):
			self.drawNews()
		if (self.showAlert == True):
			self.drawAlert()
		if (self.showTicker == True):
			self.drawTicker()

	def mousePressed(self, event):
		#ticker always shows
		self.showTicker = True
		#if not clicking on a button (widget):
		if len(str(event.widget)) < 12:
			if ((event.x < self.tabWidth) and (event.y < self.headerHeight)):
				self.showPortfolio =True
				self.showNews = False
				self.showAlert = False 
				self.showTrade = False
				self.redrawAll()
			elif ((event.x > self.tabWidth) and (event.x < 2.0*self.tabWidth)
				 and (event.y < self.headerHeight)):
				self.showPortfolio =False
				self.showNews = False
				self.showAlert = False 
				self.showTrade = True
				self.redrawAll()
			elif ((event.x > 2.0*self.tabWidth/3.0) and
				 (event.y < self.headerHeight)):
				self.showPortfolio =False
				self.showNews = True
				self.showAlert = False 
				self.showTrade = False
				self.redrawAll()
			elif ((self.showTrade == True) and
				(event.x >self.width/4.0) and
				(event.x <self.width/2.0) and
				(event.y > 2 * self.headerHeight) and
				(event.y < 3 *self.headerHeight)):
				self.showTrade = True
				self.showBuy = True
				self.showSell = False 
				self.showAlert = False 
				self.redrawAll()
			elif ((self.showTrade == True) and
				(event.x >self.width/2.0) and
				(event.x <3.0* self.width/4.0) and
				(event.y > 2 * self.headerHeight) and
				(event.y < 3 *self.headerHeight)):
				self.showTrade = True
				self.showBuy = False
				self.showSell = True 
				self.showAlert = False 
				self.redrawAll()
			elif ((event.x) < 9/10.0 * self.width + self.imageWidth/2.0 and
				event.x > 9/10.0 * self.width - self.imageWidth/2.0 and 
				event.y < (self.height - 1.75 * self.tickerHeight) + self.imageHeight/2.0 and
				event.y > (self.height - 1.75 * self.tickerHeight) - self.imageHeight/2.0):
				self.textAlertFile = open("textAlertData.txt", "r")
				self.showAlert = True
				self.showPortfolio = False
				self.showNews = False
				self.showTrade =False 
				self.redrawAll()

	#draw the portfolio screen
	def drawPortfolio(self):
		#create Tabs
		self.canvas.create_rectangle(0,0,
								self.width,self.height, fill = "#fbcf72")
		self.canvas.create_rectangle(self.tabWidth,0,
								self.width,
								self.headerHeight, fill="#FF9729")
		self.canvas.create_line(self.tabWidth*2.0,0,
								self.tabWidth*2,self.headerHeight)
		self.canvas.create_text(self.tabWidth/2.0,self.headerHeight/2,
							 text = "Portfolio", font = ("Impact", 30))
		self.canvas.create_text(3.0*self.tabWidth/2.0,self.headerHeight/2, 
								text = "Trade", font = ("Impact", 30))
		self.canvas.create_text(5.0*self.tabWidth/2.0,self.headerHeight/2,
								 text = "News", font = ("Impact", 30))
		#create Portfo3lio text
		font = ("Helvetica", 16, "bold")
		self.walletText = "Wallet:    %s BTC  |  %s USD" % (self.bitcoinsInWallet, self.USDInWallet)
		self.canvas.create_text(self.width/2.0, 7.0 *self.height/20, 
								text= self.walletText, font=font)
		self.canvas.create_text(self.width/2.0, 9.0 * self.height/20,
								 text= "Initial Investment: $%.2f USD  | %.2f BTC" % (
								 self.initialInvestmentUSD, self.initialInvestmentBTC),
								  font=font)
		self.canvas.create_window(self.width/2.0, 5.0*self.height/20,
								 window=self.investmentButton)
		try:
			avPP = float(self.initialInvestmentUSD) / self.initialInvestmentBTC
		except:
			avPP = 0
		self.canvas.create_text(self.width/2.0,11.0*self.height/20,
							 text="Average Purchase Price: $%.2f" % avPP, font=font)
		self.canvas.create_text(self.width/2.0,13.0*self.height/20, 
								text="Revenue:  $%.2f" % (self.revenue),
								 font=font)
		self.canvas.create_text(self.width/2.0,15.0*self.height/20, text="Profit:  $%+.2f" % self.profit, font=font)
		self.canvas.create_image(9/10.0 * self.width, self.height - 1.75 * self.tickerHeight, image =self.smallImage)

	#draw trading screen
	def drawTrade(self):
		self.canvas.create_rectangle(0,0,
						self.width,self.height, fill = "#fbcf72")
		self.canvas.create_rectangle(0,0,self.tabWidth,self.headerHeight, fill="#FF9729")
		self.canvas.create_rectangle(2*self.tabWidth,0,self.width,self.headerHeight, fill="#FF9729")
		self.canvas.create_text(self.tabWidth/2.0,self.headerHeight/2,
								 text = "Portfolio", font = ("Impact", 30))
		self.canvas.create_text(3.0*self.tabWidth/2.0,self.headerHeight/2,
								 text = "Trade", font = ("Impact", 30))
		self.canvas.create_text(5.0*self.tabWidth/2.0,self.headerHeight/2, 
									text = "News", font = ("Impact", 30))
		self.canvas.create_rectangle(self.width/4.0, 2.0 * self.headerHeight, 
									self.width/2.0, 3.0 *self.headerHeight, 
									fill = "#1FFA8F", outline  = "")
		self.canvas.create_rectangle(self.width/2.0, 2.0 * self.headerHeight,
										 self.width *3.0/4, 3.0 *self.headerHeight,
										  fill = "#FA221F", outline = "")
		self.canvas.create_line(self.width/2.0, 2.0*self.headerHeight, 
								self.width/2.0, 3.0 * self.headerHeight, width="2")
		self.canvas.create_text(3.0 * self.width/8.0, 2.5 * self.headerHeight,
								 text = "BUY", font = ("courier new", 35, "bold"))
		self.canvas.create_text(5.0 * self.width/8.0, 2.5 * self.headerHeight, 
								text = "SELL", font = ("courier new", 35, "bold"))
		self.canvas.create_image(9/10.0 * self.width,
								self.height - 1.75 * self.tickerHeight, image =self.smallImage)
		if (self.showBuy == True):
			self.canvas.create_rectangle(self.width/12.0, 3.0 * self.headerHeight,
										 self.width *11.0/12, 3.0*self.headerHeight + self.height/3.0,
										  fill = "#1FFA8F", outline = "")
			self.canvas.create_window(self.width/2.0, 3.5 *self.headerHeight,
									 window=self.buyButton)
			self.USDSpent = (float(self.bitcoinsToBuy) * float(self.buyPrice))
			self.canvas.create_text(self.width/3.0, 4.2*self.headerHeight, 
									text= "LAST PURCHASE:\n --> Bitcoins bought: %.2f \n --> Buying price: $%.2f \n --> USD spent: $%.2f" % (
									float(self.bitcoinsToBuy), float(self.buyPrice), float(self.USDSpent)))
		self.showTrade = True
		if (self.showSell == True):
			self.canvas.create_rectangle(self.width/12.0,
										 3.0 * self.headerHeight, 
										 self.width *11.0/12, 3.0*self.headerHeight + self.height/3.0,
										  fill = "#FA221F", outline  = "")
			self.canvas.create_window(self.width/2.0, 3.5 *self.headerHeight, 
										window=self.sellButton)
			self.USDGained = (float(self.bitcoinsToSell) * float(self.sellPrice))
			self.canvas.create_text(self.width/3.0, 4.2*self.headerHeight,
								 text= "LAST SELL:\n --> Bitcoins Sold: %.2f \n --> Buying price: $%.2f \n --> USD gained: $%.2f" % (
								 float(self.bitcoinsToSell), float(self.sellPrice), float(self.USDGained)))
	#draw alert setup window
	def drawAlert(self):
		self.canvas.create_rectangle(0,0,
								self.width,self.height, fill = "#fbcf72")
		self.canvas.create_rectangle(0,0,self.width,self.headerHeight,
									 fill  = "#FF9729")
		self.canvas.create_text(self.width/2.0, 1.5 *self.headerHeight, 
								text = "Set Text Alert", fill = "#651808",
								 font  = ("Impact",30, "underline"))
		self.canvas.create_rectangle(0,0,self.tabWidth,self.headerHeight,
									 fill="#FF9729")
		self.canvas.create_rectangle(2*self.tabWidth,0,self.width,self.headerHeight,
									 fill="#FF9729")
		self.canvas.create_text(self.tabWidth/2.0,self.headerHeight/2, 
								text = "Portfolio", font = ("Impact", 30))
		self.canvas.create_text(3.0*self.tabWidth/2.0,self.headerHeight/2,
								 text = "Trade", font = ("Impact", 30))
		self.canvas.create_text(5.0*self.tabWidth/2.0,self.headerHeight/2,
								 text = "News", font = ("Impact", 30))
		font = ("Helvetica", 14,"bold")
		self.canvas.create_text(self.width/5.0, 2.5*self.headerHeight,
								 text= "Current Alerts:", font=font)
		self.canvas.create_window(4.5/6 *self.width, 1.85 *self.height/4.0, 
									window  = self.textAlertButton)
		self.canvas.create_window(4.5/6 *self.width, 1.50*self.height/4.0, 
									window  = self.setupPhone)
		self.canvas.create_window(4.5/6 *self.width, 2.2*self.height/4.0,
									 window  = self.deleteAlertButton)
		if self.isFileEmpty(self.textAlertFile):
			self.canvas.create_text(self.width/3.0, 3*self.headerHeight,
									 text = "No Text Alerts", font=font)
		else:
			startHeight=3.0
			self.textAlertFile.seek(0)
			for (num,line) in enumerate(self.textAlertFile):
				if num > 7:
					break
				self.canvas.create_text(self.width/3.0-0.1,startHeight * self.headerHeight,
									 text = "-->Alert when price hits $%s" % (line), font=font)
				startHeight += 0.30
		self.phoneDataFile.seek(0)
		if self.isFileEmpty(self.phoneDataFile):
			self.canvas.create_text(4.5*self.width/6, 1.25*self.height/4.0,
									 text = "No Phone Set Up", font=font)
		else:
			self.canvas.create_text(4.5*self.width/6, 1.25*self.height/4.0, 
									text = "Current Number: %s\nCarrier: %s" % (
											self.phoneNumber, self.phoneCarrier), font= font)

	#determines if the external text file is empty
	def isFileEmpty(self,dataFile):
		count = 0

		for line in dataFile:
			if line != "":
				count+=1
		dataFile = dataFile.seek(0)
		if count == 0:
			return True
		else:
			return False



	#draws news window
	def drawNews(self):
		self.canvas.create_rectangle(0,0,
								self.width,self.height, fill = "#fbcf72")
		self.canvas.create_rectangle(0,0,self.tabWidth,self.headerHeight,
									 fill="#FF9729")
		self.canvas.create_rectangle(self.tabWidth,0,2.0*self.tabWidth,
									self.headerHeight, fill="#FF9729")
		self.canvas.create_text(self.tabWidth/2.0,self.headerHeight/2,
								 text = "Portfolio", font = ("Impact", 30))
		self.canvas.create_text(3.0*self.tabWidth/2.0,self.headerHeight/2,
								 text = "Trade", font = ("Impact", 30))
		self.canvas.create_text(5.0*self.tabWidth/2.0,self.headerHeight/2,
								 text = "News", font = ("Impact", 30))
		self.canvas.create_image(9/10.0 * self.width,
								 self.height - 1.75 * self.tickerHeight,
								  image =self.smallImage)
		self.canvas.create_rectangle(1/9.0 * self.width,
								 1.5*self.headerHeight, 3.1/8.0 * self.width,
								  2.25 *self.headerHeight, fill = "#3d79ca", 
								  outline  = "")
		self.canvas.create_text(1/4.0* self.width,  1.87* self.headerHeight,
								 text = "Recent News:", 
								 font = ("Helvetica",19,"bold"))
		self.canvas.create_rectangle(1/15.0 * self.width, 2.25 * self.headerHeight,
		 							7.5/9.0 *self.width, self.height- 2.0* self.tickerHeight,
		 								 fill ="#3d79ca", outline = "")
		titleStartY = 2.5*self.headerHeight
		urlStartY = 3*self.headerHeight
		dateStartY = 3.32*self.headerHeight
		for title in self.titles:
			self.canvas.create_text(1.05/15.0*self.width,titleStartY, text = "%s" % title, anchor = "w", font= ("Helvetica",13, "bold", "underline"))
			titleStartY+=1.18*self.headerHeight
		#create Indiviudal website buttons
		self.canvas.create_window(1.15/15.0*self.width,urlStartY, window = self.urlButton1, anchor = "w")
		self.canvas.create_window(1.15/15.0*self.width,urlStartY+1.18*self.headerHeight, window = self.urlButton2, anchor = "w")
		self.canvas.create_window(1.15/15.0*self.width,urlStartY+ 2*1.18*self.headerHeight, window = self.urlButton3, anchor = "w")
		for date in self.dates:
			self.canvas.create_text(1.05/15.0*self.width,dateStartY, text = "%s" % date, anchor = "w", font= ("Helvetica",11))
			dateStartY+=1.18*self.headerHeight
	#initially finds news articles
	def getNews(self):
		self.titles=[]
		self.urls=[]
		self.dates=[]
		req = urllib2.Request("https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=bitcoin")
		resp = urllib2.urlopen(req)
		data = json.load(resp,object_hook=json_ascii.decode_dict)
		titlesDict = data["responseData"]["results"]
		for title in xrange(3):
			self.titles+=[lxml.html.fromstring(titlesDict[title]["titleNoFormatting"]).text_content()]
			self.urls+=[titlesDict[title]["unescapedUrl"]]
			self.dates+= [titlesDict[title]["publishedDate"][:-5]]
		self.fitTitles()
	#shrink titles so they fit on applcation window
	def fitTitles(self):
		for title in xrange(len(self.titles)):
			for letter in xrange(1,len(self.titles[title])):
				if letter % 50== 0:
					self.titles[title]= self.titles[title][0:letter] + "-\n" + self.titles[title][letter:]

	def openWebPage(self,url):
		webbrowser.open(str(url), new=1)

	#saves initialInput to an external file for permanent save data
	def inputInitialInvestment(self):
		InvestmentDialog = InvestmentPopup(self.canvas)
		try:
			self.inputInvestmentUSD = (InputInitialInvestmentVariable[0])
			self.inputInvestmentBTC= (InputInitialInvestmentVariable[1])
			self.dataFileUSD = open("termDataUSD.txt","w")
			self.dataFileUSD.write(str(self.inputInvestmentUSD))
			self.dataFileUSD.close()
			self.dataFileUSD = open("termDataUSD.txt","r")
			self.initialInvestmentUSD = float(self.dataFileUSD.readline())
			self.dataFileUSD.close()
			self.dataFileBTC = open("termDataBTC.txt","w")
			self.dataFileBTC.write(str(self.inputInvestmentBTC))
			self.dataFileBTC.close()
			self.dataFileBTC = open("termDataBTC.txt","r")
			self.initialInvestmentBTC = float(self.dataFileBTC.readline())
			self.dataFileBTC.close()
		except:
			pass
		self.profitPortfolio = Portfolio(initialInvestment = self.initialInvestmentUSD)
		self.profit = self.profitPortfolio.profit()
		self.redrawAll()
	#used for the buy bitcoins button
	def buyBitcoins(self):
		self.showTrade = True
		self.showBuy = True
		buyWindow = BuyPopup(self.canvas)
		try:
			self.bitcoinsToBuy = buyData[0]
			self.buyPrice = buyData[1]
		except:
			pass
		self.redrawAll()
	#used for the sell bitcoins button
	def sellBitcoins(self):
		sellDialog = SellPopup(self.canvas)
		try:
			self.bitcoinsToSell = sellData[0]
			self.sellPrice = sellData[1]
		except:
			pass
		self.redrawAll()
	# gets phone number and carrier from the setupphone button
	#saves the phone number for future reference
	def setupPhone(self):
		phonePopup = SetupPhone(self.canvas)
		try:
			self.phoneNumber = phoneData[0]
			self.phoneCarrier =	phoneData[1]
			self.phoneDataFile.close()
			self.phoneDataFile = open("phoneData.txt","w")
			self.phoneDataFile.write(str(self.phoneNumber) + "-" + str(self.phoneCarrier))
			self.phoneDataFile.close()
			self.phoneDataFile = open("phoneData.txt", "r")
		except:
			pass
		self.redrawAll()
	#creates and saves multiple text alerts
	def setTextAlert(self):
		setAlertPopup = SetTextAlert(self.canvas)
		try:
			textAlertFile = open("textAlertData.txt", "r")
			if textAlertData not in textAlertFile:
				textAlertFile.close()	
				if textAlertData.isdigit():
					self.alertPrice = textAlertData
					self.textAlertFile.close()
					self.textAlertFile = open("textAlertData.txt","a")
					self.textAlertFile.write(str(self.alertPrice)+"\n")
					self.textAlertFile.close()
					self.textAlertFile = open("textAlertData.txt","r") 
		except:
			pass
		self.redrawAll()
	#deletes the text alert of the specififed price
	#complicated because I need to edit and remake the save data file
	def deleteTextAlert(self):
		deleteAlertPopup = DeleteTextAlert(self.canvas)
		try:
			self.priceToDelete = priceToDelete
			self.textAlertFile = open("textAlertData.txt", "r")
			self.textAlertFile.seek(0)
			lineList = []
			for line in self.textAlertFile:
				if "\n" in line:
					line  = line[0:-1]
				if line.isdigit() and int(line) != int(self.priceToDelete):
					lineList+=[line]
			self.textAlertFile.close()
			self.textAlertFile = open("textAlertData.txt","w")
			for line in lineList:
				self.textAlertFile.write(line + "\n")
			self.textAlertFile.close()
			self.textAlertFile = open("textAlertData.txt","r")
			self.textAlertFile.seek(0)
		except:
			pass
		self.redrawAll()

	#determines whether the app should send text alert after ticker is updated
	def shouldAlert(self):
		self.shouldRedrawAll = False
		lastPrice = self.ticker["last"]
		self.textAlertFile = open("textAlertData.txt","r")
		self.textAlertFile.seek(0)
		lineList = []
		for line in self.textAlertFile:
			lineList+=[line]
			if "\n" in line:
				line  = line[0:-1]
			if line.isdigit() and abs(float(line) - lastPrice) < 1.5:
				EmailAlert.send_text(lastPrice, self.phoneNumber, self.phoneCarrier)
				lineList.remove(line + "\n")
				self.shouldRedrawAll=True
		self.textAlertFile.close()
		self.textAlertFile = open("textAlertData.txt","w")
		for line in lineList:
			self.textAlertFile.write(line)
		self.textAlertFile.close()
		self.textAlertFile = open("textAlertData.txt","r")
		self.textAlertFile.seek(0)
		if self.shouldRedrawAll == True:
			self.redrawAll()

	#updates ticker every 11 second
	#updates news daily
	#updates profit every hour
	def timerFired(self, canvas, count):
		delay = 1000
		#refresh ticker every 11 seconds
		if (count%11 == 0):
			self.ticker = API.get_ticker() 
			self.shouldAlert()
		#refresh news daily
		if (count % 86400 == 0):
			self.getNews()
		if (count != 0 and count % 60 == 0):
			self.revenue = float(self.ticker["last"])*float(self.bitcoinsInWallet)
			self.profit = self.profitPortfolio.profit()
		self.drawTicker()
		canvas.after(delay,lambda: self.timerFired(canvas, count+1))

	#draws the ticker at bottom of screen
	def drawTicker(self):
		self.canvas.create_rectangle(0,self.height-self.tickerHeight, self.width, self.height, fill = "#FFE14D")
		self.high = self.ticker["high"]
		self.low = self.ticker["low"]
		self.last = self.ticker["last"]
		self.avg = self.ticker["avg"]
		self.textHeight = (self.height - self.tickerHeight/2.0)
		self.textX = self.width/2.0
		#input ticker prices
		self.canvas.create_text(self.textX, self.textHeight, text = "Last: $%.2f     High: $%.2f     Low: $%.2f     Avg: $%.2f"%(self.last,self.high,self.low,self.avg), font = ("verdana",13, "bold"))

	def run(self):
		# create the root and the canvas
		self.root = Tk()
		self.root.wm_title("BITCOIN Trader")
		self.root.resizable(width=FALSE, height=FALSE)
		self.canvas = Canvas(self.root, width=500, height=500)
		self.canvas.pack(fill=BOTH, expand=YES)
		# Store canvas in root and in canvas itself for callbacks
		self.timerDelay = 250
		self.timerFiredIsRunning = True 
		# Set up canvas data and call init
		self.canvas.data = { }
		self.init()
		# set up events
		self.root.bind("<Button-1>", lambda event: self.mousePressed(event))
		#self.startTimerFired
		count = 0
		self.timerFired(self.canvas, count)
		# and launch the app
		self.root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)


def testFunction():
	gui=GUI()
	gui.run()

print testFunction()

