import os
import imghdr
import re
import html2text
from flask import render_template, flash, url_for, redirect, Response, current_app, request, abort, send_from_directory
from flask_login import login_required, current_user
from wtforms import Label
from werkzeug.utils import secure_filename
from sqlalchemy import func
from app.models import World, Character, Story, Prompt, relatives_character
from app.main import bp
from app.main.forms import AddWorld, AddCharacter, AddStory, Delete, Rename, Edit, Add, Remove, ImageUpload, ChangeGender
from app.main.global_dicts import *

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

parser = html2text.HTML2Text()
parser.ignore_emphasis = True

## INDEX ##

@bp.route('/')
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    story_list = story_dict()
    number_of_stories = len(story_list)

    world_list = world_dict()
    number_of_worlds = len(world_list)

    character_list = character_dict()
    number_of_characters = len(character_list)

    return render_template(
        'index.html',
        title = 'Home',
        number_of_stories = number_of_stories,
        number_of_worlds = number_of_worlds,
        number_of_characters = number_of_characters
        )

@bp.route('/about', methods=['GET', 'POST'])
def about():

    return render_template(
        'about.html',
        title = 'About'
        )




## WORLDS ##

@bp.route('/worlds', methods=['GET', 'POST'])
@login_required
def worlds():
    worlds = world_dict()

    rename_form = Rename()
    rename_form.rename.label = Label(rename_form.rename.id, 'Rename World')

    if rename_form.rename.data and rename_form.validate():
        world_entry = World.query.filter(World.id == rename_form.id.data).first()
        world_entry.name = rename_form.new_name.data
        db.session.commit()
        return redirect(url_for('main.worlds'))

    delete_form = Delete()
    delete_form.delete.label = Label(delete_form.delete.id, 'Delete World') # changes label on button

    if delete_form.validate_on_submit():
        world_entry = World.query.filter(World.id == delete_form.id.data).first()
        chars_flash = ""
        characters = Character.query.filter(Character.user_id == current_user.id, Character.world_id == world_entry.id).all()
        for char in characters:
            chars_flash += char.name + ", "
            db.session.delete(char)
        db.session.delete(world_entry)
        db.session.commit()
        flash('{} deleted! Including characters: {}'.format(world_entry.name, chars_flash))
        return redirect(url_for('main.worlds'))

    return render_template(
        'worlds.html',
        title = '{}\'s Worlds'.format(current_user.username),
        worlds = worlds,
        rename_form = rename_form,
        delete_form = delete_form
    )

## CHARACTERS ##

@bp.route('/characters/<character_id>', methods=['GET', 'POST']) # is there another way to combine name and id in the same URL?
@login_required
def character(character_id):

    character_entry = Character.query.filter(Character.id == character_id).first()
    relatives = Character.query.join(relatives_character, (relatives_character.c.relative_b == Character.id)).filter(relatives_character.c.relative_a == character_entry.id).order_by(Character.name).all()

    files = os.listdir(current_app.config['UPLOAD_PATH'])


    if character is not None:

        rename_form = Rename()
        rename_form.rename.label = Label(rename_form.rename.id, 'Rename Character')

        if rename_form.rename.data and rename_form.validate():
            name_split = rename_form.new_name.data.split(" ", 1)
            character_entry.first_name = name_split[0]
            character_entry.last_name = name_split[1]
            character_entry.name = rename_form.new_name.data
            db.session.commit()
            return redirect(url_for('main.character', character_id = character_id))

        avatar_form = ImageUpload()

        if request.files and request.method == 'POST':
            uploaded_file = request.files['file']
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                new_name = character_id + "-" + character_entry.first_name + file_ext
                uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], new_name))

                character_entry.avatar = new_name
                db.session.commit()


            return redirect(url_for('main.character', character_id = character_id))


        gender_form = ChangeGender()
        gender_form.change.label = Label(gender_form.change.id, 'Change Gender')

        if gender_form.change.data and gender_form.validate():
            character_entry.gender = gender_form.gender.data
            db.session.commit()
            return redirect(url_for('main.character', character_id = character_id))

        description_form = Edit()
        description_form.update.label = Label(description_form.update.id, 'Update Description')

        if description_form.update.data and description_form.validate():
            character_entry.description = description_form.edit.data
            db.session.commit()
            return redirect(url_for('main.character', character_id = character_id))




        delete_form = Delete()
        delete_form.delete.label = Label(delete_form.delete.id, 'Delete Character') # changes label on button

        if delete_form.delete.data and delete_form.validate():
            db.session.delete(character_entry)

            db.session.commit()
            flash('{} deleted!'.format(character_entry.name))
            return redirect(url_for('main.worlds'))


        return render_template(
            'character.html',
            title = character_entry.name,
            character = character_entry,
            relatives = relatives,
            rename_form = rename_form,
            avatar_form = avatar_form,
            gender_form = gender_form,
            description_form = description_form,
            delete_form = delete_form,
        )

    else:

        return render_template(
            'access_denied.html',
            title = 'Access Denied',
            item = 'character'
        )


## STORIES ##

@bp.route('/stories')
@login_required
def stories():

    stories = story_dict()
    worlds = world_dict()
    prompts = prompt_dict()


    return render_template(
        'stories.html',
        title = '{}\'s Stories'.format(current_user.username),
        stories = stories,
        worlds = worlds,
        prompts = prompts
    )


@bp.route('/stories/<story_id>', methods=['GET', 'POST'])
@login_required
def story(story_id):
    story_entry = Story.query.filter(Story.id == story_id).first()

    if story_entry is not None:

        worlds = world_dict()
        characters = []
        other_characters = []
        for character in story_entry.characters:
            characters.append(character.name)
        other_characters_names = []

        for world in worlds:
            w_dict = {}
            w_dict["name"] = world["name"]
            w_dict["characters"] = []
            for character in world["characters"]:
                c_dict = {}
                story_ids = []
                if len(character["stories"]) == 0:
                    c_dict["name"] = character["name"]
                    other_characters_names.append(character["name"])
                    w_dict["characters"].append(c_dict)
                else:
                    for story in character["stories"]:
                        story_ids.append(story["id"])
                    if int(story_id) not in story_ids:
                        if character not in other_characters:
                            c_dict["name"] = character["name"]
                            w_dict["characters"].append(c_dict)
            other_characters.append(w_dict)

        rename_form = Rename()
        rename_form.rename.label = Label(rename_form.rename.id, 'Rename Story')

        if rename_form.rename.data and rename_form.validate():
            old_name = story_entry.title
            story_entry.title = rename_form.new_name.data
            db.session.commit()
            flash('{} renamed to {}!'.format(old_name, story_entry.title))
            return redirect(url_for('main.story', story_id = story_id))


        edit_form = Edit()

        if edit_form.update.data and edit_form.validate:
            story_entry.text = edit_form.edit.data
            db.session.commit()
            flash('{} updated!'.format(story_entry.title))
            return redirect(url_for('main.story', story_id = story_id))

        remove_form = Remove()

        if remove_form.remove.data and remove_form.validate:
            character_entry = Character.query.filter_by(id=remove_form.characterID.data).first()
            character_entry.stories.remove(story_entry)
            db.session.commit()
            flash('{} removed from {}!'.format(character_entry.name, story_entry.title))
            return redirect(url_for('main.story', story_id = story_id))


        add_character_form = Add()
        character_choices = []
        for world in other_characters:
            for character in world["characters"]:
                character_choices.append(character["name"])
        add_character_form.characters.choices = character_choices

        if add_character_form.add.data and add_character_form.validate:

            if len(add_character_form.characters.data) != 0:

                selected_characters = add_character_form.characters.data
                character_entries = []
                for character in selected_characters:
                    character_entry = Character.query.filter_by(user_id=current_user.id, name=character).first()
                    character_entries.append(character_entry)
                for character in character_entries:
                    character.stories.append(story_entry)
                db.session.commit()
                flash('{} added to {}!'.format(selected_characters[0], story_entry.title))
                return redirect(url_for('main.story', story_id = story_id))

            else:

                flash('No characters selected!')



        delete_form = Delete()
        delete_form.delete.label = Label(delete_form.delete.id, 'Delete Story') # changes label on button

        if delete_form.delete.data and delete_form.validate():
            db.session.delete(story_entry)
            db.session.commit()
            flash('{} deleted!'.format(story_entry.title))
            return redirect(url_for('main.stories'))


        return render_template(
            'story.html',
            title = story_entry.title,
            story = story_entry,
            rename_form = rename_form,
            edit_form = edit_form,
            remove_form = remove_form,
            add_character_form = add_character_form,
            delete_form = delete_form,
            characters = characters,
            other_characters = other_characters,
            other_characters_names = other_characters_names
        )

    else:

        return render_template(
            'access_denied.html',
            title = 'Access Denied',
            item = 'story'
        )

@bp.route('/stories/<story_id>/download')
@login_required
def download(story_id):
    story_entry = Story.query.filter(Story.id == story_id).first()
    filename = story_entry.title.replace(' ', '_')
    file_contents = story_entry.text
    return Response(
                    file_contents,
                    mimetype="application/rtf",
                    headers={"Content-Disposition": "attachment;filename=%s.rtf" % filename}
                    )


## POPULATE ##

@bp.route('/populate', methods=['GET', 'POST'])
@login_required
def populate():

    world_form = AddWorld()
    character_form = AddCharacter()

    files = os.listdir(current_app.config['UPLOAD_PATH'])

    worlds = world_dict()
    characters = character_dict()

    character_form.select_world.choices = [('', '---')] + [(world["name"], world["name"]) for world in worlds]
    character_form.relatives.choices = [char["name"] for char in characters]

    if world_form.create_world.data and world_form.validate():
        world_entry = World(
            name = world_form.world_name.data,
            user_id = current_user.id
        )
        db.session.add(world_entry)
        db.session.commit()
        flash('{} added to your worlds!'.format(world_form.world_name.data))
        return redirect(url_for('main.populate'))



    if character_form.add_character.data and character_form.validate():
        full_name = character_form.first_name.data + " " + character_form.last_name.data
        new_name = ""
        for world in worlds:
            if world["name"] == character_form.select_world.data:
                world_id = world["id"]

        character_entry = Character(
            name = full_name,
            first_name = character_form.first_name.data,
            last_name = character_form.last_name.data,
            gender = character_form.gender.data,
            description = character_form.description.data,
            user_id = current_user.id,
            world_id = world_id
        )
        db.session.add(character_entry)
        db.session.flush()

        ## Logic for adding files ##

        if request.files:
            character_entry = Character.query.filter(Character.user_id == current_user.id, Character.first_name == character_form.first_name.data, Character.last_name == character_form.last_name.data).first()
            uploaded_file = request.files['avatar']
            filename = secure_filename(uploaded_file.filename)
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(uploaded_file.stream):
                    abort(400)

                new_name = str(character_entry.id) + "-" + character_entry.first_name + file_ext
                uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], new_name))

                character_entry.avatar = new_name
                db.session.flush()


        ## Logic for adding relatives ##

        submitted_char_id = Character.query.filter(Character.user_id == current_user.id, Character.first_name == character_form.first_name.data, Character.last_name == character_form.last_name.data).first()
        relatives = character_form.relatives.data
        for relative in relatives:
            relative_id = Character.query.filter(Character.user_id == current_user.id, Character.name == relative).first()
            submitted_char_id.relatives.append(relative_id)
            relative_id.relatives.append(submitted_char_id)

        db.session.commit()

        flash('{} added to {}!'.format(character_form.first_name.data, character_form.select_world.data))

        return redirect(url_for('main.populate'))

    return render_template(
        'populate.html',
        title = 'Populate',
        world_form = world_form,
        character_form = character_form,
        worlds = worlds,
        files = files
    )

## WRITE ##

@bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():

    prompts = prompt_dict()
    characters = character_dict()

    story_form = AddStory()
    worlds = world_dict()
    story_form.select_characters.choices = []
    for world in worlds:
        for character in world["characters"]:
            story_form.select_characters.choices.append(character["name"])

    if story_form.validate_on_submit():
        story_title = story_form.story_title.data
        story_text = story_form.story_text.data
        story_entry = Story(
            user_id = current_user.id,
            title = story_title,
            text = story_text,
        )
        db.session.add(story_entry)
        db.session.flush() # "flush" seems to mean "commit, but keep database open for more changes"
        story = Story.query.filter_by(user_id=current_user.id, title=story_title, text=story_text).first()
        selected_characters = story_form.select_characters.data
        character_entries = []
        for character in selected_characters:
            character_entry = Character.query.filter_by(user_id=current_user.id, name=character).first()
            character_entries.append(character_entry)
        for character in character_entries:
            character.stories.append(story)
        db.session.commit()
        flash('{} added!'.format(story_title))



    return render_template(
        'write.html',
        title = 'Write!',
        story_form = story_form,
        prompts = prompts,
        worlds = worlds,
        characters = characters
    )
