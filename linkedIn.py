import time,math,random,os
import utils,constants,config
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from utils import prRed,prYellow,prGreen
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import re
import openai
from openai import OpenAI
from dotenv import load_dotenv

options = Options()

# Use a raw string for the path or replace backslashes with forward slashes
#webdriver_path = r"C:\chromedriver.exe"

openai.api_key = os.getenv('OPENAI_API_KEY')
# Create a Service object and pass it to the WebDriver
service = Service(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=service, options=options)

summary_of_experience = "7 years in Information Technology overall. 6 years of experience with Test automation, manual tesing, performance testing, jmeter, selenium webdriver, python programming language, pytest, Postman, Jenkins, DevOps, Jira, white box, SQL, agile methodologies, robot framework, Confluence, testrail, data base, test cases, Testrail, test scenarios, scrum, user acceptance testing, git, continuous integration, qa/qc, Linux, REST API, unit testing, azure boards, Microsoft azure, healfcare domain. 5 years of selenium, appium, chrome dev tool, ISTQB, Mobile testing, Charles Proxy, iOS. 3 years managing QA team, Salesforce, AWS, C#, Cypress, surpervising QA team. 2 years of etl testing, javascript, customer service experience. Salary: $135,000/year which equal $65/hr. I heard about this job from LinkedIn. Not comfortable commuting to job location."
summary_radio_questions = "yes for drug test, background check, US Citizen. no for sponsorship, I will never require sponsoreship, I'm US Citizen."
summary_select_questions = "profectional english, yes for full time, contract, part time. US citizen, Do not required sponsorship."
file_path = 'cleaned_book.txt'
class Linkedin:
    def __init__(self):
        
            #prYellow("🌐 Bot will run in Chrome browser and log in Linkedin for you.")
            #self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=utils.chromeBrowserOptions())
            options.add_argument(r"--user-data-dir=C:\Users\DELL\AppData\Local\Google\Chrome\User Data")
            options.add_argument(r'--profile-directory=Profile 1')
            #options.add_argument(r'--profile-directory=Profile')
            #options.add_argument('--headless')
            options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(service=service, options=options)

    
    def generateUrls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try: 
            with open('data/urlData.txt', 'w',encoding="utf-8" ) as file:
                linkedinJobLinks = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedinJobLinks:
                    file.write(url+ "\n")
            prGreen("✅ Urls are created successfully, now the bot will visit those urls.")
        except:
            prRed("❌ Couldn't generate url, make sure you have /data folder and modified config.py file for your preferances.")

    # Read the Clean Text from File
    def read_clean_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    # Partition Text by Chapters
    def partition_text_by_chapters(self, text):
        # Regular expression to identify chapter and subchapter headings
        # This pattern looks for sequences of numbers separated by dots,
        # possibly followed by additional characters (e.g., "3.1 Forms of ML")
        chapter_pattern = re.compile(r'\n\d+(\.\d+)*\s+[A-Za-z]')
        
        # Use the regular expression to find all matches; add start and end indices
        chapters_starts = [match.start() for match in chapter_pattern.finditer(text)]
        chapters_starts.append(len(text))  # Add the end of the text to close the last segment
        
        # Extract segments based on the indices
        segments = [text[chapters_starts[i]:chapters_starts[i + 1]].strip() for i in range(len(chapters_starts) - 1)]
        
        return segments

    def remove_non_bmp_characters(self, text):

        """Remove non-BMP characters from a string."""
        return ''.join(char for char in text if ord(char) <= 0xFFFF)

    def linkJobApply(self):
        self.generateUrls()
        countApplied = 0
        countJobs = 0

        urlData = utils.getUrlDataFile()

        for url in urlData:        
            self.driver.get(url)

            # JavaScript code to find the home button and click it
            homeButton = """
            var linkElement = document.querySelector('a[data-test-app-aware-link]');
            if (linkElement) {
                linkElement.click();
            } else {
                console.log('Element not found');
            }
            """
            self.driver.execute_script(homeButton)
            time.sleep(5)

        # click the button to post on LinkedIn
        self.driver.find_element(By.XPATH,"//button[contains(@class, 'artdeco-button') and contains(@class, 'share-box-feed-entry__trigger')]").click()
        time.sleep(5)

        # Example usage
        file_path = 'cleaned_book.txt'
        clean_text = self.read_clean_text(file_path)
        segments = self.partition_text_by_chapters(clean_text)

        # To randomly select a segment
        selected_segment = random.choice(segments)
        print(f"Selected Segment:\n{selected_segment}")

        hashtag = "#chatgpt, #ai, #education, #learning, #career, #softwaretesting, #qualityassurance"
        bookExcerpt = selected_segment
        print("The segment from the book I am sending gpt is:")
        print(bookExcerpt)
        #prompt = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise and engaging LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. The post should be informative, demonstrate thought leadership, and engage my network in a discussion on the future of AI testing. let it be 50 words or less. Choose 3 hashtags from this: {hashtag}."
        #prompt = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. The post should be informative. let it be 50 words or less. Choose 3 hashtags from this: {hashtag}."
        prompt = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise LinkedIn post that is informative. let it be 50 words or less. Choose 3 hashtags from this: {hashtag}."
        gpt_response = self.get_gpt_response(prompt)
        time.sleep(2)
        # Clean the GPT response before sending it
        clean_gpt_response = self.remove_non_bmp_characters(gpt_response)
        time.sleep(random.uniform(1, constants.botSpeed))
        
        # Find the content-editable element (ql-editor) within the Quill container
        editor = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ql-editor') and @contenteditable='true']")

        # Use send_keys to input text
        editor.send_keys(clean_gpt_response)
        time.sleep(5)
        print("I just sent the gpt response to the linkedin post editor")
        print("I am about to click the post button")

        time.sleep(25)
        # Click the post button
        # Define your XPath
        xpath = "//button[contains(@class, 'share-actions__primary-action') and contains(@class, 'ember-view')]"
        #self.driver.find_element(By.XPATH,"//button[contains(@class, 'share-actions__primary-action') and contains(@class, 'ember-view')]").click()

        # JavaScript to find and click the element
        js_click_script = f"""
        var xpath = "{xpath}";
        var button = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (button) button.click();
        """
        print("I am here")
        # Execute the script
        self.driver.execute_script(js_click_script)
        print("I clicked the post button")
        print("I am waiting for 20 seconds")

        time.sleep(20)
        # Post in groups if it asks for
        try:
            # Click on post in group button
            xpathPostInGroup = "//a[contains(@class, 'app-aware-link') and contains(@class, 'artdeco-button--primary')]"
            # JavaScript to find and click the element
            js_click_script = f"""
            var xpath = "{xpathPostInGroup}";
            var button = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (button) button.click();
            """
            # Execute the script
            self.driver.execute_script(js_click_script)
            print("I clicked the post in group button")
            time.sleep(8)

            # now post in the group
            xpathPostGroup = "//a[contains(@class, 'share-actions__primary-action') and contains(@class, 'ember-view')]"

            # JavaScript to find and click the element
            js_click_script = f"""
            var xpath = "{xpathPostGroup}";
            var button = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (button) button.click();
            """
            print("I am here")
            # Execute the script
            self.driver.execute_script(js_click_script)
            print("I just post in a group")
        except:
            print("I could not post in a group as it was not prompted")

        #element = self.driver.find_element(By.XPATH, "//div[@class='ql-clipboard']")
        #self.driver.execute_script("arguments[0].click();", element)
        #self.driver.find_element(By.XPATH,"//div[@class='ql-clipboard']").click()

        time.sleep(30)

        

    """def chooseResume(self):
        try: 
            beSureIncludeResumeTxt = self.driver.find_element(By.CLASS_NAME, "jobs-document-upload__title--is-required")
            if(beSureIncludeResumeTxt.text == "Be sure to include an updated resume"):
                resumes = self.driver.find_elements(By.CSS_SELECTOR,"button[aria-label='Choose Resume']")
                if(len(resumes) == 1):
                    resumes[0].click()
                elif(len(resumes)>1):
                    resumes[config.preferredCv-1].click()
                else:
                    prRed("❌ No resume has been selected please add at least one resume to your Linkedin account.")
        except:
            pass"""

    """def getJobProperties(self, count):
        textToWrite = ""
        jobTitle = ""
        jobCompany = ""
        jobLocation = ""
        jobWOrkPlace = ""
        jobPostedDate = ""
        jobApplications = ""

        try:
            jobTitle = self.driver.find_element(By.XPATH,"//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            #res = [blItem for blItem in config.blackListTitles if(blItem.lower() in jobTitle.lower())]
            want = [blItem for blItem in config.desired_words if(blItem.lower() in jobTitle.lower())]
            #if (len(res)>0):
                #jobTitle += "(blacklisted title: "+ ' '.join(res)+ ")"
            if (len(want)==0):
                jobTitle += "(blacklisted title: "+ ' '.join(want)+ ")"
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobTitle: " +str(e)[0:50])
            jobTitle = ""

        try:
            jobCompany = self.driver.find_element(By.XPATH,"//main/div/div[1]/div/div[1]/div/div/div[1]/div[2]/div/a").get_attribute("innerHTML").strip()
            res = [blItem for blItem in config.blacklistCompanies if(blItem.lower() in jobCompany.lower())]
            if (len(res)>0):
                jobCompany += "(blacklisted company: "+ ' '.join(res)+ ")"
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobCompany: " +str(e)[0:50])
            jobCompany = ""
            
        try:
            jobLocation = self.driver.find_element(By.XPATH,"//span[contains(@class, 'bullet')]").get_attribute("innerHTML").strip()
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobLocation: " +str(e)[0:50])
            jobLocation = ""

        try:
            jobWOrkPlace = self.driver.find_element(By.XPATH,"//span[contains(@class, 'workplace-type')]").get_attribute("innerHTML").strip()
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobWorkPlace: " +str(e)[0:50])
            jobWOrkPlace = ""

        try:
            jobPostedDate = self.driver.find_element(By.XPATH,"//span[contains(@class, 'posted-date')]").get_attribute("innerHTML").strip()
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobPostedDate: " +str(e)[0:50])
            jobPostedDate = ""

        try:
            jobApplications= self.driver.find_element(By.XPATH,"//span[contains(@class, 'applicant-count')]").get_attribute("innerHTML").strip()
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobApplications: " +str(e)[0:50])
            jobApplications = ""

        textToWrite = str(count)+ " | " +jobTitle+  " | " +jobCompany+  " | "  +jobLocation+ " | "  +jobWOrkPlace+ " | " +jobPostedDate+ " | " +jobApplications
        return textToWrite"""
    
    """def getXpathEasyApplyButton(self):
        easyApplyButtonXpath = ""
        jobTitlestp = ""
        jobCompanystp = ""

        try:
            jobTitle = self.driver.find_element(By.XPATH,"//h1[contains(@class, 'job-title')]").get_attribute("innerHTML").strip()
            jobTitlestp = jobTitle.strip('<!---->').strip()
            print("I'm here")
            print("I got the job title: ")
            print(jobTitlestp)
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobTitle: " +str(e)[0:50])

        try:
            print("I am in the try block to get the job company")
            jobCompany = self.driver.find_element(By.CSS_SELECTOR,"div[class='job-details-jobs-unified-top-card__primary-description-without-tagline mb2'] a[class='app-aware-link ']").get_attribute("innerHTML").strip()
            print("I got the job company: ")
            print(jobCompany)
            jobCompanystp = jobCompany.strip('<!---->').strip()
            print("I got the job company: ")
            print(jobCompanystp)
        except Exception as e:
            if(config.displayWarnings):
                prYellow("⚠️ Warning in getting jobCompany: " +str(e)[0:50])
        

        easyApplyButtonXpath = f"//button[@aria-label='Easy Apply to {jobTitlestp} at {jobCompanystp}']"
        print("Here is the xpath for the easy apply button: ")
        print(easyApplyButtonXpath)
        return easyApplyButtonXpath"""


    '''def easyApplyButton(self, buttonXpath):
        try:
            time.sleep(random.uniform(1, constants.botSpeed))
            button = self.driver.find_element(By.XPATH, f'{buttonXpath}')
                #"{buttonXpath}") #//button[@id='ember64']//span[contains(@class,'artdeco-button__text')][normalize-space()='Easy Apply']    /html[1]/body[1]/div[5]/div[3]/div[2]/div[1]/div[1]/main[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/button[1]
            print("I am trying to find the easy apply button")
            button = self.driver.find_element(By.CSS_SELECTOR,
                "button[id='ember60'] span[class='artdeco-button__text']")
            print("I found the easy apply button")
            print("I am printing the button type")
            print(type(button))
            print("I am printing the button text")
            print(button.text)
            print("code line 236")
            EasyApplyButton = button
        except: 
            EasyApplyButton = False

        return EasyApplyButton'''

    """def applyProcess(self, percentage, offerPage):
        applyPages = math.floor(100 / percentage) 
        result = ""  
        try:
            for pages in range(applyPages-2):
                # Check and fill empty fields on the continue page and fill them with gpt response
                # Input text field
                try:
                    input_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']:not(.search-global-typeahead__input)")
                    for field in input_fields:
                        value = field.get_attribute('value')
                        if not value:  # If the field is empty
                            outer_html = field.get_attribute('outerHTML')
                            field_id = field.get_attribute('id')  # Get the id of the input field
                            print("I got the field id: ")
                            print(field_id)
                            if field_id:
                                label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{field_id}']")
                                question = label.text
                                print("I just retrieve the following question continue page: ")
                                print(question)
                            print("I got the outerHTML of the input field continue page")
                            print(outer_html)

                            # Send the question text related to this field to GPT for answer generation
                            if question:
                                time.sleep(random.uniform(1, constants.botSpeed))
                                #prompt = f"Given the profile summary: '{summary_of_experience}', answer the following: '{question}' as a single digit. Just send the digit, as I am sending it directly to a variable for automation. send 0 when there is no answer."
                                prompt = f"Given the profile summary: '{summary_of_experience}', answer the following: '{question}' as a single digit. Just send the digit, as I am sending it directly to a variable for automation. send 1 when there is no answer. Send in this format: '6', Do not send in the following format: 'Given the information provided, the number of years of work experience with python is 6'."
                                response = self.get_gpt_response(prompt)
                                print("Here is the response from GPT in the if block: ")
                                print(response)

                            # Send outerHTML to GPT for XPath generation
                            time.sleep(random.uniform(1, constants.botSpeed))
                            print("I am sending the outerHTML to GPT for XPath generation continue page")
                            xpath_prompt = f"Given this outerHTML element: '{outer_html}', Send me the Xpath locator. (do not teach me how to write a Xpath) Just send me a single xpath without comment. Just One single Xpath. I am sending it to a variable for automation. Do not send something like this: //input[@class='artdeco-text-input--input' and @id='single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-2705633535-106227781-numeric'], but something in this format: //*[@id='single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-2705633535-33492811-numeric'] "
                            #xpath_prompt = f"Generate a precise XPath locator for the following HTML element: {outer_html}. Provide a single, accurate XPath expression. I am sending it to a variable for automation."
                            xpath_response = self.get_gpt_response(xpath_prompt)
                            print("Here is the xpath generated by gpt GPT main function on continue application page: ")
                            print(xpath_response)
                            try:
                                self.driver.find_element(By.XPATH, xpath_response).send_keys(response)
                                print("Filing the form with the generated response from gpt")
                            except:
                                print("I could not find the xpath generated by gpt")

                except Exception as e:
                    print("there is no input field empty ", e)
                    result = "* 🥵 " +str(applyPages)+ " Pages, couldn't apply to this job! Extra info needed. Link: " +str(offerPage)

                # Find the fieldset that contains the radio buttons continue page
                # Radio button
                try:
                    # Find all fieldsets that contain radio buttons continue page
                    time.sleep(random.uniform(1, constants.botSpeed))
                    fieldsets = self.driver.find_elements(By.XPATH, "//fieldset[@data-test-form-builder-radio-button-form-component='true']")
                    for fieldset in fieldsets:
                        # Check if a response is needed (no existing selection)
                        radio_containers = fieldset.find_elements(By.XPATH, ".//div[@data-test-text-selectable-option]")
                        if not any(container.find_element(By.XPATH, ".//input[@type='radio']").is_selected() for container in radio_containers):
                            # Send the question to GPT for answer (assuming function get_gpt_response exists)
                            # Extract the question
                            question_span = fieldset.find_element(By.XPATH, ".//span[@aria-hidden='true']")
                            question = question_span.text.strip()
                            print("I just retrieve the following question for radio button from continue page: ")
                            print(question)
                            if question:
                                promptradio = f"Given the profile summary: '{summary_radio_questions}', answer the following: '{question}' by sending yes or no. Just send the word yes or the word no, as I am sending it directly to a variable for automation. Do not add anything else."
                                gpt_response = self.get_gpt_response(promptradio)
                                time.sleep(random.uniform(1, constants.botSpeed))
                                print("Here is the response from GPT for radio button continue page: ")
                                print(gpt_response)
                                # Iterate through radio containers to find and click the appropriate option
                                for container in radio_containers:
                                    print("I am iterating through radio containers to find and click the appropriate option")
                                    radio_input = container.find_element(By.XPATH, ".//input[@type='radio']")
                                    print("I found the radio input")
                                    label = container.find_element(By.XPATH, ".//label")
                                    print("I found the label that contain yes or no and I am ready to click continue pge")
                                    # Decide which radio button to click based on its value
                                    # Use case-insensitive comparison for matching GPT response with label text
                                    if gpt_response.lower() == label.text.strip().lower():  # Stripping any leading/trailing whitespace
                                        print("I am clicking the radio button on continue page")
                                        label.click()
                                        break  # Assuming only one needs to be selected
                except Exception as e:
                    print(f"Error handling radio buttons within div containers: {e}")

                # Find unselected dropdowns and select it based on gpt response to the question from continue page
                # Dropdown
                try:
                    # Find all select elements
                    selects = self.driver.find_elements(By.XPATH, "//select[@data-test-text-entity-list-form-select]")
                    for select_element in selects:
                        select_id = select_element.get_attribute('id')
                        # Create a Select object to interact with the <select> element
                        select = Select(select_element)
                        # Check if the first option (default "Select an option") is selected
                        if select.first_selected_option.get_attribute('value') == "Select an option":
                            # Find the corresponding label with the question
                            label = self.driver.find_element(By.XPATH, f"//label[@for='{select_id}']")
                            question = label.text.strip()
                            print("I just retrieve the following question for dropdown from continue page: ")
                            print(question)

                            # Extract all dropdown options except the default "Select an option"
                            options = [option.text.strip() for option in select.options if option.get_attribute('value') != "Select an option"]
                            print("I just retrieve the following options for dropdown from continue page: ")
                            print(options)

                            # Send the question and options to GPT for an answer
                            if question and options:
                                promptselect = f"Given the profile summary: '{summary_select_questions}', and the available options {options}, answer the following: '{question}'. Please send the exact option that you choose, as I am sending it directly to a variable for automation. Do not send anything else. No comment, nothing else. Send you choice from the available options."
                                gpt_response = self.get_gpt_response(promptselect)
                                time.sleep(random.uniform(1, constants.botSpeed))
                                print("Here is the response from GPT for dropdown: ")
                                print(gpt_response)
                                # Iterate through options to find and select the appropriate one
                                # Select the option that matches the GPT response
                                try:
                                    select.select_by_visible_text(gpt_response)
                                except Exception as e:
                                    print(f"Error selecting dropdown option: {e}")
                        else:
                            print("The dropdown has already been selected, skipping GPT call")
                except Exception as e:
                    print(f"Error handling dropdowns: {e}")



                try:
                    # Click the continue button
                    time.sleep(random.uniform(1, constants.botSpeed))
                    self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                    time.sleep(random.uniform(1, constants.botSpeed))
                except Exception as e:
                    print(f"Error clicking continue button: {e}")
                    result = "* 🥵 " +str(applyPages)+ " Pages, couldn't apply to this job! Extra info needed. Link: " +str(offerPage)
                # Click 'Continue to next step' after handling fields
                #self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Continue to next step']").click()
                #time.sleep(random.uniform(1, constants.botSpeed))


            # On the review button page check and file require fields before clicking on review your application
            # which is the page after applyPages-2
            # Input text field
            try:
                input_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']:not(.search-global-typeahead__input)")
                for field in input_fields:
                    value = field.get_attribute('value')
                    if not value:  # If the field is empty
                        # Logic to fill the field
                        outer_html = field.get_attribute('outerHTML')
                        field_id = field.get_attribute('id')  # Get the id of the input field
                        print("I got the field id:")
                        print(field_id)
                        if field_id:
                            label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{field_id}']")
                            question = label.text
                            print("I just retrieve the following question: ")
                            print(question)
                        print("I got the outerHTML of the input field")
                        print(outer_html)

                        # Send the question text related to this field to GPT for answer generation from review page.
                        if question:
                            time.sleep(random.uniform(1, constants.botSpeed))
                            prompt = f"Given the profile summary: '{summary_of_experience}', answer the following: '{question}' as a single digit. Just send the digit, as I am sending it directly to a variable for automation. send 1 when there is no answer. Send in this format: '6', Do not send in the following format: 'Given the information provided, the number of years of work experience with python is 6'"
                            response = self.get_gpt_response(prompt)
                            print("Here is the response from GPT in the if block: ")
                            print(response)

                        # Send outerHTML to GPT for XPath generation  response['choices'][0].message.content
                        time.sleep(random.uniform(1, constants.botSpeed))
                        print("I am sending the outerHTML to GPT for XPath generation from review page")
                        #xpath_prompt = f"Given this outerHTML element: '{outer_html}', write for me the XPath locator (do not teach me how to write a Xpath) Just send me a single xpath without comment, do not send all the ways I can write a xpath. Just send one because I am sending it to a variable for automation."
                        xpath_prompt = f"Given this outerHTML element: '{outer_html}', Send me the Xpath locator. (do not teach me how to write a Xpath) Just send me a single xpath without comment. Just One single Xpath. I am sending it to a variable for automation. Do not send in this format: //input[@class='artdeco-text-input--input' and @id='single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-2705633535-106227781-numeric'], but send in this format: //*[@id='single-line-text-form-component-formElement-urn-li-jobs-applyformcommon-easyApplyFormElement-2705633535-33492811-numeric'] "
                        #xpath_prompt = f"Generate a precise XPath locator for the following HTML element: {outer_html}. Provide a single, accurate XPath expression. I am sending it to a variable for automation."
                        xpath_response = self.get_gpt_response(xpath_prompt)
                        print("Here is the xpath generated by gpt GPT printing from main function on review page: ")
                        print(xpath_response)
                        try:
                            self.driver.find_element(By.XPATH, xpath_response).send_keys(response)
                            print("Filing the form with the generated response from gpt")
                        except:
                            print("I could not find the xpath generated by gpt")
            except Exception as e:
                print("there is no input field empty ", e)

            # Find the fieldset that contains the radio buttons on review page
            # Radio button
            try:
                # Find all fieldsets that contain radio buttons
                time.sleep(random.uniform(1, constants.botSpeed))
                fieldsets = self.driver.find_elements(By.XPATH, "//fieldset[@data-test-form-builder-radio-button-form-component='true']")
                for fieldset in fieldsets:
                    # Check if a response is needed (no existing selection)
                    radio_containers = fieldset.find_elements(By.XPATH, ".//div[@data-test-text-selectable-option]")
                    if not any(container.find_element(By.XPATH, ".//input[@type='radio']").is_selected() for container in radio_containers):
                        # Send the question to GPT for answer (assuming function get_gpt_response exists)
                        # Extract the question
                        question_span = fieldset.find_element(By.XPATH, ".//span[@aria-hidden='true']")
                        question = question_span.text.strip()
                        print("I just retrieve the following question for radio button from review page: ")
                        print(question)
                        if question:
                            promptradio = f"Given the profile summary: '{summary_radio_questions}', answer the following: '{question}' by sending yes or no. Just send the word yes or the word no, as I am sending it directly to a variable for automation. Do not add anything else."
                            gpt_response = self.get_gpt_response(promptradio)
                            time.sleep(random.uniform(1, constants.botSpeed))
                            print("Here is the response from GPT for radio button: ")
                            print(gpt_response)
                            # Iterate through radio containers to find and click the appropriate option
                            for container in radio_containers:
                                print("I am iterating through radio containers to find and click the appropriate option")
                                radio_input = container.find_element(By.XPATH, ".//input[@type='radio']")
                                print("I found the radio input")
                                print("Now I am finding the label that contain yes or no")
                                label = container.find_element(By.XPATH, ".//label")
                                print("I found the label that contain yes or no and I am ready to click")
                                # Decide which radio button to click based on its value
                                # Use case-insensitive comparison for matching GPT response with label text
                                if gpt_response.lower() == label.text.strip().lower():  # Stripping any leading/trailing whitespace
                                    print("I am clicking the radio button")
                                    label.click()
                                    print("I clicked the radio button")
                                    break  # Assuming only one needs to be selected
            except Exception as e:
                print(f"Error handling radio buttons within div containers: {e}")


            # Find unselected dropdowns and select it based on gpt response to the question from review page
            # Select dropdown
            try:
                # Find all select elements
                selects = self.driver.find_elements(By.XPATH, "//select[@data-test-text-entity-list-form-select]")
                for select_element in selects:
                    select_id = select_element.get_attribute('id')
                    # Create a Select object to interact with the <select> element
                    select = Select(select_element)
                    # Check if the first option (default "Select an option") is selected
                    if select.first_selected_option.get_attribute('value') == "Select an option":
                        # Find the corresponding label with the question
                        label = self.driver.find_element(By.XPATH, f"//label[@for='{select_id}']")
                        question = label.text.strip()
                        print("I just retrieve the following question for dropdown from review page: ")
                        print(question)

                        # Extract all dropdown options except the default "Select an option"
                        options = [option.text.strip() for option in select.options if option.get_attribute('value') != "Select an option"]
                        print("I just retrieve the following options for dropdown from continue page: ")
                        print(options)

                        # Send the question and options to GPT for an answer
                        if question and options:
                            promptselect = f"Given the profile summary: '{summary_select_questions}', and the available options {options}, answer the following: '{question}'. Please send the exact option that you choose, as I am sending it directly to a variable for automation. Do not send anything else. No comment, nothing else. Send you choice from the available options."
                            gpt_response = self.get_gpt_response(promptselect)
                            time.sleep(random.uniform(1, constants.botSpeed))
                            print("Here is the response from GPT for dropdown: ")
                            print(gpt_response)
                            # Iterate through options to find and select the appropriate one
                            # Select the option that matches the GPT response
                            try:
                                select.select_by_visible_text(gpt_response)
                            except Exception as e:
                                print(f"Error selecting dropdown option: {e}")
                    else:
                        print("The dropdown has already been selected, skipping GPT call")
            except Exception as e:
                print(f"Error handling dropdowns: {e}")




            self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Review your application']").click() 
            time.sleep(random.uniform(1, constants.botSpeed))

            #self.driver.find_element(By.CSS_SELECTOR,"button[aria-label='Submit application']").click()
            time.sleep(random.uniform(1, constants.botSpeed))
            submit_button =  WebDriverWait(self.driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,"button[aria-label='Submit application']")))
            #submit_button = self.driver.find_element(By.XPATH,"/html[1]/body[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/footer[1]/div[3]/button[2]")
            actions = ActionChains(self.driver)
            actions.move_to_element(submit_button).perform()
            submit_button.click()
            time.sleep(random.uniform(1, constants.botSpeed))

            result = "* 🥳 Just Applied to this job: " +str(offerPage)

        except:
            # If for some reason it couldn't apply to the job, it will return the link of the job
            result = "* 🥵 " +str(applyPages)+ " Pages, couldn't apply to this job! Extra info needed. Link: " +str(offerPage)
        return result"""

    '''def get_gpt_response(self, prompt):
        try:
            client = OpenAI()
            response = client.chat.completions.create(
  model="gpt-3.5-turbo-0125",
  messages=[
    {"role": "system", "content": "You are my assistant"},
    {"role": "user", "content": prompt}
  ]
)
            print("Here is the response from GPT: ")
            print(response.choices[0].message)
            gpt_response = response.choices[0].message.content
            print("Here is the response from GPT gpt_response: ")
            print(gpt_response)
            
            return gpt_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None'''



    def get_gpt_response(self, prompt):
        try:
            client = OpenAI()
            response = client.chat.completions.create(
  model="gpt-4-0125-preview",
  messages=[
    {"role": "system", "content": "You are my assistant"},
    {"role": "user", "content": prompt}
  ]
)
            print("Here is the response from GPT: ")
            print(response.choices[0].message)
            gpt_response = response.choices[0].message.content
            print("Here is the response from GPT gpt_response: ")
            print(gpt_response)
            
            return gpt_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None




    def displayWriteResults(self,lineToWrite: str):
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            prRed("❌ Error in DisplayWriteResults: " +str(e))

start = time.time()
Linkedin().linkJobApply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")