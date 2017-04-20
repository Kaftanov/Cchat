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

        sql = """CREATE TABLE IF NOT EXISTS link
            (
                uid TEXT NOT NULL PRIMARY KEY,
                address TEXT NOT NULL
            )"""
        self.cursor.execute(sql)

    def add_user(self, userform):
        """ add user into TABLE """
        user = (userform['uid'], userform['login'],
                userform['pswd'], userform['state'],
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
            print(str(error) + 'in "get_user"')
            return 'UID unknown'
        else:
            return self.cursor.fetchone()

    def get_all_users(self):
        sql = "SELECT * FROM users ORDER BY id"
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + 'in "get_all_users"')
        else:
            return self.get_list_rows(self.cursor.fetchall())

    def get_online_users(self):
        """ get all users which are online"""
        sql = "SELECT * FROM users WHERE state = 1 ORDER BY id"
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + 'in "get_online_users"')

    def add_socket(self, row):
        """ params: tuple(uid, address)"""
        sql = "INSERT INTO link (uid, address) VALUES (?,?)"
        try:
            self.cursor.execute(sql, row)
        except sqlite3.DatabaseError as error:
            print(str(error) + 'in "add_socket"')
        finally:
            self.connection.commit()

    def get_uid(self, address):
        """ get uid by address"""
        sql = "SELECT * FROM link WHERE address = '%s'" % address
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as error:
            print(str(error) + 'in "get_uid"')
        else:
            return self.cursor.fetchone()['uid']

    def get_user_by_address(self, address):
        """ get user by socket address"""
        uid = self.get_uid(address)
        return self.get_user(uid)

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
