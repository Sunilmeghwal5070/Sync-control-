import re
with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

target = """                onBack = {
                    navController.popBackStack()
                }"""
replacement = """                onBack = {
                    navController.popBackStack("use_case", inclusive = false)
                }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
