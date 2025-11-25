'use client';

import { useRef } from 'react';
import { Button } from '@/components/ui/button';
import Image from 'next/image';

interface ImageUploaderProps {
  onImageSelect: (file: File, preview: string) => void;
  imagePreview: string;
}

export function ImageUploader({ onImageSelect, imagePreview }: ImageUploaderProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('Image size should be less than 10MB');
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        onImageSelect(file, reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onloadend = () => {
        onImageSelect(file, reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  return (
    <div className="w-full">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />

      {imagePreview ? (
        <div className="space-y-4">
          <div className="relative w-full aspect-video rounded-md overflow-hidden bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800">
            <Image
              src={imagePreview}
              alt="Uploaded preview"
              fill
              className="object-contain"
            />
          </div>
          <Button
            onClick={handleClick}
            variant="outline"
            className="w-full"
          >
            Change Image
          </Button>
        </div>
      ) : (
        <div
          onClick={handleClick}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          className="border-2 border-dashed border-neutral-300 dark:border-neutral-700 rounded-md p-12 text-center cursor-pointer hover:border-neutral-400 dark:hover:border-neutral-600 hover:bg-neutral-50 dark:hover:bg-neutral-900 transition-colors"
        >
          <div className="flex flex-col items-center gap-4">
            <div className="w-12 h-12 rounded-md bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center">
              <svg
                className="w-6 h-6 text-neutral-600 dark:text-neutral-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>
            <div>
              <p className="text-sm font-medium text-neutral-900 dark:text-neutral-50 mb-1">
                Click to upload or drag and drop
              </p>
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                PNG, JPG, GIF up to 10MB
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
