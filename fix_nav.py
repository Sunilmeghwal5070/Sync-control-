with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

target = """        composable("login") {
            LoginScreen(onLoginSuccess = {
                navController.navigate("splash") {
                    popUpTo("login") { inclusive = true }
                }
            })
        }"""

content = content.replace(target, "")

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
