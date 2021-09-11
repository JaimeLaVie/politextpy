#必要なパッケージ、モジュール
import requests
from bs4 import BeautifulSoup
import json
import re

#textに保存する
def save_as_text(context:list, name:str, pattern='w'):
  file = open(f'{name}.text', pattern, encoding = 'utf-8')
  for i in range(0, len(context)):
    file.write(context[i] + '\n')
  file.close()
  
  
#listをjsonとして保存する
def save_as_json(data:list, name:str, pattern='w'):
  #データをファイルに書き込む
  file = open(f'{name}.json', pattern)
  for i in data:
    json_i = json.dumps(i)
    file.write(json_i+'\n')
  file.close()

  
#jsonファイルをlistに転換する
def json_to_list(name:str, pattern='r'):
  #jsonからデータを読み込む
  result = []
  with open(f'{name}.json', pattern) as f:
    #データを読み込み、分割する。
    #最後の要素が「改行」なので、それを削除する
    new_list = f.read().split('\n')[:-1]
    for x in new_list:
        json_x = json.loads(x)
        result.append(json_x)
  f.close()
  return result


def save_to_GoogleDriver(name:str):
  auth.authenticate_user()
  gauth = GoogleAuth()
  gauth.credentials = GoogleCredentials.get_application_default()
  drive = GoogleDrive(gauth)
  upload_text = drive.CreateFile()
  upload_text.SetContentFile(name)
  upload_text.Upload()


def save(Context:list, filename:str):
  #listをjsonとして保存する
  save_as_json(Context, f'{filename}', 'a')
  #listをtextとして保存する
  save_as_text(Context, f'{filename}', 'a')
  #GoogleDriverへアップロードする
  save_to_GoogleDriver(f'{filename}.text')
  save_to_GoogleDriver(f'{filename}.json')


def GetText(url:str, filename='Context'):
  response = requests.get(url)
  response.encoding = response.apparent_encoding
  html = response.text
  soup = BeautifulSoup(html)
  
  [s.extract() for s in soup('ul')]
  paragraphs = soup.find('body').find_all('p')
  MaxLengthIndex = [len(x) for x in paragraphs].index(max([len(x) for x in paragraphs]))
  p_max = soup.find('body').find_all('p')[MaxLengthIndex]
  context = p_max.parent.get_text()
  #不要の文字を削除する
  context = re.sub('[ 　\r\n\u3000]', '', context)
  print(context)
  list_temp = []
  list_temp.append(context)
  save_as_text(list_temp, filename)
  return context


if __name__ == '__main__':
  context = GetText('https://www.asahi.com/articles/ASP8F6J6CP8FULZU008.html?iref=pc_rellink_03', filename='Context')
