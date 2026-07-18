import re
with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'r') as f:
    content = f.read()

target1 = """                onNavigateToRoleSelection = {
                    navController.navigate("role_selection")
                },"""
replacement1 = """                onNavigateToRole = { role ->
                    navController.navigate("permissions/$role")
                },"""
content = content.replace(target1, replacement1)

target2 = """                onAddDevice = {
                    navController.navigate("role_selection")
                }"""
replacement2 = """                onAddDevice = {
                    navController.navigate("permissions/child")
                }"""
content = content.replace(target2, replacement2)

target3 = """        composable("role_selection") {
            RoleSelectionScreen(
                onRoleSelected = { role ->
                    navController.navigate("permissions/$role")
                }
            )
        }"""
replacement3 = ""
content = content.replace(target3, replacement3)

target4 = """                onPaired = {
                    navController.navigate("use_case") {
                        popUpTo("role_selection") { inclusive = true }
                    }
                }"""
replacement4 = """                onPaired = {
                    navController.popBackStack("use_case", inclusive = false)
                },
                onBack = {
                    navController.popBackStack()
                }"""
content = content.replace(target4, replacement4)

with open('app/src/main/java/com/example/navigation/AppNavigation.kt', 'w') as f:
    f.write(content)
