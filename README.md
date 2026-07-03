# Multi-Agent Customer Support System

> **A production-inspired multi-agent customer support platform built
> with LangGraph, Groq Llama 3.3, FastAPI, Retrieval-Augmented
> Generation (RAG), and Tool Calling.**

## Overview

This project demonstrates how to build a modular AI application that
separates planning, retrieval, external tool usage, and response
generation into independent agents coordinated by LangGraph.



<img width="1912" height="906" alt="image" src="https://github.com/user-attachments/assets/a4936b52-7ce7-43be-992d-d651a7e2e875" />
<img width="1902" height="898" alt="image" src="https://github.com/user-attachments/assets/2b112eb7-49a5-457b-bf21-513f8bbf9b29" />
<img width="1902" height="898" alt="image" src="https://github.com/user-attachments/assets/417425ce-0e88-436f-b4b9-b507d67a61b0" />
<img width="1911" height="878" alt="image" src="https://github.com/user-attachments/assets/7c536972-96e2-4f11-b18e-c075dd6e76b5" />



<img width="1905" height="897" alt="image" src="https://github.com/user-attachments/assets/6f4b414f-1f91-4c33-9640-c2878403aa66" />



Rather than relying on a single LLM prompt, the system routes work to
specialized agents:

-   **Planner** decides what capabilities are required.
-   **Retriever** searches the internal knowledge base (RAG).
-   **Researcher** executes external tools (order lookup, refund policy,
    ticket creation, shipping policy).
-   **Support** synthesizes a final customer-facing response.

------------------------------------------------------------------------

# Motivation

Traditional chatbot architectures place every responsibility inside one
prompt.

Problems include:

-   poor maintainability
-   no clear separation of concerns
-   hallucinations
-   difficult debugging
-   hard to extend

This project adopts a multi-agent architecture where every component has
one responsibility.

------------------------------------------------------------------------

# Architecture

``` text
                    User
                      │
                      ▼
                 FastAPI API
                      │
                      ▼
                  LangGraph
                      │
                      ▼
                 Planner Agent
              /                 \
      Retriever              Researcher
     (Knowledge Base)      (Tool Calling)
              \                 /
               \               /
                 ▼           ▼
                  Support Agent
                       │
                       ▼
                Structured Response
                       │
                       ▼
                    Frontend
```

------------------------------------------------------------------------

# Tech Stack

-   Python
-   FastAPI
-   LangGraph
-   LangChain
-   Groq
-   Llama-3.3-70B-Versatile
-   ChromaDB
-   HuggingFace Embeddings
-   Sentence Transformers
-   Jinja2
-   HTML/CSS/JavaScript

------------------------------------------------------------------------

# Agents

## Planner

The planner is responsible only for deciding **what capabilities** are
required.

Early design:

``` python
next_agent = "retriever"
```

This tightly coupled planning with execution.

Refactored design:

``` python
use_retriever: bool
use_researcher: bool
```

The planner now expresses intent instead of execution strategy.

------------------------------------------------------------------------

## Retriever

Responsible only for Retrieval-Augmented Generation.

Responsibilities:

-   Search ChromaDB
-   Retrieve relevant documents
-   Return structured documents

No routing logic is performed here.

------------------------------------------------------------------------

## Researcher

Responsible only for external tools.

Tools include:

-   lookup_order
-   refund_policy
-   shipping_policy
-   create_ticket

Originally tool outputs were plain strings.

Example:

``` text
Processing
```

Refactored to structured outputs:

``` json
{
  "order_id":"ORD002",
  "status":"Processing",
  "estimated_delivery":"Tomorrow"
}
```

This greatly simplified downstream reasoning.

------------------------------------------------------------------------

## Support Agent

Consumes:

-   conversation
-   retrieved documents
-   tool outputs

Produces structured output:

-   resolution
-   confidence
-   escalate
-   sources
-   tools_used

------------------------------------------------------------------------

# Shared State

The LangGraph state contains:

-   messages
-   plan
-   use_retriever
-   use_researcher
-   retrieved_docs
-   tool_results
-   agents_used
-   final_response

Each node only updates its own portion of the state.

------------------------------------------------------------------------

# RAG Pipeline

1.  Markdown documents are ingested.
2.  Documents are chunked.
3.  Embeddings generated using BAAI/bge-small-en-v1.5.
4.  Stored in ChromaDB.
5.  Relevant chunks retrieved at runtime.
6.  Support agent uses retrieved context.

------------------------------------------------------------------------

# Tool Calling

The researcher binds tools to the LLM.

The model chooses which tools to invoke.

Returned tool results are structured dictionaries instead of strings.

------------------------------------------------------------------------

# API

POST `/chat`

Request

``` json
{
  "message":"How do I get a refund?",
  "thread_id":"demo"
}
```

Response

``` json
{
  "resolution":"...",
  "confidence":0.95,
  "escalate":false,
  "sources":["refund.md"],
  "tools_used":["refund_policy"]
}
```

------------------------------------------------------------------------

# Frontend

A custom HTML/CSS/JavaScript interface was integrated.

Features include:

-   futuristic UI
-   conversation history
-   confidence badges
-   source chips
-   agent trace
-   demo mode

Future improvement: Use backend-provided `agents_used` to drive the
trace instead of a simulated animation.

------------------------------------------------------------------------

# Problems Encountered

## sentence-transformers missing

Error:

    ModuleNotFoundError: sentence_transformers

Solution:

    pip install sentence-transformers

------------------------------------------------------------------------

## Tool docstring error

    Function must have a docstring

Solution:

Added docstrings to every `@tool`.

------------------------------------------------------------------------

## next_agent design limitation

Original routing relied on

    next_agent

Refactored into

    use_retriever
    use_researcher

This decouples planning from execution.

------------------------------------------------------------------------

## Plain string tool outputs

Original:

    Processing

New:

Structured dictionaries.

------------------------------------------------------------------------

## Missing final_response

Support node returned nothing.

Fixed by returning:

``` python
return {
    "final_response": output
}
```

------------------------------------------------------------------------

## Jinja2 TemplateResponse

Resolved by using the correct `TemplateResponse` signature for the
installed FastAPI/Starlette version.

------------------------------------------------------------------------

## 405 Error

Cause:

Frontend used `localhost` while backend served `127.0.0.1`, triggering
CORS/preflight.

Solution:

Use a consistent host and enable CORS if needed.

------------------------------------------------------------------------

# Design Decisions

-   Planner decides capabilities rather than execution.
-   Retriever never performs routing.
-   Researcher returns structured data.
-   Support agent is the only node generating user-facing language.
-   State is shared through LangGraph instead of global variables.

------------------------------------------------------------------------

# Future Improvements

-   Parallel Retriever + Researcher execution
-   Streaming responses
-   Persistent chat history
-   Authentication
-   Docker Compose
-   Unit and integration tests
-   Observability with LangSmith
-   Production deployment

------------------------------------------------------------------------

# Lessons Learned

Building a reliable AI system requires much more than prompting a
language model. Clear agent responsibilities, structured state, typed
outputs, retrieval, tool orchestration, and iterative refactoring lead
to a system that is easier to understand, debug, and extend.

------------------------------------------------------------------------

