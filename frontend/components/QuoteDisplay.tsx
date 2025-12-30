"use client";

import React from "react";
import { formatCurrency, formatDate } from "@/lib/utils";
import type { Quote as QuoteType } from "@/lib/types";

interface QuoteDisplayProps {
  quote: QuoteType;
}

export default function QuoteDisplay({ quote }: QuoteDisplayProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 space-y-4">
      <div className="border-b pb-4">
        <h3 className="text-xl font-bold text-gray-900 mb-2">Quote Details</h3>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Supplier:</span>
            <p className="font-medium text-gray-900">{quote.supplier_name}</p>
          </div>
          {quote.quote_number && (
            <div>
              <span className="text-gray-600">Quote Number:</span>
              <p className="font-medium text-gray-900">{quote.quote_number}</p>
            </div>
          )}
          {quote.quote_date && (
            <div>
              <span className="text-gray-600">Date:</span>
              <p className="font-medium text-gray-900">
                {formatDate(quote.quote_date)}
              </p>
            </div>
          )}
          {quote.supplier_id && (
            <div>
              <span className="text-gray-600">Supplier ID:</span>
              <p className="font-medium text-gray-900">{quote.supplier_id}</p>
            </div>
          )}
        </div>
      </div>

      <div>
        <h4 className="font-semibold text-gray-900 mb-3">Items</h4>
        <div className="space-y-2">
          {quote.items.map((item, index) => (
            <div
              key={index}
              className="flex justify-between items-start p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex-1">
                <p className="font-medium text-gray-900">{item.item_name}</p>
                {item.description && (
                  <p className="text-sm text-gray-600">{item.description}</p>
                )}
                <p className="text-sm text-gray-600 mt-1">
                  Quantity: {item.quantity} × {formatCurrency(item.unit_price, item.currency)}
                </p>
              </div>
              <div className="text-right">
                <p className="font-semibold text-gray-900">
                  {formatCurrency(item.total_price, item.currency)}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="border-t pt-4">
        <div className="flex justify-between items-center">
          <span className="text-lg font-semibold text-gray-900">Total Amount:</span>
          <span className="text-2xl font-bold text-primary-600">
            {formatCurrency(quote.total_amount, quote.currency)}
          </span>
        </div>
      </div>
    </div>
  );
}
