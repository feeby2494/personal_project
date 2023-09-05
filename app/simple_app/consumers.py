from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import JsonWebsocketConsumer

from django.template.loader import render_to_string

from datetime import datetime
import time
import threading
from random import randint

class EchoConsumer(WebsocketConsumer):
    
    def connect(self):
        """Event when client connects"""

        # Informs client of successful connection
        self.accept()

        # Send message to client
        self.send(text_data="you are connected by websockets!")

        # Send message to client every second
        def send_time(self):
            while True:
                # send message to client
                self.send(text_data=str(datetime.now().strftime("%H:%M:%S")))
                # sleep for 1 second
                time.sleep(1)
        
        threading.Thread(target=send_time, args=(self,)).start()

    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

    def receive(self, text_data):
        """Event when data is received"""
        pass

class BingoConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

        ## Send numbers to client
        # Generates numbers 5 random numbers
        random_numbers = list(set(
            [randint(1, 10) for _ in range(5)]
            ))
        message = {
            'action': 'New ticket',
            'ticket': random_numbers
        }

        self.send_json(content=message)

        ## Send balls
        def send_ball(self):
            while True:
                # Send message to client
                random_ball = randint(1, 10)
                message = {
                    'action': 'New ball',
                    'ball': random_ball
                }

                self.send_json(content=message)
                # Sleep for 1 second
                time.sleep(1)
        
        threading.Thread(target=send_ball, args=(self,)).start()
    
    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

    def receive_json(self, data):
        """Event when data is received"""
        pass


class BMIConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive_json(self, data):
        height = data['height'] / 100
        weight = data['weight']
        bmi = round(weight / (height ** 2), 1)

        self.send_json(content={
            "action": "BMI result",
            "html": render_to_string(
                "simple_app/components/_bmi_result.html",
                {
                    "height": height,
                    "weight": weight,
                    "bmi": bmi
                }
            )
        })

