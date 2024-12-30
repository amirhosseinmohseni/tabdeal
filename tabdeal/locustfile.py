from locust import HttpUser, TaskSet, task, between
import rstr
import random

pattern = r"/^0(9)\d{9}$/"

NUM_CUSTOMERS = 10
NUM_CUSTOMER_CHARGES = 100
NUM_SELF_CHARGES = 10

USER_CREDENTIALS = [
    {"phone_number": "09128302694", "password": "1708"},
    {"phone_number": "09122190492", "password": "1708"},
]

CUSTOMERS = []


class BaseUserTasks(TaskSet):
    def on_start(self):
        global CUSTOMERS
        
        if not CUSTOMERS:
            self.register_customer()
        self.login_user()

    def register_customer(self):
        for i in range(NUM_CUSTOMERS):
            phone_number = str(rstr.xeger(pattern)[1:-1])
            # print(f"{phone_number}")
            response = self.client.post("/api/users/register_customer/", json={
                "phone_number": phone_number
            })
            if response.status_code == 201:
                print(f"Customer registered with phone number: {phone_number}")
                CUSTOMERS.append({"phone_number": phone_number})
            else:
                print(f"Registration failed: {response.status_code} {response.text}")

    def login_user(self):
        # print(self.seller)
        response = self.client.post("/api/users/login_seller/", json={
            "phone_number": self.user.user_data["phone_number"],
            "password": self.user.user_data["password"]
        })
        if response.status_code == 200:
            self.user.user_data["token"] = response.json()["access"]
            print(f"Seller logged in with phone number: {self.user.user_data["phone_number"]}")
        else:
            print(f"Login failed: {response.status_code} {response.text}")

    @task(NUM_CUSTOMER_CHARGES)
    def charge_customer_wallet(self):
        customer = random.choice(CUSTOMERS)
        amount = random.randint(10, 100)
        headers = {"Authorization": f"Bearer {self.user.user_data["token"]}"}
        response = self.client.post("/api/transactions/charge-customer-wallet/", json={
            "phone_number": customer["phone_number"],
            "amount": amount
        }, headers=headers)
        if response.status_code == 201:
            print(f"{customer["phone_number"]} wallet charged by {self.user.user_data['phone_number']} with amount: {amount}")
        else:
            print(f"charge_customer_wallet failed: {response.status_code} {response.text}")

    @task(NUM_SELF_CHARGES)
    def charge_wallet(self):
        amount = random.randint(10, 100)
        headers = {"Authorization": f"Bearer {self.user.user_data["token"]}"}
        response = self.client.post("/api/transactions/charge-wallet/", json={
            "amount": amount
        }, headers=headers)
        if response.status_code == 201:
            print(f"seller {self.user.user_data["phone_number"]} wallet charged with amount: {amount}")
        else:
            print(f"charge_wallet failed: {response.status_code} {response.text}")

class APIUser1(HttpUser):
    tasks = [BaseUserTasks]
    wait_time = between(1, 2)
    host = "http://127.0.0.1:9100"
    user_data = USER_CREDENTIALS[0]
    
class APIUser2(HttpUser):
    tasks = [BaseUserTasks]
    wait_time = between(1, 2)
    host = "http://127.0.0.1:9100"
    user_data = USER_CREDENTIALS[1]