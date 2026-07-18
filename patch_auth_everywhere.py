import re
import os

files = ['app/src/main/java/com/example/ui/screens/MainScreens.kt', 'app/src/main/java/com/example/ui/screens/ParentScreens.kt', 'app/src/main/java/com/example/ui/screens/LoginScreen.kt']

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
        
        target = "com.google.firebase.auth.FirebaseAuth.getInstance().currentUser"
        replacement = "try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }"
        content = content.replace(target, replacement)
        
        target2 = "FirebaseAuth.getInstance().currentUser"
        replacement2 = "try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }"
        content = content.replace(target2, replacement2)
        
        with open(filename, 'w') as f:
            f.write(content)

