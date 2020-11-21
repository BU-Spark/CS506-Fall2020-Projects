# CS506 Fall 2020 Final Projects--- vibons_journey_app_team1
Journey App, designed by Vibons, is a motivational app for users to easily jot down their daily ideas, write down their daily emotions and receive educational articles about customized topics through notifications. Nevertheless, as every user can be inundated with so many app notifications, our client wants to find an optimal time to notify the users of the contents and inspire them to read.

In a nutshell, our goal is to find the send time optimization for each user of the Journey App, based on the dataset given by our clients. Send time optimization analyzes when is the most likely time for each recipient to open the notifications. Such an analysis can boost the open rates for our client and enhance engagement with all the users. More information about the “send time optimization” can be found here: https://blog.robly.com/the-science-behind-send-time-optimization/.


## Data souces
  - https://s3-spaced-learning-prod.s3.amazonaws.com/raw_data.xlsx
  
 
### Data Representation
  1. Info Customer ID - The ID number of the users' company, there are about 20 company IDs in total.
  2. User Id - Each user’s Id on behalf of which notifications are sent.
  3. User-Created At - The first date of hire of the user to whom notification is sent.
  4. Activation Date - Date and time when a notification is sent.
  5. Activity Date - Date and time when a notification is opened by the receiving user.
  6. Name - The title of the notification content.
  7. Content ID - the ID of the notification content name.
  8. Content Type - The type of notification content.
  9. Journey Name - The journey that the content of the notification comes from.
  10. Action - Percentage of content read by the end user. 
  11. Device - The device used by the user to read the notification. Due to the current universality and convenience of mobile phones, the focus is on mobile phone users.
  12. Channel - The channel that users click on the notification.
  13. Session Id: When a notification is sent to the user, a session is locked in the system.



