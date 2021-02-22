# Task and notes

## Task

- Write a queue-writer service
    - The service should expose a REST API endpoint to define the message contents
    - The service should write the message to an SQS Queue

- Write a queue-processor service for the SQS Queue
    - The service reads messages from the queue
    - The service should ideally handle batching, concurrent processing, error conditions etc.

Should have:

- Unit tests
- Functional documentation (README)

Programming language: python or golang


## Questions
**NOTE:** Those are mainly my answers/decisions.

> Any preference on queue type?

No. Standard is fine. 

> That means no strict ordering and "at-least-once" delivery guarantee. Can we "significantly" delay some messages in favor of overall availability or experience?

Yes, we can.

> What time will it take to process one message? I need to estimate queue parameters.

Around 0.1s.

> Who is a client for this API, external users or some internal server?

External users

> Will the endpoint be frontended by proxy/API Gateway? This way I'll not think about, say, error code masking, or other typical actions.

Yes. But include something to give an idea of what you expect from this layer. 

> What about error messages generalizing? Should I think about it here?

No. Passthrough the ones that makes sense or can be useful for testing\debugging.

> We'll be getting base usage and health metrics from standard SQS monitoring. Should I think about extra logging?

You may want to. If you see obvious reasons helping with ops or testing - please go ahead.

> In this case, is local-only logging fine?

Yes.


## What I'm NOT touching in this exercise

While it's clear that this is just a test assignment, I think it's worth mentioning connected topics that I'm purposely avoiding.

1. AuthN/AuthZ, any service-to-service trust questions, OBO schemes, etc.
2. Ops\health metrics and monitoring beyond trivial.
3. Service lifecycle, deployment, upgrades, patching, etc.
4. Methods to ensure meeting availability requirements.
5. API versioning
6. LB and scaling strategy


## What could be a high-level test and quality assurance strategy?

1. Wash your hands
    1. Nail the basics: ensure base systems are not sources of pain to devs (regular build or test failures due to issues with these systems, etc).
    2. Unit plus functional tests suitable for dev environments (resource and exec time constrains)
    3. Commit-triggered tests. Can take longer, and more resources. Could be e2e with load from traffic generators (comparative perf or resource consumption data).
    4. Canaries executing public APIs
    5. Tack and bubble up quality metrics. Quality metrics should be easily available. Things like deployment success ratio per service should not require one engineering day to obtain.
2. Play with evil carefully
    1. Pre-prod integration environment. Dogfood program, duplicating life traffic to this environment, etc to ensure enough pain is being received. Remember: more or longer tests is not necessary leads to a better quality or customer satisfaction. 
    2. Auto-deploy strategy with aim to provide feedback as fast as possible.
3. There are known unknowns
    1. Exploratory with aim to identify unmonitored resources or components that could or are affecting availability or quality of service.

