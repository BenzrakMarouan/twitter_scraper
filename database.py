import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    sql_create_tweets_table = """ CREATE TABLE IF NOT EXISTS tweets (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        text TEXT NOT NULL,
                                        username TEXT,
                                        link TEXT,
                                        timestamp TEXT,
                                        replies INTEGER,
                                        reposts INTEGER,
                                        likes INTEGER,
                                        bookmarks INTEGER,
                                        views INTEGER,
                                        sentiment REAL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_tweets_table)
    except sqlite3.Error as e:
        print(e)

def insert_tweet(conn, tweet):
    sql = ''' INSERT INTO tweets(text, username, link, timestamp, replies, reposts, likes, bookmarks, views, sentiment)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (tweet['text'], tweet['username'], tweet['link'], tweet['timestamp'], tweet['replies'],
                      tweet['reposts'], tweet['likes'], tweet['bookmarks'], tweet['views'], tweet['sentiment']))
    conn.commit()
    return cur.lastrowid
