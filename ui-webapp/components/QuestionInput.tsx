'use client';

import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { useMemo } from 'react';

interface QuestionInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  loading: boolean;
  disabled: boolean;
}

const exampleQuestions = [
  "What's written on this sign?",
  "What color is the car?",
  "How many people are in this image?",
  "What is this person doing?",
  "Read the text from this document",
];

const MAX_CHARS = 240;

export function QuestionInput({ value, onChange, onSubmit, loading, disabled }: QuestionInputProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && !loading && value.trim()) {
        onSubmit();
      }
    }
  };

  const remaining = useMemo(() => Math.max(0, MAX_CHARS - value.length), [value]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const nextValue = e.target.value.slice(0, MAX_CHARS);
    onChange(nextValue);
  };

  return (
    <div className="space-y-4">
      <Textarea
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder="Type your question here... (e.g., What's in this image? or What does the text say?)"
        className="min-h-[120px] resize-none"
        disabled={disabled || loading}
        maxLength={MAX_CHARS}
        aria-describedby="question-helper"
      />

      <div className="flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400" id="question-helper">
        <span>Press Enter to submit or Shift + Enter for a new line</span>
        <span className={remaining < 20 ? 'text-red-500 dark:text-red-400 font-medium' : ''}>
          {remaining} characters left
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        <p className="text-xs text-neutral-500 dark:text-neutral-400 w-full mb-1">Example questions:</p>
        {exampleQuestions.map((question, index) => (
          <button
            key={index}
            onClick={() => onChange(question)}
            disabled={disabled || loading}
            className="text-xs px-2.5 py-1 bg-neutral-100 dark:bg-neutral-800 hover:bg-neutral-200 dark:hover:bg-neutral-700 rounded-md text-neutral-700 dark:text-neutral-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {question}
          </button>
        ))}
      </div>

      <Button
        onClick={onSubmit}
        disabled={disabled || loading || !value.trim()}
        className="w-full bg-neutral-900 hover:bg-neutral-800 dark:bg-neutral-50 dark:hover:bg-neutral-200 text-white dark:text-neutral-900"
        size="lg"
      >
        {loading ? (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
            Processing...
          </div>
        ) : (
          'Ask Question'
        )}
      </Button>
    </div>
  );
}
