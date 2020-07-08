from pymysql import *

class myconnection:
    def connect(self):
        conn=connect('localhost','root','','foodordering')
        return conn
    def fethcategories(self):
        list=['--Select Category--','Punjabi','North Indian','West Indian','East Indian','South India','Fast Food']
        return list

