from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_login import current_user
from flask_ckeditor import CKEditorField
from wtforms import StringField, SelectField, SelectMultipleField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired
from app.models import World, Character

class AddWorld(FlaskForm):
    world_name = StringField('Name', validators=[DataRequired()])
    create_world = SubmitField('Create World')

    def validate_world_name(self, world_name): # the name of this function needs to match the field you're validating!
        world = World.query.filter_by(user_id=current_user.id, name=world_name.data).first()
        if world is not None:
            flash('This world already exists!', 'error')
            raise ValidationError('This world already exists.')

class AddCharacter(FlaskForm):
    select_world = SelectField('World')
    avatar = FileField('Upload Avatar?')
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    gender = StringField('Gender')
    description = TextAreaField('Description/Bio')
    relatives = SelectMultipleField('Blood Relatives')
    add_character = SubmitField('Create Character')

    def validate_last_name(self, last_name): # the name of this function needs to match the field you're validating!
        if self.select_world.data != '':
            world_query = World.query.filter_by(user_id=current_user.id, name=self.select_world.data).first()
            character = Character.query.filter_by(user_id=current_user.id, world_id=world_query.id, first_name=self.first_name.data, last_name=self.last_name.data).first()
            if character is not None:
                flash('This character already exists in the selected world!', 'error')
                raise ValidationError('This character already exists.')

    def validate_select_world(self, select_world):
        if select_world.data == '':
            flash('Please select a world for your character!')
            raise ValidationError('Please select a world.')

class AddStory(FlaskForm):
    story_title = StringField('Title', validators=[DataRequired()])
    story_text = CKEditorField('Text', validators=[DataRequired()])
    select_characters = SelectMultipleField('Featured Characters:')
    prompt_id = IntegerField('Prompt ID')
    submit = SubmitField('Add Story')

class Delete(FlaskForm):
    id = IntegerField('ID')
    delete = SubmitField('Delete') # this should be changed to 'Delete [story/character/world/whatever]' depending on where it is

class Rename(FlaskForm):
    id = IntegerField('ID')
    new_name = StringField('New Name')
    rename = SubmitField('Rename')

class Edit(FlaskForm):
    edit = CKEditorField('Edit')
    update = SubmitField('Save Changes')

class Add(FlaskForm):
    characters = SelectMultipleField('Add Existing Character To This Story:')
    add = SubmitField('Add')

class Remove(FlaskForm):
    characterID = IntegerField('Character ID')
    remove = SubmitField('Remove')

class ImageUpload(FlaskForm):
    file = FileField('Image')
    upload = SubmitField('Upload')

class ChangeGender(FlaskForm):
    gender = StringField('Gender')
    change = SubmitField('Change')
