# app/core/tracing/tracer.py

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.jaeger.thrift import JaegerExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


def setup_tracing(app):

    resource = Resource.create({
        "service.name": "fastapi-realworld-app"
    })

    provider = TracerProvider(resource=resource)

    jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
    )

    processor = BatchSpanProcessor(jaeger_exporter)

    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    # Auto instrumentation
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()

    return trace.get_tracer(__name__)
