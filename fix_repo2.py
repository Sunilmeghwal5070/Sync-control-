import re

with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()

content = content.replace("private val db = FirebaseFirestore.getInstance()", "val db = FirebaseFirestore.getInstance()")

with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(content)
