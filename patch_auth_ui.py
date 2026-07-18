import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """            val user = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
            if (user != null) {
                Text(
                    text = "Signed in as: ${user.email}",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    modifier = Modifier.align(Alignment.End)
                )
            }"""
replacement = """            val user = try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch(e: Exception) { null }
            if (user?.email != null) {
                Text(
                    text = "Signed in as: ${user.email}",
                    fontSize = 14.sp,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                    modifier = Modifier.align(Alignment.End)
                )
            }"""
content = content.replace(target, replacement)

target2 = """        val user = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
        if (user != null) {
            Text(
                text = "Signed in as: ${user.email}",
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                modifier = Modifier.align(Alignment.End)
            )
        }"""
replacement2 = """        val user = try { com.google.firebase.auth.FirebaseAuth.getInstance().currentUser } catch (e: Exception) { null }
        if (user?.email != null) {
            Text(
                text = "Signed in as: ${user.email}",
                fontSize = 14.sp,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f),
                modifier = Modifier.align(Alignment.End)
            )
        }"""
content = content.replace(target2, replacement2)

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
