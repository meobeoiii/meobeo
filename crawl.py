import requests
import json
from concurrent.futures import ThreadPoolExecutor

def check_stream(blv_slug):
    """Kiểm tra xem luồng phát có đang trực tiếp hay không"""
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
    # Danh sách các kênh và BLV hệ thống Hội Quán
    list_to_check = [
        "hqtv_channel_1", "hqtv_channel_2", "hqtv_channel_3", "hqtv_channel_4", "hqtv_channel_5",
        "hqtv_blv_phanbap", "hqtv_blv_giangapho", "hqtv_blv_soctho", "hqtv_blv_thichthay", 
        "hqtv_blv_caphe", "hqtv_blv_binhluandien", "hqtv_blv_01", "hqtv_blv_02", "hqtv_blv_03"
    ]
    
    active_streams = []
    print("Robot đang quét các luồng trực tiếp...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_stream, list_to_check)
        for res in results:
            if res:
                active_streams.append(res)
                
    # 🌟 KHỞI TẠO MẢNG PHẲNG CHUẨN 100% THEO FILE HOIQUAN1.JSON MẪU
    mon_data = []
    
    # Nếu có luồng online, nạp vào danh sách
    for stream in active_streams:
        name_display = stream.replace("hqtv_blv_", "🎙️ BLV ").replace("hqtv_channel_", "📺 KÊNH ").upper()
        mon_data.append({
            "name": name_display,
            "url": f"https://hqlive.yarncdn.live/live/{stream}/playlist.m3u8",
            "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"
        })
        
    # 🌟 NẾU KHÔNG CÓ TRẬN (ÉP BUỘC TẠO RA FILE GIỐNG HỆT CÁC KÊNH CHÍNH CỦA FILE MẪU)
    # Loại bỏ hoàn toàn cụm "headers" phức tạp gây lỗi định dạng trên MonPlayer
    if not mon_data:
        print("Không có trận đấu. Tiến hành tạo danh sách kênh dự phòng chuẩn mẫu...")
        for i in [1, 2, 3]:
            mon_data.append({
                "name": f"Hội Quán TV - Kênh {i}",
                "url": f"https://hqlive.yarncdn.live/live/hqtv_channel_{i}/playlist.m3u8",
                "logo": "https://pub-26bab83910ab4b5781549d12d2f0ef6f.r2.dev/hq.png"
            })

    # Xuất ra file nguon.json công khai
    with open("nguon.json", "w", encoding="utf-8") as f:
        json.dump(mon_data, f, ensure_ascii=False, indent=2)
        
    print("Đã cấu trúc lại file JSON siêu sạch đạt chuẩn MonPlayer!")

if __name__ == "__main__":
    main()
