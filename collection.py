""" File with implementations of additional data structures """

import pygame


class BoostsGroup(pygame.sprite.Group):
    """ Extension of default pygame.sprite.Group for more easier control
        of boosts. Boosts are stored in two groups: active (which were
        activated) and passive (which were not activated). Active group
        cannot contain more than one boost of one type. Boosts are stored
        in form name-boost:

            {'time': <TimeBoost sprite(in 1 groups)>}

        Passive group contains other boosts in spritedict-likely style
        (boost-None):

            {<ShieldBoost sprite(in 1 groups)>: 0} """

    active = {}
    passive = {}
    next_spawn = 3

    def add_internal(self, boost):
        """ Adds boost to passive group """

        self.passive[boost] = 0
        pygame.sprite.Group.add_internal(self, boost)

    def remove_internal(self, boost):
        """ Removes boost. If boost is located in passive group,
            it simply will remove it from group. If boost is located
            in active group, it will update number in queue of other
            boosts and remove boost from group """

        if self.get(boost.name) == boost:
            flag = False

            for name, item in self.active.items():
                if name == boost.name:
                    flag = True

                elif flag:
                    item.number_in_queue -= 1

            del self.active[boost.name]
            pygame.sprite.Group.remove_internal(self, boost)

        elif self.passive.get(boost) == 0:
            del self.passive[boost]
            pygame.sprite.Group.remove_internal(self, boost)

    def empty(self):
        """ Resets itself """

        pygame.sprite.Group.empty(self)
        self.active.clear()
        self.passive.clear()
        self.next_spawn = 3

    def __contains__(self, item):
        """ Will return True, if group contains activated
            boost with passed name, else - False """

        if item.__class__.__name__ == 'str':
            return bool(self.get(item))
        return self.has(item)

    def activate(self, boost):
        """ Activates passed boost and move boost from passive group
            to active. If boost with boost's name have already activated,
            it will nullify tick (boost timer will start again) """

        boost.number_in_queue = len(self.active) + 1

        if self.active.get(boost.name):
            self.active[boost.name].tick = 0
            self.remove_internal(boost)
        else:
            del self.passive[boost]
            self.active[boost.name] = boost
            boost.activate()

    def get(self, name):
        """ Will return boost if active group contains boost
            with passed name. Else it will return None """

        return self.active.get(name)
