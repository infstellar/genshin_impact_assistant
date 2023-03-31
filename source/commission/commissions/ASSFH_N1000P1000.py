from source.commission.commission_template import CommissionTemplate

meta = {
    "type":"ASSFH",
    "position":[-1000,1000]
}
class ASSFH_N1000P1000(CommissionTemplate):
    def __init__(self):
        super().__init__(meta["type"], meta["position"])