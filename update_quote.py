import requests
import datetime
import re

quote_api = "https://api.quotable.io/random"
res = requests.get(quote_api, verify=False)
data = res.json()
quote = f'"{data["content"]}" — {data["author"]}'

today = datetime.datetime.now().strftime("%Y-%m-%d")

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

new_content = re.sub(
    r"<!--START_SECTION:quote-->.*<!--END_SECTION:quote-->",
    f"<!--START_SECTION:quote-->\n🗓️ {today}\n💬 {quote}\n<!--END_SECTION:quote-->",
    content,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
