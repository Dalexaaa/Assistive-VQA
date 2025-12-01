'use client';

import { useCallback, useMemo, useRef, useState } from 'react';
import { ImageUploader } from '@/components/ImageUploader';
import { QuestionInput } from '@/components/QuestionInput';
import { AnswerDisplay, type AnalysisStatus, type AnswerDetails } from '@/components/AnswerDisplay';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const sleep = (ms = 160) => new Promise<void>((resolve) => setTimeout(resolve, ms));

export default function Home() {
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [module, setModule] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [statusLog, setStatusLog] = useState<AnalysisStatus[]>([]);
  const [details, setDetails] = useState<AnswerDetails | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const apiBaseUrl = useMemo(() => {
    if (process.env.NEXT_PUBLIC_API_URL) {
      return process.env.NEXT_PUBLIC_API_URL;
    }
    if (typeof window !== 'undefined') {
      const { protocol, hostname } = window.location;
      return `${protocol}//${hostname}:5001`;
    }
    return 'http://localhost:5001';
  }, []);

  const baseStatuses: AnalysisStatus[] = useMemo(
    () => [
      { id: 'prep', label: 'Preparing request', state: 'pending' },
      { id: 'upload', label: 'Uploading image', state: 'pending' },
      { id: 'ocr', label: 'Running OCR', state: 'pending' },
      { id: 'vqa', label: 'Running VQA', state: 'pending' },
      { id: 'merge', label: 'Finalizing answer', state: 'pending' },
    ],
    [],
  );

  const initializeStatuses = useCallback(() => {
    setStatusLog(
      baseStatuses.map((status, index) => ({
        ...status,
        state: index === 0 ? 'active' : 'pending',
        hint: undefined,
      })),
    );
  }, [baseStatuses]);

  const updateStatus = useCallback((id: string, patch: Partial<AnalysisStatus>) => {
    setStatusLog((prev) => prev.map((status) => (status.id === id ? { ...status, ...patch } : status)));
  }, []);

  const handleImageSelect = (file: File, preview: string) => {
    setImage(file);
    setImagePreview(preview);
    setAnswer('');
    setError('');
    setDetails(null);
    setStatusLog([]);
  };

  const handleSubmit = async () => {
    if (!image || !question.trim()) {
      setError('Please provide both an image and a question.');
      return;
    }

    abortControllerRef.current?.abort();

    initializeStatuses();
    setLoading(true);
    setError('');
    setAnswer('');
    setDetails(null);

    try {
      const controller = new AbortController();
      abortControllerRef.current = controller;

      const formData = new FormData();
      formData.append('image', image);
      formData.append('question', question);

      updateStatus('prep', { state: 'done', hint: 'Inputs validated' });
      updateStatus('upload', { state: 'active', hint: 'Uploading image securely' });

      const requestStarted = performance.now();
      const response = await fetch(`${apiBaseUrl}/api/query`, {
        method: 'POST',
        body: formData,
        signal: controller.signal,
      });

      updateStatus('upload', { state: 'done', hint: 'Image uploaded' });
      updateStatus('ocr', { state: 'active', hint: 'Extracting text' });
      await sleep();

      const data = await response.json();

      const latencyMs = Math.round(performance.now() - requestStarted);

      if (!response.ok || !data.success) {
        const message = data?.error
          || (response.status >= 500
            ? 'Server error: the assistant API is unavailable. Please try again shortly.'
            : 'Unable to process the request. Double-check the image and question and try again.');
        setError(message);
        updateStatus('ocr', { state: 'error', hint: 'Processing aborted' });
        updateStatus('vqa', { state: 'error', hint: 'Not started' });
        updateStatus('merge', { state: 'error', hint: 'Response unavailable' });
        return;
      }

      updateStatus('vqa', { state: 'active', hint: 'Generating visual answer' });
      updateStatus('merge', { state: 'pending', hint: 'Waiting for results' });
      await sleep();

      const normalizedDetails: AnswerDetails = {
        ocrText: data.details?.ocr_text ?? '',
        vqaAnswer: data.details?.vqa_answer ?? '',
        vqaQuestionUsed: data.details?.vqa_question_used ?? question,
        latencyMs,
      };

      const ocrHint = normalizedDetails.ocrText
        ? 'Text detected successfully'
        : 'No readable text detected in this frame';
      const vqaHint = normalizedDetails.vqaAnswer
        ? 'Visual answer ready'
        : 'VQA could not find enough context';

      updateStatus('ocr', { state: normalizedDetails.ocrText ? 'done' : 'error', hint: ocrHint });
      await sleep();
      updateStatus('vqa', { state: normalizedDetails.vqaAnswer ? 'done' : 'error', hint: vqaHint });
      updateStatus('merge', { state: 'active', hint: 'Summarizing results' });
      await sleep();
      updateStatus('merge', { state: 'done', hint: 'UI updated with latest answer' });

      setAnswer(data.answer);
      setModule(data.module?.toUpperCase?.() ?? data.module ?? '');
      setDetails(normalizedDetails);
    } catch (err) {
      if (err instanceof DOMException && err.name === 'AbortError') {
        setError('Request canceled before completion.');
        updateStatus('upload', { state: 'error', hint: 'Canceled by user' });
        updateStatus('ocr', { state: 'error', hint: 'Canceled by user' });
        updateStatus('vqa', { state: 'error', hint: 'Canceled by user' });
        updateStatus('merge', { state: 'error', hint: 'Request canceled' });
      } else {
        console.error(err);
        setError('Failed to connect to the API. Make sure the Flask backend is running on port 5001.');
        updateStatus('upload', { state: 'error', hint: 'Image never reached the server' });
        updateStatus('ocr', { state: 'error', hint: 'OCR did not start' });
        updateStatus('vqa', { state: 'error', hint: 'VQA did not start' });
        updateStatus('merge', { state: 'error', hint: 'Network failure' });
      }
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleClear = () => {
    abortControllerRef.current?.abort();
    setImage(null);
    setImagePreview('');
    setQuestion('');
    setAnswer('');
    setModule('');
    setError('');
    setStatusLog([]);
    setDetails(null);
  };

  const handleCancel = () => {
    abortControllerRef.current?.abort();
  };

  return (
    <main className="min-h-screen bg-neutral-50 dark:bg-neutral-950">
      <div className="max-w-6xl mx-auto px-4 py-8 md:py-12">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-3xl md:text-4xl font-semibold text-neutral-900 dark:text-neutral-50 mb-2">
            Assistive Vision & Reading Lab
          </h1>
          <p className="text-neutral-600 dark:text-neutral-400 text-base">
            One streamlined workspace where you can upload an image, ask anything about it, and let the assistant handle both visual reasoning and text recognition for you.
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Left Column - Image & Question */}
          <div className="space-y-6">
            <Card className="border-neutral-200 dark:border-neutral-800">
              <CardHeader className="space-y-1">
                <CardTitle className="text-xl font-medium">Upload Image</CardTitle>
                <CardDescription className="text-sm">
                  Choose an image to analyze
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ImageUploader
                  onImageSelect={handleImageSelect}
                  imagePreview={imagePreview}
                />
              </CardContent>
            </Card>

            <Card className="border-neutral-200 dark:border-neutral-800">
              <CardHeader className="space-y-1">
                <CardTitle className="text-xl font-medium">Ask a Question</CardTitle>
                <CardDescription className="text-sm">
                  What would you like to know about this image?
                </CardDescription>
              </CardHeader>
              <CardContent>
                <QuestionInput
                  value={question}
                  onChange={setQuestion}
                  onSubmit={handleSubmit}
                  loading={loading}
                  disabled={!image}
                />
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Answer */}
          <div>
            <Card className="border-neutral-200 dark:border-neutral-800 h-full">
              <CardHeader className="space-y-1">
                <CardTitle className="text-xl font-medium">Answer</CardTitle>
                <CardDescription className="text-sm">
                  {module && `Processed using ${module.toUpperCase()} module`}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <AnswerDisplay
                  answer={answer}
                  error={error}
                  loading={loading}
                  moduleName={module}
                  statusLog={statusLog}
                  details={details}
                  onClear={handleClear}
                  onCancel={handleCancel}
                  showCancel={loading}
                />
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Feature Info */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-md bg-neutral-900 dark:bg-neutral-100 flex items-center justify-center text-white dark:text-neutral-900 text-lg shrink-0">
                  👁️
                </div>
                <div>
                  <h3 className="font-medium text-neutral-900 dark:text-neutral-50 mb-1">Visual Questions</h3>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400">
                    Ask about objects, colors, scenes, and what&apos;s happening in the image
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-md bg-neutral-900 dark:bg-neutral-100 flex items-center justify-center text-white dark:text-neutral-900 text-lg shrink-0">
                  📝
                </div>
                <div>
                  <h3 className="font-medium text-neutral-900 dark:text-neutral-50 mb-1">Text Recognition</h3>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400">
                    Extract and read text from signs, documents, and labels
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900">
            <CardContent className="pt-6">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-md bg-neutral-900 dark:bg-neutral-100 flex items-center justify-center text-white dark:text-neutral-900 text-lg shrink-0">
                  ♿
                </div>
                <div>
                  <h3 className="font-medium text-neutral-900 dark:text-neutral-50 mb-1">Accessibility</h3>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400">
                    Designed to assist visually impaired users in understanding their surroundings
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}
