# Robot Example
## What the example is for
The provided cases are meant to show how the Viihde APIs can be called.
Especially the user authentication might be a tricky proposition to start with no reference.

## How to use
First, make sure you have Python and pip installed (Python 2, unfortunately)

Then, install Robot Framework
```shell
pip install robotframework
```
Open api-elisa-viihde-cases.robot in your editor of choice and fill in the parameters as you see fit.
Mandatory parameters are `username` and `password`; you can use whatever valid Elisa Viihde user.

Open ApiElisaViihdeLibrary.py and fill in the parameter `external_api_key` with the API key you received from Elisa

> **N.B.** the provided `username` and `password` are for example only and should be replaced!

Run the cases with
```shell
robot --loglevel=debug api-elisa-viihde-cases.robot
```
If all the stars are aligned, all cases should pass and a log file will be generated from which you can see more info.
