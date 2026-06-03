from django.test import TestCase, Client
from .models import Product
from django.contrib.auth.models import User

class ProductViewTest(TestCase):
    def test_product_str_returns_name(self):
        product = Product.objects.create(name='produktNR1', quantity=3)
        self.assertEqual(str(product), 'produktNR1')
        self.assertEqual(product.quantity, 3)


class ProductFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
    def test_product_list_redirects_when_not_logged_in(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 302)

    def test_product_list_accessible_when_logged_in(self):
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_add_product_creates_record(self):
        self.client.login(username='testuser', password='testpassword123')
        self.client.post('/products/add-product/', {
            'name': 'new product',
            'quantity': '3'
        })
        self.assertEqual(Product.objects.count(), 1)

# Trzy podstawowe elementy:
# class ProductModelTest(TestCase):
#     def test_coś(self):
#         # arrange — przygotuj dane
#         # act — wykonaj akcję
#         # assert — sprawdź wynik
#         self.assertEqual(wynik, oczekiwany)


# Prosty — test modelu:
# from .models import Product

# class ProductModelTest(TestCase):
#     def test_product_str_returns_name(self):
#         product = Product.objects.create(name='Śrubka M8', quantity=100)
#         self.assertEqual(str(product), 'Śrubka M8')

# Średni — test widoku:
# from django.test import TestCase, Client
# from django.contrib.auth.models import User

# class ProductListViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             username='testuser',
#             password='testpass123'
#         )
    
#     def test_product_list_requires_login(self):
#         response = self.client.get('/products/')
#         self.assertEqual(response.status_code, 302)  # redirect do logowania
    
#     def test_product_list_accessible_when_logged_in(self):
#         self.client.login(username='testuser', password='testpass123')
#         response = self.client.get('/products/')
#         self.assertEqual(response.status_code, 200)

# Trudniejszy — test formularza:
# def test_add_product_saves_to_database(self):
#     self.client.login(username='testuser', password='testpass123')
#     response = self.client.post('/products/add-product/', {
#         'name': 'Nowy produkt',
#         'quantity': '50'
#     })
#     self.assertEqual(response.status_code, 302)
#     self.assertEqual(Product.objects.count(), 1)
#     self.assertEqual(Product.objects.first().name, 'nowy produkt')