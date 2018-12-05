from gevent import monkey
monkey.patch_all()
import scrapper.steam

scrapper.steam.main()