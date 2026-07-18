import re
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'r') as f:
    content = f.read()

target = """    fun generatePairCode(): String {
        val currentTime = System.currentTimeMillis()
        if (currentPairCode == null || currentTime - pairCodeGenerationTime > 10 * 60 * 1000) {
            val chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            currentPairCode = (1..10).map { chars.random() }.joinToString("")
            pairCodeGenerationTime = currentTime
        }
        return currentPairCode!!
    }"""

replacement = """    fun generatePairCode(): String {
        if (currentPairCode == null) {
            val chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            currentPairCode = (1..10).map { chars.random() }.joinToString("")
        }
        return currentPairCode!!
    }
    
    fun refreshPairCode(): String {
        val chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        currentPairCode = (1..10).map { chars.random() }.joinToString("")
        return currentPairCode!!
    }"""

content = content.replace(target, replacement)
with open('app/src/main/java/com/example/viewmodel/AppViewModel.kt', 'w') as f:
    f.write(content)
