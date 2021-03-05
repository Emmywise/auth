from .test_setup import TestSetUp
from ..models import User

class TestViews(TestSetUp):
    # test to assert that user have to submit the neccessary informations before account get created
    def test_user_cannot_register_with_no_data(self):
        res=self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)
    
    # test that user can is successfully create an account, saver can send us back the email 
    # (that is the information provided during registration are fine are current and accessable from the database)
    def test_user_can_register_successfully(self):
        res=self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(res.data['email'], self.user_data['email'])
        self.assertEqual(res.data['username'], self.user_data['username'])
        self.assertEqual(res.status_code, 201)

    # test to make sure user is authenticated correctly
    # test to make sure a unverified user cannot login 
    def test_user_cannot_login_with_unverified_email(self):
        self.client.post(self.register_url, self.user_data, format="json")
        res=self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)
    
    # test to make sure user can login after account verification
    def test_user_can_login_after_verification(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        email = response.data['email']
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        res=self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 200)



    