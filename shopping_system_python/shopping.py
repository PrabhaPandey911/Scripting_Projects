from __future__ import print_function
import pickle
import sys
import getpass
import os


class Products:
	def __init__(self, id, name, group, subgroup,price):
		self.id=id
		self.name=name
		self.group=group
		self.subgroup=subgroup
		self.price=price
		
	def storeProducts(self):
		dict={"id":self.id,"name":self.name,"group":self.group,"subgroup":self.subgroup,"price":self.price}
		file=open('products','a')
		pickle.dump(dict,file)
		file.close()

class Admin:
	def __init__(self, id, name):
		self.id = id
		self.name = name
	@staticmethod
	def ViewProducts():
		data = open('products','rb')
		objects=[]
		while True:
			try:
				objects.append(pickle.load(data))
			except EOFError:
				break
		data.close()
		return objects

	def AddProducts(self, id, name, group, subgroup, price):
		product=Products(id, name, group, subgroup, price)
		data=open('products','rb')
		obj=[]
		while True:
			try:
				obj.append(pickle.load(data))
			except EOFError:
				break
		flag=0
		for r in obj:
			for i in r.keys():
				if i=='id' and r[i]==id:
					flag=1
					break
		if flag==1:
			print('\033[3m'+"This Product Id is already Occupied!"+'\033[0m')
			# print() 
			print("Please Try Again:")
			pid1=raw_input("Product Id: ")
			pname1=raw_input("Product Name: ")
			pgr1=raw_input("Product Group: ")
			psgr1=raw_input("Product subgroup: ")
			ppr1=raw_input("Product Price: ")
			self.AddProducts(pid1,pname1,pgr1,psgr1,ppr1)
		else:
			print('\033[3m'+"Entered In the file"+'\033[0m')
			# print() 
			product.storeProducts()

		data.close()
		

	def DeleteProducts(self,id):
		l=self.ViewProducts()
		for r in l:
			for i in r.keys():
				if i=='id' and r[i]==id:
					l.remove(r)
					break
		out=open('products','wb')
		for i in l:
			pickle.dump(i,out)
		print('\033[3m'+"Deleted from file"+'\033[0m')
		# print() 
		out.close()

	def ModifyProducts(self,id, name='', group='',subgroup='',price=''):
		l=self.ViewProducts()
		for r in l:
			for i in r.keys():
				if i=='id' and r[i]==id:
					if name!='':
						r['name']=name
					if group!='':
						r['group']=group
					if subgroup!='':
						r['subgroup']=subgroup
					if price!='':
						r['price']=price
					break
		file=open('products','wb')
		for i in l:
			pickle.dump(i,file)
		print('\033[3m'+"Product Modified"+'\033[0m')
		# print()
		file.close()



class Cart:
	def __init__(self, products, total):
		self.products=products
		self.total=total

	def add(self, id):
		l=Admin.ViewProducts()
		temp=self.products
		x=self.total
		flag=0
		for r in l:
			for i in r.keys():
				if i=='id' and r[i]==id:
					temp.append(r)
					x+=int(r['price'])
					flag=1
					break
		self.products=temp
		self.total=x
		if flag==1:
			print('\033[3m'+"Item added to cart"+'\033[0m')
		else:
			print('\033[3m'+"Item NOT added to cart"+'\033[0m')

	def view(self):
		print('Name'+'\t'+'Price'+'\t'+'ID')
		for i in self.products:	
			print(i['name']+"\t"+i['price']+'\t'+i['id'])

	def delete(self, id):
		flag=0
		for i in self.products:
			for k in i.keys():
				if k=="id" and i[k]==id:
					self.products.remove(i)
					flag=1
					break
		if flag==0:
			print('\033[3m'+"Item Not in cart!"+'\033[0m')
			# print
		else:
			print('\033[3m'+"Successfull Deletion"+'\033[0m')
			# print()

class Payment():
	def showBill(self, cart):
		print('\033[3m'+"You Bought: "+'\033[0m')
		# print()
		print("Name"+"\t"+"Price")
		for i in cart.products:
			print(i['name']+"\t"+i['price'])
		print("\n\n")
		print('\033[3m'+"Total Bill: ",str(cart.total)+'\033[0m')
		# print()


class Customer:
	def __init__(self, id, name, address, phone, cart, pay,password):
		self.id=id
		self.name=name
		self.address=address
		self.phone=phone
		self.cart=cart
		self.pay=pay
		self.password=password

	def store_cust(self):
		dict={'id':self.id,'name':self.name,'address':self.address, 'phone':self.phone,'Password':self.password}
		out=open('customer','a')
		pickle.dump(dict,out)
		out.close()

	def ViewProducts(self):
		data = open('products','rb')
		objects=[]
		while True:
			try:
				objects.append(pickle.load(data))
			except EOFError:
				break
		data.close()
		for i in objects:
			print(i) 

	def AddToCart(self,id):
		self.cart.add(id)
		
		

	def ViewCart(self):
		self.cart.view()

	def DeleteFromCart(self,id):
		self.cart.delete(id)

	def makePayment(self):
		self.pay.showBill(self.cart)
		out=open('order_history','a')
		pickle.dump(self.cart.products,out)
		out.close()


def admin_login(u,p):
	# print("\033[H\033[J")
	# u=raw_input("User id: ")
	# p=getpass.getpass(prompt='Password: ')
	flag=0
	# name=""
	file=open('admin','rb')
	while True:
		try:
			dict=pickle.load(file)
			if dict['id']==u and dict['Password']==p:
				flag=1
				name=dict['name']
				break
		except EOFError:
			break
	file.close()
	if flag==1:
		print("\033[H\033[J")
		print('\033[94m'+'\033[3m'+"Welcome ",name+'\033[0m')
		# print("Welcome ",name)
		print("\n")
		admin=Admin(u,name)
		print("1.View Products")
		print("2.Add Product")
		print("3.Delete Product")
		print("4.Modify Product")
		print("5.Logout")
		x=raw_input("Enter your choice: ")
		if x=="1":
			print('\033[94m'+'\033[3m'+"Product List"+'\033[0m')
			l=admin.ViewProducts()
			# print l
			for i in l:
				print(i)
			print("\n\n")
			print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
			# print("To GO Back press 1")
			g=raw_input()
			if g=='1':
				admin_login(u,p)
		if x=='2':
			pid=raw_input("Product Id: ")
			pname=raw_input("Product Name: ")
			pgr=raw_input("Product Group: ")
			psgr=raw_input("Product subgroup: ")
			ppr=raw_input("Product Price: ")
			admin.AddProducts(pid,pname,pgr,psgr,ppr)
			print("\n\n")
			print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
			# print("To GO Back press 1")
			g=raw_input()
			if g=='1':
				admin_login(u,p)

		if x=='3':
			print('\033[94m'+'\033[3m'+"Product List"+'\033[0m')
			l=admin.ViewProducts()
			# print l
			for i in l:
				print(i)
			print("\n\n")
			pid=raw_input("Product Id: ")
			admin.DeleteProducts(pid)
			print("\n\n")
			print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
			# print("To GO Back press 1")
			g=raw_input()
			if g=='1':
				admin_login(u,p)

		if x=='4':
			print('\033[94m'+'\033[3m'+"Product List"+'\033[0m')
			l=admin.ViewProducts()
			# print l
			for i in l:
				print(i)
			print("\n\n")
			mpid=raw_input("Product Id: ")
			mpname=raw_input("Product Name: ")
			mpgr=raw_input("Product Group: ")
			mpsgr=raw_input("Product subgroup: ")
			mppr=raw_input("Product Price: ")
			admin.ModifyProducts(mpid,mpname,mpgr,mpsgr,mppr)
			print("\n\n")
			print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
			# print("To GO Back press 1")
			g=raw_input()
			if g=='1':
				admin_login(u,p)

		if x=='5':
			print("\033[H\033[J")
			print('\033[94m'+'\033[3m'+"Successfully Logged out"+'\033[0m')
			mainmodule()
			# print()
			return
	else:
		print('\033[94m'+'\033[3m'+"Wrong Credentials!"+'\033[0m')
		# print()
		print("Try Again")
		# print("\033[H\033[J")
		u=raw_input("User id: ")
		p=getpass.getpass(prompt='Password: ')
		admin_login(u,p)
	

def admin_reg(u,n,p):
	# print("\033[H\033[J")
	# u=raw_input("User id: ")
	# n=raw_input("Name: ")
	# p=getpass.getpass(prompt='Password: ')
	# admin=Admin(u,n)
	flag=0
	file=open('admin','rb')
	while True:
		try:
			dict=pickle.load(file)
			if dict['id']==u:
				flag=1
				break
		except EOFError:
			break
	file.close()
	if flag==0:
		t={"id":u,"name":n,"Password":p}
		f=open('admin','a')
		pickle.dump(t,f)
		f.close()
		print('\033[94m'+'\033[3m'+"Registered Successfully!"+'\033[0m')
		# print()
	else:
		print('\033[94m'+'\033[3m'+"User Id already exists!"+'\033[0m')
		# print("User ID already exists!")
		# print("\033[H\033[J")
		u1=raw_input("User id: ")
		n1=raw_input("Name: ")
		p1=getpass.getpass(prompt='Password: ')
		admin_reg(u1,n1,p1)
	admin_login(u,p)

def tempModule(name,c):
	print("\033[H\033[J")
	print('\033[94m'+'\033[3m'+"Welcome ",name+'\033[0m')
	print("\n")
	# cust=Customer(u,name)
	print("1.View Products")
	print("2.Add To Cart")
	print("3.View Cart")
	print("4.Delete From Cart")
	print("5.Make Payment")
	print("6.Logout")
	x=raw_input("Enter your choice: ")
	if x=="1":
		print('\033[94m'+'\033[3m'+"Product List"+'\033[0m')
		c.ViewProducts()
		print("\n\n")
		print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
		g=raw_input()
		if g=='1':
			tempModule(name,c)
	if x=="2":
		print('\033[94m'+'\033[3m'+"Product List"+'\033[0m')
		c.ViewProducts()
		print("\n\n")
		pu=raw_input("Enter Product Id: ")
		c.AddToCart(pu)
		print("\n\n")
		print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
		g=raw_input()
		if g=='1':
			tempModule(name,c)
	if x=='3':
		print('\033[94m'+'\033[3m'+"Your Cart"+'\033[0m')
		c.ViewCart()
		print("\n\n")
		print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
		g=raw_input()
		if g=='1':
			tempModule(name,c)
	if x=='4':
		print('\033[94m'+'\033[3m'+"Your Cart"+'\033[0m')
		c.ViewCart()
		print("\n\n")
		px=raw_input("Enter Product Id: ")
		c.DeleteFromCart(px)
		print("\n\n")
		print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
		g=raw_input()
		if g=='1':
			tempModule(name,c)
	if x=="5":
		c.makePayment()
		print("\n\n")
		print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
		g=raw_input()
		if g=='1':
			tempModule(name,c)
	
	if x=="6":
		print("\033[H\033[J")
		print('\033[94m'+'\033[3m'+"Logged out Successfully!"+'\033[0m')
		# return
		mainmodule()



def cust_login(u,p):
	flag=0
	name=''
	file=open('customer','rb')
	while True:
		try:
			dict=pickle.load(file)
			if dict['id']==u and dict['Password']==p:
				flag=1
				name=dict['name']
				l=[]
				car=Cart(l,0)
				pay=Payment()
				print("here")
				c=Customer(u,name,dict['address'],dict['phone'],car,pay,dict['Password'])
				break
		except EOFError:
			break
	file.close()
	if flag==1:
		tempModule(name,c)

	else:
		print('\033[94m'+'\033[3m'+"Wrong Credentials!"+'\033[0m')
		print("Try Again")
		u=raw_input("User id: ")
		p=getpass.getpass(prompt='Password: ')
		cust_login(u,p)

def guest_reg(u,n,a,ph,car,pay,pas):
	print("\033[H\033[J")
	flag=0
	file=open('customer','rb')
	while True:
		try:
			dict=pickle.load(file)
			if dict['id']==u:
				flag=1
				break
		except EOFError:
			break
	file.close()
	if flag==0:
		c=Customer(u,n,a,ph,car,pay,pas)
		c.store_cust()
		print('\033[94m'+'\033[3m'+"Registered Successfully!"+'\033[0m')
		# print()
	else:
		print('\033[94m'+'\033[3m'+"User Id already exists!"+'\033[0m')
		# print()
		u1=raw_input("User Id: ")
		n1=raw_input("Name: ")
		pas1=getpass.getpass(prompt='Password: ')
		a1=raw_input("Address: ")
		ph1=raw_input("Phone No.: ")
		e1=[]
		car1=Cart(e1,0)
		pay1=Payment()
		guest_reg(u1,n1,a1,ph1,car1,pay1,pas1)
	cust_login(u,pas)

def GuestViewProducts():
		data = open('products','rb')
		objects=[]
		while True:
			try:
				objects.append(pickle.load(data))
			except EOFError:
				break
		data.close()
		for i in objects:
			print(i)

def order_history():
	# out=open(,'a')
	data = open('order_history','rb')
	print('\033[94m'+'\033[3m'+"Order History: "+'\033[0m')
	objects=[]
	while True:
		try:
			objects.append(pickle.load(data))
		except EOFError:
			break
	data.close()
	for i in objects:
		print(i) 

def mainmodule():
	print("\033[H\033[J")
	print("---------------------------------------------")
	print('\033[94m'+'\033[1m'+"Welcome to Online Shopping Store".center(40)+'\033[0m')
	print("---------------------------------------------",end='')
	print("\n")
	print('\033[94m'+'\033[3m'+"Select Role: "+'\033[0m')
	# print()
	print("1.Admin")
	print('2.Customer')
	print('3.Guest')
	print('4.Exit')
	print("\n")
	x=input("Enter your choice: ")
	if x==1:
		print("\033[H\033[J")
		print('\033[94m'+'\033[3m'+"Choose an option: "+'\033[0m')
		print("\n")
		print("1.Register")
		print("2.Order History")
		print("3.Login")
		
		y=input()
		if y==1:
			print("\033[H\033[J")
			u=raw_input("User id: ")
			n=raw_input("Name: ")
			p=getpass.getpass(prompt='Password: ')
			admin_reg(u,n,p)
		if y==3:
			print("\033[H\033[J")
			u=raw_input("User id: ")
			p=getpass.getpass(prompt='Password: ')
			admin_login(u,p)
		if y==2:
			print("\033[H\033[J")
			order_history()
			print("\n\n")
			print('\033[94m'+'\033[3m'+"To GO Back press 1"+'\033[0m')
			g=raw_input()
			if g=='1':
				mainmodule()
	if x==2:
		print("\033[H\033[J")
		print('\033[94m'+'\033[3m'+"Choose an option: "+'\033[0m')
		print("\n")
		print("1.Login")
		print("2.Quit")
		y=input()
		if y==1:
			print("\033[H\033[J")
			u=raw_input("User id: ")
			p=getpass.getpass(prompt='Password: ')
			cust_login(u,p)
		if y==2:
			print("\033[H\033[J")
			print('\033[94m'+'\033[1m'+"Thanks for visiting!"+'\033[0m')
			sys.exit()

	if x==3:
		print("\033[H\033[J")
		print('\033[94m'+'\033[3m'+"Choose an option: "+'\033[0m')
		# print()
		print("\n")
		print("1.Register")
		print("2.View Products")
		print("3.Quit")
		y=input()
		if y==1:
			print("\033[H\033[J")
			u=raw_input("User Id: ")
			n=raw_input("Name: ")
			a=raw_input("Address: ")
			ph=raw_input("Phone No.: ")
			e=[]
			car=Cart(e,0)
			pay=Payment()
			pas=getpass.getpass(prompt='Password: ')
			guest_reg(u,n,a,ph,car,pay,pas)
		if y==2:
			print("\033[H\033[J")
			GuestViewProducts()
			print("\n\n")
			print('\033[94m'+'\033[1m'+"To GO Back press 1"+'\033[0m')
			# print("To GO Back press 1")
			g=raw_input()
			if g=='1':
				mainmodule()
			#view products
		if y==3:
			print("\033[H\033[J")
			print('\033[94m'+'\033[1m'+"Thanks for visiting!"+'\033[0m')
			sys.exit()

	if x==4:
		print("\033[H\033[J")
		print('\033[94m'+'\033[1m'+"Thanks for visiting!"+'\033[0m')
		sys.exit()

if __name__=='__main__':
	mainmodule()
	