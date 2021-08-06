from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse

from coffquiz.models import Coffee, Article
from django.contrib.auth.models import User

# Model test
# make sure the number of views for coffee is positve
class CoffeeMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        '''
        Ensures the number of views received for a Coffee are positive or zero
        '''
        u = User.objects.get_or_create(username='test')[0]
        u.save()
        coffee = Coffee(user=u, name='test', description='test', views=-1)
        coffee.save()

        self.assertEqual((coffee.views >= 0),True)


    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        """
        u = User.objects.get_or_create(username='test')[0]
        u.save()
        coffee = Coffee(user=u, name='Random Coffee String')
        coffee.save()

        self.assertEqual(coffee.slug,'random-coffee-string')

# this function is for test the add coffee
def add_coffee(user, name,views=0,likes=0):
    coffee = Coffee.objects.get_or_create(user=user, name=name)[0]
    coffee.views = views
    coffee.likes = likes

    coffee.save()
    return coffee

# View test
class IndexViewTests(TestCase):
    def test_index_view_with_no_coffee(self):
        '''
        If no coffeelist exist, the appropriate message should be displayed
        '''

        response = self.client.get(reverse('coffquiz:index'))

        self.assertEqual(response.status_code,200)
        self.assertContains(response,'There are no coffee list present.')
        self.assertQuerysetEqual(response.context['coffeelist'],[])

    def test_index_view_with_coffeelist(self):
        """
        Checks whether coffeelist are displayed correctly when present
        """
        u = User.objects.get_or_create(username='test')[0]
        u.save()
        add_coffee(u, 'Java', 1, 1)
        add_coffee(u, 'latte', 1, 1)
        add_coffee(u, 'black coffee', 1, 1)

        response = self.client.get(reverse('coffquiz:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Java")
        self.assertContains(response,"latte")
        self.assertContains(response,"black coffee")

        num_coffee = len(response.context['coffeelist'])
        self.assertEquals(num_coffee,3)