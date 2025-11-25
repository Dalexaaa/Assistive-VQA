'use client';

import { Button } from '@/components/ui/button';

interface AnswerDisplayProps {
  answer: string;
  error: string;
  loading: boolean;
  onClear: () => void;
}

export function AnswerDisplay({ answer, error, loading, onClear }: AnswerDisplayProps) {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16 space-y-4">
        <div className="w-12 h-12 border-4 border-neutral-900 dark:border-neutral-100 border-t-transparent rounded-full animate-spin" />
        <p className="text-neutral-600 dark:text-neutral-400 font-medium">Analyzing your image...</p>
        <p className="text-sm text-neutral-500 dark:text-neutral-500">This may take a few moments</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-4">
        <div className="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 rounded-md p-6">
          <div className="flex items-start gap-3">
            <div className="w-5 h-5 rounded-md bg-red-600 dark:bg-red-500 flex items-center justify-center flex-shrink-0 mt-0.5">
              <svg
                className="w-3 h-3 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-red-900 dark:text-red-200 mb-1">Error</h3>
              <p className="text-red-800 dark:text-red-300 text-sm">{error}</p>
            </div>
          </div>
        </div>
        <Button onClick={onClear} variant="outline" className="w-full">
          Try Again
        </Button>
      </div>
    );
  }

  if (answer) {
    return (
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
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-neutral-900 dark:text-neutral-50 mb-2">Answer</h3>
              <p className="text-neutral-700 dark:text-neutral-300 leading-relaxed text-sm break-words">{answer}</p>
            </div>
          </div>
        </div>
        <Button onClick={onClear} variant="outline" className="w-full">
          Start Over
        </Button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-16 h-16 rounded-md bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center mb-4">
        <svg
          className="w-8 h-8 text-neutral-400 dark:text-neutral-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </div>
      <p className="text-neutral-500 dark:text-neutral-400 text-sm">Upload an image and ask a question to get started</p>
    </div>
  );
}
