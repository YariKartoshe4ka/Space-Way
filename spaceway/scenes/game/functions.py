from sys import exit
from random import choice, randint

import pygame

from .objects import *


pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()


def init(screen, base_dir, config, msg):
    bg = Background(screen, base_dir, 0, 0)
    plate = SpacePlate(screen, base_dir, config)
    score = Score(screen, base_dir, msg)
    end = End(screen, base_dir, config)
    pause = Pause(screen, base_dir, config)

    return bg, plate, score, end, pause


def check_events(config, base_dir, plate, astrs, boosts, end, pause, play, table, settings):
    if config['sub_scene'] == 'game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                config['sub_scene'] = 'pause'

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if plate.rect.top >= plate.screen_rect.top + 50 and not plate.flip:
                    if config['user']['effects'] and plate.jump == 10:
                        pygame.mixer.Sound(plate.sounds['jump']).play()
                    plate.is_jump = True
                elif plate.rect.bottom <= plate.screen_rect.bottom - 50 and plate.flip:
                    if config['user']['effects'] and plate.jump == 10:
                        pygame.mixer.Sound(plate.sounds['jump']).play()
                    plate.is_jump = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if plate.rect.top >= plate.screen_rect.top + 50 and not plate.flip:
                    if config['user']['effects'] and plate.jump == 10:
                        pygame.mixer.Sound(plate.sounds['jump']).play()
                    plate.is_jump = True
                elif plate.rect.bottom <= plate.screen_rect.bottom - 50 and plate.flip:
                    if config['user']['effects'] and plate.jump == 10:
                        pygame.mixer.Sound(plate.sounds['jump']).play()
                    plate.is_jump = True

    elif config['sub_scene'] == 'end':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                play.to_bottom = True
                table.to_top = True
                settings.to_top = True
                config['sub_scene'] = 'game'
                config['scene'] = 'lobby'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if end.buttons.sprites()[0]._rect.collidepoint((x, y)):
                    print('click lobby!')
                    play.to_bottom = True
                    table.to_top = True
                    settings.to_top = True

                    config['score'] = 0
                    config['sub_scene'] = 'game'
                    config['scene'] = 'lobby'

                elif end.buttons.sprites()[1]._rect.collidepoint((x, y)):
                    print('click again!')
                    config['score'] = 0
                    config['sub_scene'] = 'game'
                    config['scene'] = 'game'

    elif config['sub_scene'] == 'pause':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                config['sub_scene'] = 'game'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if pause.buttons.sprites()[0]._rect.collidepoint((x, y)):
                    print('click lobby!')
                    play.to_bottom = True
                    table.to_top = True
                    settings.to_top = True

                    plate.reset()
                    astrs.empty()
                    boosts.empty()
                    config['speed'] = 2
                    config['score'] = 0
                    config['sub_scene'] = 'game'
                    config['scene'] = 'lobby'

                elif pause.buttons.sprites()[1]._rect.collidepoint((x, y)):
                    print('click resume!')
                    config['sub_scene'] = 'game'


def spawn(screen, base_dir, config, tick, plate, astrs, boosts):
    # Spawn asteroid
    if len(astrs) == 0 or astrs.sprites()[-1].rect.x < config['mode'][0] - 200:
        astrs.add(Asteroid(screen, base_dir, config))

    # Spawn flying asteroid if difficulty >= middle
    if config['score'] >= 10 and config['score'] % 5 == 0 and config['user']['difficulty'] >= 1:
        for sprite in astrs:
            if sprite.name == 'flying':
                break
        else:
            astrs.add(FlyingAsteroid(screen, base_dir, config))

    # Spawn boost
    if config['score'] >= boosts.next_spawn:
        boosts.next_spawn += randint(4, 8)

        choices = {'time': TimeBoost, 'double': DoubleBoost, 'shield': ShieldBoost}

        # Spawn mirror boost if difficulty >= hard
        if config['user']['difficulty'] >= 2:
            choices['mirror'] = MirrorBoost

        name = choice(list(choices))

        # if (len(boosts) == 3 and config['user']['difficulty'] == 2) or \
        #    (len(boosts) == 4 and config['user']['difficulty'] == 3):
        #    boosts.next_spawn += 1

        # while name in boosts:
        #     name = choice(list(choices))

        if name == 'time' or name == 'double':
            boost = choices[name](screen, base_dir, config)
        elif name == 'shield' or name == 'mirror':
            boost = choices[name](screen, base_dir, config, plate)

        while pygame.sprite.spritecollideany(boost, astrs):
            name = choice(list(choices))
            if name == 'time' or name == 'double':
                boost = choices[name](screen, base_dir, config)
            elif name == 'shield' or name == 'mirror':
                boost = choices[name](screen, base_dir, config, plate)

        boosts.add(boost)


def update(screen, config, base_dir, bg, plate, astrs, boosts, score, end, pause, tick):
    if config['sub_scene'] == 'game':
        if tick % 2 == 0:
            bg.update()

        bg.blit()

        if tick % (config['FPS'] * 7) == 0:
            for boost in boosts.sprites():
                if boost.name == 'time' and boost.is_active:
                    boost.speed += 1
                    break
            else:
                config['speed'] += 1

        spawn(screen, base_dir, config, tick, plate, astrs, boosts)

        for astr in astrs:
            if astr.rect.right < 0 or astr.rect.top > config['mode'][1]:
                astrs.remove(astr)
                if config['user']['effects']:
                    pygame.mixer.Sound(plate.sounds['score']).play()

                if 'double' in boosts:
                    config['score'] += 2
                else:
                    config['score'] += 1

        for astr in astrs:
            astr.update()
            astr.blit()

        plate.update()

        for boost in boosts:
            boost.update()
            boost.blit()

        score.msg = f"score: {config['score']}"
        score.update()
        score.blit()

        plate.blit()

    elif config['sub_scene'] == 'end':
        bg.blit()

        end.update()
        end.blit()

    elif config['sub_scene'] == 'pause':
        bg.blit()

        pause.update()
        pause.blit()


def check_collides(config, base_dir, astrs, boosts, plate, play, table, settings, score):
    astrs_collides = pygame.sprite.spritecollide(plate, astrs, True)
    boosts_collides = pygame.sprite.spritecollide(plate, boosts, False)

    if astrs_collides:
        if config['user']['effects']:
            pygame.mixer.Sound(plate.sounds['bang']).play()
    
        if 'shield' in boosts:
            boosts.remove(boosts.get('shield'))

        else:
            with open(f'{base_dir}/config/score.csv', 'a') as file:
                line = ','.join([str(config['score']), config['user']['nick']]) + '\n'
                file.write(line)

            score.is_update = True

            plate.reset()
            astrs.empty()
            boosts.empty()

            config['speed'] = 2
            config['sub_scene'] = 'end'

    elif boosts_collides:
        for boost in boosts_collides:
            if not boost.is_active:
                boosts.activate(boost)

    elif (plate.rect.bottom >= plate.screen_rect.bottom and not plate.flip) or (plate.rect.top <= plate.screen_rect.top and plate.flip):
        if config['user']['effects']:
            pygame.mixer.Sound(plate.sounds['bang']).play()

        if 'shield' in boosts:
            boosts.remove(boosts.get('shield'))
            plate.is_jump = True

        else:
            with open(f'{base_dir}/config/score.csv', 'a') as file:
                line = ','.join([str(config['score']), config['user']['nick']]) + '\n'
                file.write(line)

            score.is_update = True

            plate.reset()
            astrs.empty()
            boosts.empty()

            config['speed'] = 2
            config['sub_scene'] = 'end'
