import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bingo_coffquiz_project.settings')

import django
django.setup()
from coffquiz.models import Coffee, Article
from django.contrib.auth.models import User

# Coffee product information and reviews come from Amazon website https://www.amazon.com/

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

    peet = [
        {'title': 'Espresso Forte Review', 'views': 43,
         'content': 'This is my favorite coffee to make at home or at the office. There\'s 0 bitterness. It has a full, bold taste as opposed to having a watery, thin profile. \
         I\'ve had my friends say they love it as well - so much that I\'ve actually gifted it. I\'ve purchased it numerous times from Amazon and I have absolutely zero complaints regarding taste.'
        },
        {'title': 'Espresso Forte Taste', 'views':56,
         'content': 'Our favorite coffee delivered straight to our door for prices below supermarket or coffee shop retail. What more could a girl ask for? Rich dark brew, never bitter, the perfect thing to wake up to. \
             We order two bags at a time, and have been Pete\'s Coffee devotees for more than 30 years. So happy to get San Francisco Bay area coffee down in San Diego! Thank you Amazon for carrying this product.'        
        }
    ]

    manatee = [
        {'title': 'Caribbean Delight Review', 'views':48,
         'content': 'I love the added flavor notes in this coffee. The item description describes the flavor well. I like sweet and creamy coffee and have even been able to do this coffee with half and half only (no sugar/sweetener). \
             My favorite is to still add a little bit of sweetness though. Even with the flavor notes included in the coffee already, I’ve enjoyed it with a chocolate creamer too.'
        }, 
        {'title': 'Caribbean Delight Exploded', 'views':80,
         'content': 'I love the taste of the coffee but I’m so tired of throwing it away due to MORE than HALF of my Kcups exploding in the brewer!!! This is now the THIRD BOX in a row that I have thrown away already more than half of what I have brewed. \
            This is the reason I refuse to order the coffee when it jumps in price and to be honest, getting ready to stop wasting my money all together. I’m sick of having to clean the brewer out after as well !!! \
            Who the heck wants to wait on a KCUP and also have to clean up the mess it leaves behind when quick convenience is the reason we buy them in the first place! Oh and I’ve looked on the package for any visible customer service number, email or website to call and let them know....... and NOTHING!!!!'
        }
    ]

    copper = [
        {'title': 'Guagraphan Antigua Review', 'views':59,
         'content': 'Has a nice mix of slightly fruity and a dark roast flavor, which is exactly what I was after with a medium-dark roast. Doesn\'t have that beany flavor like a Colombian, which I don\'t really like so this is very good imo. \
             The beans look nice. Didn\'t find any small, broken, off roasted or otherwise bad looking beans when I ground some this morning which shows care in roasting. You can pay a lot more for coffee this good. Definitely recommend.'
        },
        {'title': 'Guagraphan Antigua Taste', 'views':60, 
        'content': 'A very mild taste. I ordered while waiting for some Sumatra to arrive. I was surprised how non-offensive this roast was. What I don\'t like it acidic coffee that bites. \
            What I got in this roast was a roast that did not feel sharp on the tongue and smooth. I rarely, if ever buy pre-roasted coffee so this was absolutely ON-TARGET for my taste. If you don\'t like sharp, tangy, smoky coffee this is your best bet!'
        },
    ]

    kicking = [
        {'title': 'Grizzly Claw Taste', 'views': 23,
         'content': 'I have worked in coffee shops for many years and am a bit of a snob when it comes to coffee. I got this coffee as my espresso roast on a whim because, pound-wise, it was actually a good deal. I normally use Pete’s espresso and hate deviating. \
              This was a great coffee. Not only is it fair-trade, it’s good, too. I found it to be medium-bold but not bitter at all. It produced a thick and sweet crema and I didn’t even have to adjust my grinder. It has a good flavor to it and I would describe it as almost nutty. \
                  I already ordered more and am happy to say I will likely stick with Kicking Horse for a while. If you like dark and bitter coffees, you likely won’t like this though.'
        },
        {'title': 'Grizzly Claw is My Favorite', 'views': 42,
         'content': 'I tried many different brands of coffee beans until I found the one that I like the best for my Latte\'s. I wanted a bean with a strong flavor that was not overwhelmed by the milk. I don\'t like a bitter coffee just a strong coffee. The Kicking Horse dark roast seems to be the one. \
                The price is about average for a good coffee. I generally get a big bag or two per order and it is fresh and stays that way until I use it up. My wife and I have one or two latte\'s a day, every day. We use a large Breville machine.'
        }
    ]

    lavazza = [
        {'title': 'Lavazza is so good', 'views': 76,
         'content': 'I have spent years refining my \'go to\' coffee bean for my machine and settled on the the standard red bag Lavazza. Yes, there are some really nice ones out there at higher prices, but for a good quality all rounder, you can\'t beat this for value....\
             I stumbled on this \'Top Class\' one unintentionally and to be fair, was attracted by the blue and red bag. At a similar price to the other one, I gave it a go.... It is much better than the red bag. A more full flavour, so many more notes and depth. A moderate crème on top..... it is my relatively new \'go to\' coffee bean.'
        }, 
        {'title': 'Lavazza E Gusto Review', 'views': 35,
         'content': 'This is to Lavazza Rossa what a single malt is to a £20 blend - whereas Rossa is a solid, flavoursome and great all-rounder, it is clumsy in its dependable delivery of decent coffee flavour. The Tierra is a more refined beast with more fruity, floral flavours that the robusta of rossa blockades. \
            With this blend, you get dark chocolate, vanilla and almost a slight liquorice note like you do from dark cocoa. It’s a superior flavour and one that suits darker, more roasted palates but is not bitter or acrid at all. It’s really decent coffee and a happy bridge between a “medium” and an “espresso” roast. I’d buy it again. Happy I did.'
        }, 
    ]

    amazon = [
        {'title': 'AmazonFresh is bad', 'views':40,
         'content': 'Since Amazon purchased Whole Foods, I figured these products on line would be superior quality. Boy was I wrong here. I did buy several different excellent coffees on amazon recently, to compare, but this one greatly disappoints. Very surprising. \
             Opening the bag, the smell is excellent but I’ve seen this before in bitter drinking coffees. They have a great nose but the flavor is inferior, and here I dare say “bad”.'
        },
        {'title': 'AmazonFresh Review', 'views':40,
         'content': 'This wasn’t the best coffee I’ve ever had but it certainly wasn’t the worst. For the price point you get a ton of coffee. If you’re on a budget, this easily can make coffee for a month (or two if you don’t make 12cups at a time). Shipping was quick as usual. Only wish it came with a scoop already in.'
        }
    ]

    healthwise = [
        {'title': 'Trying Low Acid Coffee for the first time', 'views':38,
         'content': 'Do not buy this coffee it is very acidic. We used litmus paper to test it. This came in on the litmus paper as 5.0 - very acidic... compared to Kava low acid coffee which is 6.9 - 7 being neutral. \
             It is important to my stomach that the acid content be low if I am going to drink coffee. I have no idea how this company can list this as low acid. It is a lie.'
        },
        {'title': 'Low Acid Coffee Review', 'views':20,
         'content': 'Iv\'e had acid reflux for a long time and have a really bad reaction to most coffee brands. This is a lot better than any brewed coffee Iv\'e ever had. It still causes some reflux for me some of the time (hence the 4 start review), but it\'s very manageable. \
             I buy the grounds and cold brew it for 24 hours, and the flavor is incredible. Cold brewing coffee also lowers the acidity, so that\'s also worth a try if you have acid reflux. The price might seem like a lot, but I cold brew a nice sized pitcher and have it for a week so it does last. Enjoy!'
        },
    ]

    tieman = [
        {'title': 'Tieman\'s Fusion Coffee Review', 'views': 25,
         'content': 'This coffee is smooth, not at all bitter. It does not make your stomach upset like other coffees can. Really like it! I often mix it with other more acidic coffees that I also enjoy. It helps to cut down on the acidity, big time. The only thing I don\'t care as much for is the packaging. \
             The outer paper bag really needs to be discarded once you\'ve opened the package, else it becomes a nuisance. Problem is the inside package is an unmarked shiny silver vacuum sealed package for practicality reasons. If you don\'t write on it what it is, you may forget what it is!'
        },
        {'title': 'Tieman\'s Fusion Coffee is the Best', 'views': 25,
         'content': 'LOVE, LOVE, LOVE this coffee! I often have issues with my gut and yeast. Some research that I have found seem to say that over time coffee can affect the stomach/gut (which just seemed to all link together to me) \so when I saw that this coffee is low acidity and also mixed with Koji berry I had to try. \
             Completely cutting out coffee isn\'t int he cards yet so I wanted to try something that might help. You will not be disappointed! The taste is great, I like the Medium but Im sure all of them are good. If you have the same issues I do, try this and see if it helps.'
        },
    ]

    coffeelist = {'Starbucks Sumatra Dark': {'articles': starbucks, 'likes':64,
                  'description':'Sumatra coffee is a dark-roasted, full-bodied coffee with spicy and herbal notes and a deep, earthy aroma. \n Darker-roasted coffees have fuller body with robust, bold taste'
                  },
                  'Nescafe Instant Coffee': {'articles': nescafe, 'likes':20,
                  'description': 'Nescafe signature blend. Its Master Coffee Crafters mildly roast and brew our special blend of premium quality coffee beans and then flash freeze the coffee to lock in the smooth and well-balanced flavor.'
                  },
                  'Peet\'s Coffee Espresso Forte': {'articles': peet, 'likes':62,
                  'description': 'Espresso Forte: crafted specifically for espresso, this superbly balanced blend has stout body, rich flavor and perfect crema. Prepare with your espresso machine to create a coffee bar-quality espresso, latte or cappuccino.'
                  },
                  'Manatee Gourmet Caribbean Delight': {'articles': manatee, 'likes': 24,
                  'description': 'Manatee Gourmet Coffee imports only the finest coffee beans from around the world. Manatee Gourmet Coffees are roasted, blended to perfection and then packaged and shipped with care. \
                      At Manatee Gourmet Coffee we have taken great pride in sourcing pure Arabica beans that produce a very satisfying rich body of complex flavors.'
                  },
                  'Copper Moon Guagraphan Antigua': {'articles': copper, 'likes':40,
                  'description': 'At Copper Moon Coffee, we roast single batches of beans for the best flavor. Our variety of origins, blends, & roasts bring you the freshest coffee to brew & serve, with a delightfully full body & creamy, smooth finish to each sip.'
                  },
                  'Kicking Horse Coffe Grizzly Claw': {'articles': kicking, 'likes': 32,
                  'description': 'DARK ROAST, WHOLE BEAN: Rich, dark chocolate, decadent. From the heart of the mountains, a strong spirit roars. The most magical hand mother nature can deal.'
                  },
                  'Lavazza Crema E Gusto': {'articles': lavazza, 'likes': 58,
                  'description': 'Lavazza crema E Gusto is a whole bean coffee offering a distinctive character perfectly combining an intense aroma and full-bodied taste. It consists of a selection of high quality Arabica and Robusta beans with a fragrant flavor and a pleasant chocolatey finish.'
                  },
                  'AmazonFresh Go For The Bold': {'articles': amazon, 'likes':42,
                  'description': 'Our AmazonFresh Go For The Bold dark roast ground coffee is made with high quality 100% Arabica beans, expertly roasted and immediately packed for freshness. This full-bodied blend has a notes of dark chocolate, making it bold in flavor and destined to please.'
                  },
                  'HealthWise Low Acid Coffee': {'articles': healthwise, 'likes': 15,
                  'description': 'HealthWise Gourmet Coffees use Colombian Arabica Supremo beans exclusively, one of the highest grades of coffee beans available. The company roasts coffee in small batches to ensure quality and consistency. \
                      The TechnoRoasting process eliminates acids and irritants, which helps all who suffer from heartburn or stomach conditions exacerbated by acid.'
                  },
                  'Tieman\'s Fusion Coffee': {'articles': tieman, 'likes': 43,
                  'description': 'Tieman\'s Fusion Decaf is a super rich, full bodied semi-dark roast. Tieman\'s Fusion Decaf is the only Low Acid, Naturally Decaffeinated, Antioxidant Infused Coffee that provides a stomach settling ultra smooth, full bodied flavor. '
                  }
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