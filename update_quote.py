import requests
import datetime
import re
import random
import json
import os

# APIリソース
QUOTE_APIS = {
    "english": {
        "default": "https://api.quotable.io/random",
        "programming": "https://api.quotable.io/random?tags=technology",
        "business": "https://api.quotable.io/random?tags=business",
        "life": "https://api.quotable.io/random?tags=life"
    },
    "japanese": {
        "default": "https://meigen.doodlenote.net/api/json.php",
        "programming": "https://meigen.doodlenote.net/api/json.php?c=computer",
        "business": "https://meigen.doodlenote.net/api/json.php?c=business",
        "life": "https://meigen.doodlenote.net/api/json.php?c=life"
    }
}

# 設定
CONFIG_PATH = ".quote_config.json"
DEFAULT_CONFIG = {
    "language": "random",  # "english", "japanese", "random"
    "category": "random",  # "default", "programming", "business", "life", "random"
    "show_source": True,   # 出典情報を表示するかどうか
    "show_category": True  # カテゴリを表示するかどうか
}

def load_config():
    """設定ファイルを読み込む"""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_CONFIG
    else:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def get_quote(config):
    """指定された設定に基づいて名言を取得する"""
    # 言語の選択
    if config["language"] == "random":
        language = random.choice(["english", "japanese"])
    else:
        language = config["language"]
    
    # カテゴリの選択
    if config["category"] == "random":
        category = random.choice(["default", "programming", "business", "life"])
    else:
        category = config["category"]
    
    # APIからデータを取得
    api_url = QUOTE_APIS[language][category]
    try:
        res = requests.get(api_url, verify=False, timeout=10)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"Error fetching quote: {e}")
        # エラー時はデフォルトの引用を返す
        return {
            "content": "The best preparation for tomorrow is doing your best today.",
            "author": "H. Jackson Brown Jr.",
            "source": "Unknown",
            "language": language,
            "category": category
        }
    
    # レスポンスを解析
    if language == "english":
        quote_data = {
            "content": data["content"],
            "author": data["author"],
            "source": data.get("tags", ["Unknown"])[0] if data.get("tags") else "Unknown",
            "language": "english",
            "category": category
        }
    else:  # japanese
        quote_data = {
            "content": data["meigen"],
            "author": data["author"],
            "source": data.get("source", "不明"),
            "language": "japanese",
            "category": category
        }
    
    return quote_data

def format_quote(quote_data, config):
    """引用情報をフォーマットする"""
    quote_str = f'"{quote_data["content"]}" — {quote_data["author"]}'
    
    # カテゴリと言語の絵文字
    category_emoji = {
        "default": "💭",
        "programming": "💻",
        "business": "💼",
        "life": "🌱"
    }
    
    language_emoji = {
        "english": "🇬🇧",
        "japanese": "🇯🇵"
    }
    
    # 今日の日付
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # 出力の構築
    output = [f"🗓️ {today}"]
    
    # 言語とカテゴリの表示
    display_info = []
    display_info.append(language_emoji[quote_data["language"]])
    
    if config["show_category"]:
        display_info.append(category_emoji[quote_data["category"]])
    
    if display_info:
        output.append(" ".join(display_info))
    
    # 引用の追加
    output.append(f"💬 {quote_str}")
    
    # 出典情報の追加
    if config["show_source"] and quote_data["source"] != "Unknown" and quote_data["source"] != "不明":
        output.append(f"📚 Source: {quote_data['source']}")
    
    return "\n".join(output)

def update_readme(quote_content):
    """READMEファイルを更新する"""
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = re.sub(
        r"<!--START_SECTION:quote-->.*<!--END_SECTION:quote-->",
        f"<!--START_SECTION:quote-->\n{quote_content}\n<!--END_SECTION:quote-->",
        content,
        flags=re.DOTALL
    )
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    # 設定を読み込む
    config = load_config()
    
    # 引用を取得
    quote_data = get_quote(config)
    
    # 引用をフォーマット
    formatted_quote = format_quote(quote_data, config)
    
    # READMEを更新
    update_readme(formatted_quote)
    
    print("Quote updated successfully!")

if __name__ == "__main__":
    main()