from pyrogram import Client, filters, compose
import re
import random as r
from fake_useragent import UserAgent
import requests
import json
import asyncio,time
import random
from pyrogram.errors import FloodWait
from pyrogram.enums import ParseMode

api_id = '26248398'
api_hash = 'ac317aa8365982df91570c7aff0838aa'
bot_token = '7048815602:AAHMF0Fh6Q_So9hMF_OsVoqVb7dPbeDFZ5A'
maingroupchatid = '-1002208761425' #dont enter it as string, make it int(else will give errors)

me = Client(name='user', api_id=api_id, api_hash=api_hash)
bot = Client(name='bot',bot_token=bot_token,api_id = api_id,api_hash=api_hash)
def getcards(text):
    if text is None:
        return None
    text = text.replace('\n', ' ').replace('\r', '')
    card_pattern = r'\b(\d{16})[^\d]*(\d{2})[^\d]*(\d{2}|\d{4})[^\d]*(\d{3})\b'
    matches = re.findall(card_pattern, text)
    valid_cards = []
    for match in matches:
        if len(match) == 3:
            card_number = match[0]
            expiry_month = match[1][:2]
            expiry_year = match[2][2:]
            cvv = match[2]
        else:
            card_number = match[0]
            expiry_month = match[1]
            expiry_year = match[2]
            cvv = match[3]
        
        if int(expiry_month) > 12:
            expiry_year = match[1]
            expiry_month = match[2]
        
        # Adjust expiry_year format if needed
        if len(expiry_year) == 2:
            if int(expiry_year) > 23:
                expiry_year = f'20{expiry_year}'
            else:
                continue
        elif len(expiry_year) == 4:
            if int(expiry_year) <= 2023:
                continue
        
        card_info = f'{card_number}|{expiry_month}|{expiry_year}|{cvv}'
        valid_cards.append(card_info)
    
    if len(valid_cards) == 1:
        return valid_cards[0]
    elif len(valid_cards) > 1:
        return tuple(valid_cards)
    else:
        return None
    
#MODIFY CC TO APPORVED LIKE TEXT

def modify(cc,cctype,brand,level,issuer,country,countrycode):
    a = str(r.randint(0,20)) + '.' + str(r.randint(0,9))

     
    flag = countrycode
    return f'''𝘾𝙃𝘼𝙍𝙂𝙀𝘿 0.5$ ✨

𝘾𝘼𝙍𝘿-»  **`{cc}`**
𝙂𝘼𝙏𝙀𝙒𝘼𝙔-» 𝖡𝗋𝖺𝗂𝗇𝗍𝗋𝖾𝖾 0.5$ 
𝙍𝙀𝙎𝙋𝙊𝙉𝙎𝙀-» 1000: 𝖠𝗉𝗉𝗋𝗈𝗏𝖾𝖽 ✅
━━━━━━━━━━━━━━
𝙄𝙉𝙁𝙊-» {cctype} - {brand} - {level}
𝙄𝙎𝙎𝙐𝙀𝙍-» {issuer}
𝘾𝙊𝙐𝙉𝙏𝙍𝙔-» {country} {flag}
━━━━━━━━━━━━━━
𝙏𝙄𝙈𝙀-» {a} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
━━━━━━━━━━━━━━
𝘿𝙀𝙑-» @SHUBH4M_THAKUR
'''

#for getting bin info

async def get_bin(bin : str):
    
    url = f'https://binlist.io/lookup/{bin}/'
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent':user_agent}
    response = requests.get(url=url,headers=headers)
    result = json.loads(response.text)
    

    L = [result["scheme"],result["type"],result["category"],result["country"]["name"],result["country"]["emoji"],result["bank"]["name"]]
    
    return L

#FOR DROPPING MESSAGE TO GROUP

async def drop_message(text):
    try:
        await bot.send_message(chat_id = maingroupchatid,text=text,parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await asyncio.sleep(5)
#retrieve updates from telegram chats
last20 = [] # a list basically to store the last 20 messages sent to avoid duplicates
@me.on_message()
async def main(client, message):
    if len(last20) > 20:
        last20.pop(0)
    Text = message.text
    fullz = getcards(Text)
    if fullz != None:
        if type(fullz) is tuple:
            for full in fullz:
                if full in last20:
                    continue
                info = await get_bin(full[:6])
                last20.append(full)
                time.sleep(2)
                fully_ready_message = modify(cc=full, cctype=info[0], brand=info[1],level = info[2],issuer = info[5],country = info[3],countrycode = info[4])
                await drop_message(fully_ready_message)

        elif type(fullz) is str:
            if fullz in last20:
                return
            info = await get_bin(fullz[:6])
            last20.append(fullz)
            time.sleep(2)
            fully_ready_message = modify(cc=fullz, cctype=info[0], brand=info[1],level = info[2],issuer = info[5],country = info[3],countrycode = info[4])
            await drop_message(fully_ready_message)
            
if __name__ == "__main__":
    apps = [me,bot]
    compose(apps)
    for app in apps:
        asyncio.run(app.run())
