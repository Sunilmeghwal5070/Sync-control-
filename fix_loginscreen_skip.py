with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()

replacement = """    // Check if already logged in
    LaunchedEffect(Unit) {
        if (FirebaseAuth.getInstance().currentUser != null) {
            onLoginSuccess()
        }
    }"""

content = content.replace(replacement, replacement)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)
