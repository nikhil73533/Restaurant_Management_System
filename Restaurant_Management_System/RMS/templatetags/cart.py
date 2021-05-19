from django import template
register = template.Library()



# For Discount 
@register.filter(name="is_discount")
def is_discount(product,cart):
    print(cart)
    if(product.Discount_In_Percentage>0):
        return True
    return False

@register.filter(name = "discount_calculater")
def discount_calculater(product,cart):
    difference = (product.Food_Price)*((product.Discount_In_Percentage)/(100))
    return int(product.Food_Price - difference)



# Cart filters

@register.filter(name="is_in_cart")
def is_in_cart(product,cart):
    keys= cart.keys()
    for id in keys:
        if(int(id)==product.id):
            return True
    return False


@register.filter(name="cart_count")
def cart_count(product,cart):
    keys= cart.keys()
    for id in keys:
        if(int(id)==product.id):
            return cart.get(id)
    return 0

@register.filter(name="price_total")
def price_total(product,cart):
    food_price = product.Food_Price
    if(is_discount(product,cart)):
        food_price = discount_calculater(product,cart)
    return food_price* cart_count(product,cart) 

@register.filter(name="Total_Price")
def Total_Price(product,cart):
    sum = 0
    for p in product:
        sum+=price_total(p,cart)
    return sum

