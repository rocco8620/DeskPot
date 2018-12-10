# DeskPot
An open implementation of a desktop workstation honeypot to fool/prank colleagues working in the information security industry that wants to take advantage of your juicy unlocked workstation while you are away.

### Installation:

~~~
git clone https://github.com/rocco8620/DeskPot.git
cd DeskPot
virtualenv -p python3 env
pip install -r requirements.txt
~~~

### Usage:

To launch it just run

~~~
$ python3 DeskPot.py
~~~

then within 3 seconds move to a virtual desktop on your machine full with juicy open root terminals and any appealing command panel you can think of.

#### Phase 1

Move away from you chair (take a walk, go to the toilet, take a coffe, etc.) and wait for your coworkers to try to play a joke on you.

When they will try to move your mouse and press keys on your keyboard the honeypot will trigger takeing photo of the intruder and displaying an user configurable message.

If you return to your workstation and nothing happened (nobody tried do do anything), exit the program with the hotkey to avoid triggering the honeypot yourself.

#### Phase 2

After a successfull honeypot activation you will find the raw intrusion data in the folder

~~~
reports/hack_attemp_<date-time>
~~~

To generate a PDF report of the intrusion, with a customizable template run

~~~
$ python3 CreateReport.py reports/hack_attemp_<date-time>
~~~

you will end up with a nice report to show to the collegues!