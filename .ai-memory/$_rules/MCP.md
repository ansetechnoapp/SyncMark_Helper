# MCP (Master Control Program) Configurations

This project uses two main MCP configurations for database access:

## 1. Production Environment - 'postgres-pro_scrappyodds_supabase'
- **Purpose**: Production and deployment operations
- **Connection Type**: Full Supabase database connection
- **Access Level**: Unrestricted access
- **Security Level**: High (requires proper authentication)
- **Use Cases**:
  - Live application deployment
  - Production data management
  - System-wide operations

## 2. Development Environment - 'postgres-pro_scrappyodds_local'
- **Purpose**: Local development and testing
- **Connection Type**: Local database connection
- **Access Level**: Full administrator access
- **Permissions**: Complete rights (including critical operations)
- **Use Cases**:
  - Development testing
  - Database schema modifications
  - Local debugging
  - Feature implementation testing

**Important Notes**:
- Always use the appropriate MCP configuration based on your environment
- Exercise caution with critical operations in both environments
- Follow security best practices when handling database connections
