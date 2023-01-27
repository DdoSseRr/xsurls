from sweater import db

class Database(db.Model):
    __tablename__ = 'Database'
    id = db.Column(db.Integer,primary_key=True, unique=True, nullable=False)
    dest_link = db.Column(db.Text, nullable=False)
    src_link = db.Column(db.Text, nullable=False, unique=True)
    user_id = db.Column(db.Integer)
    date_time = db.Column(db.Text)
    clicks = db.Column(db.Integer,default=0)
    
    def __repr__(self):
        return "<{} : {}>".format(self.dest_link[::],  self.src_link[::])


