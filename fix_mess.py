import os

files = ['app/src/main/java/com/example/ui/screens/MainScreens.kt', 'app/src/main/java/com/example/ui/screens/ParentScreens.kt', 'app/src/main/java/com/example/ui/screens/LoginScreen.kt']

for f in files:
    if os.path.exists(f):
        with open(f, 'r') as file:
            c = file.read()
        c = c.replace('try { com.google.firebase.auth.com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }', 'com.google.firebase.auth.FirebaseAuth.getInstance().currentUser')
        c = c.replace('try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }', 'com.google.firebase.auth.FirebaseAuth.getInstance().currentUser')
        c = c.replace('auth.signInAnonymously().await()', 'auth.signInAnonymously().await()')
        with open(f, 'w') as file:
            file.write(c)

