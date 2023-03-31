"""This file is generated automatically. Do not manually modify it."""
COMMISSION_INDEX = {'ASSFH_N1000P1000': {'type': 'ASSFH', 'position': [-1000, 1000]}}
def get_commission_object(commission_name:str):
    if commission_name == 'ASSFH_N1000P1000':
        import source.commission.commissions.ASSFH_N1000P1000
        return source.commission.commissions.ASSFH_N1000P1000.ASSFH_N1000P1000()
