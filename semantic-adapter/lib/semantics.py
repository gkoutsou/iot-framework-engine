__author__ = 'ehonlia'

from time import time

from elasticsearch import Elasticsearch
from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, URIRef, XSD, OWL
from decimal import Decimal

from constants import SSN, DUL, GEO, SAO, CT, PROV, TL, UCUM, ID, METADATA
from util import lucene_escape

__INDEX = 'sensorcloud'
__SOURCE = '_source'
__ID = '_id'
__HITS = 'hits'


def __connect():
    return Elasticsearch([{'host': 'localhost', 'port': 9200}])


def mapping():
    es = __connect()

    return es.indices.get_mapping(index=__INDEX)


def __semantic_stream(g, stream, id):
    stream_node = URIRef(id)

    g.add((stream_node, RDF.type, SSN.Sensor))
    g.add((stream_node, RDF.type, FOAF.Person))
    g.add((stream_node, RDF.ID, Literal(id)))

    accuracy = BNode()
    g.add((accuracy, RDF.type, SSN.Accuracy))
    g.add((accuracy, DUL.hasDataValue, Literal(stream['accuracy'])))
    g.add((stream_node, SSN.hasMeasurementProperty, accuracy))

    deployment = BNode()
    g.add((deployment, RDF.type, SSN.Deployment))
    g.add((deployment, DUL.hasEventDate, Literal(stream['creation_date'], datatype=XSD.date)))
    g.add((stream_node, SSN.hasDeployment, deployment))

    g.add((stream_node, FOAF.depiction, Literal(stream['description'])))

    a,b = stream['location'].split(',')
    location = BNode()
    g.add((location, RDF.type, GEO.Point))
    g.add((location, GEO.hasDataValue, Literal(a)))
    g.add((stream_node, FOAF.based_near, location))
    g.add((location, RDF.type, GEO.Point))
    g.add((location, GEO.hasDataValue, Literal(b)))
    g.add((stream_node, FOAF.based_near, location))

    observation = BNode()
    g.add((observation, RDF.type, SSN.Observation))
    g.add((observation, DUL.hasEventDate, Literal(stream['last_updated'], datatype=XSD.dateTime)))
    g.add((stream_node, SSN.madeObservation, observation))

    g.add((stream_node, FOAF.name, Literal(stream['name'])))

    g.add((stream_node, SSN.observes, Literal(stream['type'])))

    # theFeatureOfInterest = BNode()

    # g.add((observation, SSN.featureOfInterest, theFeatureOfInterest)
    # g.add((stream_node, SSN.observes, observation)))

    unit = BNode()
    g.add((unit, RDF.type, DUL.UnitOfMeasure))
    g.add((unit, DUL.hasParameterDataValue, Literal(stream['unit'])))
    g.add((stream_node, SSN.hasProperty, unit))

    maker = BNode()
    g.add((maker, RDF.type, FOAF.Person))
    g.add((maker, RDF.ID, Literal(stream['user_id'])))
    g.add((stream_node, FOAF.maker, maker))


def __create_stream_graph():
    g = Graph()
    g.bind('ssn', SSN)
    g.bind('dul', DUL)
    g.bind('foaf', FOAF)
    g.bind('geo', GEO)
    return g


def semantic_stream(stream, output_format='n3'):
    g = __create_stream_graph()
    __semantic_stream(g, stream[__SOURCE], stream[__ID])
    return stream[__ID], g.serialize(format=output_format)


def semantic_streams(output_format='n3', params=None):
    es = __connect()

    results = es.search(index=__INDEX, doc_type='stream', params=params)

    streams = []
    for item in results[__HITS][__HITS]:
        g = __create_stream_graph()
        __semantic_stream(g, item[__SOURCE], item[__ID])
        streams.append({ID: item[__ID], METADATA: g.serialize(format=output_format)})

    return streams


def semantic_streams_combined(output_format='n3', params=None):
    es = __connect()

    results = es.search(index=__INDEX, doc_type='stream', params=params)

    g = __create_stream_graph()

    for item in results[__HITS][__HITS]:
        __semantic_stream(g, item[__SOURCE], item[__ID])

    return g.serialize(format=output_format)


def __semantic_virtual_stream(g, stream, id):
    stream_node = URIRef(id)

    g.add((stream_node, RDF.type, SSN.Sensor))
    g.add((stream_node, RDF.type, FOAF.Person))
    g.add((stream_node, RDF.type, FOAF.Group))
    g.add((stream_node, RDF.ID, Literal(id)))

    deployment = BNode()
    g.add((deployment, RDF.type, SSN.Deployment))
    g.add((deployment, DUL.hasEventDate, Literal(stream['creation_date'], datatype=XSD.date)))
    g.add((stream_node, SSN.hasDeployment, deployment))

    g.add((stream_node, FOAF.depiction, Literal(stream['description'])))

    observation = BNode()
    g.add((observation, RDF.type, SSN.Observation))
    g.add((observation, DUL.hasEventDate, Literal(stream['last_updated'], datatype=XSD.dateTime)))
    g.add((stream_node, SSN.madeObservation, observation))

    g.add((stream_node, FOAF.name, Literal(stream['name'])))

def __create_virtual_stream_graph():
    g = Graph()
    g.bind('ssn', SSN)
    g.bind('foaf', FOAF)
    return g


def semantic_virtual_stream(stream, output_format='n3'):
    g = __create_virtual_stream_graph()
    __semantic_virtual_stream(g, stream[__SOURCE], stream[__ID])
    return stream[__ID], g.serialize(format=output_format)


def semantic_virtual_streams(output_format='n3', params=None):
    es = __connect()

    results = es.search(index=__INDEX, doc_type='virtual_stream', params=params)

    virtual_streams = []
    for item in results[__HITS][__HITS]:
        g = __create_virtual_stream_graph()
        __semantic_virtual_stream(g, item[__SOURCE], item[__ID])
        virtual_streams.append({ID: item[__ID], METADATA: g.serialize(format=output_format)})

    return virtual_streams


def semantic_virtual_streams_combined(output_format='n3', params=None):
    es = __connect()

    results = es.search(index=__INDEX, doc_type='virtual_stream', params=params)

    g = __create_virtual_stream_graph()

    for item in results[__HITS][__HITS]:
        __semantic_virtual_stream(g, item[__SOURCE], item[__ID])

    return g.serialize(format=output_format)


def __semantic_datapoint(g, datapoint, id):
    datapoint_node = URIRef(id)

    g.add((datapoint_node, RDF.type, SSN.SensorOutput))
    g.add((datapoint_node, RDF.ID, Literal(id)))

    sensor = BNode()
    g.add((sensor, RDF.type, SSN.Sensor))
    g.add((sensor, RDF.ID, Literal(datapoint['stream_id'])))
    g.add((datapoint_node, SSN.isProducedBy, sensor))

    value = BNode()
    g.add((value, RDF.type, SSN.ObservationValue))
    g.add((value, DUL.hasDataValue, Literal(datapoint['value'])))
    g.add((datapoint_node, SSN.hasValue, value))

    g.add((datapoint_node, DUL.hasEventDate, Literal(datapoint['timestamp'], datatype=XSD.dateTime)))


def __create_datapoint_graph():
    g = Graph()
    g.bind('ssn', SSN)
    g.bind('dul', DUL)
    return g


def semantic_datapoint(datapoint, output_format='n3'):
    g = __create_datapoint_graph()
    __semantic_datapoint(g, datapoint[__SOURCE], datapoint[__ID])
    return datapoint[__ID], g.serialize(format=output_format)


def semantic_datapoints(output_format='n3', doc_type='datapoint', params=None):
    es = __connect()

    results = es.search(index=__INDEX, doc_type=doc_type, params=params)

    datapoints = []
    for item in results[__HITS][__HITS]:
        g = __create_datapoint_graph()
        __semantic_datapoint(g, item[__SOURCE], item[__ID])
        datapoints.append({ID: item[__ID], METADATA: g.serialize(format=output_format)})

    return datapoints


def semantic_datapoints_combined(output_format='n3', doc_type='datapoint', params=None):
    es = __connect()

    results = es.search(index=__INDEX, doc_type=doc_type, params=params)

    g = __create_datapoint_graph()

    for item in results[__HITS][__HITS]:
        __semantic_datapoint(g, item[__SOURCE], item[__ID])

    return g.serialize(format=output_format)


def __fix_params(params, id):
    import copy

    if params is not None:
        new_params = copy.deepcopy(params.copy())
    else:
        new_params = dict()

    sort_by_timestamp = 'timestamp:asc'
    if not new_params.has_key('sort'):
        new_params['sort'] = sort_by_timestamp
    elif new_params['sort'].find(sort_by_timestamp) == -1:
        new_params['sort'] += ',' + sort_by_timestamp

    stream_id_query = 'stream_id:' + lucene_escape(id)
    if not new_params.has_key('q'):
        new_params['q'] = stream_id_query
    else:
        new_params['q'] += ' AND ' + stream_id_query
    return new_params


def __create_datapoint_graph_citypulse():
    g = Graph()
    g.bind('ssn', SSN)
    g.bind('sao', SAO)
    g.bind('ct', CT)
    g.bind('prov', PROV)
    g.bind('tl', TL)
    g.bind('ucum', UCUM)
    return g


def __semantic_point_citypulse(g, datapoint, id, stream, stream_node):
    point = URIRef('_'.join(['point', id, str(int(time()))]))
    g.add((point, RDF.type, SAO.Point))

    timestamp = BNode()
    g.add((timestamp, RDF.type, TL.Instant))
    g.add((timestamp, TL.at, Literal(datapoint['timestamp'], datatype=XSD.dateTime)))

    g.add((point, SAO.time, timestamp))
    g.add((point, SAO.value, Literal(datapoint['value'])))

    unit = stream['unit']
    type = stream['type']
    if unit == "celsius":
	unit = "degree-Celsius"
    if unit == "Fahrenheit":
	unit = "degree-Fahrenheit"

    if unit != '':
        unit_node = UCUM.term(unit)
    else:
        unit_node = BNode()
        g.add((unit_node, RDF.type, OWL.Nothing))
    g.add((point, SAO.hasUnitOfMeasurement, unit_node))

    if type != '':
        type_node = UCUM.term(type)
    else:
        type_node = BNode()
        g.add((type_node, RDF.type, OWL.Nothing))
    g.add((point, SSN.observedProperty, type_node))

    g.add((point, SSN.featureOfInterest, stream_node))

    return point


def __semantic_stream_event_citypulse(g, id):
    stream_event = URIRef('_'.join(['stream_event', id, str(int(time()))]))
    g.add((stream_event, RDF.type, SAO.StreamEvent))
    return stream_event


def update_time(g, stream_event, results):
    start = results[0][__SOURCE]['timestamp']
    end = results[-1][__SOURCE]['timestamp']

    interval = BNode()
    g.add((interval, RDF.type, TL.Interval))
    g.add((interval, TL.start, Literal(start, datatype=XSD.dateTime)))
    g.add((interval, TL.end, Literal(end, datatype=XSD.dateTime)))

    g.add((stream_event, SAO.time, interval))


def __semantic_stream_citypulse(g, id):
    es = __connect()

    results = es.search(index=__INDEX, doc_type='stream', params={'q': '_id:' + lucene_escape(id)})
    stream = results[__HITS][__HITS][0][__SOURCE]

    stream_node = URIRef('_'.join(['stream', id, str(int(time()))]))
    g.add((stream_node, RDF.type, SSN.FeatureOfInterest))

    first_node = BNode()
    g.add((first_node, RDF.type, CT.Node))
    a,b = stream['location'].split(',')
    g.add((first_node, CT.hasLatitude, Literal(Decimal(a))))
    g.add((first_node, CT.hasLongtitude, Literal(Decimal(b))))
    g.add((first_node, CT.hasNodeName, Literal(stream['name'])))

    g.add((stream_node, CT.hasFirstNode, first_node))

    return stream, stream_node


def semantic_datapoints_citypulse(id, output_format='n3', doc_type='datapoint', params=None):
    es = __connect()

    new_params = __fix_params(params, id)

    results = es.search(index=__INDEX, doc_type=doc_type, params=new_params)

    g = __create_datapoint_graph_citypulse()

    if len(results[__HITS][__HITS]) != 0:
        stream_event = __semantic_stream_event_citypulse(g, id)
        stream, stream_node = __semantic_stream_citypulse(g, id)

        for item in results[__HITS][__HITS]:
            point = __semantic_point_citypulse(g, item[__SOURCE], item[__ID], stream, stream_node)
            g.add((stream_event, PROV.used, point))

        update_time(g, stream_event, results[__HITS][__HITS])

    return g.serialize(format=output_format)


if __name__ == '__main__':
    print semantic_datapoints_citypulse('HiqjRxrdSlaRyIAki4gQog', 'n3', params={
        'q': 'timestamp:[2013-12-04T17:42:22.000 TO 2013-12-04T18:43:22.000]',
        'from': 0, 'size': 100})
