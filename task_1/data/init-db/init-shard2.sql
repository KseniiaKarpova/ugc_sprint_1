CREATE DATABASE IF NOT EXISTS shard;
CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE IF NOT EXISTS shard.events (
      id UUID DEFAULT generateUUIDv4(),
      user_id UUID,
      film_id UUID,
      action String,
      created_at DateTime('Europe/Moscow')
      )
      Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/events', 'replica_1') PARTITION BY toYYYYMMDD(created_at) ORDER BY id;

CREATE TABLE IF NOT EXISTS replica.events (
      id UUID DEFAULT generateUUIDv4(),
      user_id UUID,
      film_id UUID,
      action String,
      created_at DateTime('Europe/Moscow')
      )
      Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/events', 'replica_2') PARTITION BY toYYYYMMDD(created_at) ORDER BY id;

CREATE TABLE IF NOT EXISTS default.events (
      id UUID DEFAULT generateUUIDv4(),
      user_id UUID,
      film_id UUID,
      action String,
      created_at DateTime('Europe/Moscow')
      )
      ENGINE = Distributed('company_cluster', '', events, rand());
