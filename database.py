import sqlite3
class dbms():
    def __init__(self):
        self.__conn = sqlite3.connect('database.db')
        self.__cursor = self.__conn.cursor()
    
    def Createtable(self):
        self.__cursor.execute('''CREATE TABLE usernames
                              (username VARCHAR(50) PRIMARY KEY,
                              password VARCHAR(50))''')
        self.__cursor.execute('''CREATE TABLE statistics
                              (username VARCHAR(50) PRIMARY KEY,
                              wins INT,
                              loss INT,
                              score INT)''')
        self.__cursor.execute('''CREATE TABLE preferences,
                              (username VARCHAR(50) PRIMARY KEY,
                              computerdiff INT,
                              hints BOOLEAN,
                              boardcolour VARCHAR(50),
                              validmoves BOOLEAN
                              preferenceno INT) ''')
        self.__conn.commit()
        
    def Insert(self, table, values):
        self.__cursor.execute("INSERT INTO "+table+" VALUES "+values)
        self.__conn.commit()
    
    def checkUser(self, username, password):
        self.__cursor.execute("SELECT * FROM usernames WHERE username = ? AND password = ?", (username, password))
        return self.__cursor.fetchall()
    
    def checkifUserExists(self, username):
        self.__cursor.execute("SELECT * FROM usernames WHERE username = ?", (username,))
        return len(self.__cursor.fetchall()) > 0
    
    def getstatistics(self, username):
        self.__cursor.execute("SELECT * FROM statistics WHERE username = ?", (username,))
        return self.__cursor.fetchall()
    
    def getallstats(self):
        self.__cursor.execute("SELECT * FROM statistics")
        return self.__cursor.fetchall()

    def editstatistics(self, username, column, value):
        self.__cursor.execute("UPDATE statistics SET "+column+" = ? WHERE username = ?", (value, username))
        self.__conn.commit()
    
    def getpreferences(self,username):
        self.__cursor.execute("SELECT * FROM preferences WHERE username = ?", (username,))
        return self.__cursor.fetchall()
    
    def editpreference(self, username, column, value, prefno):
        self.__cursor.execute("UPDATE preferences SET "+column+" = ? WHERE username = ? AND preferenceno = ?", (value, username, prefno))
        self.__conn.commit()
