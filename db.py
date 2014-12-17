from time import strftime,localtime
import MySQLdb

# Mysql connection
def connect():
    return MySQLdb.connect(host="localhost", user="<user-name>", passwd="<password>", db="<database>")

# Write card readings to database
def write(tagId,action):
    db = connect()
    c = db.cursor()
    currentTime=strftime("%d-%m-%Y %H:%M:%S", localtime())
    c.execute("""INSERT INTO readings (tagId, time, action) VALUES (%s, %s, %s)""",(tagId,currentTime,action))
    db.commit()
    db.close()
    action ="Submitted. Have a nice day!"
    return action

# Write new card registration to database 
def writeUser(userId,tagId,permission):
    db = connect()
    c = db.cursor()
    added=strftime("%d-%m-%Y %H:%M:%S", localtime())
    c.execute("""INSERT INTO cards (userId, tagId, added, permission) VALUES (%s, %s, %s, %s)""",(userId,tagId,added,permission))
    db.commit()
    db.close()
    action ="New card user added!"
    return action