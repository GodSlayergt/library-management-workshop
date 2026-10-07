"""Custom exception for duplicate resource conflicts.

Raised when attempting to create a resource that already exists.
"""


class DuplicateResourceException(Exception):
    """Exception raised when attempting to create a duplicate resource.
    
    Typically used when a unique constraint would be violated,
    such as creating a book with an ISBN that already exists.
    
    Attributes:
        resource_type: Type of resource (e.g., 'Book', 'User')
        identifier: Unique identifier that caused the conflict (e.g., ISBN)
        message: Human-readable error message
    """
    
    def __init__(self, resource_type: str, identifier: str, message: str = None):
        """Initialize the exception.
        
        Args:
            resource_type: Type of resource that caused the conflict
            identifier: Unique identifier value (e.g., ISBN number)
            message: Optional custom error message
        """
        self.resource_type = resource_type
        self.identifier = identifier
        
        if message is None:
            self.message = (
                f"A {resource_type} with identifier '{identifier}' already exists in the system"
            )
        else:
            self.message = message
        
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation of the exception."""
        return self.message
