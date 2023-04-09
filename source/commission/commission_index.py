"""This file is generated automatically. Do not manually modify it."""
COMMISSION_INDEX = {'ASmallStepForHilichurls_N1000P1000': {'type': 'ASmallStepForHilichurls', 'position': [-1000, 1000]}, 'BasicKnowledgeOfTheKnights_P2682N5673': {'type': 'BasicKnowledgeOfTheKnights', 'position': [2682, -5673]}, 'BigPudgyProblem_P2469N4886': {'type': 'BigPudgyProblem', 'position': [2469, -4886]}, 'BigPudgyProblem_P2526N5796': {'type': 'BigPudgyProblem', 'position': [2526, -5796]}, 'TheUnnoticedGuy_P2568N5889': {'type': 'TheUnnoticedGuy', 'position': [2568, -5889]}}
def get_commission_object(commission_name:str):
    if commission_name == 'ASmallStepForHilichurls_N1000P1000':
        import source.commission.commissions.ASmallStepForHilichurls_N1000P1000
        return source.commission.commissions.ASmallStepForHilichurls_N1000P1000.ASmallStepForHilichurls_N1000P1000()
    if commission_name == 'BasicKnowledgeOfTheKnights_P2682N5673':
        import source.commission.commissions.BasicKnowledgeOfTheKnights_P2682N5673
        return source.commission.commissions.BasicKnowledgeOfTheKnights_P2682N5673.BasicKnowledgeOfTheKnights_P2682N5673()
    if commission_name == 'BigPudgyProblem_P2469N4886':
        import source.commission.commissions.BigPudgyProblem_P2469N4886
        return source.commission.commissions.BigPudgyProblem_P2469N4886.BigPudgyProblem_P2469N4886()
    if commission_name == 'BigPudgyProblem_P2526N5796':
        import source.commission.commissions.BigPudgyProblem_P2526N5796
        return source.commission.commissions.BigPudgyProblem_P2526N5796.BigPudgyProblem_P2526N5796()
    if commission_name == 'TheUnnoticedGuy_P2568N5889':
        import source.commission.commissions.TheUnnoticedGuy_P2568N5889
        return source.commission.commissions.TheUnnoticedGuy_P2568N5889.TheUnnoticedGuy_P2568N5889()
