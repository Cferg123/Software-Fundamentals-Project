# All libraries imported at the beginning of code in accordance with structuring conventions
import csv
import time, os, string
import requests
from tkinter import *

#function for when submit button is pressed
def click():
    nameQuery = textentry.get()#gets user input
    output.delete(0.0, END)


    #open file for reading
    with open('RawData.csv', 'r', encoding='utf-8') as rawCSV: #opens existing file for reading        
        csvreader = csv.reader(rawCSV, delimiter='|')
        #return result
            #lists of headings for each type of card
        fieldListMonster = ['ID:', 'Name:', 'Card Type:', 'Desc:', 'ATK:', 'DEF:', 'Level:', 'Monster Type:', 'Attribute:']
        fieldListSpell = ['ID:', 'Name:', 'Card Type:', 'Desc:', 'Spell Type:']
        fieldListTrap = ['ID:', 'Name:', 'Card Type:', 'Desc:', 'Trap Type:']
            
        for row in csvreader:
            if len(row) == 0: #some of the rows in the API are empty, this skips over them
                continue
            if nameQuery.lower().translate(str.maketrans('', '', string.punctuation)).replace(" ", "") in row[1].lower().translate(str.maketrans('', '', string.punctuation)).replace(" ", ""): #ignores case, space and punctuation
                num = 5 #total number of fields for spells/traps
                if 'Monster' in row[2]:
                    num = 9 #total number of fields for monsters
                    

                #prints each field of data depending on card type
                for x in range(0, num):
                    if row[2] == 'Spell Card':
                        output.insert(INSERT, "{} {}\n".format(fieldListSpell[x], row[x]))
                    elif row[2] == 'Trap Card':
                        output.insert(INSERT, "{} {}\n".format(fieldListTrap[x], row[x]))
                    else:
                        output.insert(INSERT, "{} {}\n".format(fieldListMonster[x], row[x]))
                output.insert(INSERT, "\n")


# Reqeusting data from API
print('retrieving card data...')

try: #connects to API, times out after 5 secs if no response
    req = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php', timeout=5)

    connection_successful = True

    cardData = req.json()['data'] #stores json data in variable and gets rid of unnecessary dictionary


    # open a file for writing and reading, write and query the file
        #section for writing to CSV file starts here
    with open('RawData.csv', 'w+', encoding='utf-8') as rawCSV: #creates file for writing, overwrites if file already exists
        csvwriter = csv.writer(rawCSV, delimiter='|')
        count = 0
        for item in cardData: # for loop writes the card data from the parsed API data into the CSV file
            item.pop('card_sets', None)
            item.pop('card_images', None)# remove less useful/region-specific data, like prices
            item.pop('card_prices', None)
            if count == 0: # if statement adds the keys of the item as headings for the first line in the CSV file
                fields = item.keys()
                csvwriter.writerow(fields) # writes the fields array into the first row of the CSV file
                count += 1 # increments count by 1 so that count =/= 0
            csvwriter.writerow(item.values())

#runs if there is no network connection
except (requests.ConnectionError, requests.Timeout) as exception:
    connection_successful = False
    print("No internet connection. Looking for existing csv file on disc...") #looks for file in same folder as program
          
    if os.path.exists('RawData.csv') == False: #if no internet connection, looks for existing file on same folder
        print('Unable to retrieve card data. Please check your internet connection and try again.')
        time.sleep(5) #give the user 15 secs to read the message, automatically closes and ends the code after
        quit()


#GUI
window = Tk()
window.title('Yu-Gi-Oh! Card Finder - Last Updated {}'.format(time.ctime(os.path.getmtime('RawData.csv'))))
window.configure(background='black')

#First label and textbox
Label (window, text='Please enter the name of the card you want to find:\n', bg='black', fg='white', font='none 10 bold') .grid(row=0, column=0, sticky=W)

textentry = Entry(window, width=50, bg='white') #user input
textentry.grid(row=1, column=0, sticky=W)

#Submit button
Button(window, text='SUBMIT', width=6, command=click) .grid(row=2, column=0, sticky=W)

#Second label and output textbox
Label (window, text='\nCard Data:\n', bg='black', fg='white', font='none 10 bold') .grid(row=3, column=0, sticky=W)

output = Text(window, width=75, height=10, wrap=WORD, background='white',)
output.grid(row=4, column=0, columnspan=3, sticky=W)
window.mainloop()
