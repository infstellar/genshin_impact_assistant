"""This file is generated automatically. Do not manually modify it."""
COMMISSION_INDEX = {'ASmallStepForHilichurls_N1000P1000': {'type': 'ASmallStepForHilichurls', 'position': [-1000, 1000]}, 'BigPudgyProblem_P2526N5796': {'type': 'BigPudgyProblem', 'position': [2526, -5796]}}
def get_commission_object(commission_name:str):
    if commission_name == 'ASmallStepForHilichurls_N1000P1000':
        import source.commission.commissions.ASmallStepForHilichurls_N1000P1000
        return source.commission.commissions.ASmallStepForHilichurls_N1000P1000.ASmallStepForHilichurls_N1000P1000()
    if commission_name == 'BigPudgyProblem_P2526N5796':
        import source.commission.commissions.BigPudgyProblem_P2526N5796
        return source.commission.commissions.BigPudgyProblem_P2526N5796.BigPudgyProblem_P2526N5796()
