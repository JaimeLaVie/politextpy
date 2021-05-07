#必要なパッケージ、モジュール
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials


#textに保存する
def save_as_text(articles:list, name:str, pattern='w'):
  file = open(f'{name}.text', pattern, encoding = 'utf-8')
  for i in range(0, len(articles)):
    file.write(articles[i]['日付'] +'\n')
    file.write(articles[i]['url'] +'\n')
    file.write(articles[i]['リスト'] +'\n')
    file.write(articles[i]['本文'] + '\n' + '\n' + '\n')
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
'''
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
'''


def save(filename:str):
  #listをjsonとして保存する
  save_as_json(Context, f'{filename}', 'a')
  #listをtextとして保存する
  save_as_text(Context, f'{filename}', 'a')
  #GoogleDriverへアップロードする
  save_to_GoogleDriver(f'{filename}.text')
  save_to_GoogleDriver(f'{filename}.json')


def get_range(paragraphs:list, alpha=0):
  diff = [len(paragraphs[i])-len(paragraphs[i-1]) for i in range(1, len(paragraphs))]
  diff.insert(0, len(paragraphs[0]))
  start = diff.index(max(diff))
  end = diff.index(min(diff)) -1
  end += alpha*(end - start + 1)
  return (start, end)


def get_text(url:str, method='requests', alpha=0, filename='Context'):
  if method == 'requests':#
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html = response.text
    soup = BeautifulSoup(html)
    paragraphs = soup.find('body').find_all('p')
    #
    paragraphs = [x.get_text(separator='') for x in paragraphs]
  elif method == 'selenium':#
    #ブラウザードライブを起動させる
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('chromedriver',options=options)
    driver.implicitly_wait(10) # 一度設定すると、全てのfind_element等の処理時に、
                             # 要素が見つかるまで指定した最大時間待機させるようにすることができます。
                             # 設定した時間内に要素が見つかった場合、残りの時間を無視して次の処理に移ります。
    driver.get(url)
    paragraphs = driver.find_element_by_tag_name('body').find_elements_by_tag_name('p')
    paragraphs = [x.text for x in paragraphs]
    #ブラウザードライブを停止させる
    driver.quit()
  else:
    pass
  #不要の文字を削除する
  paragraphs = [re.sub('[\r\n\u3000]', '', x) for x in paragraphs]
  #本文の範囲を獲得する
  start, end = get_range(paragraphs, alpha)
  #本文に所属する段落を獲得する
  paragraphs = paragraphs[start:end+1]
  #本文を獲得する
  text = '\n'.join(paragraphs)
  save(filename)
  
  return [text, paragraphs]
