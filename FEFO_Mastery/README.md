# FEFO Inventory management
In this Jupyter Notebook we want to write a comprehensive script that allows us to tackle inventory management strategy called FEFO, First Expiry First Out. 

# Issue
This warehouse management technique is very simple and allows to make good use of products with limited shelf life. By definition it allocates to production  the inventory that is expiring first. 

As we know, inventory is not necessarily physically ordered by expiration dates. The organisation of a warehouse that stores food, automotive bits or electronics follow many complex rules that consider the consumption, the weight, the hazard class and many other parameters. So having a software based calculation that tells us what product to use first, among many in many different locations, is quite necessary.

# Scope of this notebook
In this notebook I guide the reader through the passages that allow me to build a functioning model of FEFO allocation given:
- An inventory with articles and dates of expiry
- A demand list with articles and dates

We start from simple steps, like building and iterating through our objects.
Then we move to allocation.
And thus we discover more complex behaviours (costs, waste, ratios) and scenarios (multi-warehouse, multi-batch)

I hope you find this useful and thank you for reading so far! 