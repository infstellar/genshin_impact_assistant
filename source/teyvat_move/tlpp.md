```python
{
    "start_position":[x,y]
    "end_position":[x,y]
    "position_list":[
        {"id": 1, "motion": "ANY|WALKING|FLYING|SWIMMING", "position": [x,y], "special_key": None}, 
        {"id": 2, "motion": "ANY|WALKING|FLYING|SWIMMING", "position": [x,y], "special_key": None}],
    "break_position":[...],
    "time":123456789,
    "additional_info": {
        "kyt2m_version": "1.0", 
        "pickup_points": [1, 4], 
        "adsorptive_position": [],
        "is_cliff_collection":True|False,
        "is_active_pickup_in_bp":True|False,
        "ads_offset":float=10
        "bp_ads_offset":float=30
        },
}
```