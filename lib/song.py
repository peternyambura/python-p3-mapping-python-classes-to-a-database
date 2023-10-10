from config import CONN, CURSOR

class Song:
    
    def __init__(self, name, album, id=None):
        self.id = id
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id:
            sql = "UPDATE songs SET name = ?, album = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.album, self.id))
        else:
            sql = "INSERT INTO songs (name, album) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.album))
            self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, name, album):
        song = cls(name, album)
        song.save()
        return song

    @classmethod
    def all(cls):
        CURSOR.execute("SELECT * FROM songs")
        rows = CURSOR.fetchall()
        return [cls(row[1], row[2], row[0]) for row in rows]

    def delete(self):
        if self.id:
            CURSOR.execute("DELETE FROM songs WHERE id = ?", (self.id,))
            CONN.commit()
