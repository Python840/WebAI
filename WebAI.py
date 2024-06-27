import tkinter as Tk
from tkinter import filedialog
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

# Local variable for identifiers
identifier_items = ['textarea', 'input[type="text"]', 'input[type="email"]', 'input[type="password"]', 'input[type="search"]', 'input[type="tel"]', 
                    'input[type="url"]']

class App():
    def __init__(self):
        # Keep track of entries count
        self.text_entries = []

        # Button to open file explorer
        self.open_file_exp_button = Tk.Button(bg='Green', text='Open File Browser', fg='white', command=self.OpenFileBrowser)
        self.open_file_exp_button.place(x=15, y=35)

        # Button and URL to search for, displayed later in OpenFileBrowser()
        self.website_to_search_entry = Tk.Entry(fg='#1C39BB', bg='white', width='128')
        self.website_to_search_button = Tk.Button(bg='#FFD700', fg='black', command=self.OpenWebsite, text='Insert URL')

        # Text area part
        # Labels
        self.textareas_label = Tk.Label(text='Amount of different texts to send', bg="#151B54", fg='white')
        self.textareas_label.place(x=600, y=120+15)
        # Enter amount of texts to send (Drop-down List)
        self.textarea_selection = ttk.Combobox(state='readonly', values=[1, 2, 3, 4, 5])
        self.textarea_selection.place(x=600, y=150+15)
        self.textarea_selection.current(0)
        # Button to print the value
        self.print_button = Tk.Button(root, text='Update', command=self.Update)
        self.print_button.place(x=600, y=105)
        # Label for text class
        self.text_class_name = Tk.Label(text='Text Fields', fg='#ADD8E6', bg='#DB737F')
        self.text_class_name.place(x=600, y=175+15)
        # By attribute drop-down menu
        self.by_attribute_selection_combobox = ttk.Combobox(state='readonly', values=['By.ID', 'By.CLASS_NAME', 'By.TAG_NAME', 'By.NAME', 'By.XPATH'])
        self.by_attribute_selection_combobox.place(x=450, y=135)
        self.by_attribute_selection_combobox.current(2)
        # By attribute label
        self.by_attribute_selection_label = Tk.Label(text="By attribute and identifier\n(default recommended)", bg="#151B54", fg='white')
        self.by_attribute_selection_label.place(x=450, y=95)
        # Identifier attribute label (check textarea method)
        # Identifier drop-down selection
        self.identifier_selection_Combobox = ttk.Combobox(state='readonly', values=identifier_items,)
        self.identifier_selection_Combobox.place(x=450, y=160)
        self.identifier_selection_Combobox.current(0)
        # Button for sending text
        self.send_text_button = Tk.Button(text='Send Text', command=self.text_area_send)
        self.send_text_button.place(x=650, y=105)  # Adjust the placement as needed

        # Entry to display which webdriver is selected
        self.input_field_webdriver = Tk.Entry(fg='#FF0000', width='64')
        self.input_field_webdriver.place(x=10, y=10)

    def OpenFileBrowser(self):
        # Open file explorer
        self.file_path = filedialog.askopenfilename()
        # Insert the file desination here
        self.input_field_webdriver.insert(0, self.file_path)

        # Display only after opening a webdriver
        if self.input_field_webdriver.get():
            self.website_to_search_entry.place(x=10, y=75)
            self.website_to_search_entry.insert(0, 'Insert URL in full format, e.g. "https://www.youtube.com/".')
            self.website_to_search_button.place(x=15, y=100)

        self.driver = webdriver.Edge(str(self.input_field_webdriver.get()))

    def OpenWebsite(self):
        self.get_results_website = self.website_to_search_entry.get() # Get the website URL from the given URL in the entry
        self.driver.get(str(self.get_results_website))  # Navigate to the given URL
        time.sleep(1.5)  # Wait for the page to load

    def print_value(self):
        # Get the selected value from the Combobox and print it
        selected_value = self.textarea_selection.get()
        print("Selected value:", selected_value)

        # Check if the selected value is empty
        if not selected_value:
            print("No value selected for textarea amount.")
            return  # Exit the function if no value is selected

        # Destroy all entries if we have less than last time we entered a value
        for entry in self.text_entries:
            entry.destroy()

        # Create and place new entries based on the selected value
        for i in range(int(selected_value)):
            # Entry to select the class name
            self.textarea_class_name = Tk.Entry(fg='black', bg='white')
            y_value = 235 + i * 30  # Adjust 30 to change the spacing
            self.textarea_class_name.place(x=600, y=y_value)
            # Pass amount of entries here
            self.text_entries.append(self.textarea_class_name)
            print("text entries", self.text_entries)

    def text_area(self):
        self.textarea_get_selected_value = self.identifier_selection_Combobox.get()
        self.identifier_label = Tk.Label(fg="#a0d1f7", bg="#0d1117", text=str(self.textarea_get_selected_value), borderwidth=2, relief='raised')
        self.identifier_label.place(x=450, y=180)
        # Map the combobox selection to the appropriate By attribute
        by_mapping = {
            'By.ID': By.ID,
            'By.CLASS_NAME': By.CLASS_NAME,
            'By.TAG_NAME': By.TAG_NAME,
            'By.NAME': By.NAME,
            'By.XPATH': By.XPATH
        }
        # Attributes
        self.by = self.by_attribute_selection_combobox.get()
        self.identifier = self.identifier_label.cget(key='text')
        print("By:", self.by)
        print("Identifier:", self.identifier)

        # Use the map of by
        self.by = by_mapping.get(self.by, By.TAG_NAME)

    def text_area_send(self):
        print("self.text_entry: ", self.textarea_class_name.get())
        # Get the text in each field
        phrases = [entry.get() for entry in self.text_entries]
        print("Phrases", phrases)
        # Search for textarea and send if the condition is met
        if self.textarea_class_name.get():
            text_areas = self.driver.find_elements(self.by, self.identifier)
            for text_area in text_areas:
                random_text = str(random.choice(phrases))
                text_area.send_keys(random_text)
            time.sleep(1)

    # Function to enter the pin and start the feedback process
    def start_feedback(self):
        # Find the pin input box and enter the pin
        pin_box = self.driver.find_element(By.NAME, 'code')
        pin_box.send_keys('')

        # Find and click the start button
        start_button = self.driver.find_element(By.CLASS_NAME, 'submit-button')
        start_button.click()
        time.sleep(1.5)  # Wait for the next page to load

    # Function to fill in the feedback form
    def fill_feedback_form(self):
        # Wait for the feedback form to load
        time.sleep(2)

        # Find any element with class name
        checkboxes = self.driver.find_elements(By.CLASS_NAME, 'btn-primary')
        print(checkboxes)

        # Checkbox iterates through checkboxes
        for checkbox in checkboxes:
            # Button Text gets the text from checkbox
            button_text = checkbox.text
            print(f"checkbox iterator: {checkbox}")
            print(f"checkbox.text: {checkbox.text}")
            if button_text == 'Stimmt' or button_text == 'Sehr zufrieden':
                checkbox.click()
        time.sleep(1)

        # Example: Submit the form (modify based on actual form elements)
        submit_button = self.driver.find_element(By.CLASS_NAME, 'btn-red')  # Replace with actual submit button selector
        submit_button.click()
        time.sleep(1)  # Wait for submission to complete

    def Update(self):
        self.print_value()
        self.text_area()

    # Run the bot multiple times
    def run_bots(self, number_of_bots):
        for _ in range(number_of_bots):
            self.start_feedback()
            self.fill_feedback_form()
            time.sleep(5)  # Random delay between submissions

# Initialize Tkinter window
root = Tk.Tk()
root.configure(bg='#151B54')
root.title("WebAI")
root.minsize(200, 200)
root.maxsize(1920,1080)
root.geometry("800x800+50+50")
icon = Tk.PhotoImage(file="WebAI.png")
root.iconphoto(True, icon)

app = App()

root.mainloop()