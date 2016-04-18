def body_mass_index(weight, height):
    return weight/(height**2)


def shape_of(weight, height):
    bmi = body_mass_index(weight, height)
    if bmi <= 15:
        return 'тежко недохранване'
    elif bmi > 15 and bmi <= 16:
        return 'средно недохранване'
    elif bmi > 16 and bmi <= 18.5:
        return 'леко недохранване'
    elif bmi > 18.5 and bmi <= 25:
        return 'нормално тегло'
    elif bmi > 25 and bmi <= 30:
        return 'наднормено тегло'
    elif bmi > 30 and bmi <= 35:
        return 'затлъстяване I степен'
    elif bmi > 35 and bmi <= 40:
        return 'затлъстяване II степен'
    else:
        return 'затлъстяване III степен'
