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
    
    # Ép đúng thứ tự thuộc tính: name -> url -> logo giống hệt file mẫu
    for stream in active_streams:
        name_display = stream.replace("hqtv_blv_", "🎙️ BLV ").replace("hqtv_channel_", "📺 KÊNH ").upper()
        mon_data.append({
            "name": name_display,
            "url": f"https://hqlive.yarncdn.live/live/{stream}/playlist.m3u8",
            "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"
        })
        
    if not mon_data:
        # Giữ nguyên cấu trúc mảng sạch viết liền từng dòng
        mon_data = [
          {"name": "Hội Quán TV - Kênh 1", "url": "https://hqlive.yarncdn.live/live/hqtv_channel_1/playlist.m3u8", "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"},
          {"name": "Hội Quán TV - Kênh 2", "url": "https://hqlive.yarncdn.live/live/hqtv_channel_2/playlist.m3u8", "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"},
          {"name": "Hội Quán TV - Kênh 3", "url": "https://hqlive.yarncdn.live/live/hqtv_channel_3/playlist.m3u8", "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"}
        ]

    # Tạo chuỗi JSON viết liền không khoảng trắng thụt lề
    json_string = json.dumps(mon_data, ensure_ascii=False, separators=(',', ':'))

    # 🌟 GHI FILE THÔ (Dạng nhị phân để bóc sạch sẽ ký tự BOM lỗi ẩn nếu có)
    # Đồng thời ghi thẳng vào đúng file hoiquan.json như bạn muốn
    with open("hoiquan.json", "wb") as f:
        f.write(json_string.encode('utf-8'))

if __name__ == "__main__":
    main()
