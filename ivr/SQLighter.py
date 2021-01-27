# -*- coding: utf-8 -*-
import sqlite3


class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)

    def get_suboly(self, sub):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Olympiads WHERE Subject = ?", (sub, ))
        rows = cursor.fetchall()
        return rows

    def get_diruny(self, dir):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Universities WHERE Direction = ?", (dir, ))
        rows = cursor.fetchall()
        return rows

    def get_oly(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Olympiads WHERE ID = ?", (str(id), ))
        row = cursor.fetchone()
        return row

    def get_prefers(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM preferences WHERE ID = ?", (str(id), ))
        row = cursor.fetchone()
        return row

    def insert_oly(self, level, name, subject, id, url, descr):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO Olympiads 
                                  (Level, Name, Subject, ID, URL, Description) 
                                  VALUES (?,?,?,?,?,?)''',
                       (level, name, subject, id, url, descr))
        cursor.close()
        self.connection.commit()

    def insert_uny(self, id, name, location, oly, url, ders, dir):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO Universities 
                                  (ID, Name, Location, Olympiads, URL, Description, Direction) 
                                  VALUES (?,?,?,?,?,?,?)''',
                       (id, name, location, oly, url, ders, dir))
        cursor.close()
        self.connection.commit()

    def get_univer(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Universities WHERE ID = ?", (str(id), ))
        row = cursor.fetchone()
        return row

    def get_user_info(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id = ?", (str(id), ))
        row = cursor.fetchone()
        return row

    def insert_user(self, id, name, clas, Location, Levels, Subjects, School):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO Users 
                                  (id, Name, class, Location, Levels, Subjects, School) 
                                  VALUES (?,?,?,?,?,?,?)''',
                       (id, name, clas, Location, Levels, Subjects, School))
        cursor.close()
        self.connection.commit()

    def del_prefers(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM preferences WHERE id = ?''', (id, ))
        cursor.close()
        self.connection.commit()

    def delete_user(self, id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM Users WHERE id = ?''', (id, ))
        cursor.close()
        self.connection.commit()

    def insert_prefers(self, id, oly, uny):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO preferences
                                          (id, oly, uny) 
                                          VALUES (?,?,?)''',
                       (id, oly, uny))
        cursor.close()
        self.connection.commit()

    def exists_user(self, id):
        cursor = self.connection.cursor()
        print(str(id))
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(id),))
        row = cursor.fetchone()
        cursor.close()
        return row

    def close(self):
        self.connection.close()
