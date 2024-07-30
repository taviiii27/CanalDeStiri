import mysql.connector #SIUD
class CanalDeStiri():
    def __init__(self):
        self.mydb=mysql.connector.connect(host='localhost', password='root', user='root', database='stiri')
        self.cursor=self.mydb.cursor()
    def select(self,query,values=None):
        self.cursor.execute(query,values)
        return self.cursor.fetchall()#selectam tot 
    def insert(self, query,values=None):
        self.cursor.execute(query, values)
        self.mydb.commit()
        return self.cursor.rowcount #numaram randurile 
    def update(self, query, values=None):
        self.cursor.execute(query, values)
        self.mydb.commit()
    def delete(self, query, values=None):
        self.cursor.execute(query, values)# la fel ca la celelalte
        self.mydb.commit()