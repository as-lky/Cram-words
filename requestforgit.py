import requests
import re
import os
from bs4 import BeautifulSoup


session = requests.Session()
login_text = session.get('https://www.cram.com/user/login')
soup = BeautifulSoup(login_text.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrfToken"})["value"]
login_data = {
    'username': '*******',
    'password': '*******',
    'csrfToken': csrf_token,
    'loginButton': 'Sign in',
}
print(csrf_token)
login = session.post('https://www.cram.com/user/login', data=login_data, allow_redirects=False)

def upload_flashcard(title, subject, lines):
    cnt = 0
    position = []
    card_front_html = []
    card_back_html = []
    for text in lines:
        front = re.match(r'(.+)@', text).group(1)
        back = re.match(r'.+@(.+)', text).group(1)
        position.append(str(cnt + 1))
        card_front_html.append(front)
        card_back_html.append(back)
        cnt += 1

    payload = {
        'title' : title,
        'subject' : subject,
        'position[]' : position,
        'card_front_html[]' : card_front_html,
        'card_back_html[]' : card_back_html,
        'uploadTo' : '/image/upload-image',
        'access' : 'public',
        'item_delimiter' : r'\t',
        'custom_wd' : '-',
        'line_delimiter' : r'\n',
        'custom_ld' : '\n\n',
        'csrfToken' : f'{csrf_token}',
        'description' : '',
        'user_text' : '',
        'show_hints' : '',
        'lang_front' : '',
        'lang_back' : '',
        'lang_hint' : '',
        'image_front_preview[]' : '',
        'image_front[]' : '',
        'image_front_provider[]' : '',
        'image_front_id[]' : '',
        'image_back_preview[]' : '',
        'image_back[]' : '',
        'image_back_provider[]' : '',
        'image_back_id[]' : '',
        'image_hint_preview[]' : '',
        'image_hint[]' : '',
        'image_hint_provider[]' : '',
        'image_hint_id[]' : '',
        'card_hint_html[]' : '',
    }
    while(True):
        response = session.post('https://www.cram.com/flashcards/create', data=payload, allow_redirects=False)
        print(response.status_code)  # Check if the flashcards were created successfully
        if response.status_code == 200:
            continue
        elif response.status_code == 302:
            break
        
W = [_ for _ in range(12, 28)]
for i in W:
    print(i)
    name = ''
    if i < 10:
        name = f'list0{i}'
    else:
        name = f'list{i}'

    if os.path.exists(f'四级/list_{i}.txt'):
        with open(f'四级/list_{i}.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        title = f'lky CET4 ' + name
        subject = 'CET4'
        upload_flashcard(title, subject, lines)

#upload_flashcard('bb', 'try', ['abandon@v.抛弃', 'acute@j.剧烈的;强度大的', 'adopt@v.采纳;采用', 'adventure@n.冒险', 'advice@n.建议'])
