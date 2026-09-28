"""Narrow observed-protection evidence; independent of existing damage policies."""
import campaign_events as ce

class ProtectionFailure:
    def __init__(self):
        self.previous = None
        self.failure = None

    def observe(self, turn, location, hp, maxhp, intact, polymorph):
        ce.hit('C.observations')
        current = (turn, location, hp, maxhp, intact, polymorph)
        if self.failure and (location != self.failure[1] or not intact or polymorph
                             or turn - self.failure[0] > 3 or (self.previous and maxhp != self.previous[3])):
            self.failure = None
        prev = self.previous
        if prev and turn == prev[0]:
            # Same-turn callbacks cannot establish or extend consecutive-turn evidence.
            self.previous = current
            return
        if prev and turn == prev[0] + 1 and location == prev[1] and intact and prev[4] \
                and not polymorph and not prev[5] and maxhp == prev[3] and hp < prev[2]:
            self.failure = (turn, location)
            ce.hit('C.qualified_loss')
            ce.sample('protected_hp_loss', turn=int(turn), hp=int(hp), previous_hp=int(prev[2]))
        self.previous = current

    def active(self, turn, location, intact, polymorph):
        return bool(self.failure and intact and not polymorph and location == self.failure[1]
                    and 0 <= turn - self.failure[0] <= 3)
