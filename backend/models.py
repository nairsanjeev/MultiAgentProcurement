"""Data models for procurement workflow."""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class QuoteItem(BaseModel):
    """A single item in a quote."""
    item_name: str
    description: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float
    currency: str = "USD"


class Quote(BaseModel):
    """Extracted quote information from a document."""
    supplier_name: str
    supplier_id: Optional[str] = None
    items: List[QuoteItem]
    total_amount: float
    currency: str = "USD"
    quote_date: Optional[str] = None
    quote_number: Optional[str] = None
    raw_text: Optional[str] = None


class SupplierValidation(BaseModel):
    """Result of supplier validation."""
    supplier_name: str
    is_approved: bool
    supplier_id: Optional[str] = None
    rating: Optional[float] = None
    certifications: List[str] = Field(default_factory=list)
    validation_message: str


class CompetitiveAnalysis(BaseModel):
    """Result of competitive analysis."""
    is_competitive: bool
    market_price_range: Optional[str] = None
    price_comparison: str
    recommendation: str
    confidence_score: float = 0.0


class PurchaseOrder(BaseModel):
    """Purchase order information."""
    po_number: str
    quote: Quote
    supplier_validation: SupplierValidation
    competitive_analysis: CompetitiveAnalysis
    status: str = "pending_approval"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    approver_email: Optional[str] = None


class ProcessingStatus(BaseModel):
    """Current processing status."""
    stage: str
    status: str  # "processing", "completed", "failed"
    message: str
    data: Optional[dict] = None
