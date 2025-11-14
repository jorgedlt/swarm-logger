# Swarm Ecosystem

This project defines a coordinated ecosystem of autonomous service pods, each implemented as a Docker container running inside a Swarm environment. Every pod has a single, well-defined purpose, but all pods rely on each other to create a functioning multi-agent platform that AIs can use as a toolbox.

## Overview

The system enables AIs to interact safely, obtain credentials, trigger workflows, request services, share information, and coordinate tasks by communicating through a central NATS messaging fabric.

## Components

### swarm-natscore
The NATS server that forms the communication backbone. It routes all inter-pod messages, maintains subject hierarchies, and provides a safe, tightly controlled messaging environment.

- **Purpose**: Message routing, stability, predictable performance
- **Responsibilities**: No interpretation or logic; minimal communication layer

### swarm-logger
The system's record keeper. Subscribes broadly to messages flowing across NATS subjects and writes them to durable logs.

- **Purpose**: Observability, auditability, long-term traceability
- **Responsibilities**: Subscribe cleanly, record reliably, handle throughput without backpressure
- **Message Format**: JSON with timestamp, subject, data

### swarm-cronctl
Provides scheduled task activation. Crafts and sends timed triggers that wake AI agents, initiate workflows, or start recurring tasks.

- **Purpose**: Deliver structured activation messages at correct moments
- **Responsibilities**: Clear schemas, consistent scheduling, proper formatting
- **Documentation**: Trigger formats, timing rules, metadata

### swarm-vaultctl
The credential and secret authority. Holds all sensitive material and issues scoped, short-lived credentials to requesting agents.

- **Purpose**: Strict access control, reliable encryption
- **Responsibilities**: Predictable message patterns, well-defined credential lifecycles
- **Documentation**: Subject names, request/response formats, error states, renewal rules

### swarm-gateway
Provides the safe public-facing interface for AIs. Translates HTTP requests into NATS messages and vice versa.

- **Purpose**: Communication relay between external interfaces and internal messaging
- **Responsibilities**: Clean, secure translator
- **Documentation**: HTTP endpoints, NATS subject mappings, response methods

## Architecture Principles

- Each pod focuses on a single responsibility
- All communication via NATS
- Strong emphasis on documentation for interfaces, message patterns, and operational state
- Modularity, resilience, and clarity of boundaries
- Future agents can join easily

## Getting Started

Each component is built as a Docker container. Refer to individual component READMEs for build and deployment instructions.

## Swarm-Logger Specifics

A reliable logging agent for the swarm that captures and stores all events from NATS subjects.

### Features

- Subscribes to all NATS subjects (`>`)
- Logs messages in JSON format with timestamp, subject, and data
- Durable and reliable with automatic reconnection
- Easy to integrate as a Docker container

### Environment Variables

- `NATS_URL`: NATS server URL (default: `nats://localhost:4222`)
- `LOG_FILE`: Path to the log file (default: `/logs/swarm.log`)

### Running the Container

1. Build the image:
   ```bash
   docker build -t swarm-logger .
   ```

2. Run the container with a volume for logs:
   ```bash
   docker run -e NATS_URL=nats://your-nats-server:4222 -v /host/logs:/logs swarm-logger
   ```

Ensure the NATS server is accessible and the log directory is writable.