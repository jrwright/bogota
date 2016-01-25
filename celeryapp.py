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

    if cfg.app.logfile is not None:
        app.log.setup(loglevel=(cfg.app.loglevel or 'INFO'), logfile=cfg.app.logfile)


else:
    class DummyApp(object):
        def task(fn, *args, **kwArgs):
            return fn
        def worker_main():
            pass

    app = DummyApp()

if __name__ == '__main__':
    app.worker_main()
