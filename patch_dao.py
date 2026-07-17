with open('app/src/main/java/com/example/data/AppDao.kt', 'r') as f:
    content = f.read()
target = """    @Query("SELECT * FROM paired_devices")
    fun getAllPairedDevices(): Flow<List<PairedDevice>>"""
replacement = """    @Query("SELECT * FROM paired_devices")
    fun getAllPairedDevices(): Flow<List<PairedDevice>>

    @Query("SELECT * FROM paired_devices")
    suspend fun getPairedDevicesSync(): List<PairedDevice>"""
content = content.replace(target, replacement)
with open('app/src/main/java/com/example/data/AppDao.kt', 'w') as f:
    f.write(content)
