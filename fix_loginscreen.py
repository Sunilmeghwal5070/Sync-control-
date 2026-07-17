with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'r') as f:
    content = f.read()

replacement = """                                val resId = context.resources.getIdentifier("default_web_client_id", "string", context.packageName)
                                if (resId == 0) {
                                    Toast.makeText(context, "Setup Error: default_web_client_id not found. Please add a valid google-services.json", Toast.LENGTH_LONG).show()
                                    isLoading = false
                                    return@launch
                                }
                                val webClientId = context.getString(resId)"""

content = content.replace('val webClientId = context.getString(context.resources.getIdentifier("default_web_client_id", "string", context.packageName))', replacement)

with open('app/src/main/java/com/example/ui/screens/LoginScreen.kt', 'w') as f:
    f.write(content)
