'use client';

import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';

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

export function QuestionInput({ value, onChange, onSubmit, loading, disabled }: QuestionInputProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!disabled && !loading && value.trim()) {
        onSubmit();
      }
    }
  };

  return (
    <div className="space-y-4">
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your question here... (e.g., What's in this image? or What does the text say?)"
        className="min-h-[100px] resize-none"
        disabled={disabled || loading}
      />

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
