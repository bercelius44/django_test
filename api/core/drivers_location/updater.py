from core.drivers_location.drivers_location_updater import update_drivers_location
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_drivers_location, 'interval', minutes=60, id="1", replace_existing=True)
    scheduler.start()