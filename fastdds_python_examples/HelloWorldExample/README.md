# Python binding HelloWorldExample

This example implements a basic publication/subscription application.
In order to launch the example it is required to indicate if the application is run as publisher or subcriber.
Therefore, open two terminals and move to the folder where the Python script is located.
On the first terminal run the publisher executing the following command:

```bash
python3 HelloWorldExample.py -p publisher
```

On the second terminal run the subscriber as follows:

```bash
python3 HelloWorldExample.py -p subscriber
```

After launching the publisher application, the publisher will wait until discovering a subscriber, before sending the samples.
Once the subscriber is discovered the samples are sent.
The QoS settings are by default: BEST_EFFORT and VOLATILE.
Consequently, some samples may be lost if the publisher discovers the subscriber earlier.
Also, when the publisher sends the last sample, it is destroyed and the samples are removed from the history.
Therefore, sometimes the last samples are also not received depending on the network performance.

## Parameters

This example allows the following parameters:

* `--parameter`/`-p`: whether the application is run as publisher or subscriber. This parameter is required always.
* `--domain`/`-d`: domain ID where the application is run. This parameter is optional. In case that it is not provided by the user, domain ID will be 0.
* `--machine`/`-m`: distinguish between different publishing applications. This parameter only applies if the application is run as publisher.
