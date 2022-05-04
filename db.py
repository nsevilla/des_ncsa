import sqlite3
import uuid
import os
from global_vars import log

class DbInterface:
    def __init__(self):
        self.db = os.path.join('/db', 'db.sqlite3')
        log.debug(self.db)
        self.conn = None
        self.cur = None
        # Initialize the monitor SQLite database
        self.open_db()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS HELP_REQUESTS (
                id INTEGER PRIMARY KEY,
                time_created TEXT,
                token TEXT,
                email TEXT,
                last_name TEXT,
                first_name TEXT,
                subject TEXT,
                message TEXT,
                topics TEXT,
                received INTEGER
            )'''
        )
        self.close_db()

    def open_db(self):
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def close_db(self):
        self.conn.commit()
        self.conn.close()

    def generate_uuid(self):
        return str(uuid.uuid4()).replace("-", "")

    def add_new_request(self, form_data):
        token = self.generate_uuid()
        self.open_db()
        self.cur.execute(f'''
            INSERT INTO HELP_REQUESTS (
                token,
                time_created,
                email,
                last_name,
                first_name,
                subject,
                message,
                topics,
                received
            ) VALUES(
                :token,
                datetime('now'),
                :email,
                :last_name,
                :first_name,
                :subject,
                :message,
                :topics,
                0
            )
        ''',
        {
            'token': token,
            'email': form_data['email'],
            'last_name': form_data['last_name'],
            'first_name': form_data['first_name'],
            'subject': form_data['subject'],
            'message': form_data['message'],
            'topics': form_data['topics'],
        })
        self.close_db()
        return token

    def get_request_data(self, token):
        self.open_db()
        self.cur.execute(f'''
            SELECT
                token,
                email,
                last_name,
                first_name,
                subject,
                message,
                topics,
                received
            FROM
                HELP_REQUESTS
            WHERE
                token = :token
        ''',
        {
            'token': token,
        })
        results = self.cur.fetchall()
        self.close_db()
        return results


    def delete_request(self, token):
        self.open_db()
        self.cur.execute(f'''
            DELETE FROM
                HELP_REQUESTS
            WHERE
                token = :token
        ''',
        {
            'token': token,
        })
        self.close_db()
        return self.cur.rowcount == 1


    def mark_received(self, token):
        self.open_db()
        self.cur.execute(f'''
            UPDATE
                HELP_REQUESTS
            SET
                received = 1
            WHERE
                token = :token
        ''',
        {
            'token': token,
        })
        self.close_db()
        return self.cur.rowcount == 1
