from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import markdown

os.system("rm -rf images/*")

driver = webdriver.Firefox()

wait = WebDriverWait(driver, timeout=20, poll_frequency=1)
url = "https://www.examtopics.com/exams/comptia/n10-008/view/"

driver.get(url)

questions_list = []
while True:

    wait.until(
        lambda driver: driver.find_elements(
            "xpath", '//div[@class="card exam-question-card"]'
        )
    )

    element = driver.find_element("css selector", "div.menu-area")
    driver.execute_script(
        """
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """,
        element,
    )

    questions = driver.find_elements("xpath", '//div[@class="card exam-question-card"]')

    for question in questions:
        question_number = question.find_element(
            "xpath", './/div[contains(@class, "card-header")]'
        ).text

        question_text = question.find_element(
            "xpath", './/div[@class="card-body question-body"]/p[@class="card-text"]',
        ).text

        question_choices_li = question.find_elements(
            "xpath",
            './/div[@class="question-choices-container"]/ul/li[contains(@class, "multi-choice-item")]',
        )
        question_choices = [answer.text for answer in question_choices_li]

        question_images_img = question.find_elements(
            "xpath",
            './/div[@class="card-body question-body"]/p[@class="card-text"]/img',
        )

        question_images = []
        for i in range(len(question_images_img)):
            filename = question_images_img[i].get_attribute("src").split("/")[-1]
            with open("images/" + filename, "wb") as file:
                file.write(question_images_img[i].screenshot_as_png)
            question_images.append("images/" + filename)

        # question_images = [image.get_attribute("src") for image in question_images_img]

        question_answers_span = question.find_elements(
            "xpath",
            './/p[contains(@class, "question-answer")]/span[@class="correct-answer-box"]/span[@class="correct-answer"]',
        )

        question_answers = [
            answer.get_attribute("innerHTML") for answer in question_answers_span
        ]

        question_description = (
            question.find_element(
                "xpath",
                './/p[contains(@class, "question-answer")]/span[@class="answer-description"]',
            )
            .get_attribute("innerHTML")
            .replace("<br>", "\n")
        )

        questions_list.append(
            # Question(
            #     question_text, question_choices, question_answers, question_description
            # )
            {
                "number": question_number,
                "question": question_text,
                "choices": question_choices,
                "images": question_images,
                "answers": question_answers,
                "description": question_description,
            }
        )

    print(questions_list[-1])
    driver.find_element("xpath", "//a[@class='btn btn-success pull-right']").click()

    json_questions = json.dumps(questions_list, indent=4)

    with open("questions.json", "w") as outfile:
        outfile.write(json_questions)

