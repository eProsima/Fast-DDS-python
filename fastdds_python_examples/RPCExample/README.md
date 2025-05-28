# Python binding CalculatorExample

This example implements a basic client/server RPC application.
In order to launch the example it is required to indicate if the application is run as client or server.
Therefore, open two terminals and move to the folder where the Python script is located.
On the first terminal run the server executing the following command:

```bash
python3 CalculatorExample.py -p server
```

On the second terminal run the client as follows:

```bash
python3 CalculatorExample.py -p client
```

The client application waits for two seconds for the server to be discovered, and then performs several RPC calls.
For each call, the operation result is shown.
On the server application, the GUID of the client and the requested operation is shown for each processed request.

## Parameters

This example allows the following parameters:

* `--parameter`/`-p`: whether the application is run as client or server. This parameter is required.
* `--domain`/`-d`: domain ID where the application is run. This parameter is optional. In case that it is not provided by the user, domain ID will be 0.
* `--server_threads`/`-t`: the number of threads for processing requests (defaults to 1). This parameter only applies if the application is run as server.
