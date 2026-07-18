import re
with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'r') as f:
    content = f.read()

target = """fun UseCaseCard(title: String, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .clickable(onClick = onClick)
            .background(MaterialTheme.colorScheme.surfaceVariant),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Box(modifier = Modifier
            .height(120.dp)
            .fillMaxWidth(), contentAlignment = Alignment.Center) { 
            Text("Illustration", color = MaterialTheme.colorScheme.primary)
        }
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.primary)
                .padding(12.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(title, color = MaterialTheme.colorScheme.onPrimary, fontWeight = FontWeight.Bold, fontSize = 18.sp)
        }
    }
}"""
replacement = """fun UseCaseCard(title: String, icon: androidx.compose.ui.graphics.vector.ImageVector, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(160.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Box(
                modifier = Modifier
                    .size(64.dp)
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.1f), androidx.compose.foundation.shape.CircleShape),
                contentAlignment = Alignment.Center
            ) {
                androidx.compose.material3.Icon(
                    imageVector = icon,
                    contentDescription = title,
                    modifier = Modifier.size(32.dp),
                    tint = MaterialTheme.colorScheme.primary
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            Text(title, color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.Bold, fontSize = 20.sp)
        }
    }
}"""
content = content.replace(target, replacement)

# Now update the calls to UseCaseCard
target2 = """UseCaseCard(title = "Parent Dashboard", onClick = { onNavigateToParentDashboard() })"""
rep2 = """UseCaseCard(title = "Parent Dashboard", icon = androidx.compose.material.icons.Icons.Filled.AdminPanelSettings, onClick = { onNavigateToParentDashboard() })"""
content = content.replace(target2, rep2)

target3 = """UseCaseCard(title = "Parent", onClick = { onNavigateToRole("parent") })"""
rep3 = """UseCaseCard(title = "Parent", icon = androidx.compose.material.icons.Icons.Filled.AdminPanelSettings, onClick = { onNavigateToRole("parent") })"""
content = content.replace(target3, rep3)

target4 = """UseCaseCard(title = "Child Dashboard", onClick = { activeChildView = true })"""
rep4 = """UseCaseCard(title = "Child Dashboard", icon = androidx.compose.material.icons.Icons.Filled.ChildCare, onClick = { activeChildView = true })"""
content = content.replace(target4, rep4)

target5 = """UseCaseCard(title = "Child", onClick = { onNavigateToRole("child") })"""
rep5 = """UseCaseCard(title = "Child", icon = androidx.compose.material.icons.Icons.Filled.ChildCare, onClick = { onNavigateToRole("child") })"""
content = content.replace(target5, rep5)

# Add icon imports if needed
if "import androidx.compose.material.icons.Icons" not in content:
    content = "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.*\n" + content

with open('app/src/main/java/com/example/ui/screens/MainScreens.kt', 'w') as f:
    f.write(content)
