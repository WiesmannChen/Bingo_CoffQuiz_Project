import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bingo_coffquiz_project.settings')

import django
django.setup()
from coffquiz.models import Coffee, Article
from django.contrib.auth.models import User

def populate():

    user_data = {'username': 'Admin', 'email': 'coffquiz@gmail.com', 'passward': 'coffquizadmin'}

    

    starbucks = [
        {'title': 'Starbucks Sumatra Dark Blind Assessment', 'views':58,
         'content': 'Roast-dominant, smoky-sweet. Dark chocolate, burned mesquite, lily, prune, fresh earth in aroma and cup. Bittersweet structure with barely perceptible acidity; \
             heavy, smooth mouthfeel. Persistent dark chocolate notes lift a rather bitter, earthy finish. \n A good choice for those who like classic dark-roasted Sumatras: earthy-sweet, smoky chocolate.'}
    ]

    nescafe = [
        {'title': 'Nescafe Instant Coffee Review', 'views':40,
         'content': 'Evaluated at proportions of 5 grams of instant coffee powder mixed with 8.5 ounces (250 ml) of hot water. Flat, salty, expressionless. Salted graham cracker, a faint vegetal note in aroma and cup. \
             Sweet-salty-acrid in structure. Flat, lifeless mouthfeel. Rounds and sweetens just a bit in the finish. \n Not a pleasant experience.'
        },
    ]


    coffeelist = {'Starbucks Sumatra Dark': {'articles': starbucks, 'likes':56,
                  'description':'Sumatra coffee is a dark-roasted, full-bodied coffee with spicy and herbal notes and a deep, earthy aroma. \n Darker-roasted coffees have fuller body with robust, bold taste'},
                  'Nescafe Instant Coffee': {'articles': nescafe, 'likes':10,
                  'description': 'Nescafe signature blend. Its Master Coffee Crafters mildly roast and brew our special blend of premium quality coffee beans and then flash freeze the coffee to lock in the smooth and well-balanced flavor.'},
    }


    user = add_user(user_data['username'], user_data['email'], user_data['passward'])
    
    for coffee, coffee_data in coffeelist.items():
        c = add_coffee(user, coffee, likes=coffee_data['likes'], description=coffee_data['description'])
        for a in coffee_data['articles']:
            add_article(user, c, a['title'], views=a['views'], content=a['content'])

    print('Success!')

def add_article(user, coffee, title, views=0, content=''):
    a = Article.objects.get_or_create(writer=user, coffee=coffee, title=title)[0]
    a.views = views
    a.content = content
    a.save()
    return a

def add_coffee(user, name, likes=0, description=''):
    c = Coffee.objects.get_or_create(user=user, name=name)[0]
    c.likes = likes
    c.description = description
    c.save()
    return c

def add_user(name, email, password):
    u = User.objects.get_or_create(username=name)[0]
    u.emailaddress = email
    u.password = password
    u.save()
    return u

# Start execution here!
if __name__ == '__main__':
    print('Starting CoffQuiz population script...')
    populate()