import re
with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()

target1 = """Toast.makeText(context, "Login Failed. Check connection.", Toast.LENGTH_SHORT).show()"""
replacement1 = """Toast.makeText(context, "Login Failed: ${e.message}. Please enable Anonymous Authentication in Firebase Console.", Toast.LENGTH_LONG).show()"""
content = content.replace(target1, replacement1)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)
