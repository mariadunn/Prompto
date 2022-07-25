from app import db
from app.models import World, Character, Story, Prompt, story_character, relatives_character
from flask_login import current_user

def world_dict():
    world_query = World.query.filter(World.user_id == current_user.id).order_by(World.name).all()
    character_query = Character.query.filter(Character.user_id == current_user.id).order_by(Character.last_name, Character.name).all()
    world_list = []
    for world in world_query:
        w_dict = {}
        w_dict["id"] = world.id
        w_dict["name"] = world.name
        w_dict["characters"] = []
        for character in character_query:
            if character.world_id == world.id:
                c_dict = {}

                c_dict["id"] = character.id

                c_dict["name"] = character.name

                c_dict["first_name"] = character.first_name

                c_dict["avatar"] = character.avatar

                c_dict["relatives"] = []
                relatives_query = Character.query.join(relatives_character, (relatives_character.c.relative_b == Character.id)).filter(relatives_character.c.relative_a == character.id).order_by(Character.name).all()
                for relative in relatives_query:
                    c_dict["relatives"].append(relative.name)

                c_dict["stories"] = []
                story_ids = Story.query.join(story_character).join(Character).filter(story_character.c.character_id == character.id).all()
                for story in story_ids:
                    s_dict = {}
                    s_dict["id"] = story.id
                    s_dict["title"] = story.title
                    s_dict["text"] = story.text
                    c_dict["stories"].append(s_dict)

                w_dict["characters"].append(c_dict)

        world_list.append(w_dict)
    return world_list

def story_dict():
    story_query = Story.query.filter(Story.user_id == current_user.id).order_by(Story.title).all()
    story_list = []
    for story in story_query:
        s_dict = {}
        s_dict["id"] = story.id
        s_dict["title"] = story.title
        s_dict["text"] = story.text
        storyList = story.text.split()
        snippetList = storyList[:50]
        snippet = ' '.join(snippetList)
        s_dict["snippet"] = snippet
        s_dict["characters"] = []
        character_query = Character.query.join(story_character).join(Story).filter(story_character.c.story_id == story.id).all() ### added .all()
        for character in character_query:
            c_dict = {}
            c_dict["id"] = character.id
            c_dict["name"] = character.name
            c_dict["first_name"] = character.first_name
            c_dict["world_id"] = character.world_id
            s_dict["characters"].append(c_dict)
        story_list.append(s_dict)
    return story_list

def prompt_dict():
    prompts_list = []
    prompt_query = Prompt.query.all()
    for p in prompt_query:
        p_dict = {}
        p_dict["id"] = p.id
        p_dict["text"] = p.text
        p_dict["hints"] = p.hints
        p_dict["category"] = p.category
        p_dict["participants"] = p.participants
        p_dict["inspired_stories"] = []
        # story_query = Story.query.filter(Story.user_id == current_user.id, Story.prompt_id == p.id).all()
        # for s in story_query:
        #     s_dict = {}
        #     s_dict["id"] = s.id
        #     s_dict["title"] = s.title
        #     s_dict["text"] = s.text
        #     p_dict["inspired_stories"].append(s_dict)
        prompts_list.append(p_dict)
    return prompts_list

def character_dict(): # combine with world_dict?
    character_list = []
    character_query = Character.query.filter(Character.user_id == current_user.id).all()
    for character in character_query:
        c_dict = {}
        c_dict["id"] = character.id
        c_dict["name"] = character.name
        c_dict["first_name"] = character.first_name
        c_dict["world_id"] = character.world_id
        c_dict["relatives"] = []


        relatives_query = Character.query.join(relatives_character, (relatives_character.c.relative_b == Character.id)).filter(relatives_character.c.relative_a == character.id).order_by(Character.name).all()

        for relative in relatives_query: # turn this into dictionary?
            c_dict["relatives"].append(relative.name)


        character_list.append(c_dict)
    return character_list
