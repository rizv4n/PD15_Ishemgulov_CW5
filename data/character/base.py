from data.character.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):

    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):

        if self.enemy.unit_class.max_health <= 0:
            return f'Игрок {self.player.name} выиграл битву'
        elif self.player.unit_class.max_health <= 0:
            return f'Игрок {self.player.name} проиграл битву'
        else:
            return False

    def _stamina_regeneration(self):

        if self.player.stamina - self.player.unit_class.max_stamina > 1:
            self.player.unit_class.max_stamina += self.STAMINA_PER_ROUND
        if self.enemy.stamina - self.enemy.unit_class.max_stamina > 1:
            self.enemy.unit_class.max_stamina += self.STAMINA_PER_ROUND

    def next_turn(self):

        if self._check_players_hp():
            return self._check_players_hp()

        self._stamina_regeneration()

        return self.enemy.hit(self.player)

    def _end_game(self):

        self._instances = {}
        self.game_is_running = False

        return 'Ok'

    def player_hit(self):

        return self.player.hit(self.enemy)

    def player_use_skill(self):

        return self.player.use_skill(self.enemy)
