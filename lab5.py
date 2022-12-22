import os
import urllib.parse as up
import psycopg2

class TagsSearch:

  def __init__(self, url):
    up.uses_netloc.append("postgres")
    self.url = up.urlparse(url)
    self.conn = psycopg2.connect(database=self.url.path[1:],
                            user=self.url.username,
                            password=self.url.password,
                            host=self.url.hostname,
                            port=self.url.port)
    self.cours = self.conn.cursor()

  def search(self, tags, n=1, m=5):
    self.cours.execute(f"Select * from Docs WHERE \"tags\" @@ plainto_tsquery('{tags}') ORDER BY doc_id ASC LIMIT {n+m}") # использовали индекс для полносвязного поиска
    result = self.cours.fetchall()
    return result[(n-1)*m:]

  def searchNot(self, tags, n=1, m=5):
    not_tags = tags.replace("tag", "nottag")
    self.cours.execute(f"Select * from Docs WHERE \"tags\" @@ plainto_tsquery('{not_tags}') ORDER BY doc_id ASC LIMIT {n+m}")
    result = self.cours.fetchall()
    return result[(n-1)*m:]


t = TagsSearch("postgres://pnghmzli:oLJiImPE-8vUSkyIQRHtLHXFqhHd_nM6@snuffleupagus.db.elephantsql.com/pnghmzli")

print(t.search(tags='tag004', n=2, m=2))
print(t.searchNot(tags='tag004', n=2, m=2))
    


# CREATE TABLE Docs (
# doc_id serial PRIMARY KEY,
# doc_name VARCHAR ( 50 ) NOT NULL,
# doc_path VARCHAR ( 50 ) UNIQUE NOT NULL,
# tags VARCHAR ( 255 ) NOT NULL
# );

# INSERT INTO Docs(doc_name, doc_path, tags)
# VALUES
# ('Doc1', 'c://Doc1', 'tag001, tag002, tag003, nottag004, nottag005'),
# ('Doc2', 'c://Doc2', 'tag001, tag002, tag003, nottag004, nottag005'),
# ('Doc3', 'c://Doc3', 'tag001, tag002, tag003, nottag004, nottag005'),
# ('Doc4', 'c://Doc4', 'tag002, tag003, tag004, nottag005, nottag001'),
# ('Doc5', 'c://Doc5', 'tag002, tag003, tag004, nottag005, nottag001'),
# ('Doc6', 'c://Doc6', 'tag002, tag003, tag004, nottag005, nottag001'),
# ('Doc7', 'c://Doc7', 'tag001, tag002, nottag004, tag005, nottag002'),
# ('Doc8', 'c://Doc8', 'tag001, tag002, nottag004, tag005, nottag002'),
# ('Doc9', 'c://Doc9', 'tag001, tag002, nottag004, tag005, nottag002')

# CREATE INDEX tag_idx ON Docs USING gin("tags")

