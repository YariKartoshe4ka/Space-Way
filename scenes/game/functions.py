import pygame
from sys import exit
from random import randint

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


def check_events(config, base_dir, plate, astrs, end, pause, play, table, settings):
    if config['sub_scene'] == 'game':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                config['sub_scene'] = 'pause'

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and plate.rect.top >= plate.screen_rect.top + 50:
                    if config['user']['effects'] and plate.jump == 10:
                        pygame.mixer.music.load(plate.sounds['jump'])
                        pygame.mixer.music.play()
                    plate.is_jump = True

            elif event.type == pygame.MOUSEBUTTONDOWN and plate.rect.top >= plate.screen_rect.top + 50:
                if config['user']['effects'] and plate.jump == 10:
                    pygame.mixer.music.load(plate.sounds['jump'])
                    pygame.mixer.music.play()
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
                    config['speed'] = 2
                    config['score'] = 0
                    config['sub_scene'] = 'game'
                    config['scene'] = 'lobby'

                elif pause.buttons.sprites()[1]._rect.collidepoint((x, y)):
                    print('click resume!')
                    config['sub_scene'] = 'game'


def spawn(screen, base_dir, config, tick, astrs, boosts):
    if len(astrs) == 0 or astrs.sprites()[-1].rect.x < config['mode'][0] - 200:
        astrs.add(Asrteroid(screen, base_dir, config))

    if len(boosts) == 0:
        choice = randint(0, 0)
        y = randint(1, config['mode'][1] - 35)
        astr = astrs.sprites()[-1]
        print(astr.rect)

        while not (y < astr.rect.y - 40) and not (y > astr.rect.y + astr.rect.height + 10):
            y = randint(1, config['mode'][1] - 35)

        if choice == 0:
            boosts.add(TimeBoost(screen, base_dir, config, y))


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

        spawn(screen, base_dir, config, tick, astrs, boosts)

        for astr in astrs.copy():
            if astr.rect.right < 0:
                astrs.remove(astr)
                if config['user']['effects']:
                    pygame.mixer.music.load(plate.sounds['score'])
                    pygame.mixer.music.play()
                config['score'] += 1

        for astr in astrs.sprites():
            astr.update() 
            astr.blit()

        for boost in boosts.sprites():
            boost.update()
            boost.blit()

        score.msg = f"score: {config['score']}"
        score.update()
        score.blit()

        plate.update()
        plate.blit()

    elif config['sub_scene'] == 'end':
        bg.blit()

        end.update()
        end.blit()

    elif config['sub_scene'] == 'pause':
        bg.blit()

        pause.update()
        pause.blit()


def check_collides(config, base_dir, astrs, boosts, plate, play, table, settings):
    astrs_collides = pygame.sprite.spritecollide(plate, astrs, True)
    boosts_collides = pygame.sprite.spritecollide(plate, boosts, False)

    if astrs_collides:
        for astr in astrs_collides:
            if config['user']['effects']:
                pygame.mixer.music.load(plate.sounds['bang'])
                pygame.mixer.music.play()
            astr.is_bang = True

            with open(f'{base_dir}/config/score.csv', 'a') as file:
                line = ','.join([str(config['score']), config['user']['nick']]) + '\n'
                file.write(line)

            plate.reset()
            astrs.empty()
            boosts.empty()

            config['speed'] = 2
            config['sub_scene'] = 'end'

    elif boosts_collides and not boosts_collides[0].is_active:
        boost = boosts_collides[0]

        if boost.name == 'time':
            boost.is_active = True
            boost.speed = config['speed']
            config['speed'] = 2

    elif plate.rect.bottom >= plate.screen_rect.bottom:
        if config['user']['effects']:
            pygame.mixer.music.load(plate.sounds['bang'])
            pygame.mixer.music.play()
        plate.is_jump = True


        with open(f'{base_dir}/config/score.csv', 'a') as file:
            line = ','.join([str(config['score']), config['user']['nick']]) + '\n'
            file.write(line)

        plate.reset()
        astrs.empty()
        boosts.empty()

        config['speed'] = 2
        config['sub_scene'] = 'end'
