from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse

from coffquiz.models import Coffee, Article

# Model test
# make sure the number of views for coffee is positve
class CoffeeMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        '''
        Ensures the number of views received for a Coffee are positive or zero
        '''
        coffee = Coffee(title='test',description='test',views=0,likes=0)
        coffee.save()

        self.assertEqual((coffee.views >= 0),True)


    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        """
        coffee = Coffee(name='Random Coffee String')
        coffee.save()

        self.assertEqual(coffee.slug,'random-category-string')

# this function is for test the add coffee
def add_coffee(name,views=0,likes=0):
    coffee = Coffee.objects.get_or_create(name=name)[0]
    coffee.views = views
    coffee.likes = likes

    coffee.save()
    return coffee

class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        '''
        If no categories exist, the appropriate message should be displayed
        '''

        response = self.client.get(reverse('coffquiz:index'))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'],[])

    def test_index_view_with_coffeelist(self):
        """
        Checks whether categories are displayed correctly when present
        """
        add_coffee('Java',1,1)
        add_coffee('latte',1,1)
        add_coffee('black coffee',1,1)

        response = self.client.get(reverse('coffquiz:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Java")
        self.assertContains(response,"latta")
        self.assertContains(response,"black coffee")

        num_coffee = len(response.context['coffeelist'])
        self.assertEquals(num_coffee,3)





