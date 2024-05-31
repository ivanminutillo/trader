# Frontend Development Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Frontend Compoenent Specification](#frontend-specification)
3. [Agent Configuration](#agent-configuration)
4. [Roadmap](#roadmap)

## Introduction
The purpose the frontend loader ui ABCI is to provide an easy means for frontend developers the ability to create and co-own frontends to be served by Agents.

This represents a new way to interact with agents and services, by providing a frontend that can be served by the agent.

Additionally, as this should enable a much broader range of applications and services to be built on top of the agents, as now additional languages other than the underlying python can be used within Olas EcoSystem.

The enables developers other than python developers to benefit from the developer incentives enabled by the Olas Protocol.

The ABCI frontend loader is designed to not interfer with agent development and applications, but rather to allow services to be augmented with a frontend.

The frontend components are defined as `custom_components` and are loaded by the frontend loader.

Please see [Tatha's Trader UI](../packages/tatha/customs/trader_ui)

### Current Features.

- Generate routes from the `build` directory.
- enable `API` routes from the `openapi3_spec.yaml` file.
- ABCI spec with healthcheck for the served frontend.

```yaml
alphabet_in:
  - DONE
  - ERROR

default_start_state: SetupRound

final_states:
  - DoneRound

label: ComponentLoadingAbciApp

start_states:
  - SetupRound
  - HealthcheckRound

states:
  - SetupRound
  - HealthcheckRound
  - DoneRound
  - ErrorRound

transition_func:
  (SetupRound, DONE): HealthcheckRound
  (SetupRound, ERROR): ErrorRound
  (HealthcheckRound, DONE): DoneRound
  (HealthcheckRound, ERROR): ErrorRound
  (ErrorRound, DONE): SetupRound
```


- Independant Protocols and servers for the frontend components meaning no interaction with core skills.


## Frontend Specification

The frontnend directory structure is as follows;


```bash
packages/AUTHOR/customs/COMPONENT_NAME/
├── build
│   └── index.html
├── component.yaml
├── __init__.py
└── openapi3_spec.yaml
```

The `component.yaml` file is used to define the frontend component and its dependencies.

The `openapi3_spec.yaml` file is used to define the openapi3 spec for the frontend component.

The `build` directory contains the compiled frontend component.

### Component.yaml

An example of a `component.yaml` file is as follows;

```yaml
name: trader_ui
author: tatha
version: 0.1.0
type: custom
description: Custom UI representing a user interface for the trader skill.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
fingerprint:
  __init__.py: bafybeih4oyyzgld4vqtbub6zrcrrfofbhmhbr37rvoxuhzchn3bhhjs7za
  build/index.html: bafybeidtlac2qbn6oohhyyuvbwz36dqxofyiv7s4tsipwbrsl5mnbn65ga
  openapi3_spec.yaml: bafybeiagdbghwj4t4o7uctojvtkjp7i6zxpwu6dltjsawcaeuteyipftty
fingerprint_ignore_patterns: []
dependencies: {}
api_spec: open_api3_spec.yaml
frontend_dir: build
```

Notice the extra fields `api_spec` and `frontend_dir` which are used to define the openapi3 spec and the frontend directory respectively.

### Openapi3 Spec
The framework uses the openapi3 spec to define the API for the frontend component.

An example of an `openapi3_spec.yaml` file is as follows;

```yaml
openapi: 3.0.0
info:
  title: Pandora API
  description: Allows interactions with Autonomous Agents
  version: 0.1.0
servers:
  - url: http://0.0.0.0:5555
paths:
  /:
    get:
      summary: Returns the main HTML page
      responses:
        '200':
          description: HTML response
          content:
            text/html:
              schema:
                type: string
  api/agent-info:
    get:
      summary: Returns the agent's state and info
      responses:
        '200':
          description: A Json response
          content:
            application/json:
              schema:
                type: object
                properties:
                  service-id:
                    type: string
                  safe-address:
                    type: string
                  agent-address:
                    type: string
                  agent-status:
                    type: string
```

The openapi3 spec is used to define the API for the frontend component.

Note: Future extension will include the ability to define `handlers` for the frontend apis.


### Build
The `build` directory contains the compiled frontend code generated from Javascript frameworks like React, Angular, Vue etc.

For example, the `build` directory for a React app would look like this;

```bash
packages/AUTHOR/customs/COMPONENT_NAME
`
├── build
│   ├── asset-manifest.json
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
```

A very simple example of a `index.html` file is as follows;

```html
<!-- Simple html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trader UI</title>
</head>

<body>
    <div id="root"></div>
    <script src="main.js"></script>
    <!-- 
        Table for the simlpe json from the api call. 
    {
      "service-id": null,
      "safe-address": "0x0000000000000000000000000000000000000000",
      "agent-address": "0xfA8d890F50B13e0bC9C7F9424b3bE45F9854C303",
      "agent-status": "active"
    }
    -->
     <!-- We make sure the table has strict lines. serperating the rows and columns. -->
    <table style="border: 1px solid black; border-collapse: collapse; width: 100%; text-align: left;">
        <tr>
            <th>Service ID</th>
            <th>Safe Address</th>
            <th>Agent Address</th>
            <th>Agent Status</th>
        </tr>
        <tr>
            <td id="service-id"></td>
            <td id="safe-address"></td>
            <td id="agent-address"></td>
            <td id="agent-status"></td>
        </tr>
</body>
</html>

<!-- Script to update the table after the call. -->

<script>
    fetch('http://localhost:5555/api/agent-info')
        .then(response => response.json())
        .then(data => {
            document.getElementById('service-id').innerText = data['service-id'];
            document.getElementById('safe-address').innerText = data['safe-address'];
            document.getElementById('agent-address').innerText = data['agent-address'];
            document.getElementById('agent-status').innerText = data['agent-status'];
        });
</script>
```

Notice the `fetch` api call to the `/api/agent-info` route.

This is an example of how the frontend can interact with the backend, i.e. the personal self-hosted agent.

The above page will render after calling the api to;

![image](https://github.com/8ball030/trader/assets/35799987/c2369f47-8df0-44e7-bf22-3e3b7dd57bef)


To call the api of a running agent;

```bash
curl localhost:5555/api/agent-info | jq
{
  "service-id": null,
  "safe-address": "0x0000000000000000000000000000000000000000",
  "agent-address": "0xa5A7daBf37E183DEC2a13E259f64A55554B2c13B",
  "agent-status": "active"
}
```


## Agent Configuration

In order to configre the frontend loader, the following configuration is required;

A) add the frontend loader abci to an existing service.

B) create a custom component for the frontend.


This can be used to configure the frontend as so in the `aea-config.yaml` file;


```yaml
---
public_id: valory/trader_abci:0.1.0
type: skill
models:
  params:
    args:
      user_interface:
        enabled: true
        custom_component: tatha/trader_ui
```


## Roadmap 

There are a number of features that are planned for the frontend loader.

These will be implemented based on future requirements and feedback from the community.

### Future Features.

- Extend to allow websockets.
- Extend to allow custom `handlers` for the frontend apis.
