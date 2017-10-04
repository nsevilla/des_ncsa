import requests
from bs4 import BeautifulSoup
import os
import random
import string
import re

#opens requests.sessions and inputs in user data for time spent using the get_page_content() function
with requests.session() as ssn:
    usernameinput = input("What is your XConfluence username?")
    passwordinput = input("What is your XConfluence password?")

    payload = {
        'os_username': usernameinput,
        'os_password': passwordinput
    }

    ssn.post('https://opensource.ncsa.illinois.edu/confluence/login.action', data=payload)


#gets the content of the inputted URL's main content, saves it as a file, and additonally saves any linked images as files
#PLEASE NOTE: Changing the location of the saved files is necessary for them to be saved in the correct place!
    def get_page_content():
        #goes to website and creates file based off of HTML tile
        urlinput = "http://" + input("What URL do you want to pull from?(Please do not include http://)")
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1,10)) + ".html"
        page = ssn.get(urlinput)
        soup = BeautifulSoup(page.content,'html.parser')
        newfile = open("/Users/audreykoziol/des_public_new/static/src/" + filename, "w+")

        # function to add content to the beginning of the file
        def line_prepender(file, line):
            with open("/Users/audreykoziol/des_public_new/static/src/" + file, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(line.rstrip('\r\n') + '\n' + content)

        pagecontent = soup.find("div", {"id": "main-content"})
        newfile.write(pagecontent.prettify()[207:-50])

        # saves pictures on the page to seperate files
        picturecontent = soup.findAll("img", {"class": "confluence-embedded-image"})
        for item in picturecontent:
            imagesrc = item['src']
            imageURL = "https://opensource.ncsa.illinois.edu" + imagesrc
            r = ssn.get(imageURL, allow_redirects=True)
            picturesfilename = str(item['data-linked-resource-default-alias'])
            open("/Users/audreykoziol/des_public_new/static/images/" + picturesfilename, 'wb').write(r.content)


            # add page identifiers to end of file
        pageid = input("What  should the dom-module id be? (des-home, des-data, etc.)")
        pageclass=input("What Polymer class should this is labeled as?")
        newfile = open("/Users/audreykoziol/des_public_new/static/src/" + filename, 'a')
        newfile.write("</div> \n </des-card> \n </template> \n <script> class " + pageclass+ " extends Polymer.Element { \n static get is() { return '" +pageid + "'; }\n } "
                            "\nwindow.customElements.define(" +pageclass+".is," + pageclass+" );\n </script>\n</dom-module>")

        #renames file
        #newfilename = str(soup.title.text)[:-15] + ".html"
        #newfilename = re.sub('[/]', '-', newfilename)

        newfilename=pageid+".html"
        os.rename("/Users/audreykoziol/des_public_new/static/src/"+filename, "/Users/audreykoziol/des_public_new/static/src/"+ newfilename)

        #add page identifiers to beginning of file
        line_prepender(newfilename, "<link rel='import' href='../bower_components/polymer/polymer-element.html'>\n <link rel='import' href='../bower_components/mp-slider-master/mp-slider.html'>\n"
                                    "<link rel='import' href='shared-styles.html'> \n <dom-module id='" + pageid + "'> <template> <style include='shared-styles'> \n "
                                    ":host { \n display: block; \n padding: 10px;\n}\n</style>\n<des-card>")

        #adds more pages
        def addanotherpage():
            answer = input("Do you have another page to add? Y/N")
            if answer == "yes" or answer == "Yes" or answer == "y":
                get_page_content()
                return
            if answer == "no" or answer == "No" or answer == "n":
                print("Exiting program")
                ssn.get("https://opensource.ncsa.illinois.edu/confluence/login.action?logout=true")
                return
            else:
                print("Please enter Yes or No")
                addanotherpage()
        addanotherpage()


    get_page_content()


#datasrc = "/Users/audreykoziol/Desktop/DES/des_public/static/images/" + picturesfilename
            #print(item['data-image-src'])
            #open("/Users/audreykoziol/Desktop/DES/des_public/static/elements/des-elements/"+filename, 'w+').write(pagecontent.replace(item['data-image-src'],datasrc))
            #s = open("/Users/audreykoziol/Desktop/DES/des_public/static/elements/des-elements/"+filename).read()
            #z = s.replace(hello1,picturesfilename)

            #open("/Users/audreykoziol/Desktop/DES/des_public/static/elements/des-elements/" + filename).write(z)

        #for item in soup.findAll("img", {"data-image-src": True}):
                #picturecontent = soup.findAll("img", {"class": "confluence-embedded-image"})
                #for item1 in picturecontent:
                    #bleh = item1['src']
                    #bleh['data-image-src'] = picturesfilename
                    #picturesfilename = str(hello['data-linked-resource-default-alias'])
                    #print(picturesfilename)
                    #print(bleh)



            #with open("/Users/audreykoziol/Desktop/DES/des_public/static/elements/des-elements/"+filename) as f:
                #s = f.read()
            #for pictureitem in soup.findAll("img", {"data-image-src": True}):
                #bleh = pictureitem
                #s = s.replace(str(soup.findAll(bleh['data-image-src'])), "/Users/audreykoziol/Desktop/DES/des_public/static/images/'" + picturesfilename + " ' ")
                #with open("/Users/audreykoziol/Desktop/DES/des_public/static/elements/des-elements/"+filename, "w") as f:
                    #f.write(s)