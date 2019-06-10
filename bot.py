# -*- coding: utf-8 -*-
import redis
import os
import telebot
import requests
# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['token']
#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
bot = telebot.TeleBot(token)
tgadmin=385390931
# some_api = some_api_lib.connect(some_api_token)
#fuctions
#music fuction
JM_API_URL="https://api.jamendo.com/v3.0/tracks/?client_id={cid}&format=jsonpretty&fuzzytags={gerne}&include=musicinfo&groupby=album_id"
@bot.message_handler(commands=['music'])
def music_link(message):
	print("music link triggered")
	def jmusic():
		global linkofmp3
		global titleofmp3
		global artistofmp3
		global durationofmp3
		global data_count
		headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
		counter =0
		jm_response=requests.get(JM_API_URL.format(cid="ca2a93cf",gerne="edm"),headers)
		jm_status_code=jm_response.json()['headers']['code']
		try:
			jm_status_error=jm_response.json()['headers']['error_message']
		except:
			jm_status_error="no_errors_yet_amigo"
		while jm_status_code == 0:
			try:
				jm_result_count=jm_response.json()['headers']['results_count']
			except:
				jm_result_count=False
			while counter < jm_result_count:
				data_count=counter
				linkofmp3=jm_response.json()['results'][data_count]['audiodownload']
				titleofmp3=jm_response.json()['results'][data_count]['name']
				artistofmp3=jm_response.json()['results'][data_count]['artist_name']
				durationofmp3=jm_response.json()['results'][data_count]['duration']
				print(artistofmp3,titleofmp3,durationofmp3,linkofmp3)
				bot.send_audio(message.chat.id,linkofmp3," ",artistofmp3,titleofmp3)
			#request=requests.get(URLTA,verify=False,data={'chat_id':chatID,'reply_to_message_id ':r2mid,'caption':"If there is an audio you will display it ",'audio':linkofmp3,'duration':durationofmp3,'performer':artistofmp3,'title':titleofmp3})
				counter=data_count
				counter=counter+1
			else:
				data_count=jm_result_count
			counter=counter+1
			#request=requests.get(URLTM,verify=False,data={'chat_id':chatID,'reply_to_message_id ':r2mid,'text':"Sorry ! "+" "+firstname+" "+lastname+" unabled to find music "+data_count+"_"+counter})
		else:
			print(jm_status_code,jm_status_error,jm_result_count)
		bot.send_message(message.chat.id, "*no muisc gerne found*",parse_mode='Markdown')		
	jmusic()

#telegram commands 
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
	print("welcome triggered")
	bot.reply_to(message, "*you triggered help and start*",parse_mode='Markdown')
#telegram new meber joined
@bot.message_handler(func=lambda message: True, content_types=['new_chat_members'])
def user_joined_greet(message):
	print("group Joined Welcome triggered")
	if message.new_chat_member.id != bot.get_me().id:
		print("group Joined Welcome triggered 2")
		f_name = message.new_chat_member.first_name
		title = message.chat.title
		try:
			l_name=message.new_chat_member.last_name
			newmember=str(f_name+" "+l_name)
		except:
			l_name=" "
			newmember=str(f_name)
		bot.send_message(message.chat.id, "`Welcome` " + "_"+newmember+ "_"+ "`.. to our group` "+ "*"+title+"*" + "` 🤗`",parse_mode='Markdown')
	else:
		title = message.chat.title
		print("added to a new group named "+title)
		bot.send_message(tgadmin, "*I was added by someone to group* "+title,parse_mode='Markdown')
#telegram member left			
@bot.message_handler(func=lambda message: True, content_types=['left_chat_member'])
def user_leave_greet(message):
	if message.left_chat_member.id != bot.get_me().id:
		print("group left curse triggered")
		f_name = message.left_chat_member.first_name
		try:
			l_name=message.left_chat_member.last_name
			leftmember=str(f_name+" "+l_name)
		except:
			l_name=" \n"
			leftmember=str(f_name)
		title = message.chat.title
		
		bot.send_message(message.chat.id, "_"+leftmember+"_  `left`  *"+title+"* `see you soon`",parse_mode='Markdown')
	else:
		title = message.chat.title
		print("kicked the bot by some one from a group named "+title)
		bot.send_message(tgadmin, "*I was kicked by someone from group* "+title,parse_mode='Markdown')

#telegram messgae echo		
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	print("echo_all triggered")
# 	try:
# 		link=message.entities[0].url
# 		glink='https://www.google.com/searchbyimage?image_url='+link
# 		params = urlencode(dict(access_key="87f2c5e74f2e46d2a8d0970c37f21c78",url=glink))
# 		payload = urlretrieve("https://api.apiflash.com/v1/urltoimage?" + params)
# 		bot.send_photo(message.chat.id,payload)
# 	except:
# 		payload = message.text
# 		bot.reply_to(message, payload)
	link=message.entities[0].url
	glink='https://www.google.com/searchbyimage?image_url='+link
	payload = 'https://api.apiflash.com/v1/urltoimage?access_key=87f2c5e74f2e46d2a8d0970c37f21c78&url='+glink
	bot.send_photo(message.chat.id,payload)
	
	
bot.polling(none_stop=True)
