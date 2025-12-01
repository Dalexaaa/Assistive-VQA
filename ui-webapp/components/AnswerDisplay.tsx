'use client';

import { Button } from '@/components/ui/button';

export type StatusState = 'pending' | 'active' | 'done' | 'error';

export interface AnalysisStatus {
  id: string;
  label: string;
  state: StatusState;
  hint?: string;
}

export interface AnswerDetails {
  ocrText?: string;
  vqaAnswer?: string;
  vqaQuestionUsed?: string;
  latencyMs?: number | null;
}

interface AnswerDisplayProps {
  answer: string;
  error: string;
  loading: boolean;
  moduleName: string;
  statusLog: AnalysisStatus[];
  details?: AnswerDetails | null;
  onClear: () => void;
  onCancel?: () => void;
  showCancel?: boolean;
}

export function AnswerDisplay({
  answer,
  error,
  loading,
  moduleName,
  statusLog,
  details,
  onClear,
  onCancel,
  showCancel,
}: AnswerDisplayProps) {
  const hasStatuses = statusLog.length > 0;

  const renderStatusTimeline = () => (
    <div className="border border-neutral-200 dark:border-neutral-800 rounded-md p-4 bg-neutral-50/70 dark:bg-neutral-900/50">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm font-medium text-neutral-900 dark:text-neutral-50">Analysis status</p>
        {details?.latencyMs && (
          <p className="text-xs text-neutral-500 dark:text-neutral-400">
            {Math.max(1, details.latencyMs)} ms
          </p>
        )}
      </div>
      <ul className="space-y-3">
        {statusLog.map((status, index) => (
          <li key={status.id} className="flex items-start gap-3">
            <StatusBadge state={status.state} stepNumber={index + 1} />
            <div className="flex-1">
              <p className="text-sm font-medium text-neutral-900 dark:text-neutral-100">
                {status.label}
              </p>
              {status.hint && (
                <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">{status.hint}</p>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );

  const renderSuccessDetails = () => (
    <div className="space-y-4">
      <div className="bg-neutral-50 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 rounded-md p-6">
        <div className="flex items-start gap-3">
          <div className="w-6 h-6 rounded-md bg-neutral-900 dark:bg-neutral-100 flex items-center justify-center flex-shrink-0">
            <svg
              className="w-4 h-4 text-white dark:text-neutral-900"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="font-medium text-neutral-900 dark:text-neutral-50">Answer</h3>
              {moduleName && (
                <span className="text-[11px] uppercase tracking-wide px-2 py-0.5 rounded-full bg-neutral-200/70 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-200">
                  {moduleName}
                </span>
              )}
            </div>
            <p className="text-neutral-700 dark:text-neutral-300 leading-relaxed text-sm break-words">
              {answer}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <DetailCard
          title="Detected text (OCR)"
          content={details?.ocrText}
          emptyState="No readable text was found in this image."
        />
        <DetailCard
          title="Visual reasoning (VQA)"
          content={details?.vqaAnswer}
          emptyState="VQA did not return a confident answer."
        />
      </div>

      {details?.vqaQuestionUsed && (
        <div className="border border-neutral-200 dark:border-neutral-800 rounded-md p-4 bg-neutral-100/70 dark:bg-neutral-900/70">
          <p className="text-xs uppercase tracking-wide text-neutral-500 dark:text-neutral-400 mb-1">Prompt sent to VQA</p>
          <p className="text-sm text-neutral-800 dark:text-neutral-200 whitespace-pre-wrap">{details.vqaQuestionUsed}</p>
        </div>
      )}

      <Button onClick={onClear} variant="outline" className="w-full">
        Start Over
      </Button>
    </div>
  );

  const renderError = () => (
    <div className="space-y-4">
      <div className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 rounded-md p-6">
        <div className="flex items-start gap-3">
          <div className="w-5 h-5 rounded-md bg-red-600 dark:bg-red-500 flex items-center justify-center flex-shrink-0 mt-0.5">
            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div className="flex-1">
            <h3 className="font-medium text-red-900 dark:text-red-200 mb-1">Something went wrong</h3>
            <p className="text-red-800 dark:text-red-300 text-sm">{error}</p>
          </div>
        </div>
      </div>
      <Button onClick={onClear} variant="outline" className="w-full">
        Try Again
      </Button>
    </div>
  );

  const renderIdle = () => (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-16 h-16 rounded-md bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center mb-4">
        <svg className="w-8 h-8 text-neutral-400 dark:text-neutral-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </div>
      <p className="text-neutral-500 dark:text-neutral-400 text-sm">
        Upload an image and ask a question to get started
      </p>
    </div>
  );

  return (
    <div className="space-y-5">
      {hasStatuses && (
        <>
          {renderStatusTimeline()}
          {loading && showCancel && onCancel && (
            <Button onClick={onCancel} variant="ghost" className="w-full text-red-600 hover:text-red-700 dark:text-red-400">
              Cancel request
            </Button>
          )}
        </>
      )}

      {!loading && error && renderError()}

      {!loading && !error && answer && renderSuccessDetails()}

      {!loading && !error && !answer && renderIdle()}
    </div>
  );
}

function DetailCard({
  title,
  content,
  emptyState,
}: {
  title: string;
  content?: string;
  emptyState: string;
}) {
  const hasContent = Boolean(content && content.trim().length > 0);

  return (
    <div className="border border-neutral-200 dark:border-neutral-800 rounded-md p-4 bg-white dark:bg-neutral-900 h-full">
      <p className="text-xs uppercase tracking-wide text-neutral-500 dark:text-neutral-400 mb-1">{title}</p>
      <p className={`text-sm ${hasContent ? 'text-neutral-900 dark:text-neutral-100' : 'text-neutral-400 dark:text-neutral-500 italic'}`}>
        {hasContent ? content : emptyState}
      </p>
    </div>
  );
}

function StatusBadge({ state, stepNumber }: { state: StatusState; stepNumber: number }) {
  const base = 'w-8 h-8 rounded-md flex items-center justify-center shrink-0';

  if (state === 'done') {
    return (
      <div className={`${base} bg-emerald-500 text-white`}>
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        </svg>
      </div>
    );
  }

  if (state === 'error') {
    return (
      <div className={`${base} bg-red-500 text-white`}>
        <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
    );
  }

  if (state === 'active') {
    return (
      <div className={`${base} bg-blue-600 text-white`}>
        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className={`${base} bg-neutral-200 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 font-semibold`}>
      {stepNumber}
    </div>
  );
}
