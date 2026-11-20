# Application assembly

### What is integrated

- Week 2: extraction using the zero-shot prompt.
- Week 3: routing.
- Week 4: agent loop and tools.
- Week 5: planner, validator and reviewer.
- Week 6: memory and MCP server.
- Week 7: dense retrieval with a chunk size of 600 and an overlap of 80.

### What is still missing

The Week 8 and 9 stages are still stubs. Retrieval searches the shared corpus instead of returning personal memory facts.

### What is still open

The planner sometimes produces invalid steps and the reviewer sometimes rejects answers because it doesn't have enough evidence.

The application can run from start to finish, but it is not always reliable enough to run unattended.

### Verification

All artifacts match the contract. The verifier checked 45 trace records and validated the gold set.