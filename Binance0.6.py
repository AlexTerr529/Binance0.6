from re import T
import  pandas as pd
import time
import configparser
import os
import requests

from symtable import Symbol
from colorama import Fore, Style
from binance.client import Client
from binance.exceptions import BinanceAPIException

config = configparser.ConfigParser()
pathinifile = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(pathinifile, 'config.ini'))
#config.read('config.ini')
#pathinifile=config['settings']['fullpath']
print (pathinifile)
pathinifilefull=pathinifile+'/'+'config.ini'
api_key=config['api']['api_key']
api_secret=config['api']['api_secret']
from binance.client import Client
client = Client(api_key,api_secret)
print ("Logged in")


##########################################################################################################################
apiadress = ("https://api.binance.com/api/v3/ticker/price?symbol=AXSUSDT")                                      ### Trade Coin                               # change coin //////////
price = requests.get(apiadress)  
price = price.json()  
price = float(price['price'])

coin=config['settings']['coin']
coinquantity=config['settings']['coinquantity']
stepp=config['settings']['stepp']
order1=config['settings']['order1']
order2=config['settings']['order2']
order3=config['settings']['order3']
maxprice=config['main']['maxprice']
minprice=config['main']['minprice']
enterprice=config['main']['enterprice']
midprice=config['main']['midprice']
stage=config['main']['stage']
target=config['main']['target']
status=config['main']['status']
coinquantity=float(coinquantity)
stepp=float(stepp)
stage=int(stage)
target=float(target)
midprice=float(midprice)
enterprice=float(enterprice)
maxprice=float(maxprice)
minprice=float(minprice)

anykeystart=input("Press Enter to continue, or press 0 and Enter for start new :\n")           # khm... khm...
#anykeystart=0
if anykeystart == '':
    anykeystart=505
anykeystart=int(anykeystart)
if anykeystart == 0:
    print ('Star new')
    stage=0
    enterprice=0
    midprice=price
    maxp=0
    maxprice=0
    minprice=999999999999999999                                                                                              # 0 or 999999999999999
    mixp=999999999999999999
    status="waiting"


if stage == 1 or stage == 2 or stage == 3 or stage == 4 :
    print ('Continuing  work...')
    midprice1=config['main']['midprice1']
    midprice2=config['main']['midprice2']
    midprice3=config['main']['midprice3']
    step1id=config['main']['step1id']
    step2id=config['main']['step2id']
    step3id=config['main']['step3id']
    step1price=config['main']['step1price']
    step2price=config['main']['step2price']
    step3price=config['main']['step3price']
    step1price=float(step1price)   
    step2price=float(step2price)
    step3price=float(step3price)
#    price=float(midprice)

    order1=eval(order1)
    order2=eval(order2)
    order3=eval(order3)
    order1=round((order1),3)
    order2=round((order2),3)
    order3=round((order3),3)
    maxp=maxprice
    mixp=minprice



##########################################################################################################################
##################################################       START       #####################################################
##########################################################################################################################
#clear = lambda: os.system('cls')                                                                 ###     Windows                                         #windows
clear = lambda: os.system('clear')                                                              ###     Linux                                          #linux


def chek():############################################################################################   Check
#    time.sleep(1)
    global price, maxprice, minprice
    global stage
    apiadress = ("https://api.binance.com/api/v3/ticker/price?symbol=AXSUSDT")                                             ### UI Coin                    # change coin /////
    price = requests.get(apiadress)  
    price = price.json()  
    price=float(price['price'])
    maxprice=float(max(maxprice,price))
    minprice=float(min(minprice,price))




def start():############################################################################################   Start
    global price, maxprice, minprice, maxp, mixp, enterprice, midprice, midprice1, midprice2, midprice3
    global stepp,stage, status, target
    global order1, order2, order3, order4, order5, anykeystart
    order=client.create_order(symbol=coin,side='buy',type='MARKET',quantity=coinquantity,)                                                  #   uncomment for work !!!
    enterprice=float(order["fills"][0]["price"])   
    
    #enterprice=price                                                                                                                         #   comment for work !!!
    maxprice=price
    minprice=price
    midprice=price
    maxp=0
    mixp=999999999999999999
    order1=config['settings']['order1']
    order2=config['settings']['order2']
    order3=config['settings']['order3']

    order1=str(order1)
    order2=str(order2)
    order3=str(order3)
    order1=eval(order1) #(stepp*(price*3))/100
    order2=eval(order2)
    order3=eval(order3)
    target=round((enterprice)+((midprice*stepp)/100),3)
    order1=round((order1),3)
    order2=round((order2),3)
    order3=round((order3),3)
    
    stage=1
    status=("waiting")
    stage1()



def waiting():###########################################################################################   Waiting...
    global price, maxprice, enterprice
    global stepp,stage, status, target
    global order1, order2, order3, order4, order5

    if (price)>=(target):
        print('Start Trailing...')
        status=("trailing")
    
    if (price)<=(order1) and (stage==1):
        stage2()

    if (price)<=(order2) and (stage==2):
        stage3()

    if (price)<=(order3) and (stage==3):
        stage4()






def trailing():##########################################################################################   Trailing...
    global price, maxprice, maxp, enterprice, midprice, target
    global stepp, stage, status
    global order1, order2, order3, order4, order5
    status="trailing"
    target=round(maxprice-((midprice*stepp)/100),3)
    if maxprice>maxp:
        maxp=maxprice
        config.set('main', 'maxprice', str(maxprice))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)

    if price<=target:
        print("stoploss")
        print ('Sell ', target)
        if stage==1:
            print("sell")
            client.create_order(symbol=coin,side='sell',type='MARKET',quantity=coinquantity,)                                          #   uncomment for work !!!
        if stage==2:
            print("sell")
            client.create_order(symbol=coin,side='sell',type='MARKET',quantity=coinquantity*2,)
        if stage==3:
            print("sell")
            client.create_order(symbol=coin,side='sell',type='MARKET',quantity=coinquantity*4,)
        if stage==4:
            print("sell")
            client.create_order(symbol=coin,side='sell',type='MARKET',quantity=coinquantity*8,)
        stage=0
        maxprice=0
        status="waiting"
        config.set('main', 'stage', str(stage))
        config.set('main', 'status', str(status))
        config.set('main', 'maxprice', str(maxprice))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)

        order1=config['settings']['order1']
        order2=config['settings']['order2']
        order3=config['settings']['order3']

        order1=str(order1)
        order2=str(order2)
        order3=str(order3)
        order1=eval(order1) #(stepp*(price*3))/100
        order2=eval(order2)
        order3=eval(order3)
        target=round((enterprice)+((midprice*stepp)/100),3)
        order1=round((order1),3)
        order2=round((order2),3)
        order3=round((order3),3)

        time.sleep(2)
#        start()


def UI():###############################################################################################   UI
    global price, midprice, maxprice, minprice, enterprice, target
    global stepp, stage, status
    global order1, order2, order3, order4, order5
    clear()
    print(f"Midprice is {midprice}         Enter point is {enterprice}")
    print(f"{Fore.RED}Target is   {target}{Style.RESET_ALL}\033[1m")
    print(f"Price is    {float(price):.3f}\033[0m         Maximum is  {maxprice}")
    if (stage==1) and (status=="waiting"):
        print(f"{Fore.GREEN}Order 1     {order1}{Style.RESET_ALL}")
    if (stage==1 or stage==2) and (status=="waiting"):
        print(f"{Fore.GREEN}Order 2     {order2}{Style.RESET_ALL}") 
    if (stage==1 or stage==2 or stage==3) and (status=="waiting"):
        print(f"{Fore.GREEN}Order 3     {order3}{Style.RESET_ALL}")
    if (stage=="loss-1") or (stage=="loss-2") or (stage=="loss-3"):
        print(f"Minimum is  {minprice}")
    print(f"Status: {status}   Stage {stage}") 

def stage1():##########################################################################################  Stage 1
    global price, midprice, maxprice, maxp, enterprice, stage, target
    global order1, order2, order3, order4, order5
    stage=1
    midprice=enterprice
    maxp=0
    maxprice=0
    target=round((enterprice)+(((midprice*stepp)*2)/100),3)
    config.set('main', 'stage', str(stage))
    config.set('main', 'enterprice', str(enterprice))
    config.set('main', 'midprice', str(midprice))
    config.set('main', 'target', str(target))
    with open(pathinifilefull, 'w') as fff:
        config.write(fff)


def stage2():#########################################################################################  Stage 2
    global price, midprice, maxprice, maxp, mixp, enterprice, stage, target, minprice
    global order1, order2, order3, order4, order5
    
    stage="loss-1"
    minprice=float(min(minprice,price))

    target=round(minprice+(((midprice*stepp)*2)/100),3)
    if minprice<mixp:
        mixp=minprice
        config.set('main', 'minprice', str(minprice))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)

    if price>=target:
        stage=2
        maxprice=price
        midprice=round((midprice+price)/2,3)

        order1=config['settings']['order1']
        order2=config['settings']['order2']
        order3=config['settings']['order3']

        order1=str(order1)
        order2=str(order2)
        order3=str(order3)
        order1=eval(order1) #(stepp*(price*3))/100
        order2=eval(order2)
        order3=eval(order3)
        target=round(midprice+(stepp*(price*1))/100,3)
        order1=round((order1),3)
        order2=round((order2),3)
        order3=round((order3),3)

        order=client.create_order(symbol=coin,side='buy',type='MARKET',quantity=coinquantity,)                                           #   uncomment for work !!!
        config.set('main', 'stage', str(stage))
        config.set('main', 'enterprice', str(enterprice))
        config.set('main', 'midprice', str(midprice))
        config.set('main', 'target', str(target))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)

def stage3():#########################################################################################  Stage 3
    global price, midprice, maxprice, maxp, mixp, enterprice, stage, target, minprice
    global order1, order2, order3, order4, order5

    stage="loss-2"
    minprice=float(min(minprice,price))

    target=round(minprice+(((midprice*stepp)*2)/100),3)
    if minprice<mixp:
        mixp=minprice
        config.set('main', 'minprice', str(minprice))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)

    if price>=target:
        stage=3
        maxprice=price
        midprice=round((midprice+price)/2,3)

        order1=config['settings']['order1']
        order2=config['settings']['order2']
        order3=config['settings']['order3']

        order1=str(order1)
        order2=str(order2)
        order3=str(order3)
        order1=eval(order1) #(stepp*(price*3))/100
        order2=eval(order2)
        order3=eval(order3)
        target=round(midprice+(stepp*(price*1))/100,3)
        order1=round((order1),3)
        order2=round((order2),3)
        order3=round((order3),3)

        order=client.create_order(symbol=coin,side='buy',type='MARKET',quantity=(coinquantity*2),)                                     #   uncomment for work !!!
        config.set('main', 'stage', str(stage))
        config.set('main', 'enterprice', str(enterprice))
        config.set('main', 'midprice', str(midprice))
        config.set('main', 'target', str(target))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)
def stage4():#########################################################################################  Stage 4
    global price, midprice, maxprice, maxp, mixp, enterprice, stage, target, minprice
    global order1, order2, order3, order4, order5

    stage="loss-3"
    minprice=float(min(minprice,price))

    target=round(minprice+(((midprice*stepp)*2)/100),3)
    if minprice<mixp:
        mixp=minprice
        config.set('main', 'minprice', str(minprice))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)

    if price>=target:
        stage=4
        maxprice=price
        midprice=round((midprice+price)/2,3)

        order1=config['settings']['order1']
        order2=config['settings']['order2']
        order3=config['settings']['order3']

        order1=str(order1)
        order2=str(order2)
        order3=str(order3)
        order1=eval(order1) #(stepp*(price*3))/100
        order2=eval(order2)
        order3=eval(order3)
        target=round(midprice+(stepp*(price*1))/100,3)
        order1=round((order1),3)
        order2=round((order2),3)
        order3=round((order3),3)

        order=client.create_order(symbol=coin,side='buy',type='MARKET',quantity=(coinquantity*4),)                                           #   uncomment for work !!!
        config.set('main', 'stage', str(stage))
        config.set('main', 'enterprice', str(enterprice))
        config.set('main', 'midprice', str(midprice))
        config.set('main', 'target', str(target))
        with open(pathinifilefull, 'w') as fff:
            config.write(fff)
           
######################################################################################################  END

while True:
    try:
        klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        time.sleep(1)
        chek()
        UI()
        if status=="waiting":
            if (stage==0):
                start()
            if (stage==1)or(stage==2)or(stage==3)or(stage==4)or(stage==5):
                waiting()
            if (stage=="loss-1"):
                stage2()
            if (stage=="loss-2"):
                stage3()
            if (stage=="loss-3"):
                stage4()
        if status=="trailing":
            trailing()
    except BinanceAPIException as e:
        print(e)
        print('Something went wrong. Error occured at %s. Wait for 1 hour.')
        time.sleep(3600)
        client = Client(api_key,api_secret)
        continue
    except Exception:
        print("Reconecting...")
        time.sleep(3)
        continue
