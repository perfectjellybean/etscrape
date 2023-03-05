import json
import markdown

with open("questions.json", "r") as file:
    questions = json.load(file)

    with open("questions.md", "w") as md:
        for question in questions:
            md.write("## {}\n\n".format(question["number"]))
            md.write("{}\n\n".format(question["question"]))
            if len(question["images"]) > 0:
                for image in question["images"]:
                    md.write("![alt text]({})\n".format(image))
            for choice in question["choices"]:
                md.write("> {}\n\n".format(choice))
            md.write("**Answer: {}**\n\n".format(question["answers"][0]))
            md.write("**Description**: {}\n".format(question["description"]))
