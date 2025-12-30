"use client";

import React, { useState } from "react";
import { Loader2, FileText, CheckCircle2, AlertTriangle, Play } from "lucide-react";
import FileUpload from "@/components/FileUpload";
import QuoteDisplay from "@/components/QuoteDisplay";
import ValidationDisplay from "@/components/ValidationDisplay";
import AnalysisDisplay from "@/components/AnalysisDisplay";
import PurchaseOrderDisplay from "@/components/PurchaseOrderDisplay";
import type { ProcessingResult } from "@/lib/types";

type ProcessingStage = 
  | "upload" 
  | "processing_extraction"
  | "review_extraction" 
  | "processing_validation"
  | "review_validation" 
  | "processing_analysis"
  | "review_analysis"
  | "processing_po"
  | "completed" 
  | "error";

export default function Home() {
  const [stage, setStage] = useState<ProcessingStage>("upload");
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  // Step-by-step data storage
  const [extractedData, setExtractedData] = useState<any>(null);
  const [validationData, setValidationData] = useState<any>(null);
  const [analysisData, setAnalysisData] = useState<any>(null);

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError(null);
  };

  const handleStartProcess = async () => {
    if (!selectedFile) return;
    await handleExtraction();
  };

  const handleExtraction = async () => {
    setStage("processing_extraction");
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile!);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/step/extract`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.success && data.data) {
        setExtractedData(data.data);
        setStage("review_extraction");
      } else {
        throw new Error("Extraction failed");
      }
    } catch (err) {
      console.error("Extraction error:", err);
      setError(err instanceof Error ? err.message : "Failed to extract document");
      setStage("error");
    }
  };

  const handleValidation = async () => {
    setStage("processing_validation");
    setError(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/step/validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(extractedData),
      });

      const data = await response.json();

      if (data.success && data.data) {
        setValidationData(data.data);
        setStage("review_validation");
      } else {
        throw new Error("Validation failed");
      }
    } catch (err) {
      console.error("Validation error:", err);
      setError(err instanceof Error ? err.message : "Failed to validate supplier");
      setStage("error");
    }
  };

  const handleAnalysis = async () => {
    setStage("processing_analysis");
    setError(null);

    try {
      const combinedData = {
        ...extractedData,
        ...validationData
      };

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/step/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(combinedData),
      });

      const data = await response.json();

      if (data.success && data.data) {
        setAnalysisData(data.data);
        setStage("review_analysis");
      } else {
        throw new Error("Analysis failed");
      }
    } catch (err) {
      console.error("Analysis error:", err);
      setError(err instanceof Error ? err.message : "Failed to analyze competitiveness");
      setStage("error");
    }
  };

  const handleCreatePO = async () => {
    setStage("processing_po");
    setError(null);

    try {
      const combinedData = {
        ...extractedData,
        ...validationData,
        ...analysisData
      };

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/step/create-po`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(combinedData),
      });

      const data = await response.json();

      if (data.success && data.data) {
        // Build proper ProcessingResult structure
        const fullResult: ProcessingResult = {
          type: "purchase_order",
          purchase_order: {
            po_number: data.data.po_number || "",
            quote: extractedData,
            supplier_validation: validationData,
            competitive_analysis: analysisData,
            status: data.data.status || "pending_approval",
            created_at: data.data.created_at || new Date().toISOString(),
            approver_email: data.data.approver_email
          },
          approval_required: data.data.approval_required !== false
        };
        setResult(fullResult);
        setStage("completed");
      } else {
        throw new Error("PO creation failed");
      }
    } catch (err) {
      console.error("PO creation error:", err);
      setError(err instanceof Error ? err.message : "Failed to create purchase order");
      setStage("error");
    }
  };

  const getStageStatus = (checkStage: string) => {
    // Define stage progression order
    const progressMap: Record<string, number> = {
      "upload": 0,
      "processing_extraction": 1,
      "review_extraction": 1,
      "processing_validation": 2,
      "review_validation": 2,
      "processing_analysis": 3,
      "review_analysis": 3,
      "processing_po": 4,
      "completed": 5,
    };

    const checkMap: Record<string, number> = {
      "extraction": 1,
      "validation": 2,
      "analysis": 3,
      "po": 4,
    };

    const currentProgress = progressMap[stage] || 0;
    const checkProgress = checkMap[checkStage] || 0;

    if (stage === "error") return "error";
    if (checkProgress < currentProgress) return "completed";
    if (checkProgress === currentProgress) return "active";
    return "pending";
  };

  const getStageIcon = (checkStage: string) => {
    const status = getStageStatus(checkStage);
    
    if (status === "error") return <AlertTriangle className="w-5 h-5 text-red-500" />;
    if (status === "completed") return <CheckCircle2 className="w-5 h-5 text-green-500" />;
    if (status === "active") return <Loader2 className="w-5 h-5 text-primary-500 animate-spin" />;
    return <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />;
  };

  const resetWorkflow = () => {
    setStage("upload");
    setResult(null);
    setError(null);
    setSelectedFile(null);
    setExtractedData(null);
    setValidationData(null);
    setAnalysisData(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            AI-Powered Procurement System
          </h1>
          <p className="text-lg text-gray-600">
            Accelerate procurement with intelligent multi-agent analysis
          </p>
          <p className="text-sm text-gray-500 mt-2">
            Powered by Microsoft Agent Framework & CopilotKit
          </p>
        </div>

        {/* Progress Indicator */}
        {stage !== "upload" && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Processing Pipeline
            </h3>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                {getStageIcon("extraction")}
                <span className={getStageStatus("extraction") === "active" ? "font-semibold text-primary-600" : "text-gray-600"}>
                  Document Extraction
                </span>
              </div>
              <div className="flex items-center gap-3">
                {getStageIcon("validation")}
                <span className={getStageStatus("validation") === "active" ? "font-semibold text-primary-600" : "text-gray-600"}>
                  Supplier Validation
                </span>
              </div>
              <div className="flex items-center gap-3">
                {getStageIcon("analysis")}
                <span className={getStageStatus("analysis") === "active" ? "font-semibold text-primary-600" : "text-gray-600"}>
                  Competitive Analysis
                </span>
              </div>
              <div className="flex items-center gap-3">
                {getStageIcon("po")}
                <span className={stage === "completed" ? "font-semibold text-green-600" : "text-gray-600"}>
                  Purchase Order Creation
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Upload Stage */}
        {stage === "upload" && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Upload Quote Document
            </h2>
            <FileUpload onFileSelect={handleFileSelect} />
            
            {selectedFile && (
              <div className="mt-6 flex justify-center">
                <button
                  onClick={handleStartProcess}
                  className="px-8 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors shadow-md hover:shadow-lg flex items-center gap-2"
                >
                  <FileText className="w-5 h-5" />
                  Process Document
                </button>
              </div>
            )}
          </div>
        )}

        {/* Processing Stages */}
        {stage === "processing_extraction" && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8 text-center">
            <Loader2 className="w-12 h-12 text-primary-500 animate-spin mx-auto mb-4" />
            <p className="text-lg text-gray-700">Extracting information from document...</p>
          </div>
        )}

        {stage === "processing_validation" && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8 text-center">
            <Loader2 className="w-12 h-12 text-primary-500 animate-spin mx-auto mb-4" />
            <p className="text-lg text-gray-700">Validating supplier...</p>
          </div>
        )}

        {stage === "processing_analysis" && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8 text-center">
            <Loader2 className="w-12 h-12 text-primary-500 animate-spin mx-auto mb-4" />
            <p className="text-lg text-gray-700">Analyzing competitiveness...</p>
          </div>
        )}

        {stage === "processing_po" && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8 text-center">
            <Loader2 className="w-12 h-12 text-primary-500 animate-spin mx-auto mb-4" />
            <p className="text-lg text-gray-700">Creating purchase order...</p>
          </div>
        )}

        {/* Review Extraction */}
        {stage === "review_extraction" && extractedData && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <div className="flex items-center gap-3 mb-6">
              <CheckCircle2 className="w-8 h-8 text-green-500" />
              <h2 className="text-2xl font-bold text-gray-900">
                Document Extracted Successfully
              </h2>
            </div>
            <QuoteDisplay quote={extractedData} />
            <div className="mt-6 flex justify-center">
              <button
                onClick={handleValidation}
                className="px-8 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-md hover:shadow-lg flex items-center gap-2"
              >
                <Play className="w-5 h-5" />
                Continue to Validation
              </button>
            </div>
          </div>
        )}

        {/* Review Validation */}
        {stage === "review_validation" && validationData && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <div className="flex items-center gap-3 mb-6">
              <CheckCircle2 className="w-8 h-8 text-green-500" />
              <h2 className="text-2xl font-bold text-gray-900">
                Supplier Validation Complete
              </h2>
            </div>
            <ValidationDisplay validation={validationData} />
            
            {validationData.is_approved ? (
              <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-800 font-semibold">
                  ✓ Supplier is approved and verified. Safe to proceed.
                </p>
              </div>
            ) : (
              <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <p className="text-yellow-800 font-semibold">
                  ⚠ Supplier is not on the approved list. Review carefully before proceeding.
                </p>
              </div>
            )}

            <div className="mt-6 flex justify-center">
              <button
                onClick={handleAnalysis}
                className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg flex items-center gap-2"
              >
                <Play className="w-5 h-5" />
                Continue to Analysis
              </button>
            </div>
          </div>
        )}

        {/* Review Analysis */}
        {stage === "review_analysis" && analysisData && (
          <div className="bg-white rounded-lg shadow-md p-8 mb-8">
            <div className="flex items-center gap-3 mb-6">
              <CheckCircle2 className="w-8 h-8 text-green-500" />
              <h2 className="text-2xl font-bold text-gray-900">
                Competitive Analysis Complete
              </h2>
            </div>
            <AnalysisDisplay analysis={analysisData} />
            
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-blue-800">
                <span className="font-semibold">Recommendation:</span> {analysisData.recommendation}
              </p>
            </div>

            <div className="mt-6 flex justify-center gap-4">
              <button
                onClick={resetWorkflow}
                className="px-8 py-3 bg-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-400 transition-colors"
              >
                Reject & Start Over
              </button>
              <button
                onClick={handleCreatePO}
                className="px-8 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors shadow-md hover:shadow-lg flex items-center gap-2"
              >
                <Play className="w-5 h-5" />
                Approve & Create PO
              </button>
            </div>
          </div>
        )}

        {/* Completed Stage */}
        {stage === "completed" && result && (
          <div className="space-y-8">
            <div className="bg-green-50 border-2 border-green-500 rounded-lg p-6 text-center">
              <CheckCircle2 className="w-16 h-16 text-green-500 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-green-900 mb-2">
                Purchase Order Created Successfully!
              </h2>
              <p className="text-green-700">
                All validations passed. Purchase order is ready for approval.
              </p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Quote Information</h3>
              <QuoteDisplay quote={result.purchase_order.quote} />
            </div>

            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Supplier Validation</h3>
              <ValidationDisplay validation={result.purchase_order.supplier_validation} />
            </div>

            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Competitive Analysis</h3>
              <AnalysisDisplay analysis={result.purchase_order.competitive_analysis} />
            </div>

            <div className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Purchase Order</h3>
              <PurchaseOrderDisplay 
                purchaseOrder={result.purchase_order} 
                approvalRequired={result.approval_required}
              />
            </div>

            <div className="flex justify-center">
              <button
                onClick={resetWorkflow}
                className="px-8 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 transition-colors shadow-md hover:shadow-lg"
              >
                Process Another Document
              </button>
            </div>
          </div>
        )}

        {/* Error State */}
        {stage === "error" && (
          <div className="bg-red-50 border-2 border-red-500 rounded-lg p-8 text-center">
            <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-red-900 mb-2">
              Processing Error
            </h2>
            <p className="text-red-700 mb-6">
              {error || "An unexpected error occurred"}
            </p>
            <button
              onClick={resetWorkflow}
              className="px-8 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        )}
      </div>
    </main>
  );
}
