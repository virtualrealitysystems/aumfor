-----------------------------------
##AUMFOR (AUTOMATIC MEMORY FORENSIC)
-----------------------------------

##About AUMFOR

AUMFOR is Automated Memory Forensic is GUI based Tool for helping Forensic Investigator by performing all complex and tedious work automatically, it also analyzes and gives final accurate reports about possibilities of use of malware in committing a crime.

AUMFOR is build with Django (Python webframework) and it uses Volatility to perform Memory Forensic. AUMFOR uses VirusTotal for performing Virus Scan feature.

[Django :](https://www.djangoproject.com)

[Volatility :](http://www.volatilityfoundation.org)

[VirusTotal :](https://www.virustotal.com)

-----------------------------------
##Prerequisites

    #For WINDOWS

    install python2.7
    url to download > https://www.python.org/download/releases/2.7/

    Install pip
    Open cmd with administrative privileges and execute following command
    > python -m pip install -U pip

    Microsoft Visual C++ 9.0
    url to download > https://www.microsoft.com/en-in/download/confirmation.aspx?id=44266


    #FOR Linux and Mac OS X

    Linux system and Mac OS system come with prebuilt python check your python version make sure python version must be 2.7

    To check your python version execute following command in terminal
     > $python -V

    Install the pip or Upgrade the pip
    > $pip install -U pip setuptools

    Install python-dev 
    > $sudo apt-get install python-dev

-----------------------------------
##Setup and Run

    1. Create Virtual Environment in your desired location
        > virtualenv aumfor
    2. Activate Virtual Environment
    3. Download source code from Github
        > git clone https://github.com/virtualrealitysystems/aumfor.git
    4. Install requirements from requirements.txt file
        > pip install -r requirements.txt
    5. Migrate database 
        > python manage.py migrate
    6. To enable Virus Scan Feature set VirusTotal API key in settings.py
    7. Open Terminal as Administrator User
    8. Start Django Server and Run AUMFOR as Administrator user
        > python manage.py runserver
    9. Open your browser and type http://localhost:8000 to access AUMFOR

Happy Experiment !

-----------------------------------
##Author
'''
AUMFOR is powered by Virtual Reality Systems
For premium support please contact us at
Email : info@virtualrealitysystems.net
Skype : virtualrealitysystems
Website : http://www.virtualrealitysystems.net '''
-----------------------------------
