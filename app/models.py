from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# TODO: Indexes?

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader # gets user from database, to be used by flask_login
def load_user(id):
    return User.query.get(int(id))

# Relationship tables

story_character = db.Table('story_character',
    db.Column('story_id', db.Integer, db.ForeignKey('story.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
    )

relatives_character = db.Table('relatives_character',
    db.Column('relative_a', db.Integer, db.ForeignKey('character.id')),
    db.Column('relative_b', db.Integer, db.ForeignKey('character.id')),
    )

# Normal tables

## Indexing?

class World(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, index=True)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    world_id = db.Column(db.Integer, db.ForeignKey('world.id'))
    name = db.Column(db.String, index=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    gender = db.Column(db.String)
    description = db.Column(db.String)
    avatar = db.Column(db.String)
    stories = db.relationship('Story', secondary=story_character, backref="characters")
    relatives = db.relationship(
        'Character', foreign_keys=[relatives_character.c.relative_a, relatives_character.c.relative_b], secondary=relatives_character,
        primaryjoin=(relatives_character.c.relative_a == id),
        secondaryjoin=(relatives_character.c.relative_b == id),
        backref=db.backref('relatives_character', lazy='dynamic'), lazy='dynamic'
    )

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, index=True)
    text = db.Column(db.String, index=True)

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    hints = db.Column(db.String)
    category = db.Column(db.String)
    participants = db.Column(db.Integer)



# NEXT: add prompts
