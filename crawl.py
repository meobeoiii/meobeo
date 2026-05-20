import requests
import json
from concurrent.futures import ThreadPoolExecutor

def check_stream(blv_slug):
    """Hàm kiểm tra xem luồng của BLV đó có đang phát trực tiếp hay không"""
    url = f"https://hqlive.yarncdn.live/live/{blv_slug}/playlist.m3u8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://sv2.hoiquan4.live/"
    }
    try:
        # Gửi một yêu cầu siêu ngắn (HEAD) để check xem link có chạy được không (đỡ tốn băng thông)
        response = requests.head(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return blv_slug
    except:
        pass
    return None

def main():
    # Danh sách tất cả các BLV và Kênh hệ thống của Hội Quán (Quét cạn)
    list_to_check = [
        "hqtv_channel_1", "hqtv_channel_2", "hqtv_channel_3", "hqtv_channel_4", "hqtv_channel_5",
        "hqtv_blv_phanbap", "hqtv_blv_giangapho", "hqtv_blv_soctho", "hqtv_blv_thichthay", 
        "hqtv_blv_caphe", "hqtv_blv_binhluandien", "hqtv_blv_01", "hqtv_blv_02", "hqtv_blv_03"
    ]
    
    active_streams = []
    
    print("Robot đang quét các trận đấu đang trực tiếp...")
    # Sử dụng đa luồng (Multi-threading) để quét nhanh gấp 10 lần
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_stream, list_to_check)
        for res in results:
            if res:
                active_streams.append(res)
                
    # Cấu trúc file JSON chuẩn cho MonPlayer
    mon_data = {
        "name": "Nguồn Hội Quán Auto 🔥",
        "author": "Robot Tự Động",
        "version": "1.0.0",
        "groups": [{
            "group_name": "Trận Đấu Đang Trực Tiếp ⚽",
            "channels": []
        }]
    }
    
    # Nếu tìm thấy luồng đang phát, tự động nạp vào file
    for stream in active_streams:
        name_display = stream.replace("hqtv_blv_", "🎙️ BLV ").replace("hqtv_channel_", "📺 KÊNH DỰ PHÒNG ").upper()
        mon_data["groups"][0]["channels"].append({
            "name": name_display,
            "url": f"https://hqlive.yarncdn.live/live/{stream}/playlist.m3u8",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://sv2.hoiquan4.live/",
                "Origin": "https://sv2.hoiquan4.live"
            }
        })
        
    # Trường hợp không có trận nào đá (file trống sẽ bị MonPlayer báo lỗi định dạng)
    # Robot sẽ tự động nhét 2 kênh mặc định vào để "giữ chỗ" chống lỗi định dạng cho app
    if not mon_data["groups"][0]["channels"]:
        mon_data["groups"][0]["channels"].append({
            "name": "⏰ Hiện tại chưa có trận đấu nào phát sóng",
            "url": "https://hqlive.yarncdn.live/live/hqtv_channel_1/playlist.m3u8",
            "headers": {"Referer": "https://sv2.hoiquan4.live/"}
        })

    # Ghi dữ liệu ra file nguon.json
    with open("nguon.json", "w", encoding="utf-8") as f:
        json.dump(mon_data, f, ensure_ascii=False, indent=2)
    print("Đã cập nhật xong file nguon.json!")

if __name__ == "__main__":
    main()
