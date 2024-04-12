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

        # Define the possible word limits
        word_limits = [33, 43, 53, 63, 73, 83, 93]
        # Randomly select a word limit
        selected_word_limit = random.choice(word_limits)
        print(f"Selected Word Limit: {selected_word_limit}")

        hashtag = "#chatgpt, #ai, #education, #learning, #career, #softwaretesting, #qualityassurance"
        bookExcerpt = selected_segment
        #print("The segment from the book I am sending gpt is:")
        #print(bookExcerpt)
        prompt1 = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise and engaging LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. The post should be informative, demonstrate thought leadership, and engage my network in a discussion on the future of AI testing. let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtag}."
        prompt2 = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. The post should be informative. let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtag} and add another of your choosing."
        prompt3 = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise LinkedIn post that is engaging. let it be {selected_word_limit} words or less. Choose 2 hashtags from this: {hashtag} and add another of your choosing."
        prompt4 = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise LinkedIn post that is informative. let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtag} and add another of your choosing."
        prompt5 = f"Given the following excerpt from a book on AI testing: '{bookExcerpt}', please formulate a concise LinkedIn post that is insightful. let it be {selected_word_limit} words or less."

        # Choose a prompt randomly
        prompt = random.choice([prompt1, prompt2, prompt3, prompt4, prompt5])
        print(f"Selected Prompt:\n{prompt}")
        gpt_response = self.get_gpt_response(prompt)
        time.sleep(2)
        # Clean the GPT response before sending it
        clean_gpt_response = self.remove_non_bmp_characters(gpt_response)
        time.sleep(random.uniform(1, constants.botSpeed))
        # Remove leading and trailing quotation marks
        gpt_response = clean_gpt_response.strip('"')
        
        # Find the content-editable element (ql-editor) within the Quill container
        editor = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ql-editor') and @contenteditable='true']")

        # Use send_keys to input text
        editor.send_keys(gpt_response)
        time.sleep(5)
        print("I just sent the gpt response to the linkedin post editor")
        print("I am about to click the post button")

        time.sleep(5)
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

        time.sleep(10)
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
            time.sleep(10)

            # now post in the group
            xpathPostGroup = "//button[contains(@class, 'share-actions__primary-action') and contains(@class, 'artdeco-button')]"
            #xpathPostGroup = "//a[contains(@class, 'share-actions__primary-action') and contains(@class, 'ember-view')]"
            # #ember1216
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

        time.sleep(5)


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