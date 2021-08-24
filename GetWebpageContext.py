#必要なパッケージ、モジュール
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import matplotlib.pyplot as plt

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)


#textに保存する
def save_as_text(data:list, name:str, pattern='w'):
  file = open(f'{name}.text', pattern, encoding = 'utf-8')
  for i in range(0, len(articles)):
    file.write(articles[i]['url'] +'\n')
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


def save(Context:list, filename:str):
  #listをjsonとして保存する
  save_as_json(Context, f'{filename}', 'a')
  #listをtextとして保存する
  save_as_text(Context, f'{filename}', 'a')
  #GoogleDriverへアップロードする
  save_to_GoogleDriver(f'{filename}.text')
  save_to_GoogleDriver(f'{filename}.json')


def get_range(paragraphs:list, factor, distance):
  diff = [len(paragraphs[i])-len(paragraphs[i-1]) for i in range(1, len(paragraphs))]
  diff.insert(0, len(paragraphs[0]))
  print(diff)
  #length = [len(x) for x in paragraphs]
  #length_filter = []
  filter = []
  j_prev = 0
  for j in range(0, len(diff)):
    if abs(diff[j]) >= max(diff)/factor:
      if diff[j]*diff[j_prev] <= 0 and diff[j] < 0:
        if j - j_prev <= distance:
          j_prev = j
          filter.append(j)
        elif not filter:
          j_prev = j
          filter.append(j)  
      elif diff[j]*diff[j_prev] <= 0 and diff[j] >= 0:
        if j - j_prev <= distance - 5:
          j_prev = j
          filter.append(j)
        elif not filter:
          j_prev = j
          filter.append(j)
      else:
        if j - j_prev <= distance:
          j_prev = j
          filter.append(j)
        elif not filter:
          j_prev = j
          filter.append(j)
  print(filter)
  start = filter[0]
  end = filter[-1]
  return [start, end]


def Method1(url:str):
  response = requests.get(url)
  response.encoding = response.apparent_encoding
  html = response.text
  soup = BeautifulSoup(html)
  [s.extract() for s in soup('ul')]
  paragraphs = soup.find('body').find_all('p')
  paragraphs = [x.get_text(separator='') for x in paragraphs]
  return paragraphs


def Method2(url:str):
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
  return paragraphs


#長い文章になると、distanceに5を、短い文章になると、distanceに3を指定する
def get_text(url:str, method='requests', filename='Context', factor=3.5, distance=10):
  if method == 'requests':
    paragraphs = Method1(url)
  elif method == 'selenium':
    paragraphs = Method2(url)
  else:
    pass
  #不要の文字を削除する
  paragraphs = [re.sub('[ 　\r\n\u3000]', '', x) for x in paragraphs]
  paragraphs = [x for x in paragraphs if len(x)>0]
  print([len(x) for x in paragraphs])
  #本文の範囲を獲得する
  start, end = get_range(paragraphs, factor, distance)
  #本文に所属する段落を獲得する
  paragraphs = paragraphs[start:end+1]
  #段取りなしで本文を獲得する
  text = ''.join(paragraphs)
  #save(paragraphs, filename)
  return [text, paragraphs]


if __name__ == '__main__':
  text, paragraphs = get_text('https://www.asahi.com/articles/ASP8R63RCP8RUTIL02W.html?iref=comtop_7_04', method='requests', filename='Context', factor=3.5, distance=10)
