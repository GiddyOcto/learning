from telegram import *
from telegram.ext import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime
import googleSheets
import requests
import consts

updater = Updater(consts.TOKEN, use_context=True)
dp = updater.dispatcher

print("bot started")

def handle_message(update, context):
    msg = update.message.text
    if str(update.message.chat.id) == consts.chatID:
        messageContentList = splitMessage(msg)

        isAmountInt = checkAmountIsInt(messageContentList)
        if isAmountInt == True:

            timeOfSpend = getTimeOfSpend()
            messageContentList.append(timeOfSpend)
            googleSheets.insertRow(messageContentList)
            currentMonth = getCurrentMonth()
            sendMessage(f"The current running total this month is: {googleSheets.getRunningTotal(currentMonth)}")
        
        else:
            update.message.reply_text("Did you format the message correctly?")

def checkAmountIsInt(message):
    try:
        amountProvided = int(message[1])
        return True
    except:
        return False


def getCurrentMonth():
    month = datetime.datetime.now().month
    return month

def getTimeOfSpend():
    dttime = datetime.datetime.now()
    timeOfSpend = (str(dttime)[:19])
    return timeOfSpend

def sendMessage(messageText):
    replyMsgURL = f'{consts.replyURL}{messageText}'
    requests.get(replyMsgURL)

def splitMessage(messageText):
    messageContents = messageText.split(" ")
    spendType = messageContents[0]
    spendAmount = messageContents[1]
    
    messageListItems = [spendType, spendAmount]
    return messageListItems

def main():
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()

main()
