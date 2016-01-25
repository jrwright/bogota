from __future__ import absolute_import
import bogota.cfg as cfg

if cfg.app.async:
    from celery import Celery

    app = Celery(cfg.app.name,
                 broker=cfg.app.broker,
                 backend=cfg.app.backend,
                 include=cfg.app.include.split(','))

    # Optional configuration, see the application user guide.
    app.conf.update(
        CELERY_TASK_RESULT_EXPIRES=3600,
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT = ['json'],
        CELERYD_PREFETCH_MULTIPLIER = 1,
    )

else:
    class DummyApp(object):
        def task(fn, *args, **kwArgs):
            return fn
        def worker_main():
            pass

    app = DummyApp()

def setup_logs():
    import logging
    logger = logging.getLogger()
    level = (cfg.app.loglevel or logging.INFO)
    fh = logging.FileHandler(cfg.app.logfile)
    fh.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.setLevel(min(logger.level, level))

if __name__ == '__main__':
    if cfg.app.logfile is not None:
        setup_logs()
    app.worker_main()
