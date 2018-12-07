from gevent import monkey
monkey.patch_all()
import watchdog.steamdog
import threading

watchdog.steamdog.main()