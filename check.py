import platform
import psutil
import multiprocessing

def suggest_command():
    cores = multiprocessing.cpu_count()
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3))
    
    # Gợi ý cơ bản theo mức độ mạnh của máy
    if cores <= 4 or ram_gb <= 8:
        level = "Máy yếu"
        threads = 12
        rate = 64
        time = 9999
    elif cores <= 8 or ram_gb <= 16:
        level = "Máy trung bình"
        threads = 32
        rate = 128
        time = 9999
    elif cores <= 16 or ram_gb <= 32:
        level = "Máy mạnh"
        threads = 128
        rate = 256
        time = 9999
    else:
        level = "Máy rất mạnh"
        threads = 256
        rate = 400
        time = 9999

    print("🖥️ Phát hiện hệ thống:")
    print(f"• Hệ điều hành: {platform.system()} {platform.release()}")
    print(f"• Số CPU: {cores} cores")
    print(f"• RAM: {ram_gb} GB")
    print(f"\n🎯 {level} — Gợi ý lệnh chạy:")
    print(f"node d.js GET https://target.com {time} {threads} {rate} proxy.txt")

if __name__ == "__main__":
    suggest_command()
