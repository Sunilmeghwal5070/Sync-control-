with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

target = """NavHost(navController = navController, startDestination = "login") {"""
replacement = """NavHost(navController = navController, startDestination = "login") {
        composable("login") {
            LoginScreen(onLoginSuccess = {
                navController.navigate("splash") {
                    popUpTo("login") { inclusive = true }
                }
            })
        }"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
