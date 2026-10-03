import os
from app.extraction import extract_text

RESUME_DIR = "data/resumes"
OUTPUT_DIR = "data/extracted"

MIN_LENGTH = 200

os.makedirs(OUTPUT_DIR,exist_ok=True)

suspicious = []

for name in os.listdir(RESUME_DIR):
        path = os.path.join(RESUME_DIR,name)
        text = extract_text(path)
        length = len(text)
        print(name, "->", length, "characters")

        if length < MIN_LENGTH: 
            suspicious.append(name)

        output_path = os.path.join(OUTPUT_DIR,name + ".txt")
        with open(output_path,"w",encoding="utf-8") as file:
              file.write(text)

print()
print("Files with very little text : ", len(suspicious))
for name in suspicious:
      print(" ",name)