"use client";

import React, { useState } from "react";
import { Mail, CheckCircle } from "lucide-react";
import type { PurchaseOrder } from "@/lib/types";
import { approvePurchaseOrder } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";

interface PurchaseOrderDisplayProps {
  purchaseOrder: PurchaseOrder;
  approvalRequired: boolean;
}

export default function PurchaseOrderDisplay({
  purchaseOrder,
  approvalRequired,
}: PurchaseOrderDisplayProps) {
  const [approverEmail, setApproverEmail] = useState("approver@company.com");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isApproved, setIsApproved] = useState(false);

  const handleApprove = async () => {
    setIsSubmitting(true);
    try {
      await approvePurchaseOrder(purchaseOrder.po_number, approverEmail);
      setIsApproved(true);
    } catch (error) {
      console.error("Failed to approve PO:", error);
      alert("Failed to submit for approval. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      <div className="border-b pb-4">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Purchase Order Created
        </h2>
        <div className="flex items-center justify-between">
          <div>
            <span className="text-gray-600">PO Number:</span>
            <p className="text-xl font-semibold text-primary-600">
              {purchaseOrder.po_number}
            </p>
          </div>
          <div>
            <span className="text-gray-600">Created:</span>
            <p className="font-medium text-gray-900">
              {formatDate(purchaseOrder.created_at)}
            </p>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <h3 className="font-semibold text-gray-900 mb-2">Supplier</h3>
          <p className="text-gray-700">{purchaseOrder.quote.supplier_name}</p>
          {purchaseOrder.quote.supplier_id && (
            <p className="text-sm text-gray-500">
              ID: {purchaseOrder.quote.supplier_id}
            </p>
          )}
        </div>

        <div>
          <h3 className="font-semibold text-gray-900 mb-2">Total Amount</h3>
          <p className="text-2xl font-bold text-primary-600">
            {formatCurrency(
              purchaseOrder.quote.total_amount,
              purchaseOrder.quote.currency
            )}
          </p>
        </div>
      </div>

      <div>
        <h3 className="font-semibold text-gray-900 mb-2">Status Summary</h3>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                purchaseOrder.supplier_validation.is_approved
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              Supplier:{" "}
              {purchaseOrder.supplier_validation.is_approved
                ? "Approved"
                : "Not Approved"}
            </span>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                purchaseOrder.competitive_analysis.is_competitive
                  ? "bg-green-100 text-green-800"
                  : "bg-yellow-100 text-yellow-800"
              }`}
            >
              Pricing:{" "}
              {purchaseOrder.competitive_analysis.is_competitive
                ? "Competitive"
                : "Review Needed"}
            </span>
          </div>
        </div>
      </div>

      {!isApproved ? (
        <div className="border-t pt-4">
          <h3 className="font-semibold text-gray-900 mb-3">
            {approvalRequired
              ? "⚠ Approval Required"
              : "✓ Ready to Process"}
          </h3>
          <p className="text-sm text-gray-600 mb-4">
            {approvalRequired
              ? "This purchase order requires managerial approval before processing."
              : "This purchase order meets all criteria and can be processed."}
          </p>

          <div className="flex gap-4">
            <input
              type="email"
              value={approverEmail}
              onChange={(e) => setApproverEmail(e.target.value)}
              placeholder="Approver email address"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <button
              onClick={handleApprove}
              disabled={isSubmitting || !approverEmail}
              className="flex items-center gap-2 px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Mail className="w-5 h-5" />
              {isSubmitting ? "Submitting..." : "Send for Approval"}
            </button>
          </div>
        </div>
      ) : (
        <div className="border-t pt-4">
          <div className="flex items-center gap-3 p-4 bg-green-50 border border-green-200 rounded-lg">
            <CheckCircle className="w-6 h-6 text-green-500" />
            <div>
              <p className="font-semibold text-green-900">
                Approval Request Sent!
              </p>
              <p className="text-sm text-green-700">
                An approval request has been sent to {approverEmail}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
