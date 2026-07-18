import re
with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()
target = "val auth = FirebaseAuth.getInstance()"
replacement = "val auth = try { com.google.firebase.auth.FirebaseAuth.getInstance() } catch(e: Exception) { null }"
content = content.replace(target, replacement)

target2 = "FirebaseAuth.getInstance().signInAnonymously().await()"
replacement2 = "auth?.signInAnonymously()?.await()"
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)
