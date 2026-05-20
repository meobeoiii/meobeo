import requests
import json
from concurrent.futures import ThreadPoolExecutor

def check_stream(blv_slug):
    """Kiểm tra luồng trực tiếp"""
    url = f"https://hqlive.yarncdn.live/live/{blv_slug}/playlist.m3u8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://sv2.hoiquan4.live/",
        "Origin": "https://sv2.hoiquan4.live"
    }
    try:
        response = requests.head(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return blv_slug
    except:
        pass
    return None

def main():
    list_to_check = [
        "hqtv_channel_1", "hqtv_channel_2", "hqtv_channel_3", "hqtv_channel_4", "hqtv_channel_5",
        "hqtv_blv_phanbap", "hqtv_blv_giangapho", "hqtv_blv_soctho", "hqtv_blv_thichthay", 
        "hqtv_blv_caphe", "hqtv_blv_binhluandien", "hqtv_blv_01", "hqtv_blv_02", "hqtv_blv_03"
    ]
    
    active_streams = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_stream, list_to_check)
        for res in results:
            if res:
                active_streams.append(res)
                
    mon_data = []
    
    for stream in active_streams:
        name_display = stream.replace("hqtv_blv_", "🎙️ BLV ").replace("hqtv_channel_", "📺 KÊNH ").upper()
        mon_data.append({
            "name": name_display,
            "url": f"https://hqlive.yarncdn.live/live/{stream}/playlist.m3u8",
            "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"
        })
        
    if not mon_data:
        # ÉP ĐÚNG TỪNG KÝ TỰ CỦA FILE MẪU KHI KHÔNG CÓ TRẬN
        mon_data = [
          {"name": "Hội Quán TV - Kênh 1", "url": "https://hqlive.yarncdn.live/live/hqtv_channel_1/playlist.m3u8", "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"},
          {"name": "Hội Quán TV - Kênh 2", "url": "https://hqlive.yarncdn.live/live/hqtv_channel_2/playlist.m3u8", "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"},
          {"name": "Hội Quán TV - Kênh 3", "url": "https://hqlive.yarncdn.live/live/hqtv_channel_3/playlist.m3u8", "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"}
        ]

    # 🌟 THAY ĐỔI QUAN TRỌNG: Loại bỏ hoàn toàn `indent=2` để ép JSON về dạng chuỗi thô viết liền, 
    # không xuống dòng bừa bãi, giúp MonPlayer đọc trơn tru 100%
    with open("hoiquan.json", "w", encoding="utf-8") as f:
        json.dump(mon_data, f, ensure_ascii=False, separators=(',', ':'))

if __name__ == "__main__":
    main()
