"use client";

import React from "react";
import { CheckCircle, XCircle, AlertCircle } from "lucide-react";
import type { SupplierValidation } from "@/lib/types";

interface ValidationDisplayProps {
  validation: SupplierValidation;
}

export default function ValidationDisplay({ validation }: ValidationDisplayProps) {
  const Icon = validation.is_approved ? CheckCircle : XCircle;
  const iconColor = validation.is_approved ? "text-green-500" : "text-red-500";
  const bgColor = validation.is_approved ? "bg-green-50" : "bg-red-50";
  const borderColor = validation.is_approved ? "border-green-200" : "border-red-200";

  return (
    <div className={`rounded-lg border ${borderColor} ${bgColor} p-6 space-y-4`}>
      <div className="flex items-start gap-3">
        <Icon className={`w-6 h-6 ${iconColor} flex-shrink-0 mt-1`} />
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900 mb-2">
            Supplier Validation
          </h3>
          <p className="text-gray-700">{validation.validation_message}</p>
        </div>
      </div>

      {validation.is_approved && (
        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-green-200">
          {validation.rating && (
            <div>
              <span className="text-sm text-gray-600">Rating:</span>
              <p className="font-semibold text-gray-900">
                {validation.rating} / 5.0
              </p>
            </div>
          )}
          {validation.supplier_id && (
            <div>
              <span className="text-sm text-gray-600">Supplier ID:</span>
              <p className="font-semibold text-gray-900">
                {validation.supplier_id}
              </p>
            </div>
          )}
          {validation.certifications.length > 0 && (
            <div className="col-span-2">
              <span className="text-sm text-gray-600">Certifications:</span>
              <div className="flex flex-wrap gap-2 mt-2">
                {validation.certifications.map((cert, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full"
                  >
                    {cert}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
