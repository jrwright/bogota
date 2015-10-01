from __future__ import absolute_import
from celery import Celery
import bogota.cdf as cfg

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
)

if __name__ == '__main__':
    app.worker_main()
