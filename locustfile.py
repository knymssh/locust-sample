# -*- coding:utf-8 -*-

# https://docs.locust.io/en/latest/writing-a-locustfile.html#the-locust-class

from locust import HttpLocust, TaskSet, TaskSequence, task, seq_task, events

import sys
import os
sys.path.append(os.getcwd())


class SubTaskSet(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        response = self.client.post(
            "/login", {"username": "ellen_key", "password": "education"})
        print("Response status code:", response.status_code)
        print("Response content:", response.text)

    def logout(self):
        response = self.client.post(
            "/logout", {"username": "ellen_key", "password": "education"})
        print("Response status code:", response.status_code)
        print("Response content:", response.text)

    @task(10)
    def index(self):
        self.client.get("/")

    @task(2)
    def profile(self):
        self.client.get("/profile")

    @task(1)
    def stop(self):
        # 現在のtasksetを終了し、上位tasksetに再度task振り分けを行う
        self.interrupt()


class MyTaskSet(TaskSet):
    tasks = {SubTaskSet:10}

    @task
    def index2(self):
        pass


class MyTaskSequence(TaskSequence):
    @seq_task(1)
    def first_task(self):
        pass

    @seq_task(2)
    def second_task(self):
        pass

    @seq_task(3)
    @task(10)
    def third_task(self):
        pass


class MyLocust(HttpLocust):
    weight = 3
    task_set = MyTaskSet
    # taskの実行間隔はmin_waitとmax_waitの間のランダム値
    min_wait = 5000
    max_wait = 9000

    def setup(self):
        pass
    
    def teardown(self):
        pass


class MyLocust2(HttpLocust):
    weight = 1
    task_set = MyTaskSet


def my_success_handler(request_type, name, response_time, response_length, **kw):
    print("Successfully fetched: %s" % (name))


events.request_success += my_success_handler
