## Must have

- [ ] Apply topic
- [ ] Development documentation
- [ ] Schema enforcement on streams
- [ ] Schema enforcement on tables
- [x] Apply sink
- [x] Schema creation on connect
- [x] Dependencies check (installed connnectors, UDFs, topics)
- [x] Apply streams (based on raw sql)
- [x] Jinga2 templates  
- [x] Debug command
- [x] Apply source
- [x] Dump command
- [x] Define schema (to be referenced by topics etc)

## Should have

- [ ] Topics creation with AVRO schema
- [ ] Connector can produce multiple named topics and schemas (eg JDBC)
- [ ] Automatic ordering of resources creation (dependencies tree)
- [ ] Handle case in which a stream becomes a table and vice versa
- [ ] Kafka run query
- [ ] Kafka consume message
- [ ] Schema enforcement (for connectors and streams, evaluate if topics need to be created with Avro schema separately)

## Nice to have

- [ ] Apply topics
- [ ] Apply tables (with pre-populated data) 

## Validation

- [ ] Do not support multiple sql statement in queries (it should be ok with safe sql builder already).
- [ ] Connector name follows topic name
- [ ] Rules can be disabled
- [x] Connector class installed
