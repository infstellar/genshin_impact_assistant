from source.util import *


sakura_list1 = [
            "SakuraBloom167910986687",
            "SakuraBloom16791098987",
            "SakuraBloom167911020876",
            "SakuraBloom167911023658",
            "SakuraBloom167911025376",
            "SakuraBloom167911029108",
            "SakuraBloom167911031376",
            
            # "SakuraBloom16791103543", # will die
            
            "SakuraBloom167911045521",
            "SakuraBloom167911054242",
            "SakuraBloom167911055897",
            "SakuraBloom167911062777",
            "SakuraBloom167911064519",
            "SakuraBloom167911068928",
            
            # "SakuraBloom167911071712", # will fall
            
            # "SakuraBloom167911074985", # fall
            # "SakuraBloom16791107662", # fall
            # "SakuraBloom167911081932", # fall
            # "SakuraBloom167911086202", # fall
                            ]
last_posi = [99999,99999]
for i in sakura_list1:

    jn = i+".json"
    jp = f"assets\\TeyvatMovePath"
    jsonn = load_json(jn,jp)
    print(i, euclidean_distance(jsonn["start_position"], last_posi))
    last_posi=jsonn["end_position"]