import sys,unittest
from test_strategies import FoodTests,ProtectionTests
from autoascend.protection_failure import ProtectionFailure
class FoodBoundary(FoodTests):
    def test_full_cooldown_from_failed_exit(self):
        def move(y,x):self.move(y,x);self.bl.time+=6;self.hostile=[1]
        self.a.move=move;self.run_buy()
        self.assertEqual(self.i._reserve_failed[(self.level.key(),(2,4))],self.bl.time+100)
class ObservationBoundary(ProtectionTests):
    def test_same_turn_loss_not_deferred(self):
        p=ProtectionFailure();self.observe(p,t=1,hp=10);self.observe(p,t=1,hp=9)
        self.observe(p,t=2,hp=9);self.assertFalse(self.active(p))
if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FoodBoundary if sys.argv[1]=='B' else ObservationBoundary)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
