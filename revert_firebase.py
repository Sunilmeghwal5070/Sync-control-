import re
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'r') as f:
    content = f.read()
target = "val db = try { FirebaseFirestore.getInstance() } catch(e: Exception) { null }"
replacement = "val db = FirebaseFirestore.getInstance()"
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/data/FirebaseRepository.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()
target = "try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }"
replacement = "com.google.firebase.auth.FirebaseAuth.getInstance().currentUser"
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/screens/ParentScreens.kt', 'r') as f:
    content = f.read()
target = "try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }"
replacement = "com.google.firebase.auth.FirebaseAuth.getInstance().currentUser"
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/ui/screens/ParentScreens.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()
target = "val auth = try { com.google.firebase.auth.FirebaseAuth.getInstance() } catch(e: Exception) { null }"
replacement = "val auth = com.google.firebase.auth.FirebaseAuth.getInstance()"
content = content.replace(target, replacement)
target2 = "try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }"
replacement2 = "com.google.firebase.auth.FirebaseAuth.getInstance().currentUser"
content = content.replace(target2, replacement2)
target3 = "auth?.signInAnonymously()?.await()"
replacement3 = "auth.signInAnonymously().await()"
content = content.replace(target3, replacement3)
with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()
target = "val auth = try { com.google.firebase.auth.FirebaseAuth.getInstance() } catch(e:Exception) { null }"
replacement = "val auth = com.google.firebase.auth.FirebaseAuth.getInstance()"
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
