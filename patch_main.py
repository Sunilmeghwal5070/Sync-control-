import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """    val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
    if (auth?.currentUser == null) {
        auth?.signInAnonymously()?.addOnCompleteListener { task ->
            if (!task.isSuccessful) {
                android.util.Log.e("MainActivity", "Anonymous auth failed", task.exception)
            }
        }
    }"""
replacement = """    try {
        val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
        if (auth.currentUser == null) {
            auth.signInAnonymously().addOnCompleteListener { task ->
                if (!task.isSuccessful) {
                    android.util.Log.e("MainActivity", "Anonymous auth failed", task.exception)
                }
            }
        }
    } catch (e: Exception) {
        android.util.Log.e("MainActivity", "Firebase auth skipped", e)
    }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
