Create a backend service to calculate routes for a small pizza chain that recently purchased one drone to deliver their pizzas. Drone range is 25 miles and must come back to the store for a new battery before it runs out of energy.

The drone will reach out to your backend service to receive its next destination in GPS coordinates. The drone will only request the next destination once it is ready to leave the pizza store, or once it has reached a previously commanded destination and made a delivery.

You may use any programming language you prefer. Your code should be syntactically correct, but it is not required to be functional.


Assumptions
-----------

* Assume the only requirement to come back to the Pizza store is to get new batteries (Infinite Pizza storage capacity).
* Assume the drone has a constant and stable internet connection.
* You cannot send direct commands to the drone, but you may assume that another service exists which will provide you with any information you may need about the drone (example: remaining range, current location, etc).


Expected Functionality
----------------------

* Given a CSV file with order time and delivery address, calculate the optimal path (you are free to define what "optimal path" means to you).
* Provide a HTTP GET endpoint that will send the drone its next destination in GPS coordinates upon request. Remember, the drone will only reach out to your backend service to get the next destination once it has completed its previous destination or when it's ready to leave the pizza store.
* The drone will reach out to your backend service with a set username and password to authenticate itself. Your backend service must authenticate the drone and provide it with a token that it can use to authorize all subsequent requests to your REST API. This token must be validated before providing the drone any data. The token must expire 1 hour after being issued and the drone must request to refresh the token or obtain a new one.

You are welcome to implement any additional functionality you think is important for this scenario.
