import re
with open('app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

target = """    if (auth.currentUser == null) {
        auth.signInAnonymously().addOnCompleteListener { task ->
            if (!task.isSuccessful) {
                android.util.Log.e("MainActivity", "Anonymous auth failed", task.exception)
            }
        }
    }"""
replacement = """    if (auth?.currentUser == null) {
        auth?.signInAnonymously()?.addOnCompleteListener { task ->
            if (!task.isSuccessful) {
                android.util.Log.e("MainActivity", "Anonymous auth failed", task.exception)
            }
        }
    }"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)
