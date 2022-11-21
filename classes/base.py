from typing import Optional
from classes.unit import PlayerUnit, EnemyUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 3
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: PlayerUnit, enemy: EnemyUnit):
        # Начало игры -> None.
        # Присваиваем экземпляру класса аттрибуты "игрок" и "противник",
        # а также выставляем True для свойства "началась ли игра"
        self.player = player
        self.enemy = enemy
        self.game_is_running = True
        self.battle_result = ""

    def _check_players_hp(self) -> Optional[str]:
        # Проверка здоровья игрока и врага и возвращение результата строкой.
        # Может быть три результата:
        # Игрок проиграл битву, Игрок выиграл битву, Ничья и сохраняем его в аттрибуте (self.battle_result).
        # Если Здоровья игроков в порядке то ничего не происходит.
        if self.player.health_points <= 0 and self.enemy.health_points <= 0:
            self.game_is_running = False
            self.battle_result = "Ничья"
            return self.battle_result

        if self.player.health_points <= 0:
            self.game_is_running = False
            self.battle_result = "Игрок проиграл битву"
            return self.battle_result

        if self.enemy.health_points <= 0:
            self.game_is_running = False
            self.battle_result = "Игрок выиграл битву"
            return self.battle_result

        return None

    def _stamina_regeneration(self):
        # Регенерация здоровья и стамины для игрока и врага за ход.
        # В этом методе к количеству стамины игрока и врага прибавляется константное значение.
        # Главное чтобы оно не превысило максимальные значения (используйте if).
        stamina = round(self.player.stamina + self.STAMINA_PER_ROUND * self.player.unit_class.stamina, 1)
        stamina = stamina if stamina <= self.player.unit_class.max_stamina else self.player.unit_class.max_stamina
        self.player.stamina = stamina

        stamina = round(self.enemy.stamina + self.STAMINA_PER_ROUND * self.enemy.unit_class.stamina, 1)
        stamina = stamina if stamina <= self.enemy.unit_class.max_stamina else self.enemy.unit_class.max_stamina
        self.enemy.stamina = stamina

    def next_turn(self) -> str:
        # Следующий ход -> return result | return self.enemy.hit(self.player).
        # Срабатывает когда игрок пропускает ход или когда игрок наносит удар.
        # Создаем поле result и проверяем что вернется в результате функции self._check_players_hp,
        # если result -> возвращаем его, если же результата пока нет и после завершения хода игра продолжается,
        # тогда запускаем процесс регенерации стамины и здоровья для игроков (self._stamina_regeneration)
        # и вызываем функцию self.enemy.hit(self.player) - ответный удар врага.
        result = self._check_players_hp()
        if result:
            return result

        self._stamina_regeneration()

        result = self.enemy.hit(self.player)
        # self._stamina_regeneration()

        return result

    def end_game(self) -> str:
        # Кнопка "Завершения игры" - > return result: str.
        # Очищаем синглтон - self._instances = {}, останавливаем игру (game_is_running), возвращаем результат
        self._instances = {}
        return ""

    def player_hit(self) -> str:
        # Кнопка "Удар игрока" -> return result: str.
        # Получаем результат от функции self.player.hit, запускаем следующий ход, возвращаем результат удара строкой.
        result_hit = self.player.hit(self.enemy)
        result_next = self.next_turn()
        return result_hit + " " + result_next

    def player_use_skill(self):
        # Кнопка "Игрок использует умение".
        # Получаем результат от функции self.use_skill, включаем следующий ход, возвращаем результат удара строкой.
        result_hit = self.player.use_skill(self.enemy)
        result_next = self.next_turn()
        return result_hit + " " + result_next
