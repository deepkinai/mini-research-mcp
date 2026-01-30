"""
Sample MCP Server for ChatGPT Integration

This server implements the Model Context Protocol (MCP) with search and fetch
capabilities designed to work with ChatGPT's chat and deep research features.
"""

import logging
import os
from typing import Dict, List, Any
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


server_instructions = """
This MCP server provides search and document retrieval capabilities
for chat and deep research connectors. Use the search tool to find relevant documents
based on keywords, then use the fetch tool to retrieve complete
document content with citations.
"""


def create_server():
    """Create and configure the MCP server with search and fetch tools."""

    # Initialize the FastMCP server
    mcp = FastMCP(name="Sample MCP Server",
                  instructions=server_instructions)

    @mcp.tool()
    async def search(query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for documents internal knowledge base.

        This tool searches through a local knowledge base to find semantically relevant matches.
        Returns a list of search results with basic information. Use the fetch tool to get
        complete document content.

        Args:
            query: Search query string. Natural language queries work best for semantic search.

        Returns:
            Dictionary with 'results' key containing list of matching documents.
            Each result includes id, title, text snippet, and optional URL.
        """
        if not query or not query.strip():
            return {"results": []}

        results = []

        # Mockup results based on the query
        mockup_id = f"mock@@@{hash(query) % 10000}"
        result = {
            "id": mockup_id,
            "title": "News Article on " + query.title(),
            "text": "Full text about the topic: " + query,
            "url":
            f"https://mockup-url.org/{mockup_id}"
        }

        results.append(result)

        logger.info(f"search returned {len(results)} results")
        return {
            "results": 
            results
        }


    @mcp.tool()
    async def fetch(id: str) -> Dict[str, Any]:
        """
        Retrieve complete document content by ID for detailed
        analysis and citation. This tool fetches the full document
        content from OpenAI Vector Store. Use this after finding
        relevant documents with the search tool to get complete
        information for analysis and proper citation.

        Args:
            id: File ID from vector store (file-xxx) or local document ID

        Returns:
            Complete document with id, title, full text content,
            optional URL, and metadata

        Raises:
            ValueError: If the specified ID is not found
        """
        if not id:
            raise ValueError("Document ID is required")

        logger.info(f"Fetching content for file ID: {id}")

        result = {
            "id": id,
            "title": "Retrieved Document",
            "text": "Full document content for ID: " + id,
            "url": f"https://platform.openai.com/storage/files/{id}",
            "metadata": {
                "source": "Mockup Press",
                "retrieved_by": "Somebody"
            }
        }

        logger.info(f"Fetched file: {id}")
        return result

    return mcp


if __name__ == "__main__":
    """Main function to start the MCP server."""
    # Create the MCP server
    server = create_server()

    protocal = "http"
    host = '0.0.0.0'
    port = 8000

    # Configure and start the server
    logger.info(f"Starting MCP server on {host}:{port} with {protocal} transport")

    try:
        # Use FastMCP's built-in run method with SSE transport
        server.run(transport=protocal, host=host, port=port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise
