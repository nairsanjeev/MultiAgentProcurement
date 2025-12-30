"use client";

import React from "react";
import { TrendingUp, TrendingDown, AlertTriangle } from "lucide-react";
import type { CompetitiveAnalysis } from "@/lib/types";

interface AnalysisDisplayProps {
  analysis: CompetitiveAnalysis;
}

export default function AnalysisDisplay({ analysis }: AnalysisDisplayProps) {
  const Icon = analysis.is_competitive ? TrendingUp : TrendingDown;
  const iconColor = analysis.is_competitive ? "text-green-500" : "text-yellow-500";
  const bgColor = analysis.is_competitive ? "bg-green-50" : "bg-yellow-50";
  const borderColor = analysis.is_competitive ? "border-green-200" : "border-yellow-200";

  const confidenceLevel = 
    analysis.confidence_score >= 0.7 ? "High" :
    analysis.confidence_score >= 0.4 ? "Medium" : "Low";

  const confidenceColor =
    analysis.confidence_score >= 0.7 ? "text-green-600" :
    analysis.confidence_score >= 0.4 ? "text-yellow-600" : "text-red-600";

  return (
    <div className={`rounded-lg border ${borderColor} ${bgColor} p-6 space-y-4`}>
      <div className="flex items-start gap-3">
        <Icon className={`w-6 h-6 ${iconColor} flex-shrink-0 mt-1`} />
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900 mb-2">
            Competitive Analysis
          </h3>
          
          <div className="space-y-3">
            <div>
              <span className="text-sm font-medium text-gray-700">
                Competitiveness:
              </span>
              <p className={`text-base ${analysis.is_competitive ? 'text-green-700' : 'text-yellow-700'}`}>
                {analysis.is_competitive ? '✓ Competitive pricing' : '⚠ May not be competitive'}
              </p>
            </div>

            {analysis.market_price_range && (
              <div>
                <span className="text-sm font-medium text-gray-700">
                  Market Price Range:
                </span>
                <p className="text-gray-700">{analysis.market_price_range}</p>
              </div>
            )}

            <div>
              <span className="text-sm font-medium text-gray-700">
                Price Comparison:
              </span>
              <p className="text-gray-700">{analysis.price_comparison}</p>
            </div>

            <div>
              <span className="text-sm font-medium text-gray-700">
                Recommendation:
              </span>
              <p className="text-gray-700">{analysis.recommendation}</p>
            </div>

            <div className="pt-2 border-t">
              <span className="text-sm font-medium text-gray-700">
                Confidence Level:
              </span>
              <div className="flex items-center gap-2 mt-1">
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      analysis.confidence_score >= 0.7 ? 'bg-green-500' :
                      analysis.confidence_score >= 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                    }`}
                    style={{ width: `${analysis.confidence_score * 100}%` }}
                  />
                </div>
                <span className={`text-sm font-semibold ${confidenceColor}`}>
                  {confidenceLevel} ({Math.round(analysis.confidence_score * 100)}%)
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
