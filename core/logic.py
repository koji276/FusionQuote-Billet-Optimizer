import math

def calculate_billet_quote(diameter_mm, length_mm, finish_weight_kg, material_price_per_kg, hourly_rate):
    # 素材重量の算出（アルミ比重 2.7g/cm3）
    radius_cm = (diameter_mm / 10) / 2
    length_cm = length_mm / 10
    volume_cm3 = math.pi * (radius_cm ** 2) * length_cm
    raw_weight_kg = (volume_cm3 * 2.7) / 1000  # 

    # 切粉（キリコ）重量とリサイクル益
    chip_weight = raw_weight_kg - finish_weight_kg
    material_cost = raw_weight_kg * material_price_per_kg
    scrap_return = chip_weight * (material_price_per_kg * 0.1)  # 誠実な減額

    # 正味材料原価
    net_material_cost = material_cost - scrap_return

    return {
        "raw_weight": raw_weight_kg,
        "chip_weight": chip_weight,
        "net_material_cost": net_material_cost,
        "removal_rate": (chip_weight / raw_weight_kg) * 100
    }
