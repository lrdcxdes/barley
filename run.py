

if __name__ == '__main__':
    import logging
    import subprocess
    import sys

    logging.info(f"Обновляю модули...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", '-U', "-r", "requirements.txt"])
    logging.info('Модули обновлены!')

    from app import on_startup, on_shutdown
    from aiogram import executor
    from loader import dp
    import utils.schedulers

    logging.getLogger('apscheduler.executors.default').propagate = False
    logging.basicConfig(level=logging.INFO)
    #  open('assets/last.txt', 'w', encoding='utf-8').write('')
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
