from observer import Observer
import gc

class Buff(Observer):
    def __init__(self, priority=0, owner=None, name='', life=1, reduce_time='rounds_begin'):
        super().__init__(priority)
        self.owner, self.name, self.life, self.reduce_time = owner, name, life, reduce_time

    def response_event(self):
        self.reduce()
        self.burn()
        self.freeze()
        self.stimulate()
        self.entanglement()
        self.confinement()

    def reduce(self):
        if self.get_state('behavior') == self.reduce_time:
            self.life -= 1
        #print(gc.get_referents(self))
        if self.owner:
            if self.life:
                return
            elif self in self.owner.buff:
                self.owner.buff.remove(self)
        self.remove_observer(self)
        del self

    def burn(self):
        if self.name != 'Burn' or self.get_state('behavior') != 'face_power_begin'\
                or self.get_state('target') != self.owner:
            return
        element, fixed_power = self.get_state('element', str), self.get_state('fixed_power', int)
        if element == 'Pyro' or element == 'Dendro':
            print(f'{self.owner.name}处于燃烧')
            self.modify_last_event({'fixed_power': fixed_power + 2})
            self.modify_event({'fixed_power': fixed_power + 2}, notify=False)

    def freeze(self):
        if self.name == 'Freeze' and self.get_state('source') == self.owner:
            print(f'{self.owner.name}处于冻结')
            self.modify_last_event({'ban': True})

    def stimulate(self):
        if self.name != 'Stimulate' or self.get_state('behavior') != 'face_power_begin'\
                or self.get_state('target') != self.owner:
            return
        element, fixed_power = self.get_state('element', str), self.get_state('fixed_power', int)
        if element == 'Electro' or element == 'Dendro':
            print(f'{self.owner.name}处于激化')
            self.modify_last_event({'fixed_power': fixed_power + 2})
            self.modify_event({'fixed_power': fixed_power + 2}, notify=False)

    def entanglement(self):
        if self.name != 'Entanglement' or self.get_state('behavior') != 'face_power_begin'\
                or self.get_state('target') != self.owner:
            return
        element, fixed_power = self.get_state('element', str), self.get_state('fixed_power', int)
        if element == 'Quantum':
            print(f'{self.owner.name}处于纠缠')
            self.modify_last_event({'fixed_power': fixed_power + 2})
            self.modify_event({'fixed_power': fixed_power + 2}, notify=False)

    def confinement(self):
        if self.name != 'Confinement' or self.get_state('behavior') != 'face_power_begin'\
                or self.get_state('target') != self.owner:
            return
        element, fixed_power = self.get_state('element', str), self.get_state('fixed_power', int)
        if element == 'Imaginary':
            print(f'{self.owner.name}处于禁锢')
            self.modify_last_event({'fixed_power': fixed_power + 2})
            self.modify_event({'fixed_power': fixed_power + 2}, notify=False)
