# RepoStory - GitHub Repository Analyzer

## Overview

RepoStory is a web application that analyzes GitHub repositories and generates judge-friendly documentation. It automatically detects the tech stack, provides setup instructions, and creates visual architecture diagrams. The application helps hackathon judges and developers quickly understand any public GitHub repository by parsing its contents and presenting a comprehensive overview with run instructions, dependency information, and downloadable documentation.

## Recent Changes (September 30, 2025)

- ✅ Implemented complete RepoStory application with all core features
- ✅ Enhanced framework detection: Now detects Express, Next.js, React, Vue, Vite (Node.js); Django, Flask, FastAPI (Python); Spring Boot (Java); Rails (Ruby); Laravel (PHP)
- ✅ Security hardening: XSS protection with DOMPurify, Mermaid strict mode, required SESSION_SECRET
- ✅ Production-ready: Debug mode disabled, comprehensive sanitization, framework-specific run commands

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack**: Vanilla JavaScript with modern browser APIs
- **Rationale**: Keeps the application lightweight and avoids framework overhead for a simple UI
- **Key Components**:
  - Mermaid.js for diagram rendering
  - Marked.js for Markdown parsing
  - DOMPurify for XSS protection when rendering user content

**UI Design Pattern**: Single-page application with dynamic content loading
- Form-based input for GitHub URLs
- Asynchronous fetch API calls to backend
- Real-time loading states and error handling
- Results rendered dynamically without page refresh

### Backend Architecture

**Framework**: Flask (Python web framework)
- **Rationale**: Lightweight, flexible, and well-suited for building REST APIs quickly
- **Design Pattern**: Request-response model with JSON API endpoints

**Core Functionality**:
1. **URL Parsing**: Regex-based GitHub URL extraction to identify owner and repository
2. **Repository Analysis**: PyGithub library integration for GitHub API access
3. **Tech Stack Detection**: File-based detection system that inspects repository contents
   - Scans for framework-specific files (package.json, requirements.txt, etc.)
   - Identifies dependencies and build configurations
   - Generates setup instructions based on detected technologies

**Authentication**: Environment-based session management
- Session secret stored in environment variables
- Optional GitHub token for authenticated API requests (higher rate limits)

### Data Flow

1. User submits GitHub repository URL
2. Backend parses URL to extract owner/repo information
3. Application fetches repository metadata via GitHub API
4. Tech stack detection analyzes repository file structure
5. Setup instructions generated based on detected technologies
6. Results formatted and returned as JSON to frontend
7. Frontend renders visualization and instructions

**Error Handling**:
- Client-side validation for empty URLs
- Server-side error responses with appropriate messaging
- Rate limit handling for GitHub API

### Security Considerations

**Environment Variables**: Sensitive data isolation
- `SESSION_SECRET`: Flask session encryption key (required)
- `GITHUB_TOKEN`: Optional API authentication token
- Application fails fast if SESSION_SECRET is missing

**XSS Protection**: DOMPurify sanitization for rendered content
- Prevents malicious script injection when displaying repository data
- Secure content rendering from external sources

## External Dependencies

### Third-Party Services

**GitHub API** (via PyGithub library)
- Purpose: Repository metadata and content retrieval
- Authentication: Optional personal access token
- Rate Limits: 60 requests/hour (unauthenticated), 5000/hour (authenticated)

### Frontend Libraries

- **Mermaid.js** (v10): Diagram and flowchart generation
- **Marked.js**: Markdown to HTML conversion
- **DOMPurify** (v3): HTML sanitization for security

### Backend Dependencies

- **Flask**: Web framework for Python
- **PyGithub**: GitHub API wrapper for repository analysis
- **Requests**: HTTP library for external API calls
- **Markdown**: Python Markdown parser

### Environment Requirements

- Python 3.x runtime
- Required environment variables:
  - `SESSION_SECRET` (mandatory)
  - `GITHUB_TOKEN` (optional, for enhanced API limits)