from typing import Optional, Dict, Any
from classes.unit import BaseUnit


class BaseSingleton(type):
    _instances: Dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player: BaseUnit
    enemy: BaseUnit
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
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
            self.battle_result = "Ничья!"
            return self.end_game()

        if self.player.health_points <= 0:
            self.battle_result = "Игрок проиграл битву!"
            return self.end_game()

        if self.enemy.health_points <= 0:
            self.battle_result = "Игрок выиграл битву!"
            return self.end_game()

        return None

    def _stamina_regeneration(self):
        # Регенерация здоровья и стамины для игрока и врага за ход.
        # В этом методе к количеству стамины игрока и врага прибавляется константное значение.
        # Главное чтобы оно не превысило максимальные значения (используйте if).
        stamina = round(self.player.stamina + self.STAMINA_PER_ROUND, 1)
        stamina = stamina if stamina <= self.player.unit_class.max_stamina else self.player.unit_class.max_stamina
        self.player.stamina = stamina

        stamina = round(self.enemy.stamina + self.STAMINA_PER_ROUND, 1)
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

        result = ""
        if self.game_is_running:
            self._stamina_regeneration()
            result = self.enemy.hit(self.player)

        return result

    def end_game(self) -> str:
        # Кнопка "Завершения игры" - > return result: str.
        # Очищаем синглтон - self._instances = {}, останавливаем игру (game_is_running), возвращаем результат
        self._instances: Dict[Any, Any] = {}
        result = f"{self.battle_result}"
        self.game_is_running = False
        return result

    def player_hit(self) -> str:
        # Кнопка "Удар игрока" -> return result: str.
        # Получаем результат от функции self.player.hit, запускаем следующий ход, возвращаем результат удара строкой.
        result_hit = self.player.hit(self.enemy)
        result_next = self.next_turn()
        return f"{result_hit}\n{result_next}"

    def player_use_skill(self):
        # Кнопка "Игрок использует умение".
        # Получаем результат от функции self.use_skill, включаем следующий ход, возвращаем результат удара строкой.
        result_hit = self.player.use_skill(self.enemy)
        result_next = self.next_turn()
        return f"{result_hit}\n{result_next}"
