# Implementation Plan

- [ ] 1. Set up project structure and dependencies
  - Install Express, TypeScript, Prisma, and related dependencies
  - Configure TypeScript compilation settings
  - Set up development scripts in package.json
  - _Requirements: 1.1, 1.2, 1.5_

- [ ] 2. Configure Prisma and database schema
  - Create prisma/schema.prisma with PostgreSQL datasource and client generator
  - Define Role enum with STUDENT and TEACHER values
  - Define User model with id, name, role, createdAt fields
  - Define Feedback model with id, content, confidence, userId, createdAt fields
  - Set up User-Feedback relationship (one-to-many)
  - _Requirements: 5.1, 5.2, 5.3, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 2.1 Write property test for Model ID Generation
  - **Property 2: Model ID Generation**
  - **Validates: Requirements 6.1, 7.1**

- [ ]* 2.2 Write property test for User Model Validation
  - **Property 3: User Model Validation**
  - **Validates: Requirements 6.2, 6.3**

- [ ]* 2.3 Write property test for Feedback Model Validation
  - **Property 4: Feedback Model Validation**
  - **Validates: Requirements 7.2, 7.3, 7.4**

- [ ]* 2.4 Write property test for Automatic Timestamp Generation
  - **Property 5: Automatic Timestamp Generation**
  - **Validates: Requirements 6.4, 7.5**

- [ ]* 2.5 Write property test for User-Feedback Relationship
  - **Property 6: User-Feedback Relationship**
  - **Validates: Requirements 6.5**

- [ ] 3. Initialize Prisma client and database connection
  - Create src/lib/prisma.ts with Prisma client initialization
  - Set up database connection management
  - Configure environment variables for database URL
  - _Requirements: 5.4, 5.5_

- [ ]* 3.1 Write unit tests for Prisma client initialization
  - Test database connection establishment
  - Test error handling for connection failures
  - _Requirements: 5.5_

- [ ] 4. Create Express server with basic middleware
  - Create src/index.ts with Express server setup
  - Configure CORS middleware for cross-origin requests
  - Configure express.json() middleware for JSON parsing
  - Set up basic error handling middleware
  - _Requirements: 1.2, 2.1, 2.2, 2.3, 2.4_

- [ ]* 4.1 Write property test for JSON Request Parsing
  - **Property 1: JSON Request Parsing**
  - **Validates: Requirements 2.2**

- [ ]* 4.2 Write unit tests for middleware configuration
  - Test CORS headers are present in responses
  - Test JSON parsing functionality
  - Test middleware order and functionality
  - _Requirements: 2.1, 2.2_

- [ ] 5. Implement health check endpoint
  - Create GET /health route handler
  - Return JSON response with {"status": "ok"}
  - Ensure HTTP 200 status code
  - Test endpoint accessibility without authentication
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ]* 5.1 Write unit tests for health endpoint
  - Test GET /health returns correct JSON response
  - Test HTTP 200 status code
  - Test endpoint works without authentication
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [ ] 6. Configure server startup and port binding
  - Set server to listen on port 4000
  - Add console logging for successful startup
  - Implement graceful error handling for port binding issues
  - Ensure server starts after all middleware and routes are configured
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ]* 6.1 Write unit tests for server startup
  - Test server listens on port 4000
  - Test error handling for port binding failures
  - _Requirements: 4.1, 4.3_

- [ ] 7. Set up testing framework and utilities
  - Install and configure Jest or Vitest for unit testing
  - Install and configure fast-check for property-based testing
  - Create test utilities for database setup and teardown
  - Set up test environment configuration
  - _Requirements: All testing-related requirements_

- [ ]* 7.1 Create test database setup utilities
  - Create utilities for test database initialization
  - Create utilities for test data cleanup
  - Set up test environment isolation

- [x] 8. Create Ollama AI service integration





  - Create src/services/ollama.ts for AI command execution
  - Implement Windows-safe command execution using "echo '<prompt>' | ollama run mistral"
  - Add prompt validation and sanitization
  - Implement stdout capture and response parsing
  - Add error handling for command execution failures
  - _Requirements: 9.4, 9.5, 10.1, 10.2, 10.3_

- [ ]* 8.1 Write property test for AI Prompt Validation
  - **Property 7: AI Prompt Validation**
  - **Validates: Requirements 9.2, 9.3**

- [ ]* 8.2 Write property test for AI Response Format
  - **Property 8: AI Response Format**
  - **Validates: Requirements 9.5**

- [ ]* 8.3 Write property test for AI Error Handling
  - **Property 9: AI Error Handling**
  - **Validates: Requirements 10.1, 10.2, 10.3**

- [x] 9. Implement AI feedback endpoint




  - Create POST /api/ai/feedback route handler
  - Implement JSON body validation for prompt field
  - Return HTTP 400 for missing or empty prompts
  - Integrate with Ollama service for AI processing
  - Return JSON response with feedback field
  - Implement proper error handling and HTTP status codes
  - _Requirements: 9.1, 9.2, 9.3, 9.5, 10.1, 10.4, 10.5_

- [ ]* 9.1 Write unit tests for AI endpoint
  - Test POST /api/ai/feedback endpoint accessibility
  - Test prompt validation and error responses
  - Test successful AI response formatting
  - Test error handling without authentication
  - _Requirements: 9.1, 9.2, 9.3, 10.4, 10.5_

- [ ] 10. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.