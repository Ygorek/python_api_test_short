urlin = 'http://62.109.6.35/inframanager/accountApi/SignIn'
urlout = 'http://62.109.6.35/inframanager/accountApi/SignOut'
urlinfo = 'http://62.109.6.35/inframanager/accountApi/GetAuthenticationInfo'
urlurg = 'http://62.109.6.35/inframanager/sdApi/GetUrgencyList'
urlcall = 'http://62.109.6.35/inframanager/sdApi/GetCallTypeListForClient'
urlreg = 'http://62.109.6.35/inframanager/sdApi/registerCall'
user_agent1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'

import requests
import time
import json

headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'user-agent': user_agent1
            }
print('1) Проверяем авторизацию')
s = requests.session()
response = s.post(urlin,
       headers=headers,
       data={
           'loginName':'user',
            'passwordEncrypted':'x~h%7F'
            })

print(f'Статус ответа сервера:{response.status_code}')
print(f'Headers:{response.headers}')

if response.json() == {'RedirectUrl': '', 'Success': True} :
    print(f'1) Тест один успешно пройден. Залогинились. Ответ получили:{response.json()}')
else:
    print(f'1) Тест не пройден. Ошибка авторизации. Ответ получили:{response.json()}')
time.sleep(1)

print('2) Проверяем информацию о пользователе')
respinfo = s.get(urlinfo,
                headers=headers,
                data={
                        'loginName':'user',
                        'passwordEncrypted':'x~h%7F'
                        }
                )
# print(respinfo.json())
to_python2 = json.loads(respinfo.text)
if to_python2['UserFullName'] == 'Шишкин Михаил Михайлович':
       print('2) Проверка успешна')
else:
       print(f'2) Ошибка. Ответ получили:{respinfo.json()}')

print('3) Проверяем получение списка срочностей заявки(GetUrgencyList)')
urginfo = s.get(urlurg)
to_python3 = json.loads(urginfo.text)
if to_python3[0]['ID'] == 'b77bee7b-9e25-440a-9658-fb437351f4fa':
       print('3) Заявка успешно зарегистрирована.')
else:
       print(f'3) Ошибка.Ответ получили:{urginfo.json()}')


print('4) Получение доступных клиенту типов заявок (GetCallTypeListForClient)')
callinfo = s.get(urlcall)
# print(callinfo.json())
# print(callinfo.reason)
to_python4 = json.loads(callinfo.text)
if to_python4[0]['ID'] == '00000000-0000-0000-0000-000000000002':
       print('4) Заявка успешно зарегистрирована')
else:
       print(f'4) Ошибка.Ответ получили:{callinfo.json()}')

print('5) Создание заявки от клиента (RegisterCall)')
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'user-agent': user_agent1
            }

rreg = s.post(urlreg,
       headers=headers,
       data={
                'UserID': 'e0a80e5c-2370-41fe-a6b6-94eea86cc798',
                'CalltypeID': '00000000-0000-0000-0000-000000000002',
                'UrgencyID': 'b77bee7b-9e25-440a-9658-fb437351f4fa',
                'CallSummaryName':'краткое описание заявки1',
                'HTMLDescription': 'описание заявки',
                'ServiceItemID': '',
                'ServiceAttendanceID': ''

            })
jsdict = rreg.json()
# print(jsdict)
if jsdict['Message'].startswith('Заявка зарегистрирована '):
    print('5) Заявка успешно зарегистрирована')
else :
    print(f'5) Ошибка.Ответ получили:{rreg.json()}')
# Часть6: Выход пользователя.
response1 = s.post(urlout)

# print(response1.status_code)
# print(response1.headers)
# print(response1.json())
if response1.json() == True:
    print('6) Тест пройден, успешный выход')
else:
    print(f'6) Тест не пройден. Ошибка. Ответ:{response1.json()}')