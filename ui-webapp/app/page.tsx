'use client';

import { useState } from 'react';
import { ImageUploader } from '@/components/ImageUploader';
import { QuestionInput } from '@/components/QuestionInput';
import { AnswerDisplay } from '@/components/AnswerDisplay';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function Home() {
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [module, setModule] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleImageSelect = (file: File, preview: string) => {
    setImage(file);
    setImagePreview(preview);
    setAnswer('');
    setError('');
  };

  const handleSubmit = async () => {
    if (!image || !question.trim()) {
      setError('Please provide both an image and a question.');
      return;
    }

    setLoading(true);
    setError('');
    setAnswer('');

    try {
      const formData = new FormData();
      formData.append('image', image);
      formData.append('question', question);

      const response = await fetch('http://localhost:5001/api/query', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        setAnswer(data.answer);
        setModule(data.module);
      } else {
        setError(data.error || 'An error occurred while processing your request.');
      }
    } catch (err) {
      setError('Failed to connect to the API. Make sure the Flask backend is running on port 5001.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setImage(null);
    setImagePreview('');
    setQuestion('');
    setAnswer('');
    setModule('');
    setError('');
  };

  return (
    <main className="min-h-screen bg-neutral-50 dark:bg-neutral-950">
      <div className="max-w-6xl mx-auto px-4 py-8 md:py-12">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-3xl md:text-4xl font-semibold text-neutral-900 dark:text-neutral-50 mb-2">
            Assistive VQA
          </h1>
          <p className="text-neutral-600 dark:text-neutral-400 text-base">
            Upload an image and ask a question. Our AI will help you understand the visual content or read text from the image.
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
                  onClear={handleClear}
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
