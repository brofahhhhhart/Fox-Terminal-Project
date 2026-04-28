[app]
title = Fox Terminal
package.name = foxterminal
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Requisitos do sistema
requirements = python3,kivy==2.2.1,kivymd,pillow

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a, arm64-v8a
android.allow_backup = True

# Versões críticas para o GitHub em 2026
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

# Permissões
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
