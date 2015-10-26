"""
Interface for saving/restoring values from the database.
"""
from __future__ import absolute_import
import sys
import bogota.cfg as cfg
import logging
info = logging.getLogger(__name__).info
debug = logging.getLogger(__name__).debug
from warnings import warn

# =================================== Saving ==================================

def save_mle_params(train_ll, test_ll, walltime,
                    parameter_names, parameter_values, restart_idx,
                    solver_name, pool_name, fold_seed, num_folds, fold_idx,
                    by_game, stratified):
    with db_connect() as db:
        jobid = _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)
        info("Writing results for job #%d restart #%d", jobid, restart_idx)
        c = db.cursor()

        ins_sql = _sql(db, 'replace into mle_parameters (jobid, restart_idx, name, value) '
                       ' values (%s,%s,%s,%s)')
        num_params = len(parameter_names) + 3

        c.executemany(ins_sql,
                      zip([jobid] * num_params,
                          [restart_idx] * num_params,
                          ['TRAIN_LL', 'LL', 'WALLTIME'] + parameter_names,
                          map(float, [train_ll, test_ll, walltime] + parameter_values)))
        db.commit()


# ================================== Loading ==================================

def mle_restarts(solver_name, pool_name, fold_seeds, num_folds,
                 by_game, stratified):
    """
    Return a list of completed restart indices for the specified model and data
    fold combination.
    """
    debug("Fetching restarts for %s/%s/%s/%d", solver_name, pool_name, fold_seeds, num_folds)
    with db_connect() as db:
        c = db.cursor()
        sql = """
              select j.fold_seed, j.fold_idx, p.restart_idx
                from mle_parameters p
                join mle_jobs j on p.jobid = j.jobid
               where j.solver_name=%s
                 and j.pool_name=%s
                 and j.fold_seed in ({seeds})
                 and j.num_folds = %s
                 and j.by_game = %s
                 and j.stratified = %s
              """.format(seeds=','.join(map(str, fold_seeds)))
        c.execute(_sql(db, sql), [solver_name, pool_name, num_folds, by_game, stratified])
        vals = c.fetchall()
        debug("%d restarts completed for %s/%s/%s/%d", len(vals),
              solver_name, pool_name, fold_seeds, num_folds)
        return map(lambda x: tuple(x), vals)

def mle_param(parameter_name,
              solver_name, pool_name, fold_seed, num_folds, fold_idx,
              by_game, stratified):
    """
    Return the MLE estimate of ``parameter_name`` for the specified model and
    data fold combination.
    """
    with db_connect() as db:
        jobid = _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)
        c = db.cursor()

        # Choose parameter value associated with the highest training LL
        c.execute(_sql(db,
                       """
                       select p.value, l.value
                       from mle_parameters p
                       join mle_parameters l on l.restart_idx = p.restart_idx and l.jobid = p.jobid
                       where p.jobid = %s
                       and p.name = %s
                       and l.name = 'TRAIN_LL'
                       order by l.value desc
                       limit 1
                       """), [jobid, parameter_name])
        vals = c.fetchall()
        c.close()
        if len(vals) == 0:
            raise MissingData(solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)
    return vals[0][0]

def mle_params(solver_name, pool_name, fold_seed, num_folds, fold_idx,
               by_game, stratified):
    """
    Return the MLE estimate of all parameters for the specified model and
    data fold combination.
    """
    with db_connect() as db:
        jobid = _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)
        c = db.cursor()

        # Choose parameter values associated with the highest training LL
        c.execute(_sql(db,
                       """
                       select p.name, p.value, l.value
                       from mle_parameters p
                       join mle_parameters l on l.restart_idx = p.restart_idx and l.jobid = p.jobid
                       where p.jobid = %s
                       and l.name = 'TRAIN_LL'
                       order by l.value desc
                       """), [jobid])
        vals = c.fetchall()
        c.close()
        if len(vals) == 0:
            raise MissingData(solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)

        ret = {}
        best_train_ll = None
        for name, val, train_ll in vals:
            if best_train_ll is None:
                best_train_ll = train_ll
            elif train_ll <> best_train_ll:
                break
            ret[name] = val

        return ret

# =================================== Utils ===================================

def index_str(solver_name, pool_name, fold_seed, num_folds, fold_idx,
              by_game, stratified):
    return "%s/%s/%s/%s/%s/%s/%s" % (solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)

class MissingData(Exception):
    def __init__(self, solver_name, pool_name, fold_seed, num_folds, fold_idx,
                 by_game, stratified):
        self.solver_name = solver_name
        self.pool_name = pool_name
        self.fold_seed = fold_seed
        self.num_folds = num_folds
        self.fold_idx = fold_idx
        self.by_game = by_game
        self.stratified = stratified

    def __repr__(self):
        return "%s.%s(%s, %s, %s, %s, %s, %s, %s)" % (self.__class__.__module__, self.__class__.__name__,
                                                      repr(self.solver_name), repr(self.pool_name), repr(self.fold_seed), repr(self.num_folds), repr(self.fold_idx), repr(self.by_game), repr(self.stratified))
    def __str__(self):
        return "<MissingData %s>" % index_str(self.solver_name, self.pool_name, self.fold_seed, self.num_folds, self.fold_idx, self.by_game, self.stratified)

def _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified, recursive=False):
    """
    Load the jobid out of the database, creating a new job record if necessary.
    """
    c = db.cursor()
    sql = _sql(db, 'select jobid from mle_jobs'
                   ' where solver_name=%s and pool_name=%s and fold_seed=%s and num_folds=%s and fold_idx=%s and by_game=%s and stratified=%s')
    c.execute(sql, [solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified])
    jobids = c.fetchall()
    if len(jobids) > 1:
        raise ValueError('Multiple jobids for %s/%s/%s/%s/%s/%s/%s: %s' % \
                         (solver_name, pool_name,
                          fold_seed, num_folds, fold_idx, by_game, stratified,
                          jobids))
    elif len(jobids) == 1:
        return jobids[0][0]

    elif recursive:
        raise IOError("Could not create jobid for %s/%s/%s/%s/%s/%s/%s" % \
                         (solver_name, pool_name,
                          fold_seed, num_folds, fold_idx, by_game, stratified))

    sql = _sql(db, 'insert into mle_jobs (solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified) '
                   'values (%s,%s,%s,%s,%s, %s,%s)')
    c.execute(sql, [solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified])
    db.commit()
    return _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified, recursive=True)

class MysqlExitWrapper(object):
    """
    Provide an `__exit__` method for mysql.connector connections.
    """
    def __init__(self, db, paramstyle):
        self.db = db
        self.paramstyle = paramstyle
    def __enter__(self):
        return self
    def __exit__(self, exception_type, exception_value, traceback):
        self.db.close()
    def __getattr__(self, name):
        return getattr(self.db, name)

def db_connect(dbtype=None, dbname=None, host=None, port=None, user=None, passwd=None):
    if dbtype is None:
        dbtype = cfg.db.dbtype
    if dbname is None:
        dbname = cfg.db.dbname
    if host is None:
        host = cfg.db.host
    if port is None:
        port = cfg.db.port
    if user is None:
        user = cfg.db.user
    if passwd is None:
        passwd = cfg.db.passwd
 
    if dbtype == 'sqlite3':
        import sqlite3
        db = sqlite3.connect(dbname)
    elif dbtype == 'mysql':
        import mysql.connector
        db = mysql.connector.connect(user=user, password=passwd, db=dbname, host=host, port=port)
        db = MysqlExitWrapper(db, mysql.connector.paramstyle)
    else:
        raise ValueError("Unknown db_type '%s'" % dbtype)

    return db

def create_schema(db):
    """
    Create all expected tables in ``db``.
    """
    c = db.cursor()
    sql = """
    create table mle_jobs (
    jobid integer primary key %s,
    solver_name varchar(256) not null,
    pool_name varchar(128) not null,
    fold_seed integer not null,
    num_folds integer not null,
    fold_idx integer not null,
    by_game boolean not null default false,
    stratified boolean not null default false
    )
    """
    if db.__class__.__module__ == 'mysql.connector.connection':
        sql = (sql % 'auto_increment')
        sql += 'ENGINE=InnoDB'
    else:
        sql = (sql % 'autoincrement')
    c.execute(sql)

    sql = """
    create index reverse_index on mle_jobs
    (solver_name, pool_name, fold_seed, num_folds, fold_idx)
    """
    c.execute(sql)

    sql = _sql(db, """
    create table mle_parameters (
    jobid integer not null,
    restart_idx integer not null,
    name varchar(64) not null,
    value double not null,
    primary key (jobid, restart_idx, name))
    """)
    if db.__class__.__module__ == 'mysql.connector':
        sql += 'ENGINE=InnoDB'
    c.execute(sql)

    sql = _sql(db, """
    create table mle_checkpoints (
    jobid integer not null,
    restart_idx integer not null,
    rng_state blob(3000) not null,
    primary key (jobid))
    """)
    if db.__class__.__module__ == 'mysql.connector':
        sql += 'ENGINE=InnoDB'
    c.execute(sql)

    db.commit()


def _sql(db, str):
    """
    Convert ``str`` to use qmark style if necessary for ``db``.
    """
    try:
        paramstyle = db.paramstyle
    except:
        mod = sys.modules[db.__class__.__module__]
        mod = sys.modules[mod.__package__]
        paramstyle = mod.paramstyle

    if paramstyle == 'qmark':
        return str.replace('%s', '?')
    else:
        return str

def _binary(db, value):
    """
    Wrap ``value`` in the Binary accessor provided by ``db``'s module.
    """
    mod = sys.modules[db.__class__.__module__]
    mod = sys.modules[mod.__package__]
    return mod.Binary(value)

def _solver(spec):
    """
    Evaluate ``spec`` if necessary to construct a Solver.
    """
    if isinstance(spec, str) or isinstance(spec, unicode):
        # strip "broken" prefix
        if spec[0:len("broken.")] == "broken.":
            warn("stripping 'broken.' from '%s'" % (spec,))
            spec = spec[len("broken."):]
        if spec[-1] == ')':
            return eval(spec, sys.modules)
        else:
            return eval(spec + '()', sys.modules)
    else:
        # Passthrough
        return spec
