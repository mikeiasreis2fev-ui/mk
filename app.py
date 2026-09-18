import requests
import os

# Pega as configurações das Secrets do GitHub (para não expor sua senha publicamente)
XTREAM_HOST = os.getenv("XTREAM_HOST", "http://up.kiwi")
XTREAM_USER = os.getenv("XTREAM_USER", "351921603109")
XTREAM_PASS = os.getenv("XTREAM_PASS", "34939156")
OUTPUT_FILENAME = "playlist.m3u"

def fetch_xtream_data(action):
    url = f"{XTREAM_HOST}/player_api.php"
    params = {"username": XTREAM_USER, "password": XTREAM_PASS, "action": action}
    try:
        r = requests.get(url, params=params, timeout=20)
        return r.json()
    except:
        return []

def generate():
    print("Gerando lista...")
    live_cats = {str(c['category_id']): c['category_name'] for c in fetch_xtream_data("get_live_categories") if 'category_id' in c}
    live_streams = fetch_xtream_data("get_live_streams")
    
    m3u = ["#EXTM3U\n"]
    if live_streams:
        for s in live_streams:
            name = s.get("name", "Sem Nome")
            sid = s.get("stream_id")
            cid = str(s.get("category_id", ""))
            logo = s.get("stream_icon", "")
            cat_name = live_cats.get(cid, "Canais")
            url = f"{XTREAM_HOST}/live/{XTREAM_USER}/{XTREAM_PASS}/{sid}.ts"
            m3u.append(f'#EXTINF:-1 tvg-id="{sid}" tvg-logo="{logo}" group-title="{cat_name}",{name}\n{url}\n')
    
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        f.writelines(m3u)
    print("Concluído!")

if __name__ == "__main__":
    generate()
