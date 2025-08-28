import React from 'react';
import { clsx } from 'clsx';
import { AlertCircle, CheckCircle, AlertTriangle, Info } from 'lucide-react';

interface ValidationMessage {
  type: 'error' | 'warning' | 'success' | 'info';
  message: string;
  field?: string;
}

interface ValidationMessagesProps {
  messages: ValidationMessage[];
  className?: string;
}

export const ValidationMessages: React.FC<ValidationMessagesProps> = ({ 
  messages, 
  className 
}) => {
  if (messages.length === 0) {
    return null;
  }

  const getIcon = (type: ValidationMessage['type']) => {
    switch (type) {
      case 'error':
        return <AlertCircle className="w-4 h-4" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4" />;
      case 'success':
        return <CheckCircle className="w-4 h-4" />;
      case 'info':
        return <Info className="w-4 h-4" />;
    }
  };

  const getStyles = (type: ValidationMessage['type']) => {
    switch (type) {
      case 'error':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'warning':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'success':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'info':
        return 'bg-blue-50 border-blue-200 text-blue-800';
    }
  };

  // Group messages by type
  const groupedMessages = messages.reduce((acc, msg) => {
    if (!acc[msg.type]) acc[msg.type] = [];
    acc[msg.type].push(msg);
    return acc;
  }, {} as Record<ValidationMessage['type'], ValidationMessage[]>);

  return (
    <div className={clsx('space-y-2', className)}>
      {Object.entries(groupedMessages).map(([type, msgs]) => (
        <div
          key={type}
          className={clsx(
            'border rounded-lg p-3',
            getStyles(type as ValidationMessage['type'])
          )}
        >
          <div className="flex items-start gap-2">
            {getIcon(type as ValidationMessage['type'])}
            <div className="flex-1 min-w-0">
              <div className="font-medium capitalize mb-1">
                {type === 'error' ? 'Errors' : 
                 type === 'warning' ? 'Warnings' : 
                 type === 'success' ? 'Success' : 'Information'}
              </div>
              <ul className={clsx('text-sm space-y-1', {
                'list-disc list-inside': msgs.length > 1
              })}>
                {msgs.map((msg, index) => (
                  <li key={index}>
                    {msg.field && (
                      <span className="font-medium">{msg.field}: </span>
                    )}
                    {msg.message}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};