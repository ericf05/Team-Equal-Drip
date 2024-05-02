# INFO-490-Capstone
Green Guard focuses on automating the process of watering indoor plants. This system would help people who travel a lot and/or don't water their plants often enough for a variety of reasons. Our preliminary idea is to use a Raspberry Pi with valve hoses and moisture sensors for the soil. We hope to be able to use a container to pump water out of, making the users' only job to fill the water level for our Automator to use.

Beyond watering, the system could also include sensors to monitor plant health indicators such as light exposure and temperature, helping to provide a comprehensive care system for indoor plants. Over time, Green Guard can learn the watering patterns and requirements of different plants, fully optimizing the needs of each plant. Machine learning algorithms can extract watering levels, light levels, and temperature.

The Green Guards system can be controlled and monitored remotely via a smartphone app. This is especially useful for travelers, allowing them to manage their plant care routine from anywhere in the world, ensuring their plants are well-cared for even in their absence.

A community feature allows users to share tips, seek advice on plant care, and share their plant growth stories with other plant enthusiasts. This could foster a community of users who are passionate about plant care, especially those who travel frequently.

The app can also include a knowledge base with information on different types of plants, their specific care requirements, and tips for indoor gardening. This is especially useful for beginners or those looking to expand their indoor garden.

# Continuations
For those that want to continue working on this project, you will need to create a MongoDB account and change the necessary code in sensor_loop.py. Depending on what sensors you choose for a Raspberry Pi, the code for each sensor might need to be altered when connecting via GPIO pins.

We wanted to expand this project to connect to a water tank, and use a solenoid valve to autowater the plant according to the moisture percentage. Another idea we had was to use ESP32's connected physically to the sensors and then connect wirelessly to the Pi, allowings us to host multiple plant systems on a single Raspberry Pi.

Presentation Deck: https://docs.google.com/presentation/d/1f9j_4MfCJcArVAB2oSXKxE-scNMGOCwLVW0Y8tIulVQ/edit#slide=id.p 
