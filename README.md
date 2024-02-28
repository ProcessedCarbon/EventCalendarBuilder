# EventCalendarBuilder-FYP

### Set-up
1. Install dependencies using pip install -r requirements.txt
2. Download the NER model from https://drive.google.com/file/d/1zhmh3r5Jmdj-hvMWCRAAvB3GHklJT-3i/view?usp=sharing
3. Extract the folder to PythonFiles/NER/ (Do not change the name if the folder)
4. Start application by running the EventCalendarBuilder.py file

### How-to-use
1.  Start the application
2.  Upon starting the application you are required to give permissions for both Google and Outlook. (Please check your browser tabs)
3.  Do not close these tabs/ browsers, follow through the process of either allowing/ not allowing the permissions.
    1. In the event that you accidently close the browser, open up your task manager and end task for EventCalendarBuilder and restart the application.
    2. If you are running in vscode, simple stop and restart again.
4.  Insert text into text-box and press submit. (This will trigger the algorithm and model to recognise and extract events from the text)
5.  This will bring you to the Schedule Page where each extracted event and their details are displayed in each card.
6.  You can edit these cards and their details to the desired configurations you wish your events to have.
7.  Select which calendar you wish to schedule your event to. (Default Computer calendar, Google, Outlook)
8.  Only the events scheduled to Google/ Outlook will be saved and appear under the Manage Events page.
9.  In the Manage Event page, you can remove already scheduled events individualy or all at once using the 'Clear' button.
10. You may check your corresponding calendars to see if the events are successfully scheduled.
11. You can also instead directly go to the Schedule Page without any text input by clicking on the 'Go To Schedule' button.
12. You are also allowed the creation of new events to schedule under the schedule page by clicking on the 'Create' button.
13. On the left-side you have the app toolbar where you may change the various aspects of the application