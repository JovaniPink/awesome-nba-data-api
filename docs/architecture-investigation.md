# Architecture investigation

_Reviewed: 2026-08-11_

## Decision

Keep this repository as the active, read-only NBA serving service. Evolve it incrementally; do not
replace it with a distributed platform and do not put ingestion or model training in the request
path.

The stack is infrastructure-heavy relative to the two current `Person` endpoints, but it is not
architecturally incoherent. The application has an executable API contract, migrations, request and
database tests, dependency locks, container checks, and a production-shaped non-root image. The
problem is **missing NBA domain depth**, not insufficient infrastructure.

## Question and product goals

The investigation asked whether this service and the sibling `nba-data` and `nba-task-queue`
repositories form the best architecture for an NBA analysis product covering statistics,
economics/finance data, model evaluation, and interactive predictions.

The useful architecture must:

1. preserve source, license, and observation-time lineage;
2. keep raw facts, derived features, model outputs, and evaluations distinguishable;
3. serve a small interactive application predictably;
4. support reproducible offline analysis without committing large mutable datasets to Git;
5. add operational machinery only when a real workload justifies it.

## What exists today

| Area | Evidence in this repository | Assessment |
| --- | --- | --- |
| HTTP contract | Connexion and OpenAPI 3.0.3 in `app/swagger.yaml`; strict parameter and response validation | Good executable boundary |
| Runtime | Uvicorn, Flask/Connexion, SQLAlchemy, Alembic, PostgreSQL 18 | Coherent conventional service stack |
| Public domain | Two read-only `Person` endpoints | Placeholder, not an NBA product vertical |
| Legacy surface | HTML/login scaffolding and `/nbadata` sample route | Retire as real domain routes replace it |
| Background work | No worker or broker | Correct for the current product and workload |
| Verification | Unit/integration tests, API validation, linting, audit, Compose and image checks | Stronger than the current feature set requires, but useful rather than speculative |

The service is therefore **under-modeled and over-scaffolded**, not broadly overengineered. Removing
working migrations, integration tests, or contract validation would save little and increase future
risk. Adding queues, a feature store, a model registry, or microservices now would increase cost
without answering a current product question.

## Repository boundaries

| Repository | Recommended role | Must not become |
| --- | --- | --- |
| `awesome-nba-data` | Curated catalog of sources and tools | Runtime dependency or copied data warehouse |
| `nba-data` | Historical research archive and source-discovery reference | Live ingestion system or authoritative current dataset |
| `awesome-nba-data-api` | Active serving boundary and initial home for governed batch jobs | Scraper in the request path or training cluster |
| `nba-task-queue` | Superseded design record; archive candidate | Deployed broker/worker platform without a job contract |

Keep the first production batch jobs in this repository, as a separate package and deployment
command, until their release cadence or ownership genuinely diverges. A repository boundary is an
operational commitment, not a substitute for a Python module boundary.

## Target data flow

```text
approved sources
  -> bounded batch acquisition
    -> immutable raw objects + manifest/checksum (outside Git)
      -> Polars/DuckDB validation and transformations
        -> curated PostgreSQL facts and feature snapshots
          -> offline training/evaluation
            -> versioned model artifacts and precomputed predictions
              -> read-only API
                -> web application
```

PostgreSQL remains the serving store. Parquet is the interchange/archive format for larger
analytical tables; DuckDB and Polars can query and transform those files without forcing a separate
warehouse into the first release. Model artifacts may start with a manifest and object URI. Add a
model registry only after artifact promotion, rollback, and multi-environment lineage are real
problems.

## Domain and lineage contract

The first NBA resource should carry enough context to be reproducible. Exact fields depend on the
vertical, but the contract should represent:

- stable source and provider identifiers;
- source URL or dataset identifier and terms URL;
- event time, observed-at time, and ingested-at time;
- season and game identifiers without assuming one provider's ID is universal;
- raw-object or snapshot lineage;
- transformation version for derived values;
- model version, feature cutoff, raw probability, and calibrated probability for predictions;
- correction/supersession state instead of silent overwrite.

Game facts, market/economic facts, features, predictions, and evaluations should not share one
ambiguous table merely because they all have a game ID. Their different time and provenance
semantics are product behavior, not metadata decoration.

## API evolution

1. Select one thin vertical, such as games and team box scores. Confirm source rights before
   acquisition.
2. Define provider-neutral IDs and observation-time lineage.
3. Add a migration, OpenAPI contract, read-only handlers, fixtures, and request/database tests in one
   change.
4. Add keyset pagination only when list size makes offset pagination measurably inadequate.
5. Remove the `Person`, login-page, and sample-blueprint scaffolding when no longer used.
6. Preserve the OpenAPI 3 contract and its request/response validation as real NBA resources replace
   the placeholder people surface.

Nginx is optional for local development and may eventually become a deployment-profile concern.
It is not currently the major source of complexity, so removing it is lower value than creating a
real domain contract.

## Asynchronous-work decision gate

Default to synchronous reads and precomputed results. Offline ingestion and training should run as
scheduled, bounded commands. Add a durable asynchronous user-job API only when all of these exist:

- a request regularly exceeds the chosen HTTP latency budget and cannot be cached/precomputed;
- the job has a durable input/output schema and idempotency key;
- retry, timeout, cancellation, retention, and failure ownership are defined;
- the API can return `202 Accepted` with a durable job resource or status URL;
- metrics establish expected rate, duration, concurrency, and payload size;
- deployment and on-call ownership for the worker and queue are accepted.

Start with the smallest mechanism that meets those facts. A PostgreSQL-backed job table can support
a modest queue-like workload, with careful locking and retry semantics. Celery and RabbitMQ remain
valid later choices, but they do not create reliability automatically: tasks can be redelivered, so
side effects must be idempotent.

## Source and licensing gate

The technical ability to call an endpoint does not establish reuse rights. The current NBA terms
restrict how NBA statistics may be used and specifically reserve several commercial, comprehensive,
fantasy, and gambling-related uses. Sports Reference separately restricts automated collection that
affects its services and use of its content for machine learning. Before a source enters a batch
job, record the approved purpose, terms URL, attribution, retention, redistribution, and automation
conditions.

`nba_api` is an actively maintained community client, not an official data license or stability
guarantee. Recent releases record endpoint deprecations and header fixes, so pin the dependency and
protect each used endpoint with acquisition contract tests.

## Alternatives considered

| Alternative | Decision | Reason |
| --- | --- | --- |
| Rewrite as a new framework/service | Reject | No evidence that the current service boundary is the bottleneck |
| Restore Celery/RabbitMQ now | Reject | No runnable asynchronous job, throughput evidence, or operations contract |
| Make `nba-data` the live pipeline | Reject | It is a non-reproducible historical corpus with unresolved provenance |
| Commit future raw data to Git | Reject | Poor fit for large, mutable, rights-constrained artifacts |
| Add a separate warehouse immediately | Defer | Parquet + DuckDB/Polars + PostgreSQL covers the initial scale |
| Add deep learning to interactive requests | Reject | Training and evaluation belong offline; predictions should be versioned and precomputed |

## Definition of ready for the first vertical

- Source use is approved and documented.
- Acquisition is bounded, retryable, and records a manifest/checksum.
- Raw and curated schemas distinguish event time from observation time.
- The API contract is provider-neutral and read-only.
- Fixtures cover duplicates, corrections, missing values, and upstream schema drift.
- CI executes the migration and endpoint tests against PostgreSQL.
- The web client can identify data freshness and model version from the response.

## Primary references

- [NBA Terms of Use](https://www.nba.com/termsofuse)
- [NBA Stats glossary](https://www.nba.com/stats/help/glossary)
- [Sports Reference data use](https://www.sports-reference.com/data_use.html)
- [`nba_api` project](https://github.com/swar/nba_api) and [release history](https://github.com/swar/nba_api/releases)
- [Connexion documentation](https://connexion.readthedocs.io/en/stable/)
- [OpenAPI specification versions](https://spec.openapis.org/oas/)
- [DuckDB Parquet support](https://duckdb.org/docs/stable/data/parquet/overview)
- [Polars lazy API](https://docs.pola.rs/user-guide/lazy/using/)
- [HTTP `202 Accepted` semantics (RFC 9110)](https://www.rfc-editor.org/rfc/rfc9110.html#name-202-accepted)
- [Celery task idempotency and acknowledgements](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [RabbitMQ reliability guide](https://www.rabbitmq.com/docs/reliability)
