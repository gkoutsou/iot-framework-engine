## Semantic Adapter for IoT Framework

### Used API of IoT Frameworks

* Get all streams

  http://axondev.cf.ericsson.net:8000/streams

* Get a specified stream

  http://axondev.cf.ericsson.net:8000/streams/FFqNysD8Qqe18BNUAEphkA

* Get all data of the specified stream

  http://axondev.cf.ericsson.net:8000/streams/FFqNysD8Qqe18BNUAEphkA/data


### Preparation

* Install elasticsearch

  http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/setup-repositories.html

### Mapping

```
Stream -> ssn:Sensor
  accuracy -> ssn:Accuracy
  active -> ???
  creation_date -> ssn:hasDeployment
  data_type -> ??? (applicaton/json, maybe not needed)
  description -> foaf:depiction
  history_size -> ???
  last_updated -> ssn:Observation
  location -> foaf:based_near
  # we need to add two properties to express
  # min/max value because SSN doesn't define it.
  # http://www.w3.org/2005/Incubator/ssn/wiki/SSN_Smart_product
  max_val, min_val -> ssn:MeasurementRange  
  name -> foaf:name
  nr_subscribers -> ???
  parser -> ???
  polling -> ???
  polling_freq -> ssn:Frequency
  private -> ???
  quality -> DUL:Quality
  resource -> ???
  subscribers -> ???
  tags -> ???
  # shall we model all observations?
  type -> ssn:observes
  unit -> UnitOfMeasure
  uri -> foaf:homepage
  user_id -> foaf:maker
  user_ranking -> ???
```

```
Virtual Stream -> ssn:Sensor
  creation_date -> ssn:hasDeployment
  description -> foaf:depiction
  function -> ???
  group -> ???
  history_size -> ???
  last_updated -> ssn:Observation
  name -> foaf:name
  nr_subscribers -> ???
  private -> ???
  streams_involved -> foaf:member
  subscribers -> ???
  tags -> ???
  user_id -> foaf:maker
  user_ranking -> ???
```

```
Data Point -> ssn:SensorOutput
  stream_id -> ssn:isProducedBy
  timestamp -> hasEventDate
  value -> ssn:ObservationValue
```

```
Virtual Stream Data Point -> ssn:SensorOutput
  stream_id -> ssn:isProducedBy
  timestamp -> hasEventDate
  value -> ssn:ObservationValue
```