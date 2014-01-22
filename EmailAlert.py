from email.mime.text import MIMEText
from datetime import date
import smtplib

#Skylar Weaver

smtpServer = "smtp.gmail.com"
smtpPort = 587
smtpUsername = "BitcoinTraderAlert@gmail.com"
smtpPassword = "bitcointrader"
emailFrom = "BitcoinTraderAlert@gmail.com"
emailSubject = "BITCOIN ALERT:"
emailSpace = ", "
DATA='BITCION PRICES ARE FLUCTUATING'

def send_text(currentPrice, phoneNumber, carrier):
	data = ("ALERT: Bitcoin price has hit $%d!!!!\n\nPANIC!") % (currentPrice)
	if (carrier == "att" or carrier  == "at&t" or carrier == "ATT" or carrier  == "AT&T"):
		recipient = str(phoneNumber) + "@mms.att.net"
	elif (carrier == "verizon" or carrier == "Verizon"):
		recipient = str(phoneNumber) + "@vzwpix.com"
	emailTo = recipient
	msg = MIMEText(data)
	msg['Subject'] = emailSubject 
	msg['To'] = emailTo 
	msg['From'] = emailFrom
	mail = smtplib.SMTP(smtpServer, smtpPort)
	mail.starttls()
	mail.login(smtpUsername, smtpPassword)
	mail.sendmail(emailFrom, emailTo, msg.as_string())
	mail.quit()

#Test:
#send_text(120,7174606388,"att")