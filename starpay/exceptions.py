class StarPayError(Exception):
    """Base exception for all StarPay related errors."""
    pass

class StarPayAPIError(StarPayError):
    """Raised when the StarPay API returns an error or fails."""
    pass

class StarPaySignatureError(StarPayError):
    """Raised when signature verification fails."""
    pass
