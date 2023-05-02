from source.map.position.position import *
from source.commission import commission_index
from source.util import *


"""
commission id: commission_name commission_position
example: ASmallStepForHilichurlsN1000P1000


commission name: 
thanks for https://genshin-dictionary.com/

IncreasingDanger IcD
ASmallStepForHilichurls AASFH
PudgyPyrotechnicians PP
IcyIssues II
BigPudgyProblem BPP
RulesOfSafeTransportation ROST
DangerousHaul DH
ImpregnableDefense IpD
etc.

commission position: where commission located 
format: (P/N)xxxC(P/N)xxx
P:+ N:- 
example: -1000,1000 => N1000P1000
offset within 50 TianLi Position
"""



def get_commission_object(commission_type, commission_position:list):
    offset = 50

    posi = commission_position
    logger.info(f"get commission: {commission_type, commission_position}")
    for i in commission_index.COMMISSION_INDEX:
        if commission_index.COMMISSION_INDEX[i]["type"] == commission_type:
            if euclidean_distance(commission_index.COMMISSION_INDEX[i]["position"], posi)<=offset:
                return commission_index.get_commission_object(i)
    logger.info(f"get commission fail, try to get general commission")
    if commission_type in ["ASmallStepForHilichurls", "Emergency", "IcyIssues", "ForTheHarbingers", "BigIceColdCrisis", "SpreadingEvil", "PudgyPyrotechnicians", "CrisisOfShields"]:
        import source.commission.general.OnlyFight
        return source.commission.general.OnlyFight.FightOnlyGeneral(commission_type, commission_position)
    elif commission_type == "IncreasingDanger":
        import source.commission.general.IncreasingDanger
        return source.commission.general.IncreasingDanger.IncreasingDangerGeneral(commission_position)

    logger.error(f"get commission fail: {commission_type, commission_position}")
    return False

if __name__ == "__main__":
    a = get_commission_object("ASmallStepForHilichurls",[-999,999])
    print()