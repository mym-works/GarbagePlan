import urllib.request, json, os

def line_bot_response(event, context):
  access_token = os.environ['ACCESS_TOKEN']
  group_id = os.environ['GROUP_ID']
    
  url = "https://api.line.me/v2/bot/message/push" 
  method = "POST"
  headers = {"Content-Type" : "application/json", "Authorization": 'Bearer ' + access_token }

  # PythonオブジェクトをJSONに変換する
  obj = {
    'to': group_id,
    'messages': [{
      'type': 'text',
      'text': "Hello World",
    }],
  }
  json_data = json.dumps(obj).encode("utf-8")

  # httpリクエストを準備してPOST
  request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
  with urllib.request.urlopen(request) as response:
      response_body = response.read().decode("utf-8")

