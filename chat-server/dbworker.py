"""
    
"""
import sqlite3


class DbHandler(object):
    """
        
    """
    DB_NAME = 'server.db'

    def __init__(self):
        self.connection = sqlite3.connect(self.DB_NAME)
        self.connection.row_factory = self.dict_factory

        self.cursor = self.connection.cursor()
        sql = """CREATE TABLE IF NOT EXISTS users
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT NOT NULL UNIQUE,
                login TEXT NOT NULL UNIQUE,
                password TEXT,
                state INTEGER,
                left TEXT
            )"""
        self.cursor.execute(sql)

    def add_user(self, userform):
        """ add user into TABLE """
        user = (userform['uid'], userform['login'],
                userform['password'], userform['state'],
                userform['left'])

        sql = "INSERT INTO users (uid, login, password, state, left) VALUES (?,?,?,?,?)"

        try:
            self.cursor.execute(sql, user)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "add_user"')
            pass
        finally:
            self.connection.commit()

    def del_user(self, uid):
        """ DELETE user by uid """
        sql = "DELETE FROM users WHERE uid = '%s'" % uid

        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "del_user"')
            pass
        finally:
            self.connection.commit()

    def update_state(self, uid, state, date):
        """ Update state user after left"""
        sql = "UPDATE users SET state = %d, left = '%s' WHERE uid = '%s'" % (state, date, uid)
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "update_state"')
            pass
        finally:
            self.connection.commit()

    def get_user(self, uid):
        sql = "SELECT * FROM users WHERE uid = '%s'" % uid
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "get_user"')
            return 'UID unknown'
        else:
            return self.cursor.fetchone()

    def get_all_users(self):
        sql = "SELECT * FROM users ORDER BY id"
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "get_all_users"')
        else:
            return self.get_list_rows(self.cursor.fetchall())

    def get_online_users(self):
        """ get all users which are online"""
        sql = "SELECT * FROM users WHERE state = 1 ORDER BY id"
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "get_online_users"')
        else:
            return self.get_list_rows(self.cursor.fetchall())

    def get_uid_by_login(self, login):
        sql = "SELECT * FROM users WHERE login = '%s'" % login
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "get_uid_by_login"')
        else:
            row = self.cursor.fetchone()
            if row is None:
                return None
            else:
                return row['uid']

    def get_passwd_by_login(self, login):
        sql = "SELECT * FROM users WHERE login = '%s'" % login
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + ' in "get_uid_by_login"')
        else:
            row = self.cursor.fetchone()
            if row is None:
                return None
            else:
                return row['password']

    @staticmethod
    def dict_factory(cursor, row):
        """Took from https://docs.python.org/3/library/sqlite3.html"""
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    @staticmethod
    def get_list_rows(cursor):
        row_list = []
        for row in cursor:
            row_list.append(row)
        return row_list

    def __del__(self):
        """ Close connection """
        self.connection.close()