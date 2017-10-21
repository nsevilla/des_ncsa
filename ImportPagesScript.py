import requests
from bs4 import BeautifulSoup
import os
import random
import string
from time import sleep

# opens requests.sessions and inputs in user data for time spent using the get_page_content()
# function
with requests.session() as ssn:
    usernameinput = input("What is your XConfluence username?")
    passwordinput = input("What is your XConfluence password?")
    print("If you get an error saying 'AttributeError: 'NoneType' object has no"
          "attribute 'prettify' "
          "after entering the URL for the below prompt, your password or username has"
          "probably been entered wrong. "
          "Please restart the program and enter the correct login credentials.")
    payload = {
        'os_username': usernameinput,
        'os_password': passwordinput
    }

    ssn.post('https://opensource.ncsa.illinois.edu/confluence/login.action', data=payload)

root_dir = "/home/matias/Research/des_public_new/static"
root_folder = "/des_components/des-dr1/"

# gets the content of the inputted URL's main content, saves it as a file,
# and additonally saves any linked images as files
print("PLEASE NOTE: Changing the location of the saved files from"
      "imported pages is necessary for them to be displayed correctly!")


def get_page_content():
    # goes to website and creates file based off of HTML tile
    urlinput = input("What URL do you want to pull from?")
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1, 10))
    filename += ".html"
    page = ssn.get(urlinput)
    soup = BeautifulSoup(page.content, 'html.parser')
    newfile = open(root_dir + root_folder + filename, "w+")

    # function to add content to the beginning of the file
    def line_prepender(file, line):
        with open(root_dir + root_folder + file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)

    pagecontent = soup.find("div", {"id": "main-content"})
    pagecontent = BeautifulSoup(pagecontent.__repr__(), 'html.parser')

    # saves pictures on the page to seperate files
    for item in pagecontent.find_all("img", {"class": "confluence-embedded-image"}):
        list_att = list(item.attrs.keys())
        imagesrc = item['src']
        imageURL = "https://opensource.ncsa.illinois.edu" + imagesrc
        r = ssn.get(imageURL, allow_redirects=True)
        picturesfilename = str(item['data-linked-resource-default-alias'])
        open(root_dir+"/images/" + picturesfilename, 'wb').write(r.content)
        for att in list_att:
            if att not in ['src', 'width', 'height', 'scale']:
                del item[att]
        item['src'] = '/static/images/'+picturesfilename

    # delete classes
    for tag in pagecontent():
        del tag["class"]

    newfile.write(pagecontent.prettify())


    # add page identifiers to end of file
    header = input("What should the heading be? (Title of the des-card)")
    pageid = input("What should the dom-module id be? (des-home, des-data, etc.)")
    pageclass = input("What Polymer class should this is labeled as (desHome)?")
    newfile = open(root_dir + root_folder + filename, 'a')
    endtext = """
    </div>
    </des-card>
    </template>
    <script>
    class {pageclass} extends Polymer.Element {{
      static get is() {{ return '{pageid}'; }}
       }}
     window.customElements.define({pageclass}.is,{pageclass});
     </script>
     </dom-module>
    """.format(pageclass=pageclass, pageid=pageid)
    newfile.write(endtext)

    # renames file
    # newfilename = str(soup.title.text)[:-15] + ".html"
    # newfilename = re.sub('[/]', '-', newfilename)

    newfilename = pageid+".html"
    os.rename(root_dir + root_folder + filename, root_dir + root_folder + newfilename)

    # add page identifiers to beginning of file
    initext = """\
    <dom-module id='{pageid}'>
    <template>
    <style include='shared-styles'>
    :host {{
       display: block;
       padding: 10px;
       }}
    </style>
    <des-card heading="{header}">
    <div class=card-content>
    """.format(pageid=pageid, header=header)
    line_prepender(newfilename, initext)

    # adds more pages
    def addanotherpage():
        answer = input("Do you have another page to add? Y/N")
        if answer == "yes" or answer == "Yes" or answer == "y":
            get_page_content()
            return
        if answer == "no" or answer == "No" or answer == "n":
            print("Please note that locations within imported pages for images and"
                  "other files will need to be changed to reflect the correct corresponding"
                  "location on the user's computer "
                  "(unless the file isn't imported from a local location)")
            sleep(2)
            print("Exiting program")
            ssn.get("https://opensource.ncsa.illinois.edu/confluence/login.action?logout=true")
            return
        else:
            print("Please enter Yes or No")
            addanotherpage()
    addanotherpage()

# Call main function
get_page_content()
