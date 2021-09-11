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


def GetText(url:str, separator='', filename='Context'):
  success = False
  attempt = 0
  while attempt < 3 and success = False
    try:
      response = requests.get(url)
      response.encoding = response.apparent_encoding
      html = response.text
      soup = BeautifulSoup(html)
  
      [s.extract() for s in soup('ul')]
      #著作権を声明する部分を削除する
      paragraphs = soup.find('body').find_all('p')[:-2]
      #一番長い段落を見つけ出し、そのインデックスを変数MaxLengthIndexとして保存する
      lengths = [len(x.get_text()) for x in paragraphs]
      MaxLengthIndex = lengths.index(max(lengths))
      p_max = soup.find('body').find_all('p')[MaxLengthIndex]
      paragraphs = p_max.parent.find_all('p')
      paragraphs = [x.get_text() for x in paragraphs]
  
      #不要の文字を削除する
      if separator == '':
        punctuation = '[ 　\r\n\u3000]'
      else:
        punctuation = '[　\r\n\u3000]' 
      paragraphs = [re.sub(punctuation, '', x) for x in paragraphs]
      paragraphs = [x for x in paragraphs if len(x)>0]
      #段取りなしで本文を獲得する
      context = ''.join(paragraphs)
      print(context)
      success = True
    except:
      attempt += 1
  save_as_text(context, filename)
  return context



if __name__ == '__main__':
  context = GetText('https://mainichi.jp/articles/20210911/k00/00m/010/067000c?cx_testId=122&cx_testVariant=cx_2&cx_artPos=2#cxrecs_s', filename='Context')
