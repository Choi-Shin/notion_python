import requests
import json
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

token = os.getenv("TOKEN")
databaseId = os.getenv("DATABASE_ID")
path = os.getenv("PATH")

def readDatabase(databaseId, headers):

    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)
    if res.status_code != 200:
        print(res.text)
    print(res.status_code)

    data = res.json()

    with open(f"{path}/db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)


headers = {
    "Authorization": "Bearer " + token,
    "Notion-Version": "2022-02-22"
}


def createPage(databaseId, headers, page_values):

    createdUrl = "https://api.notion.com/v1/pages"

    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "영단어": {
                "rich_text": [
                    {
                        "text": {
                            "content": page_values['영단어']
                        }
                    }
                ]
            },
            "단어뜻": {
                "rich_text": [
                    {
                        "text": {
                            "content": page_values['단어뜻']
                        }
                    }
                ]
            },
            "수준": {
                "select":
                    {
                        "name": page_values['수준']
                    }
            }
        }
    }

    data = json.dumps(newPageData)

    res = requests.post(createdUrl, headers=headers, data=data)
    if res.status_code != 200:
        print(res.text)
    print(res.status_code)


headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22"
}
# 이미 들어가 있는 단어 체크하기
uploaded_words = f'{path}/db.json'
with open(uploaded_words, 'r') as file:
    check = json.load(file)['results'][0]

# excel_to_json을 이용하여 만든 json 파일을 불러오기
file_path = f'{path}/new_word.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# 없는 단어만으로 새로운 페이지를 제작하기
for d in data:
    if not d['영단어'] in check['properties']['영단어']:
        createPage(databaseId, headers, d)
