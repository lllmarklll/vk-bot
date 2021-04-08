message = {}; attachment = {'yes':{},'yn':{},'no':{}}
'''
НАЧАЛО НАСТРОЙКИ ПАРАМЕТРОВ
НАЧАЛО НАСТРОЙКИ ПАРАМЕТРОВ
НАЧАЛО НАСТРОЙКИ ПАРАМЕТРОВ
НАЧАЛО НАСТРОЙКИ ПАРАМЕТРОВ
'''
#access token группы
group_access_token = ''


#Сообщения: 
#приветствие
message0 = ''
#ответ на "да"
message_yes = ''
#ответ на "не знаю"
message_yn = ''
#ответ на "нет"
message_no = ''
#прощание
message1=''

#Список вопросов
message[1] = ''
message[2] = ''
message[3] = ''
message[4] = ''
message[5] = ''

#Список вложений:
#ответ "да" (id из файлов группы)
attachment['yes'][1] = ''
attachment['yes'][2] = ''
attachment['yes'][3] = ''
attachment['yes'][4] = ''
attachment['yes'][5] = ''
#ответ "не знаю" (id из файлов группы)
attachment['yn'][1] = ''
attachment['yn'][2] = ''
attachment['yn'][3] = ''
attachment['yn'][4] = ''
attachment['yn'][5] = ''
#ответ "нет" (id из файлов группы)
attachment['no'][1] = ''
attachment['no'][2] = ''
attachment['no'][3] = ''
attachment['no'][4] = ''
attachment['no'][5] = ''

'''
КОНЕЦ НАСТРОЙКИ ПАРАМЕТРОВ
КОНЕЦ НАСТРОЙКИ ПАРАМЕТРОВ
КОНЕЦ НАСТРОЙКИ ПАРАМЕТРОВ
КОНЕЦ НАСТРОЙКИ ПАРАМЕТРОВ
'''
import requests
import json
import random

def keyboard_f(number):
	keyboard = {}
	for num in range(1,number+1):
		keyboard[num] = json.dumps({'inline':True,'buttons':[
				[{'color':'positive','action':{'type':'callback','label':'Да','payload':{'ans':'yes','num':num}}}],
				[{'color':'secondary','action':{'type':'callback','label':'Не заню','payload':{'ans':'yn','num':num}}}],
				[{'color':'negative','action':{'type':'callback','label':'Нет','payload':{'ans':'no','num':num}}}]
				]})
	return keyboard

version = 5.126
keyboard = keyboard_f(len(message))
print('connecting...')
group_id = json.loads(requests.get(f'https://api.vk.com/method/groups.getById?access_token={group_access_token}&v={version}').text)['response'][0]['id']
connect_info = json.loads(requests.get(f'https://api.vk.com/method/groups.getLongPollServer?group_id={group_id}&access_token={group_access_token}&v={version}').text)['response']
server = connect_info['server']
key = connect_info['key']
ts = connect_info['ts']
print('connected')
while True:
	server_answer = json.loads(requests.get(f'{server}?act=a_check&key={key}&ts={ts}&wait={25}').text)
	print(server_answer)
	#need to use the new ts from server answer
	if 'failed' in server_answer.keys():
		if server_answer['failed'] == 1:
			ts = server_answer['ts']
		elif server_answer['failed'] == 2 or server_answer['failed'] == 3:
			connect_info = json.loads(requests.get(f'https://api.vk.com/method/groups.getLongPollServer?group_id={group_id}&access_token={group_access_token}&v={version}').text)['response']
			server = connect_info['server']
			key = connect_info['key']
			ts = connect_info['ts']
	else:
		ts = server_answer['ts']
		if len(server_answer['updates']) != 0:
			for update in server_answer['updates']:
				if update['type'] == 'message_event':
						peer_id = update['object']['peer_id']
						payload = update['object']['payload']
				elif update['type'] == 'message_new':
					peer_id = update['object']['message']['peer_id']
					if 'payload' in update['object']['message'].keys():
						payload = json.loads(update['object']['message']['payload'])
					else:
						payload = {}
				else:
					continue
				if len(payload) != 0:
					if 'command' in payload.keys():
						requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message0}&access_token={group_access_token}&v={version}')
						requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message[1]}&keyboard={keyboard[1]}&access_token={group_access_token}&v={version}')
					else:
						ans = payload['ans']
						num = payload['num']
						if ans == 'yes':
							z=requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message_yes}&attachment={attachment["yes"][num]}&access_token={group_access_token}&v={version}')
							print(z.text)
						elif ans == 'no':
							requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message_no}&attachment={attachment["no"][num]}&access_token={group_access_token}&v={version}')
						else:
							requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message_yn}&attachment={attachment["yn"][num]}&access_token={group_access_token}&v={version}')
						if num+1 <= len(keyboard):
							requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message[num+1]}&keyboard={keyboard[num+1]}&access_token={group_access_token}&v={version}')
						else:
							requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message1}&access_token={group_access_token}&v={version}')
				else:
					requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message0}&access_token={group_access_token}&v={version}')
					requests.get(f'https://api.vk.com/method/messages.send?peer_id={peer_id}&random_id={random.randrange(4294967296)}&message={message[1]}&keyboard={keyboard[1]}&access_token={group_access_token}&v={version}')