"""
Interface for saving/restoring values from the database.
"""
from __future__ import absolute_import
import sys
import bogota.cfg as cfg

# =================================== Saving ==================================

def save_mle_param(parameter_name, parameter_value, restart_idx,
                   solver_name, pool_name, fold_seed, num_folds, fold_idx,
                   by_game, stratified):
    with db_connect() as db:
        # TODO
        pass

# ================================== Loading ==================================

def mle_restarts(solver_name, pool_name, fold_seed, num_folds, fold_idx,
                 by_game, stratified):
    """
    Return a list of completed restart indices for the specified model and data
    fold combination.
    """
    with db_connect() as db:
        jobid = _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified)
        c = db.cursor()

        # Choose parameter value associated with the highest training LL
        c.execute(_sql(db,
                       """
                       select restart_idx
                       from mle_parameters
                       where jobid = %s
                       order by restart_idx asc
                       """), [jobid])
        vals = c.fetchall()
        return map(lambda x: x[0], vals)

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

def _ensure_jobid(self, db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified, recursive=False):
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
        self.jobid = jobids[0][0]

    elif recursive:
        raise IOError("Could not create jobid for %s/%s/%s/%s/%s/%s/%s" % \
                         (solver_name, pool_name,
                          fold_seed, num_folds, fold_idx, by_game, stratified))

    sql = _sql(db, 'insert into mle_jobs (solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified) '
                   'values (%s,%s,%s,%s,%s, %s,%s)')
    c.execute(sql, [solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified])
    db.commit()
    return _ensure_jobid(db, solver_name, pool_name, fold_seed, num_folds, fold_idx, by_game, stratified, recursive=True)

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
    mod = sys.modules[db.__class__.__module__]
    mod = sys.modules[mod.__package__]
    if mod.paramstyle == 'qmark':
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
            print "stripping 'broken.' from '%s'" % (spec,)
            spec = spec[len("broken."):]
        if spec[-1] == ')':
            return eval(spec, sys.modules)
        else:
            return eval(spec + '()', sys.modules)
    else:
        # Passthrough
        return spec
