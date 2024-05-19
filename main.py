# 구현된 코드 import 
from server import PacketLoggerServer

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

# 프록시? 크롤러?에 URL 전달 하는 코드 구현 
print("Please enter the target URL")
input("> ")


print("======================================================================")
print("Select option")
print("1. XSS")
print("2. SQL Injection")
print("3. SSRF")
print("4. Command Injection")
print("5. File Upload Vulnerabilities")
print("6. File Download Vulnerabilities")
print("7. ALL")
print("======================================================================")

# 선택한 취약점에 따른 코드 실행 구현 

# 보고서 기능 구현 

# 오류 처리 기능 및 로깅 기능 구현 
if __name__ == '__main__':
    server = PacketLoggerServer()
    server.run()