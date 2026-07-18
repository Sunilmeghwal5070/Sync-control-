import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target1 = """android.widget.Toast.makeText(context, "Firebase DB Error on Child: $initErr", android.widget.Toast.LENGTH_LONG).show()"""
replacement1 = """android.widget.Toast.makeText(context, "Firebase DB Error: $initErr. Enable Firestore Database & Anonymous Auth in Firebase Console.", android.widget.Toast.LENGTH_LONG).show()"""
content = content.replace(target1, replacement1)

target2 = """android.widget.Toast.makeText(context, "Firebase Error: $errorMsg", android.widget.Toast.LENGTH_LONG).show()"""
replacement2 = """android.widget.Toast.makeText(context, "Firebase Error: $errorMsg. Enable Firestore Database & Anonymous Auth in Firebase Console.", android.widget.Toast.LENGTH_LONG).show()"""
content = content.replace(target2, replacement2)

target3 = """android.widget.Toast.makeText(context, "Pairing request failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()"""
replacement3 = """android.widget.Toast.makeText(context, "Pairing failed: ${e.message}. Enable Firestore Database in Firebase Console.", android.widget.Toast.LENGTH_LONG).show()"""
content = content.replace(target3, replacement3)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
