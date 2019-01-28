import requests
from bs4 import BeautifulSoup


def login():
	print("\033c")
	user = input('Username: ')
	password = input('Password: ')
	
	flag = True
	
	urls = '''http://library.iiitnr.edu.in:7001/cgi-bin/koha/opac-user.pl''' 

	datas = {
	    'userid':user,
	    'password':password
	}

	r = requests.post(url = urls, data = datas)
	p = BeautifulSoup(r.text,'lxml')
	h2 = p.find('div',class_='maincontent')
	h2 = h2.find('h2')
	if(not h2):
		flag = False
		return r.text, flag
	else:
		return r.text, flag		



def issuedBooks(text):
	print("\033c")
	parser = BeautifulSoup(text,"lxml")
	name = parser.find('div',class_='maincontent')
	name = name.find('h2')
	name= name.stripped_strings
	print("\n\n".join(name))
	print("\n\n\n")

	a = parser.find(id = 'checkoutst')
	a=a.find_all('tr')
	print(len(a))
	print("\n\n")
	for i in range(1,len(a)):
		b = a[i].find('a',{"class":"title"})
		print("Book: Name: "+ b.text)
		b = a[i].find('td',{"class":"author"})
		print("Authors:  "+b.text)
		b = a[i].find('td',{"class":"date_due"})
		b= b.stripped_strings
		print("".join(b))
		b = a[i].find('td',{"class":"barcode"})
		b= b.stripped_strings
		print("".join(b))
		b = a[i].find('td',{"class":"renew"})
		b= b.stripped_strings
		print("".join(b))
		b = a[i].find('td',{"class":"fines"})
		b= b.stripped_strings
		print("".join(b))
		print("\n\n")
		print("\n_________________________________\n\n\n")

		
def search():
	print("\033c")
	search = str(input("Search: ")).strip()
	print("\n\n")

	urls = '''http://library.iiitnr.edu.in:7001/cgi-bin/koha/opac-search.pl'''

	datas = {
		'q':search
	}

	r = requests.get(url = urls, params = datas)
	text = BeautifulSoup(r.text,'lxml')
	text = text.find('div',{'class':'searchresults'})
	if(not text):
		print("Not Found")
	else:	
		text = text.find('table')
		text = text.find_all('tr')

		for i in range(0,len(text)):
			a=text[i].find('td',{'class':'bibliocol'})
			title = a.find('a',{'class':'title'})
			if(title):
				print(title.text)
			author= text[i].find('span',{'class':'author'})
			if(author):
				print("by "+author.text)
			publisher = text[i].find('span',{'class':'results_summary publisher'})
			if(publisher):
				print('\n'+publisher.text)
			availability = text[i].find('span',{'class':'results_summary availability'})
			if(availability):
				print('\n'+availability.text)
			print('\n_________________________\n')


def menu2():
	print("\033c")
	print("1. Search\n2. Issued Books\n0. Exit")
	print("\nChoice")
	n = int(input(""))
	return n

def menu1():
	print("\033c")
	print("1. Search\n2. Login\n0. Exit")
	print("\nChoice")
	n = int(input(""))
	return n


def driver_func():
	print("\033c")
	login_auth = False

	while(not login_auth):
		n = menu1()
		if(n==0):
			exit()
		if(n==1):
			search()
			x=input("\n\nEnter any key to continue...")
		if(n==2):
			text,flag = login()
			if(flag):
				n= menu2()
				if(n==1):
					search()
				if(n==2):
					issuedBooks(text)
					x=input("\n\nEnter any key to continue...")
				if(n==0):
					exit()
	


text,flag = login()
if(not flag):
	print("Not Logged in!")
else:
	print("Logged In\n\n")
	issuedBooks(text)












