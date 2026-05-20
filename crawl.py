import requests
import json
from concurrent.futures import ThreadPoolExecutor

def check_stream(blv_slug):
    """
    Hàm kiểm tra xem luồng của BLV hoặc kênh hệ thống đó có đang phát trực tiếp hay không.
    Sử dụng phương thức HEAD để kiểm tra nhanh trạng thái link nhằm tiết kiệm thời gian.
    """
    url = f"https://hqlive.yarncdn.live/live/{blv_slug}/playlist.m3u8"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
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
    # Danh sách quét cạn toàn bộ các luồng phát khả thi của hệ thống Hội Quán
    list_to_check = [
        "hqtv_channel_1", "hqtv_channel_2", "hqtv_channel_3", "hqtv_channel_4", "hqtv_channel_5",
        "hqtv_blv_phanbap", "hqtv_blv_giangapho", "hqtv_blv_soctho", "hqtv_blv_thichthay", 
        "hqtv_blv_caphe", "hqtv_blv_binhluandien", "hqtv_blv_01", "hqtv_blv_02", "hqtv_blv_03"
    ]
    
    active_streams = []
    print("Robot đang tiến hành quét các luồng trực tiếp bằng đa luồng...")
    
    # Sử dụng ThreadPoolExecutor để kiểm tra đồng thời 10 luồng một lúc, tăng tốc độ chạy cho Robot
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_stream, list_to_check)
        for res in results:
            if res:
                active_streams.append(res)
                
    # Cấu trúc JSON chuẩn hóa bắt buộc 100% của MonPlayer
    mon_data = {
        "name": "Nguồn Hội Quán Auto 🔥",
        "author": "Robot Tự Động",
        "groups": [
            {
                "group_name": "Trận Đấu Đang Trực Tiếp ⚽",
                "channels": []
            }
        ]
    }
    
    # Nếu robot tìm thấy luồng đang online, tự động phân tích và nạp vào danh sách kênh
    for stream in active_streams:
        # Làm đẹp tên hiển thị trên giao diện MonPlayer
        name_display = stream.replace("hqtv_blv_", "🎙️ BLV ").replace("hqtv_channel_", "📺 KÊNH HỆ THỐNG ").upper()
        
        mon_data["groups"][0]["channels"].append({
            "name": name_display,
            "url": f"https://hqlive.yarncdn.live/live/{stream}/playlist.m3u8",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": "https://sv2.hoiquan4.live/",
                "Origin": "https://sv2.hoiquan4.live"
            }
        })
        
    # PHÒNG THỦ LỖI ĐỊNH DẠNG: Khi không có trận nào đá, file JSON sẽ bị trống rỗng khiến MonPlayer báo lỗi.
    # Đoạn này sẽ ép robot tự chèn 2 kênh hệ thống mặc định vào để "giữ cấu trúc khung" luôn đúng định dạng.
    if not mon_data["groups"][0]["channels"]:
        print("Hiện tại không có trận đấu nào online. Tiến hành nạp kênh dự phòng chống lỗi trống file...")
        for i in [1, 2]:
            mon_data["groups"][0]["channels"].append({
                "name": f"📺 KÊNH HỆ THỐNG {i} (CHỜ TRẬN ĐẤU)",
                "url": f"https://hqlive.yarncdn.live/live/hqtv_channel_{i}/playlist.m3u8",
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://sv2.hoiquan4.live/",
                    "Origin": "https://sv2.hoiquan4.live"
                }
            })

    # Tiến hành xuất dữ liệu lưu đè vào file nguon.json với định dạng mã hóa UTF-8 tiếng Việt chuẩn
    with open("nguon.json", "w", encoding="utf-8") as f:
        json.dump(mon_data, f, ensure_ascii=False, indent=2)
        
    print("Quá trình tạo file nguon.json hoàn tất đạt chuẩn MonPlayer!")

if __name__ == "__main__":
    main()
