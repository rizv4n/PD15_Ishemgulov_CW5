from flask import Blueprint, render_template, request, redirect, url_for

from data.character.base import Arena
from data.character.classes import get_heroes, Heroes

fight_blueprint = Blueprint('fight_blueprint', __name__)
hit_blueprint = Blueprint('hit_blueprint', __name__)
skill_blueprint = Blueprint('skill_blueprint', __name__)
pass_blueprint = Blueprint('pass_blueprint', __name__)
end_blueprint = Blueprint('end_blueprint', __name__)

arena = Arena()


@fight_blueprint.route('/fight/')
def fight():

    player_characters = request.args.getlist('player')
    enemy_characters = request.args.getlist('enemy')
    result = request.args.get('result')

    if player_characters:

        player, enemy = get_heroes(player_characters, enemy_characters)

        arena.start_game(player, enemy)

        result = 'Бой начался!'

    heroes = Heroes(arena.player, arena.enemy)

    return render_template(
        'fight.html',
        heroes=heroes,
        result=result
    )


@hit_blueprint.route('/fight/hit', methods=['GET'])
def hit():

    result = arena.player_hit() + arena.next_turn()

    return redirect(url_for('fight_blueprint.fight', result=result))


@skill_blueprint.route('/fight/use-skill', methods=['GET'])
def skill():

    result = arena.player_use_skill() + arena.next_turn()

    return redirect(url_for('fight_blueprint.fight', result=result))


@pass_blueprint.route('/fight/pass-turn', methods=['GET'])
def pass_turn():

    result = arena.next_turn()

    return redirect(url_for('fight_blueprint.fight', result=result))


@end_blueprint.route('/fight/end-fight', methods=['GET'])
def end_fight():
    return redirect('/')
