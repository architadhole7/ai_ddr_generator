def merge_observations(inspection, thermal):
    merged = []
    used_thermal = set()

    for ins in inspection:
        area_ins = (ins.get("area") or "").lower()
        details = ins.get("details", "")

        # try to attach relevant data
        for i, th in enumerate(thermal):
            if i in used_thermal:
                continue

            area_th = (th.get("area") or "").lower()

            #  match if area overlaps OR similar keywords
            if area_ins and area_th and (area_ins in area_th or area_th in area_ins):
                thermal_details = th.get("details", "")

                if thermal_details:
                    details += " | Thermal observation: " + thermal_details

                used_thermal.add(i)

        # update cleaned observation
        ins["details"] = details
        merged.append(ins)

    #  add leftover thermal observations (not matched)
    for i, th in enumerate(thermal):
        if i not in used_thermal:
            merged.append(th)

    return merged
