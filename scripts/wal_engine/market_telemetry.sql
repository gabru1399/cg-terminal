-- Initialize on a local filesystem. Reapply connection-level pragmas on open.
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA foreign_keys = ON;
PRAGMA busy_timeout = 3000;

BEGIN IMMEDIATE;

-- Short, append-only revision ring. One materializer writes each completed
-- feature bundle in a transaction. Select newest arrival <= the round cutoff.
-- observed_ms is source/effective time. received_ms is the local ingest time.
CREATE TABLE IF NOT EXISTS latest_feature (
    revision INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id TEXT NOT NULL,
    dimension INTEGER NOT NULL,
    observed_ms INTEGER NOT NULL CHECK(observed_ms >= 0),
    received_ms INTEGER NOT NULL CHECK(received_ms >= observed_ms),
    state TEXT NOT NULL CHECK(state IN ('VALID','FAILED','INSUFFICIENT_COVERAGE','UNSUPPORTED')),
    body TEXT NOT NULL CHECK(json_valid(body) AND json_type(body) = 'object'),
    CHECK((asset_id = '@runtime' AND dimension = 0)
       OR (asset_id <> '@runtime' AND dimension BETWEEN 1 AND 16))
) STRICT;

CREATE INDEX IF NOT EXISTS latest_feature_at_cutoff
    ON latest_feature(asset_id, dimension, received_ms DESC, revision DESC);

CREATE TABLE IF NOT EXISTS round (
    round_id TEXT PRIMARY KEY,
    nonce TEXT NOT NULL UNIQUE,
    cutoff_ms INTEGER NOT NULL,
    expires_ms INTEGER NOT NULL CHECK(expires_ms > cutoff_ms),
    digest TEXT NOT NULL UNIQUE CHECK(length(digest) = 64),
    envelope TEXT NOT NULL CHECK(json_valid(envelope) AND json_type(envelope) = 'object'),
    cell_count INTEGER NOT NULL CHECK(cell_count > 0),
    state TEXT NOT NULL CHECK(state IN ('AUDIT_INCOMPLETE','AUDIT_COMPLETE_NO_CANDIDATES',
                                      'AUDIT_COMPLETE_CANDIDATES')),
    CHECK(json_extract(envelope, '$.digest') IS digest),
    CHECK(json_extract(envelope, '$.payload.round_id') IS round_id)
) STRICT, WITHOUT ROWID;

-- Coverage index into the authoritative signed envelope. The copied digest
-- covers the full materialized cell, including provenance and evidence data.
CREATE TABLE IF NOT EXISTS round_cell (
    round_id TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    dimension INTEGER NOT NULL CHECK(dimension BETWEEN 1 AND 16),
    state TEXT NOT NULL CHECK(state IN ('VALID','NOT_APPLICABLE','MISSING','STALE',
                                       'FAILED','INSUFFICIENT_COVERAGE','UNSUPPORTED_REQUIRED')),
    observed_ms INTEGER,
    received_ms INTEGER,
    cell_digest TEXT NOT NULL CHECK(length(cell_digest) = 64),
    PRIMARY KEY(round_id, asset_id, dimension),
    FOREIGN KEY(round_id) REFERENCES round(round_id) ON DELETE RESTRICT
) STRICT, WITHOUT ROWID;

CREATE TRIGGER IF NOT EXISTS latest_feature_no_rewrite
BEFORE UPDATE ON latest_feature BEGIN
    SELECT RAISE(ABORT, 'insert a new feature revision');
END;

CREATE TRIGGER IF NOT EXISTS round_no_update
BEFORE UPDATE ON round BEGIN SELECT RAISE(ABORT, 'sealed round'); END;

CREATE TRIGGER IF NOT EXISTS round_no_delete
BEFORE DELETE ON round BEGIN SELECT RAISE(ABORT, 'sealed round'); END;

CREATE TRIGGER IF NOT EXISTS round_no_replace
BEFORE INSERT ON round
WHEN EXISTS (SELECT 1 FROM round WHERE round_id = NEW.round_id
             OR nonce = NEW.nonce OR digest = NEW.digest)
BEGIN SELECT RAISE(ABORT, 'sealed round'); END;

CREATE TRIGGER IF NOT EXISTS round_cell_no_update
BEFORE UPDATE ON round_cell BEGIN SELECT RAISE(ABORT, 'sealed round cell'); END;

CREATE TRIGGER IF NOT EXISTS round_cell_no_delete
BEFORE DELETE ON round_cell BEGIN SELECT RAISE(ABORT, 'sealed round cell'); END;

CREATE TRIGGER IF NOT EXISTS round_cell_no_replace
BEFORE INSERT ON round_cell
WHEN EXISTS (SELECT 1 FROM round_cell WHERE round_id = NEW.round_id
             AND asset_id = NEW.asset_id AND dimension = NEW.dimension)
BEGIN SELECT RAISE(ABORT, 'sealed round cell'); END;

PRAGMA user_version = 1;
COMMIT;
