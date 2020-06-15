import pygame
from sys import exit

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


def spawn(screen, base_dir, config, astrs):
    if len(astrs) == 0 or astrs.sprites()[len(astrs.sprites()) - 1].rect.x < config['mode'][0] - 200:
        astr = Asrteroid(screen, base_dir, config)
        astrs.add(astr)


def update(screen, config, base_dir, bg, plate, astrs, score, end, pause, tick):
    if config['sub_scene'] == 'game':
        if tick % 2 == 0:
            bg.update()

        bg.blit()

        if tick % 210 == 0:
            config['speed'] += 1

        spawn(screen, base_dir, config, astrs)

        for astr in astrs.copy():
            if astr.rect.right <= -5:
                astrs.remove(astr)
                if config['user']['effects']:
                    pygame.mixer.music.load(plate.sounds['score'])
                    pygame.mixer.music.play()
                config['score'] += 1

        for astr in astrs.sprites():
            astr.update() 
            astr.blit()

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


def check_collides(config, base_dir, astrs, plate, play, table, settings):
    collides = pygame.sprite.spritecollide(plate, astrs, True)

    if collides:
        for astr in collides:
            pygame.mixer.music.load(plate.sounds['bang'])
            pygame.mixer.music.play()
            astr.is_bang = True

            plate.reset()
            astrs.empty()

            config['speed'] = 2
            config['sub_scene'] = 'end'

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

        config['speed'] = 2
        config['sub_scene'] = 'end'
