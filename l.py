import requests
import threading
from queue import Queue
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

banner = f"""{Fore.GREEN}

████████╗██████╗░██╗░░░██╗███╗░░░███╗██████╗░██████╗░░█████╗░██╗░░░██╗██╗░░██╗
╚══██╔══╝██╔══██╗██║░░░██║████╗░████║██╔══██╗██╔══██╗██╔══██╗╚██╗░██╔╝╚██╗██╔╝
░░░██║░░░██████╔╝██║░░░██║██╔████╔██║██████╔╝██████╔╝██║░░██║░╚████╔╝░░╚███╔╝░
░░░██║░░░██╔══██╗██║░░░██║██║╚██╔╝██║██╔═══╝░██╔══██╗██║░░██║░░╚██╔╝░░░██╔██╗░
░░░██║░░░██║░░██║╚██████╔╝██║░╚═╝░██║██║░░░░░██║░░██║╚█████╔╝░░░██║░░░██╔╝╚██╗
░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░░░░╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░╚═╝
{Style.RESET_ALL}"""

print(banner)

proxy_file = input(Fore.YELLOW + "[?] Nhập tên file chứa proxy (ip:port): ").strip()
output_file = input(Fore.GREEN + "[?] Nhập tên file lưu proxy sống: ").strip()

if not os.path.exists(proxy_file):
    print(Fore.RED + f"[!] Không tìm thấy file: {proxy_file}")
    exit()

q = Queue()
lock = threading.Lock()

def check_proxy(proxy):
    try:
        proxies_dict = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        r = requests.get('http://httpbin.org/ip', proxies=proxies_dict, timeout=5)
        if r.status_code == 200:
            with lock:
                print(Fore.GREEN + f"[LIVE] {proxy}")
                with open(output_file, 'a') as out:
                    out.write(proxy + '\n')
        else:
            with lock:
                print(Fore.RED + f"[DEAD] {proxy}")
    except:
        with lock:
            print(Fore.RED + f"[DEAD] {proxy}")

def worker():
    while True:
        proxy = q.get()
        if proxy is None:
            break
        check_proxy(proxy)
        q.task_done()

# Khởi tạo luồng
num_threads = 2000
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    threads.append(t)

print(Fore.CYAN + f"\n[✓] Đang kiểm tra proxy trong: {proxy_file}...\n")

# Đọc từng dòng proxy từ file và đưa vào Queue (ít RAM, ignore lỗi)
with open(proxy_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        proxy = line.strip()
        if proxy:
            while q.qsize() > 2000:
                time.sleep(0.01)
            q.put(proxy)

# Chờ xử lý xong
q.join()

# Dừng các luồng
for _ in range(num_threads):
    q.put(None)
for t in threads:
    t.join()

print(Fore.MAGENTA + f"\n[✔] Hoàn tất! Proxy sống đã lưu tại: {output_file}")
