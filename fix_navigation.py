import re

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

replacement = """        composable("login") {
            LoginScreen(onLoginSuccess = {
                navController.navigate("splash") {
                    popUpTo("login") { inclusive = true }
                }
            })
        }
        composable("splash") {"""

content = content.replace('startDestination = "splash"', 'startDestination = "login"')
content = content.replace('composable("splash") {', replacement)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
