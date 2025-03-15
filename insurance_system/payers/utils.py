from fuzzywuzzy import fuzz

def deduplicate_payers(payers_list):
    deduped_payers = {}
    
    for payer in payers_list:
        matched = None
        for key in deduped_payers.keys():
            if fuzz.ratio(payer, key) > 85:  
                matched = key
                break

        if matched:
            deduped_payers[matched].append(payer)
        else:
            deduped_payers[payer] = [payer]

    return deduped_payers
