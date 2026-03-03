# types of ingredient units users can select
ITEM_UNITS = ["unit", "clove"]

US_VOL_UNITS = ["cup", "tbsp", "tsp", "fl oz"]
US_WEIGHT_UNITS = ["lb", "oz"]

METRIC_VOL_UNITS = ["ml"]
METRIC_WEIGHT_UNITS = ["g"]

VOL_UNITS = US_VOL_UNITS+METRIC_VOL_UNITS
WEIGHT_UNITS = US_WEIGHT_UNITS+METRIC_WEIGHT_UNITS
UNIT_OPTIONS = ITEM_UNITS+VOL_UNITS+WEIGHT_UNITS


# TODO: add pint, quart, gallon?
def convertUnitAmount(amount, oldUnit, newUnit):
    # "cup", "tbsp", "tsp", "fl oz", "ml"
    # "lb", "oz", "g"
    if oldUnit == newUnit:
        return amount
    elif oldUnit in VOL_UNITS and newUnit in VOL_UNITS:
        # good to convert
        if oldUnit == "cup":
            if newUnit == "tbsp":
                return amount*16
            elif newUnit == "tsp":
                return amount*48
            elif newUnit == "ml":
                return amount*236.588
            elif newUnit == "fl oz":
                return amount*8
        elif oldUnit == "tbsp":
            if newUnit == "cup":
                return amount/16
            elif newUnit == "tsp":
                return amount*3
            elif newUnit == "ml":
                return amount*14.787
            elif newUnit == "fl oz":
                return amount/2
        elif oldUnit == "tsp":
            if newUnit == "cup":
                return amount/48
            elif newUnit == "tbsp":
                return amount/3
            elif newUnit == "ml":
                return amount*4.929
            elif newUnit == "fl oz":
                return amount/6
        elif oldUnit == "ml":
            if newUnit == "cup":
                return amount/236.588
            elif newUnit == "tbsp":
                return amount/14.787
            elif newUnit == "tsp":
                return amount/4.929
            elif newUnit == "fl oz":
                return amount/29.574
        elif oldUnit == "fl oz":
            if newUnit == "cup":
                return amount/8
            elif newUnit == "tbsp":
                return amount*2
            elif newUnit == "tsp":
                return amount*6
            elif newUnit == "ml":
                return amount*29.574
    elif oldUnit in WEIGHT_UNITS and newUnit in WEIGHT_UNITS:
        # also good to convert
        if oldUnit == "lb":
            if newUnit == "oz":
                return amount*16
            elif newUnit == "g":
                return amount*453.592
        elif oldUnit == "oz":
            if newUnit == "lb":
                return amount/16
            elif newUnit == "g":
                return amount*28.35
        elif oldUnit == "g":
            if newUnit == "oz":
                return amount/28.35
            elif newUnit == "lb":
                return amount/453.592
    else:
        # can't convert
        return -1

# TODO: add pint, quart, gallon?
def getUnitConversionScalar(oldUnit, newUnit):
    # "cup", "tbsp", "tsp", "fl oz", "ml"
    # "lb", "oz", "g"
    if oldUnit == newUnit:
        return 1
    elif oldUnit in VOL_UNITS and newUnit in VOL_UNITS:
        # good to convert
        if oldUnit == "cup":
            if newUnit == "tbsp":
                return 16
            elif newUnit == "tsp":
                return 48
            elif newUnit == "ml":
                return 236.588
            elif newUnit == "fl oz":
                return 8
        elif oldUnit == "tbsp":
            if newUnit == "cup":
                return 1/16
            elif newUnit == "tsp":
                return 3
            elif newUnit == "ml":
                return 14.787
            elif newUnit == "fl oz":
                return 1/2
        elif oldUnit == "tsp":
            if newUnit == "cup":
                return 1/48
            elif newUnit == "tbsp":
                return 1/3
            elif newUnit == "ml":
                return 4.929
            elif newUnit == "fl oz":
                return 1/6
        elif oldUnit == "ml":
            if newUnit == "cup":
                return 1/236.588
            elif newUnit == "tbsp":
                return 1/14.787
            elif newUnit == "tsp":
                return 1/4.929
            elif newUnit == "fl oz":
                return 1/29.574
        elif oldUnit == "fl oz":
            if newUnit == "cup":
                return 1/8
            elif newUnit == "tbsp":
                return 2
            elif newUnit == "tsp":
                return 6
            elif newUnit == "ml":
                return 29.574
    elif oldUnit in WEIGHT_UNITS and newUnit in WEIGHT_UNITS:
        # also good to convert
        if oldUnit == "lb":
            if newUnit == "oz":
                return 16
            elif newUnit == "g":
                return 453.592
        elif oldUnit == "oz":
            if newUnit == "lb":
                return 1/16
            elif newUnit == "g":
                return 28.35
        elif oldUnit == "g":
            if newUnit == "oz":
                return 1/28.35
            elif newUnit == "lb":
                return 1/453.592
    else:
        # can't convert
        return -1