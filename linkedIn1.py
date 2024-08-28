import time, math, random, os, re
from selenium import webdriver
import pyperclip
import utils,constants,config
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from utils import prRed,prYellow,prGreen
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Chrome options
options = Options()
options.add_argument(r"--user-data-dir=C:\Users\DELL\AppData\Local\Google\Chrome\User Data")
options.add_argument(r'--profile-directory=Profile 1')
options.add_argument("--start-maximized")

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Chrome WebDriver
service = Service(executable_path=r"C:\Users\DELL\.wdm\drivers\chromedriver\win64\127.0.6533.72\chromedriver-win32\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

class Linkedin:
    def __init__(self):
        self.driver = driver

    def generate_urls(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        try:
            with open('data/urlData.txt', 'w', encoding="utf-8") as file:
                linkedin_job_links = utils.LinkedinUrlGenerate().generateUrlLinks()
                for url in linkedin_job_links:
                    file.write(url + "\n")
            prGreen("✅ URLs are created successfully, now the bot will visit those URLs.")
        except:
            prRed("❌ Couldn't generate URLs, make sure you have /data folder and modified config.py file for your preferences.")

    def read_clean_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def identify_sections(self, text):
        section_pattern = re.compile(r'(\n\s*(?:\d+[.-]\s+|\bPoint\s+\d+\b|\bSection\s+\d+\b|\bChapter\s+\d+\b|\bNext unit:)\s*[A-Za-z].*?)')
        sections_starts = [match.start() for match in section_pattern.finditer(text)]
        sections_starts.append(len(text))
        sections = [text[sections_starts[i]:sections_starts[i + 1]].strip() for i in range(len(sections_starts) - 1)]
        return sections

    def chunk_text(self, sections, max_chars=10000):
        chunks = []
        current_chunk = []
        current_length = 0

        for section in sections:
            section_length = len(section)
            if current_length + section_length > max_chars:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0

            current_chunk.append(section)
            current_length += section_length

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def split_large_chunks(self, chunks, max_chars=10000):
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > max_chars:
                sub_chunks = [chunk[i:i + max_chars] for i in range(0, len(chunk), max_chars)]
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)
        return final_chunks

    def link_job_apply(self):
        self.generate_urls()
        url_data = utils.getUrlDataFile()

        for url in url_data:
            self.driver.get(url)
            home_button_js = """
            var linkElement = document.querySelector('a[data-test-app-aware-link]');
            if (linkElement) {
                linkElement.click();
            } else {
                console.log('Element not found');
            }
            """
            self.driver.execute_script(home_button_js)
            time.sleep(5)

        self.driver.find_element(By.XPATH, "//button[contains(@class, 'artdeco-button') and contains(@class, 'share-box-feed-entry__trigger')]").click()
        time.sleep(5)

        file_path = 'cleaned_book.txt'
        clean_text = self.read_clean_text(file_path)
        sections = self.identify_sections(clean_text)
        chunks = self.chunk_text(sections, max_chars=3500)
        chunks = self.split_large_chunks(chunks, max_chars=3500)

        selected_chunk = random.choice(chunks)
        print(f"Selected Chunk Sent to GPT:\n{selected_chunk}")
        word_limits = [33, 43, 53, 63, 73]
        selected_word_limit = random.choice(word_limits)
        print(f"Selected Word Limit: {selected_word_limit}")

        hashtags = "#chatgpt, #ai, #education, #learning, #career, #softwaretesting, #qualityassurance"
        prompt0 = f"Given the following excerpt from a book on AI testing: '{selected_chunk}', please formulate a concise LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. Let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtags} and add another of your choosing."
        prompt1 = f"Given the following excerpt from a book on AI testing: '{selected_chunk}', please formulate a concise and engaging LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. The post should be informative, demonstrate thought leadership, and engage my network in a discussion on the future of AI testing. let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtags}."
        prompt2 = f"Given the following excerpt from a book on AI testing: '{selected_chunk}', please formulate a concise LinkedIn post that reflects my expertise as a Software QA Engineer specializing in AI testing. The post should be informative. let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtags} and add another of your choosing."
        prompt3 = f"Given the following excerpt from a book on AI testing: '{selected_chunk}', please formulate a concise LinkedIn post that is engaging. let it be {selected_word_limit} words or less. Choose 2 hashtags from this: {hashtags} and add another of your choosing."
        prompt4 = f"Given the following excerpt from a book on AI testing: '{selected_chunk}', please formulate a concise LinkedIn post that is informative. let it be {selected_word_limit} words or less. Choose 3 hashtags from this: {hashtags} and add another of your choosing."
        prompt5 = f"Given the following excerpt from a book on AI testing: '{selected_chunk}', please formulate a concise LinkedIn post that is insightful. let it be {selected_word_limit} words or less."

        # Choose a prompt randomly
        print("I am about to select a prompt")
        prompt = random.choice([prompt1, prompt0, prompt2, prompt3, prompt4, prompt5])
        print(f"Selected Prompt:\n{prompt}")
        gpt_response = self.get_gpt_response(prompt)
        time.sleep(3)

        gpt_response = gpt_response.strip('"')
        pyperclip.copy(gpt_response)

        editor = self.driver.find_element(By.XPATH, "//div[contains(@class, 'ql-editor') and @contenteditable='true']")
        editor.click()
        time.sleep(0.5)
        editor.send_keys(Keys.CONTROL + "v")

        time.sleep(5)
        xpath = "//button[contains(@class, 'share-actions__primary-action') and contains(@class, 'ember-view')]"
        js_click_script = f"""
        var xpath = "{xpath}";
        var button = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (button) button.click();
        """
        self.driver.execute_script(js_click_script)
        print("I clicked the post button")

        time.sleep(10)
        try:
            xpath_post_in_group = "//a[contains(@class, 'app-aware-link') and contains(@class, 'artdeco-button--primary')]"
            js_click_script = f"""
            var xpath = "{xpath_post_in_group}";
            var button = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (button) button.click();
            """
            self.driver.execute_script(js_click_script)
            print("I clicked the post in group button")
            time.sleep(10)

            xpath_post_group = "//button[contains(@class, 'share-actions__primary-action') and contains(@class, 'artdeco-button')]"
            js_click_script = f"""
            var xpath = "{xpath_post_group}";
            var button = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (button) button.click();
            """
            self.driver.execute_script(js_click_script)
            print("I just posted in a group")
        except:
            print("I could not post in a group as it was not prompted")

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
            gpt_response = response.choices[0].message.content
            print("Here is the response from GPT gpt_response: ")
            print(gpt_response)
            return gpt_response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

start = time.time()
Linkedin().link_job_apply()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start) / 60)) + " minute(s).")
