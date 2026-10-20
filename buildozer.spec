[app]
title = Machine Spare Parts
package.name = machinesparts
package.domain = org.industrial
source.include_exts = py,png,jpg,kv,atlas
source.include_dir = 
version = 1.1
requirements = python3,kivy,sqlite3
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
