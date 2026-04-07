import math

def calculate_billet_costs(diameter_mm, length_mm, finish_weight_kg, mat_price_per_kg, hourly_rate, machining_hours):
    # 素材重量の計算（アルミ比重 2.7g/cm3）
    radius_cm = (diameter_mm / 10) / 2
    length_cm = length_mm / 10
    volume_cm3 = math.pi * (radius_cm ** 2) * length_cm
    raw_weight_kg = (volume_cm3 * 2.7) / 1000 # 

    # 切粉（キリコ）の重量とリサイクル益（素材単価の10%で還元）
    chip_weight = raw_weight_kg - finish_weight_kg
    scrap_return = chip_weight * (mat_price_per_kg * 0.1) #

    # コスト計算
    material_net_cost = (raw_weight_kg * mat_price_per_kg) - scrap_return
    processing_cost = machining_hours * hourly_rate
    
    return {
        "raw_weight": round(raw_weight_kg, 1),
        "chip_weight": round(chip_weight, 1),
        "material_cost": round(material_net_cost, 0),
        "processing_cost": round(processing_cost, 0),
        "removal_rate": round((chip_weight / raw_weight_kg) * 100, 1)
    }
