def get_updated_nutrients(nutrients, serving_size):
    nutrients = {n: round(nutrients[n] * serving_size/100) for n in nutrients}
    return nutrients

def get_calories(fat, carbs, protein):
    return round(9*fat + 4*carbs + 4*protein)

def get_daily_values(nutrients):
    daily_values = {
        'calories': round(nutrients['calories']/2000 * 100),
        'fat': round(nutrients['fat']/65 * 100),
        'carb': round(nutrients['carb']/300 * 100),
        'protein': round(nutrients['protein']/50 * 100)
    }
    return daily_values