import re
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()

target = "val db = FirebaseFirestore.getInstance()"
replacement = "val db = try { FirebaseFirestore.getInstance() } catch(e: Exception) { null }"
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(content)
