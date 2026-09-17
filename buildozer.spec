[app]
title = Snake
package.name = snake
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.0
orientation = portrait
fullscreen = 1
android.permissions = INTERNET
android.archs = arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
