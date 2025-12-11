# class file_download:
#
#     def __init__(self, ):

import socket
import time
from urllib.parse import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.spiders.crawler import MySpider
# from proxy.certificate_manager import create_certificate, update_nginx_config
# from Myproject.Myproject.items import PacketFromDB
# from Myproject.Myproject.spiders.go_to_fuzzer import SendToFuzzer
# from server import PacketLoggerServer
from fuzzers.command_injection.commandimain import command_injection
from fuzzers.sql_injection.sqlimain import sqli_get_option, sql
from fuzzers.ssrf.ssrfmain import ssrf_get_option, ssrf
from fuzzers.file_download.filedownloadmain import file_download
from fuzzers.xss.XSS import xss


def connect_server():
    try:
        server_ip = "13.209.63.65"
        server_port = 8888
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
        client_socket.connect((server_ip, server_port))
        print("Porxy Connected")
    except Exception as e:
        print("Failed to connect to server:", e)

# def extract_domain(url):
#     parsed_url = urlparse(url)
#     domain = parsed_url.netloc
#     return domain

def display_menu(options):
    print("======================================================================")
    print("Select option to toggle (ON/OFF):")
    for i, (option, status) in enumerate(options.items(), start=1):
        status_str = "ON" if status else "OFF"
        print(f"{i}. {option} [{status_str}]")
    print(f"{len(options) + 1}. ALL")
    print("0. Exit")
    print("======================================================================")

def execute_option(option_name):
    if option_name == "xss":
        xss()
    elif option_name == "sql_injection":
        sqli_get_option()
    elif option_name == "SSRF":
        ssrf_get_option()
    elif option_name == "Command Injection":
        command_injection()
    elif option_name == "File Download Vulnerabilities":
        file_download()
    else:
        print(f"Invalid option: {option_name}")

def toggle_option(options, choice):
    if choice == len(options) + 1:  # Toggle ALL options
        all_on = all(options.values())
        for key in options:
            options[key] = not all_on
    
        xss()
        sql()
        ssrf()
        command_injection()
        file_download()

    elif choice > 0 and choice <= len(options):
        option_name = list(options.keys())[choice - 1]
        options[option_name] = not options[option_name]

        if option_name:
            execute_option(option_name)
            options[option_name] = not options[option_name]

def main():
    print("======================================================================")
    print('''
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⢀⣠⣤⣶⠾⠟⠛⠛⠛⠛⠛⠛⠻⠷⣶⣤⣄⡀⠀⠀⠀⠀⠀
    ⠀⠀⠀⣠⡾⠟⠋⠁⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠈⠙⠻⢷⣄⠀⠀⠀
    ⠀⢀⣾⠋⠀⠀⠀⠀⠶⠶⠿⠛⠛⠛⠛⠛⠛⠿⠶⠶⠀⠀⠀⠀⠙⣷⡀⠀
    ⠀⣿⠃⠀⠀⠀⠀⠀⢀⣠⣤⣤⡀⠀⠀⢀⣤⣤⣄⡀⠀⠀⠀⠀⠀⠘⣿⠀
    ⠘⣿⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣧⣼⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⣿⠃
    ⠀⠻⣧⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣼⠟⠀
    ⠀⠀⠙⢷⣄⡀⠘⣿⠛⠛⣿⡟⠛⢻⡟⠛⢻⣿⠛⠛⣿⠁⢀⣠⡾⠋⠀⠀
    ⠀⠀⠀⠀⠉⠻⢷⣿⣧⠀⠉⠁⣠⡿⢿⣄⠈⠉⠀⣼⣿⡾⠟⠉⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢹⣷⣶⣾⡟⠀⠀⢻⣷⣶⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣀⣀⣸⣿⢀⣿⠁⠀⠀⠈⣿⡀⣿⣇⣀⣀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⣴⡟⠋⢉⣉⣀⣸⡏⠀⠀⠀⠀⢹⣇⣀⣉⡉⠙⢻⣦⠀⠀⠀⠀
    ⠀⠀⠀⠀⣿⡀⠘⠛⠛⠉⣹⣷⠀⠀⠀⠀⣾⣏⠉⠛⠛⠃⢀⣿⠀⠀⠀⠀
    ⠀⠀⠀⠀⠘⠻⠷⠾⠛⠛⠛⠛⢷⣤⣤⡾⠛⠛⠛⠛⠷⠾⠟⠃⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀
    ''')

    print("Hello, this is Fuzzingzzingi")
    print("This fuzzer is a program developed together by WHS 2nd class trainees.")
    print("======================================================================\n")
    time.sleep(0.7)

    # URL 입력 받기
    print("Please enter the target URL")
    target_url = input("> ")
    print("Please enter the login URL")
    login_url = input("> ")
    print("Please enter the username")
    username = input("> ")
    print("Please enter the password")
    password = input("> ")
    
    # 도메인 추출
    # domain = extract_domain(target_url)

    # 인증서 생성 및 Nginx 설정 업데이트
    # key_file, crt_file = create_certificate(domain)
    # update_nginx_config(domain, key_file, crt_file)
    
    connect_server()
    
    # Scrapy 크롤러 프로세스 시작
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(MySpider, start_url=target_url, login_url = login_url, username = username, password = password)  # MySpider 클래스의 이름을 사용
    # process.start()

    # 취약점 옵션 선택
    options = {
    "xss": False,
    "sql_injection": False,
    "SSRF": False,
    "Command Injection": False,
    # "File Upload Vulnerabilities": False,
    "File Download Vulnerabilities": False
    }

    while True:
        time.sleep(2)
        display_menu(options)
        time.sleep(0.5)
        try:
            choice = int(input("Enter your choice: "))
            if choice == 0:
                print("Exiting...")
                break
            toggle_option(options, choice)
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")
                          
    # 보고서 기능 구현

    # 오류 처리 기능 및 로깅 기능 구현

if __name__ == '__main__':
    main()
    # server = PacketLoggerServer()
    # server.run()