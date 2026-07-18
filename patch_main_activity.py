import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """    val firebaseRepository = com.example.data.FirebaseRepository()
    
    val auth = com.google.firebase.auth.FirebaseAuth.getInstance()"""

replacement = """    val firebaseRepository: com.example.data.FirebaseRepository? = try {
        com.example.data.FirebaseRepository()
    } catch (e: Exception) {
        android.util.Log.e("MainActivity", "Firebase init failed", e)
        android.widget.Toast.makeText(this, "Firebase Init Failed: ${e.message}", android.widget.Toast.LENGTH_LONG).show()
        null
    }
    
    val auth = try { com.google.firebase.auth.FirebaseAuth.getInstance() } catch(e:Exception) { null }"""
content = content.replace(target, replacement)

target2 = """            val viewModel: AppViewModel = viewModel(
                factory = AppViewModelFactory(repository, firebaseRepository)
            )"""
replacement2 = """            val viewModel: AppViewModel = viewModel(
                factory = AppViewModelFactory(repository, firebaseRepository ?: com.example.data.FirebaseRepository())
            )"""
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
