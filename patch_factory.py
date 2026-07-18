import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()
target = """            val viewModel: AppViewModel = viewModel(
                factory = AppViewModelFactory(repository, firebaseRepository ?: try { com.example.data.FirebaseRepository() } catch (e: Exception) { null } as com.example.data.FirebaseRepository)
            )"""
replacement = """            val viewModel: AppViewModel = viewModel(
                factory = AppViewModelFactory(repository, firebaseRepository ?: com.example.data.FirebaseRepository())
            )"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
