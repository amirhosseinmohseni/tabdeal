import threading
import time
from locust.env import Environment
from locust.log import setup_logging
from locust.runners import LocalRunner
from locust.stats import stats_printer
from locust import HttpUser, TaskSet, task, between

from locustfile import APIUser1, APIUser2


def run_locust_test(environment, user_count, spawn_rate, run_time):
    """Run the Locust test."""
    runner = LocalRunner(environment)

    runner.start(user_count, spawn_rate)

    start_time = time.time()
    while time.time() - start_time < run_time:
        time.sleep(1)

    runner.stop()

    stats_printer(environment.stats)

    runner.quit()


def locust_thread(user_class, user_count, spawn_rate, run_time):
    """Set up and run Locust in a thread."""
    setup_logging("INFO", None)

    environment = Environment(user_classes=[user_class])

    def on_request(request_type, name, response_time, response_length, exception, context, **kwargs):
        if exception:
            print(f"Request failure: {name}, Exception: {exception}")
        else:
            print(f"Request success: {name}, Response Time: {response_time} ms")

    environment.events.request.add_listener(on_request)

    run_locust_test(environment, user_count, spawn_rate, run_time)


if __name__ == "__main__":
    USER_COUNT = 2
    SPAWN_RATE = 10
    RUN_TIME = 100

    thread1 = threading.Thread(target=locust_thread, args=(APIUser1, USER_COUNT, SPAWN_RATE, RUN_TIME))
    thread2 = threading.Thread(target=locust_thread, args=(APIUser2, USER_COUNT, SPAWN_RATE, RUN_TIME))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("Both Locust tests have completed.")