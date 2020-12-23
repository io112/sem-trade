class RVDItem:
    def __init__(self, arm, fit1, fit2, clutch1, clutch2):
        self._id = ''
        self.arm_id = arm['_id']
        self.fit1_id = fit1['_id']
        self.fit2_id = fit2['_id']
        self.clutch1_id = clutch1['_id']
        self.clutch2_id = clutch2['_id']

    def to_dict(self):
        res = {'arm_id': self.arm_id,
               'fit1_id': self.fit1_id,
               'fit2_id': self.fit2_id,
               'clutch1_id': self.clutch1_id,
               'clutch2_id': self.clutch2_id}
        return res