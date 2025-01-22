import random
from datetime import datetime, timedelta
import pandas as pd


def gen_inventory (num_items, num_skus):
    
    """a function that takes the argument num_items and generates a random list to feed the inventory"""
    
    # generate random skus
    random_skus = []
    def gen_skus():
        for _ in range(num_items):
            random_skus.append(f'a{random.randint(1, num_skus)}') # use 1 thousand possible skus
    gen_skus() 
    # generate random quantities
    random_quantities = []
    def gen_qty():
        for _ in range(num_items):
            random_quantities.append(random.randint(1, 10_0000)) # possible quantities up to 10k
    gen_qty() 
    # generate random dates
    s_date = '2025-01-01'
    format = '%Y-%m-%d'
    the_date = datetime.strptime(s_date, format).date()
    random_dates = []
    def gen_dates():
        for _ in range(num_items):
            rd = (the_date) + timedelta(days=random.randint(1,366))
            random_dates.append(str(rd))
    gen_dates()
    
    # pack the list of dictionaries 
    random_inventory = []
    for sku, qty, date in zip(random_skus, random_quantities, random_dates):
        random_inventory.append({'article': sku, 'quantity': qty, 'expiration_date': date})
    
    return random_inventory



def gen_demand (num_items, num_skus):
    
    """a function that takes the argument num_items and generates a random list to feed the demand"""

    # generate random skus
    random_skus = []
    def gen_skus():
        for _ in range(num_items):
            random_skus.append(f'a{random.randint(1, num_skus)}') # use 1 thousand possible skus
    gen_skus() 
    # generate random quantities
    random_quantities = []
    def gen_qty():
        for _ in range(num_items):
            random_quantities.append(random.randint(1, 10_0000)) # possible quantities up to 10k
    gen_qty() 
    # generate random dates
    s_date = '2025-01-01'
    format = '%Y-%m-%d'
    the_date = datetime.strptime(s_date, format).date()
    random_dates = []
    def gen_dates():
        for _ in range(num_items):
            rd = (the_date) + timedelta(days=random.randint(1,366))
            random_dates.append(str(rd))
    gen_dates()

    # pack the list of dictionaries 
    random_demand = []
    for sku, qty, date in zip(random_skus, random_quantities, random_dates):
        random_demand.append({'article': sku, 'quantity': qty, 'demand_date': date})

    return random_demand




def fefo_calc_opt(demand, inventory):
    """an optimised calculation of the inventory allocation to demand"""

    # order by date
    calc_dem_date = sorted(demand, key=lambda demd: demd['demand_date'])
    calc_inv_date = sorted(inventory, key=lambda expi: expi['expiration_date'])

    # expand sets 
    for i in calc_inv_date:
        i['remaining_quantity'] = i['quantity']
        i['consumed_quantity'] = 0

    for d in calc_dem_date:
        d['met_demand'] = 0
        d['unmet_demand'] = d['quantity']

    # Create a dictionary of inventory skus
    articles = {}
    for item in calc_inv_date:
        sku = item['article']
        if sku not in articles: 
            articles[sku] = []              # add the sku and assign it an empty list
            articles[sku].append(item)         # append the row to the list within the sku key
        else:
            articles[sku].append(item)         # append as before

    # Match demand to inventory and update the dynamic quantities
    # pull from articles
    for d in calc_dem_date:
        if d['article'] in articles:

            for i in articles[d['article']]:
                if d['demand_date'] < i['expiration_date']:
                    
                    if d['unmet_demand'] >= i['remaining_quantity']:    # if the unmet > remaining      |   (if d > i)
                        d['met_demand'] += i['remaining_quantity']
                        d['unmet_demand'] -= i['remaining_quantity']
                        i['consumed_quantity'] += i['remaining_quantity']
                        i['remaining_quantity'] = 0           
                    else:                                               # if the remaining > unmet      |   (if i > d)
                        d['met_demand'] += d['unmet_demand']
                        i['remaining_quantity'] -= d['unmet_demand']
                        i['consumed_quantity'] += d['unmet_demand']
                        d['unmet_demand'] = 0
                
    inventory_calc = pd.DataFrame(calc_inv_date)
    demand_calc = pd.DataFrame(calc_dem_date)
    return demand_calc, inventory_calc




def fefo_calc_slo(demand, inventory):
    """an hypothetically slow calculation of the inventory allocation to demand"""

    # order by date
    calc_dem_date = sorted(demand, key=lambda demd: demd['demand_date'])
    calc_inv_date = sorted(inventory, key=lambda expi: expi['expiration_date'])

    # expand sets 
    for i in calc_inv_date:
        i['remaining_quantity'] = i['quantity']
        i['consumed_quantity'] = 0

    for d in calc_dem_date:
        d['met_demand'] = 0
        d['unmet_demand'] = d['quantity']

    # Match demand to inventory and update the dynamic quantities
    for d in calc_dem_date:
        for i in calc_inv_date:

            if d['article'] == i['article'] and d['demand_date'] < i['expiration_date']: # if the demand happens prior to the expiration
                
                if d['unmet_demand'] >= i['remaining_quantity']:    # if the unmet > remaining      |   (if d > i)
                    d['met_demand'] += i['remaining_quantity']
                    d['unmet_demand'] -= i['remaining_quantity']
                    i['consumed_quantity'] += i['remaining_quantity']
                    i['remaining_quantity'] = 0         
                else:                                               # if the remaining > unmet      |   (if i > d)
                    d['met_demand'] += d['unmet_demand']
                    i['remaining_quantity'] -= d['unmet_demand']
                    i['consumed_quantity'] += d['unmet_demand']
                    d['unmet_demand'] = 0

    inventory_calc = pd.DataFrame(calc_inv_date)
    demand_calc = pd.DataFrame(calc_dem_date)
    return inventory_calc
    return demand_calc