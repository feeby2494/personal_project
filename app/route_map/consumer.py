from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string

from asgiref.sync import async_to_sync

from .models import Brand, Model

import threading

class MapConsumer(JsonWebsocketConsumer):
    room_name = 'broadcast'

    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()

        # Assign the Broadcast group
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

        # Send you all the messages stored in the database.
        # self.send_list_messages()



    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Remove from the Broadcast group
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive_json(self, data_received):
        """
            Event when data is received
            All information will arrive in 2 variables:
            'action', with the action to be taken
            'data', with the information
        """

        
        # Depending on the action we will do one task or another.
        match data_received['action']:

            #### Switch to MAP View ####
            case 'switch to map view':
                component_name = "_map-view"
                threading.Thread(target=self.send_view, args=[component_name]).start()

            #### Switch to LIST View ####
            case 'switch to list view':
                component_name = "_list-view"
                threading.Thread(target=self.send_view, args=[component_name]).start()

            #### Switch to NEW_ORDER View ####
            case 'switch to new order view':
                component_name = "_new-order-view"
                threading.Thread(target=self.send_view, args=[component_name]).start()

            case 'add repair form':
                # will send a partial html template to frontend
                    # front end script will add this to selector id
                        # basically client can add as many repair forms to a work order submit form
                threading.Thread(target=self.add_repair_form, args=[data_received['create_id']]).start()

            case 'get model options for this brand':
                # will send json with all models for the brand selected for populating select form
                threading.Thread(target=self.get_model_opts_for_brand, args=[data_received['value'], data_received['selector'], data_received['data']["submissionId"]]).start()


            case 'add work order':
                # Add new work order for current client
                    # add everything needed to db for new workorder



                # Send new wo to list of orders for this client
                pass
                    #self.send_somthing()
                        # remember that orders will appear on a map for admin/tech/delivery groups
                            # only current client's orders will show on their map

            case 'add repair to work order':
                # Send repair to current new work order for customer
                    # either the front end will give backend wo id
                        # or we can filter by client, and retrieve latest id for wo

                # update list of repairs on orders for client
                #self.send_somthing()
                    # remember that orders with newly added repairs will appear on a map for admin/tech/delivery groups
                       # only current client's orders/repairs will show on their map
                pass

            #### Work Order Submit Form ####

            case 'submit order and repairs':
                print(data_received)
                pass
            

            case 'remove new repair form':
                # will remove that one specific form or just repalce with blank html
                pass

            #### Show Data Points on Frontend's Map ####
                # Remember these will not be send html!
                    # These send json with the info needed to map them on the map!
                    # Admin/tech/driver see all 'not finished' workorders on map
                        # Order that need pickup
                        # Shipping Order that need's dropping off
                    # Client see only their orders/repairs and where they are and their status!
                        # this adds accountablity to us, and comunicates clearly with customer
                            # Everyone loves maps!
                    
            # will add all points to map depending on given criteir that will be used for
            # SQL quaries
            case 'add points to map':
                pass

            # For now I want this dead simple,
                # Everytime client hits that submit button (reloading page will get all points),
                # app point will be cleared from map using front end script method,
                # and the 'add points to map' along with args will be sent to server,
                # server sends points from its SQL query  

            # case 'remove points from map':
            #     pass

            # Don't even need this, a script on front end will deleted all points, BOOM!
            # case 'clear map':
            #     pass

                


            ######### THIS IS ALL FOR NOW, ADD WO, ADD REPAIRS, THE FORM
            #   THEN THE MAP, GET POINTS FROM DB    

    # Need to send json back to front end and it's script will add these to openlayer's
    # map object




    # will send html partial template
    def send_html(self, event):
        """Event: Send html to client"""
        data = {
            'selector': event['selector'],
            'action': event['action'],
            'html': event['html'],
        }
        self.send_json(data)

    

    def send_view(self, component_name):
        """Send view to client"""


        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'send.html', # Run send_html()
            'selector': 'view',
            'action': 'switch view',
            'html': render_to_string(f"route_map/components/{component_name}.html")
        })

    def add_repair_form(self, id):
        """Send repair form partial to to client"""

        """Send json with brands to client"""
        brands = Brand.objects.all()

        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'send.html', # Run send_html()
            'selector': 'new-repair-form',
            'action': 'added repair form',
            'html': render_to_string(f"route_map/components/_repair-form.html", {'id': id, 'brands': brands})
        })

    def get_model_opts_for_brand(self, value, selector, submission_id):
        """Send repair form partial to to client"""

        """Send json with brands to client"""
        models = Model.objects.filter(brand__name=value)

        # Render HTML and send to client
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            'type': 'send.html', # Run send_html()
            'selector': f"model-select-{submission_id}",
            'action': 'send model options',
            'html': render_to_string(f"route_map/components/_model-form.html", {'selector': selector, 'models': models, 'submission_id': submission_id})
        })
    
    

    # def send_list_messages(self):
    #     """Send list of messages to client"""
    #     # Filter messages to the client
    #     messages = Message.objects.order_by('-created_at')

    #     # Render HTML and send to client
    #     async_to_sync(self.channel_layer.group_send)(self.room_name, {
    #         'type': 'send.html', # Run send_html()
    #         'selector': '#message__list',
    #         'html': render_to_string('social/components/_list-messages.html', {'messages': messages})
    #     })

