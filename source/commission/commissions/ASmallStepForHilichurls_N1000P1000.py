from source.commission.commission_template import CommissionTemplate

meta = {
    "type":"ASmallStepForHilichurls",
    "position":[-1000,1000]
}
class ASmallStepForHilichurls_N1000P1000(CommissionTemplate):
    def __init__(self, position=None):
        super().__init__(meta["type"], meta["position"])