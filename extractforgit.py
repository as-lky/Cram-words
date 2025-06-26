from openai import OpenAI
from PyPDF2 import PdfReader
from tqdm import tqdm

client = OpenAI(api_key="**************", base_url="https://api.deepseek.com")
reader = PdfReader("四级.pdf")
num_pages = len(reader.pages)

def list_l_r(l, r, id=1):
    text = ""
    for i in range(l-1, r):
        text += reader.pages[i].extract_text()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"你好,我需要你帮助我完成任务。从下列文本当中的word list提取出我指定格式的内容，具体而言为每个list的单词加逗号加单词的中文释义，两个list之间留出区分。当前请你提取list {id} 的内容(即出现list{id}之前的单词都不用管)\n"},
            {"role": "user", "content": "规则如下：\n 1.以以下格式反馈给我： \n abandon@v.抛弃 \n acute@j.剧烈的;强度大的 \n 2.词性缩写与中文释义直接不要加空格，比如n. 卷改为n.卷 \n 3.如果有多个词性的单词,在两个词性的中文释义之间加入分号;而不是空格或逗号,即一行只能有一个逗号,用于分割单词和释义.\n 4.两行单词之间不要空行.\n"},
            {"role": "user", "content": f"内容如下: \n {text}"},
        ],
        stream=False
    )
    content = response.choices[0].message.content 
    with open(f"四级/list_{id}.txt", "w", encoding="utf-8") as f:
        f.write(content)

def word_list(id):
    pre = [1, 14, 26, 38, 49, 61, 73, 85, 96, 108, 118, 129, 140, 151, 163, 174, 185, 196, 207, 
           218, 228, 238, 247, 257, 266, 275, 284, 293, 302, 310, 318, 325, 332, 339, 347, 355]
    start = pre[id - 1] + 9
    end = pre[id] + 8
    list_l_r(start, end, id)

for i in tqdm(range(2, 36)):
   word_list(i)