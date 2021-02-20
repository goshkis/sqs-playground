

Will the endpoint be frontended by proxy/API Gateway?
Yes. But include some error codes masking for ilustrative purposes. 

What about error messages generalizing? Should I think about it here?
No. Passthrough the ones that makes sense or can be useful for testing\debugging.

We'll be getting base usage and health metrics from standard SQS monitoring. Should I think about extra logging?
You may want to. If you see obvious reasons helping with ops or testing - please go ahead.

In this case, is local-only logging fine?
Yes. Outline logging strategy though.

Any preference on queue type?
No. Standard is fine. (That means no strict ordering and "at-least-once" delivery guarantee)
