from sys import exit
from random import choices, randint

import pygame

from .objects import *


def check_events(config, base_dir, plate, astrs, boosts, end, pause, scene_buttons):
    if config['sub_scene'] == 'game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                scene_buttons.get_by_instance(PauseButton).press()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if plate.rect.top >= plate.screen_rect.top + 50 and not plate.flip:
                    plate.is_jump = True
                elif plate.rect.bottom <= plate.screen_rect.bottom - 50 and plate.flip:
                    plate.is_jump = True

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if plate.rect.top >= plate.screen_rect.top + 50 and not plate.flip:
                    plate.is_jump = True
                elif plate.rect.bottom <= plate.screen_rect.bottom - 50 and plate.flip:
                    plate.is_jump = True

    elif config['sub_scene'] == 'end':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                scene_buttons.get_by_instance(EndLobbyButton).press()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                scene_buttons.perform_point_collides((x, y))

    elif config['sub_scene'] == 'pause':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                scene_buttons.get_by_instance(ResumeButton).press()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                pause_lobby_button = scene_buttons.get_by_instance(PauseLobbyButton)
                if pause_lobby_button.rect.collidepoint((x, y)):
                    defeat(plate, astrs, boosts, end, config, base_dir)
                    config['scene'] = 'game'
                    config['sub_scene'] = 'pause'
                    pause_lobby_button.press()
                else:
                    scene_buttons.perform_point_collides((x, y))


def spawn(screen, base_dir, config, plate, astrs, boosts):
    # Spawn asteroid
    if len(astrs) == 0 or astrs.sprites()[-1].rect.x < config['mode'][0] - 200:
        astr = Asteroid(screen, base_dir, config)
        while pygame.sprite.spritecollideany(astr, boosts):
            astr = Asteroid(screen, base_dir, config)
        astrs.add(astr)

    # Spawn flying asteroid
    if config['ns'].score >= 10 and config['ns'].score % 5 == 0:
        for sprite in astrs:
            if sprite.name == 'flying':
                break
        else:
            astrs.add(FlyingAsteroid(screen, base_dir, config))

    # Spawn boost
    if config['ns'].score >= boosts.next_spawn:
        boosts.next_spawn += randint(4, 8)

        schema = {
            'time':   TimeBoost,
            'double': DoubleBoost,
            'shield': ShieldBoost,
            'mirror': MirrorBoost
        }

        weights = (40, 30, 10, 20)

        name = choices(list(schema), weights)[0]

        if name == 'time' or name == 'double':
            boost = schema[name](screen, base_dir, config)
        elif name == 'shield' or name == 'mirror':
            boost = schema[name](screen, base_dir, config, plate)

        while pygame.sprite.spritecollideany(boost, astrs):
            name = choices(list(schema))
            if name == 'time' or name == 'double':
                boost = schema[name](screen, base_dir, config)
            elif name == 'shield' or name == 'mirror':
                boost = schema[name](screen, base_dir, config, plate)

        boosts.add(boost)


def update(screen, config, base_dir, bg, plate, astrs, boosts, score, end, pause, pause_buttons, end_buttons, scene_buttons):
    if config['sub_scene'] == 'game':
        pygame.mixer.unpause()

        if not config['ns'].mm.get('game').get_num_channels():
            config['ns'].mm.get('game').play(-1)

        bg.update()
        bg.blit()

        scene_buttons.draw()

        config['ns'].current_time += config['ns'].dt / 30
        if config['ns'].current_time > 7:
            config['ns'].current_time = 0
            if 'time' in boosts:
                boosts.get('time').speed += 1
            else:
                config['ns'].speed += 1

        spawn(screen, base_dir, config, plate, astrs, boosts)

        for astr in astrs:
            if astr.rect.right < 0 or astr.rect.top > config['mode'][1]:
                astrs.remove(astr)
                config['ns'].mm.get('score').play()

                if 'double' in boosts:
                    config['ns'].score += 2
                else:
                    config['ns'].score += 1

        for astr in astrs:
            astr.update()
            astr.blit()

        plate.update()

        for boost in boosts:
            boost.update()
            boost.blit()

        score.msg = f"score: {config['ns'].score}"
        score.update()
        score.blit()

        plate.blit()

        check_collides(config, base_dir, astrs, boosts, plate, end)

    elif config['sub_scene'] == 'end':
        bg.blit()

        end.update()
        end.blit()

        end_buttons.draw()

    elif config['sub_scene'] == 'pause':
        pygame.mixer.pause()

        bg.blit()

        pause.update()
        pause.blit()

        pause_buttons.draw()


def check_collides(config, base_dir, astrs, boosts, plate, end):
    astrs_collides = pygame.sprite.spritecollide(plate, astrs, True)
    boosts_collides = pygame.sprite.spritecollide(plate, boosts, False)

    if astrs_collides:
        config['ns'].mm.get('bang').play()

        if 'shield' in boosts:
            boosts.remove(boosts.get('shield'))

        else:
            defeat(plate, astrs, boosts, end, config, base_dir)

    elif boosts_collides:
        for boost in boosts_collides:
            if not boost.is_active:
                boosts.activate(boost)

    elif (plate.rect.bottom >= plate.screen_rect.bottom and not plate.flip) or (plate.rect.top <= plate.screen_rect.top and plate.flip):
        config['ns'].mm.get('bang').play()

        if 'shield' in boosts:
            boosts.remove(boosts.get('shield'))
            plate.is_jump = True

        else:
            defeat(plate, astrs, boosts, end, config, base_dir)


def defeat(plate, astrs, boosts, end, config, base_dir):
    config['ns'].mm.get('game').stop()
    config['score_list'].append((config['ns'].score, config['user']['nick']))
    config.filter_score()
    config.save()

    end.score = config['ns'].score
    plate.reset()
    astrs.empty()
    boosts.empty()

    config['ns'].speed = 2
    config['ns'].current_time = 0
    config['ns'].score = 0
    config['scene'] = 'game'
    config['sub_scene'] = 'end'
