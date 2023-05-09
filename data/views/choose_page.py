from flask import Blueprint, render_template, request, redirect, url_for
from data.character.equipment import Equipment
from data.character.classes import get_classes

choose_blueprint = Blueprint('choose_blueprint', __name__)

equip = Equipment()
player_is_added = []


@choose_blueprint.route('/choose-hero/', methods=['GET', 'POST'])
def choose_page():

    classes = [i for i in get_classes().keys()]
    weapons = equip.get_weapons_names
    armors = equip.get_armors_names

    if request.method == 'GET':

        npc_type = 'Hero'

        return render_template(
            'hero_choosing.html',
            npc_type=npc_type,
            classes=classes,
            weapons=weapons,
            armors=armors
        )

    elif request.method == 'POST':

        npc_type = 'Enemy'

        npc_name = request.form.get('name')
        unit_class = request.form.get('unit_class')
        weapon = request.form.get('weapon')
        armor = request.form.get('armor')

        player_characters = [npc_name, unit_class, weapon, armor]

        if not player_is_added:

            player_is_added.append(player_characters)

            return render_template(
                'hero_choosing.html',
                npc_type=npc_type,
                classes=classes,
                weapons=weapons,
                armors=armors
            )

        else:

            enemy_characters = [npc_name, unit_class, weapon, armor]

            return redirect(url_for(
                'fight_blueprint.fight',
                player=player_is_added[0],
                enemy=enemy_characters
            ))
