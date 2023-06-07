@namespace
class SpriteKind:
    Boss = SpriteKind.create()
def lifeDecrease():
    info.change_life_by(-1)
    game.splash("OUCH! Lives remaining: " + str(info.life()))
    tiles.place_on_random_tile(protagonist, assets.tile("""
        start
    """))

def on_overlap_tile(sprite, location):
    game.game_over(True)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile0
    """),
    on_overlap_tile)

def on_b_pressed():
    global bullet
    bullet = sprites.create_projectile_from_sprite(assets.image("""
        bullet
    """), protagonist, 250, 0)
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

def bossReset():
    for value3 in sprites.all_of_kind(SpriteKind.player):
        sprites.destroy(value3)
    for value4 in sprites.all_of_kind(SpriteKind.enemy):
        sprites.destroy(value4)
    makePlayer()
    tiles.place_on_random_tile(protagonist, assets.tile("""
        boss_reset
    """))
    bossInit()

def on_a_pressed():
    protagonist.vy = -185
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_overlap_tile2(sprite2, location2):
    sprites.destroy(sprite2)
scene.on_overlap_tile(SpriteKind.enemy,
    assets.tile("""
        hazard
    """),
    on_overlap_tile2)

def enemyInit():
    global bossEnemy
    for value in tiles.get_tiles_by_type(assets.tile("""
        enemy_spawn
    """)):
        bossEnemy = sprites.create(assets.image("""
            enemy
        """), SpriteKind.enemy)
        tiles.place_on_tile(bossEnemy, value)
        bossEnemy.follow(protagonist, 30)
        bossEnemy.ay = 500
    for value2 in tiles.get_tiles_by_type(assets.tile("""
        flyingEnemy
    """)):
        bossEnemy = sprites.create(assets.image("""
            flying_enemy
        """), SpriteKind.enemy)
        tiles.place_on_tile(bossEnemy, value2)
        bossEnemy.follow(protagonist, 30)
def bossInit():
    global bossEnemy
    for value5 in tiles.get_tiles_by_type(assets.tile("""
        boss_spawn
    """)):
        bossEnemy = sprites.create(assets.image("""
            boss
        """), SpriteKind.Boss)
        tiles.place_on_tile(bossEnemy, value5)
        bossEnemy.follow(protagonist, 40)

def on_left_pressed():
    animation.run_image_animation(protagonist,
        assets.animation("""
            walk_left
        """),
        200,
        True)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def on_right_released():
    animation.stop_animation(animation.AnimationTypes.ALL, protagonist)
controller.right.on_event(ControllerButtonEvent.RELEASED, on_right_released)

def on_left_released():
    animation.stop_animation(animation.AnimationTypes.ALL, protagonist)
controller.left.on_event(ControllerButtonEvent.RELEASED, on_left_released)

def on_overlap_tile3(sprite3, location3):
    tiles.set_tile_at(location3, sprites.dungeon.chest_open)
    music.play(music.melody_playable(music.power_up),
        music.PlaybackMode.IN_BACKGROUND)
    info.change_life_by(1)
scene.on_overlap_tile(SpriteKind.player,
    sprites.dungeon.chest_closed,
    on_overlap_tile3)

def makePlayer():
    global protagonist
    protagonist = sprites.create(assets.image("""
        player
    """), SpriteKind.player)
    controller.move_sprite(protagonist, 100, 0)
    protagonist.ay = 500
    scene.camera_follow_sprite(protagonist)
    return protagonist

def on_right_pressed():
    animation.run_image_animation(protagonist,
        assets.animation("""
            walk_right
        """),
        200,
        True)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_overlap_tile4(sprite4, location4):
    game.game_over(False)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        hazard
    """),
    on_overlap_tile4)

def on_overlap_tile5(sprite5, location5):
    global currentLevelId
    tiles.set_tile_at(location5, assets.tile("""
        transparency16
    """))
    currentLevelId += 1
    if currentLevelId < 5:
        game.splash("Level " + str((currentLevelId + 1)))
    else:
        game.splash("FINAL LEVEL")
    tiles.set_current_tilemap(levels[currentLevelId])
    levelInit()
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        myTile2
    """),
    on_overlap_tile5)

def splash():
    game.show_long_text("******* STRANDED *******", DialogLayout.BOTTOM)

def on_menu_pressed():
    global debugPass, currentLevelId
    debugPass = game.ask_for_number("Enter passcode...")
    if debugPass == 675423:
        currentLevelId = game.ask_for_number("Go to which level?") - 1
        game.splash("Level " + str((currentLevelId + 1)))
        tiles.set_current_tilemap(levels[currentLevelId])
        levelInit()
controller.menu.on_event(ControllerButtonEvent.PRESSED, on_menu_pressed)

def on_life_zero():
    game.set_game_over_effect(False, effects.dissolve)
    game.game_over(False)
info.on_life_zero(on_life_zero)

def levelInit():
    for value32 in sprites.all_of_kind(SpriteKind.player):
        sprites.destroy(value32)
    for value42 in sprites.all_of_kind(SpriteKind.enemy):
        sprites.destroy(value42)
    makePlayer()
    tiles.place_on_random_tile(protagonist, assets.tile("""
        start
    """))
    if currentLevelId == 5:
        bossInit()
    else:
        enemyInit()

def on_on_overlap(sprite6, otherSprite):
    sprites.destroy(otherSprite)
sprites.on_overlap(SpriteKind.projectile, SpriteKind.enemy, on_on_overlap)

def on_on_overlap2(sprite7, otherSprite2):
    if sprite7.bottom < otherSprite2.y:
        sprites.destroy(otherSprite2)
        info.change_score_by(1)
        if info.score() % 10 == 0:
            info.change_life_by(1)
    else:
        lifeDecrease()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap2)

def on_overlap_tile6(sprite8, location6):
    tiles.set_tile_at(location6, assets.tile("""
        transparency16
    """))
    music.play(music.melody_playable(music.magic_wand),
        music.PlaybackMode.IN_BACKGROUND)
    info.change_score_by(1)
    if info.score() % 10 == 0:
        info.change_life_by(1)
        music.play(music.melody_playable(music.power_up),
            music.PlaybackMode.IN_BACKGROUND)
scene.on_overlap_tile(SpriteKind.player,
    assets.tile("""
        coin
    """),
    on_overlap_tile6)

def on_on_overlap3(sprite9, otherSprite3):
    global bossHits
    if sprite9.bottom < otherSprite3.y:
        info.change_score_by(1)
        if info.score() % 10 == 0:
            info.change_life_by(1)
        bossHits += 1
        sprites.destroy(otherSprite3)
        bossReset()
        if bossHits >= 9:
            sprites.destroy(otherSprite3)
            tiles.set_tile_at(tiles.get_tile_location(20, 10),
                assets.tile("""
                    myTile0
                """))
    else:
        lifeDecrease()
sprites.on_overlap(SpriteKind.player, SpriteKind.Boss, on_on_overlap3)

debugPass = 0
bossEnemy: Sprite = None
bullet: Sprite = None
protagonist: Sprite = None
levels: List[tiles.TileMapData] = []
bossHits = 0
currentLevelId = 0
currentLevelId = -1
bossHits = 0
levels = [tilemap("""
        level1
    """),
    tilemap("""
        level5
    """),
    tilemap("""
        level7
    """),
    tilemap("""
        level13
    """),
    tilemap("""
        level8
    """),
    tilemap("""
        level14
    """)]
info.set_life(3)
scene.set_background_color(12)
scene.set_background_image(assets.image("""
    overworld_bg
"""))
tiles.set_current_tilemap(tilemap("""
    level0
"""))
splash()
levelInit()