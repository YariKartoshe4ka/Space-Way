import pygame


class BoostsGroup(pygame.sprite.Group):
    container = {}
    next_spawn = 1

    def get(self, name):
        return self.container.get(name)

    def add_internal(self, boost):
        if not self.container.get(boost.name, False):
            self.container[boost.name] = boost
            pygame.sprite.Group.add_internal(self, boost)

    def remove_internal(self, boost):
        if self.container.get(boost.name, False):
            flag = False

            for name, item in self.container.items():
                if name == boost.name:
                    flag = True

                elif flag:
                    item.number_in_queue -= 1

            del self.container[boost.name]
            pygame.sprite.Group.remove_internal(self, boost)

    def __contains__(self, item):
        if item.__class__.__name__ == 'str':
            return bool(self.get(item))
        return self.has(item)
