from flask import Flask, render_template, request, jsonify, redirect
from classes.base import Arena
from classes.classes import unit_classes
from classes.equipment import Equipment
from classes.unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": PlayerUnit,
    "enemy": EnemyUnit
}

# инициализируем класс арены
arena = Arena()

# инициализируем класс обмундирования
equipment = Equipment()


@app.route("/")
def menu_page():
    # Рендерим главное меню (шаблон index.html).
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    # Выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы.
    # Рендерим экран боя (шаблон fight.html).
    arena.start_game(heroes["player"], heroes["enemy"])
    return render_template("fight.html", heroes=heroes, result="Бой начался!", battle_result=arena.battle_result)


@app.route("/fight/hit")
def hit():
    # Кнопка нанесения удара.
    # Обновляем экран боя (нанесение удара) (шаблон fight.html).
    # Если игра идёт, вызываем метод player.hit() экземпляра класса арены,
    # если игра не идёт, пропускаем срабатывание метода (просто рендерим шаблон с текущими данными).
    result = ""
    if arena.game_is_running:
        result = arena.player_hit()
    return render_template("fight.html", heroes=heroes, result=result, battle_result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    # Кнопка использования скилла (логика практически идентична предыдущему эндпоинту).
    result = ""
    if arena.game_is_running:
        result = arena.player_use_skill()
    return render_template("fight.html", heroes=heroes, result=result, battle_result=arena.battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    # Кнопка пропуска хода.
    # Логика практически идентична предыдущему эндпоинту,
    # однако вызываем здесь функцию следующий ход (arena.next_turn()).
    result = ""
    if arena.game_is_running:
        result = arena.next_turn()
    return render_template("fight.html", heroes=heroes, result=result, battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    # Кнопка завершения игры, переход в главное меню.
    if arena.game_is_running:
        arena.end_game()
    return redirect("/")


@app.route("/choose-hero/", methods=["post", "get"])
def choose_hero():
    # Кнопка выбора героя.
    # 2 метода GET и POST:
    # на GET отрисовываем форму,
    # на POST отправляем форму и делаем редирект на эндпоинт choose enemy.
    if request.method == "GET":
        result = {"weapons": equipment.get_weapons_names(), "armors": equipment.get_armors_names(),
                  "header": "Выберите героя", "classes": unit_classes}
        return render_template("hero_choosing.html", result=result)
    if request.method == "POST":
        name = request.form.get("name", "John Doe")
        name = "John Doe" if name == "" else name
        player = PlayerUnit(name, unit_classes[request.form.get("unit_class")])
        player.equip_weapon(equipment.get_weapon(request.form.get("weapon")))
        player.equip_armor(equipment.get_armor(request.form.get("armor")))
        heroes["player"] = player
        return redirect("/choose-enemy/")
    return jsonify("Неверный метод запроса"), 500


@app.route("/choose-enemy/", methods=["post", "get"])
def choose_enemy():
    # Кнопка выбора соперников.
    # 2 метода GET и POST:
    # также на GET отрисовываем форму,
    # а на POST отправляем форму и делаем редирект на начало битвы:
    if request.method == "GET":
        result = {"weapons": equipment.get_weapons_names(), "armors": equipment.get_armors_names(),
                  "header": "Выберите врага", "classes": unit_classes}
        return render_template("hero_choosing.html", result=result)
    if request.method == 'POST':
        name = request.form.get("name", "Joe Blow")
        name = "Joe Blow" if name == "" else name
        enemy = EnemyUnit(name, unit_classes[request.form.get("unit_class")])
        enemy.equip_weapon(equipment.get_weapon(request.form.get("weapon")))
        enemy.equip_armor(equipment.get_armor(request.form.get("armor")))
        heroes["enemy"] = enemy
        return redirect("/fight/")
    return jsonify("Неверный метод запроса"), 500


if __name__ == "__main__":
    app.run()
