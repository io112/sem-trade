def get_filtered_params(session_id):
    selection = self.selection
    self.selection.set_subtotal(self.make_subtotal())
    session.add_data({'selection': self.selection.__get__()})
    update_session(session)
    fiting1 = selection["fiting1"]
    fiting2 = selection["fiting2"]
    arm = selection["arm"]
    clutch_params = self.not_zero_amount
    if arm.get_param_name() == Arm.get_param_name():
        clutch_params = arm.get_clutch_params()
    self.selection = selection
    self.arms = db.join_queries_and_find(dbvars.arm_collection, arm.get_filter_params())
    self.clutches = db.join_queries_and_find(dbvars.clutch_collection, clutch_params)
    self.fitings['1'] = db.join_queries_and_find(dbvars.fiting_collection, fiting1.get_filter_params())
    self.fitings['2'] = db.join_queries_and_find(dbvars.fiting_collection, fiting2.get_filter_params())
