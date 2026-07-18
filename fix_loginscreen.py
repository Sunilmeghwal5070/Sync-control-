import re
with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()

target = """                                auth.signInAnonymously().await()"""
replacement = """                                FirebaseAuth.getInstance().signInAnonymously().await()"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)
