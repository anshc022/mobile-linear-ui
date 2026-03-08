import React, { useState } from 'react';
import { format } from 'date-fns'; // Assuming date-fns is used
import { Badge } from '@/components/ui/badge'; // Hypothetical UI component
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from '@/components/ui/sheet'; // Hypothetical UI component

// Types based on the request
interface Task {
  id: string;
  title: string;
  status: 'todo' | 'in-progress' | 'done';
  category: string;
  createdAt: Date;
  content: string; // The transcript
}

interface TaskListProps {
  tasks: Task[];
  onStatusToggle: (id: string) => void;
}

export function TaskList({ tasks, onStatusToggle }: TaskListProps) {
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  // Status Badge Component (Reusable)
  const StatusBadge = ({ status, onClick }: { status: string; onClick?: (e: React.MouseEvent) => void }) => {
    const colors = {
      todo: 'bg-gray-100 text-gray-800 border-gray-200',
      'in-progress': 'bg-blue-100 text-blue-800 border-blue-200',
      done: 'bg-green-100 text-green-800 border-green-200',
    };
    
    return (
      <span 
        onClick={onClick}
        className={`px-2 py-1 rounded-full text-xs font-medium border ${colors[status as keyof typeof colors] || colors.todo} cursor-pointer transition-opacity hover:opacity-80`}
      >
        {status.replace('-', ' ').toUpperCase()}
      </span>
    );
  };

  return (
    <div className="w-full space-y-4">
      
      {/* --- DESKTOP VIEW (Hidden on Mobile) --- */}
      <div className="hidden md:block overflow-hidden rounded-lg border border-gray-200 shadow-sm">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title / Transcript</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {tasks.map((task) => (
              <tr key={task.id} onClick={() => setSelectedTask(task)} className="hover:bg-gray-50 cursor-pointer">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">#{task.id}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <StatusBadge 
                    status={task.status} 
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent row click
                      onStatusToggle(task.id);
                    }} 
                  />
                </td>
                <td className="px-6 py-4 text-sm text-gray-900">
                  <div className="font-medium">{task.title}</div>
                  <div className="text-gray-500 text-xs truncate max-w-[300px]">{task.content}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{task.category}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{format(task.createdAt, 'MMM d, yyyy')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* --- MOBILE VIEW (Cards - Hidden on Desktop) --- */}
      <div className="md:hidden space-y-3">
        {tasks.map((task) => (
          <div 
            key={task.id} 
            onClick={() => setSelectedTask(task)}
            className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 active:bg-gray-50 transition-colors cursor-pointer"
          >
            {/* Top Row: ID + Status */}
            <div className="flex justify-between items-start mb-2">
              <span className="text-xs font-mono text-gray-400">#{task.id}</span>
              <StatusBadge 
                status={task.status} 
                onClick={(e) => {
                  e.stopPropagation(); // Prevent card open
                  onStatusToggle(task.id);
                }} 
              />
            </div>

            {/* Middle: Title */}
            <div className="mb-2">
              <h3 className="text-base font-bold text-gray-900 leading-tight">{task.title}</h3>
              {/* Transcript Preview (Short) */}
              <p className="text-sm text-gray-500 line-clamp-2 mt-1">
                {task.content || "No transcript available."}
              </p>
            </div>

            {/* Bottom: Category + Date */}
            <div className="flex justify-between items-center text-xs text-gray-400 mt-3 pt-3 border-t border-gray-50">
              <span className="bg-gray-100 px-2 py-0.5 rounded text-gray-600 font-medium">{task.category}</span>
              <span>{format(task.createdAt, 'MMM d, HH:mm')}</span>
            </div>
          </div>
        ))}
      </div>

      {/* --- DETAILS SHEET (Common for both) --- */}
      <Sheet open={!!selectedTask} onOpenChange={(open) => !open && setSelectedTask(null)}>
        <SheetContent className="overflow-y-auto">
          <SheetHeader>
            <SheetTitle>{selectedTask?.title}</SheetTitle>
            <SheetDescription>Task #{selectedTask?.id}</SheetDescription>
          </SheetHeader>
          
          <div className="mt-6 space-y-6">
            <div>
              <label className="text-sm font-medium text-gray-500">Status</label>
              <div className="mt-1">
                <StatusBadge 
                  status={selectedTask?.status || 'todo'} 
                  onClick={() => selectedTask && onStatusToggle(selectedTask.id)}
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-500">Full Transcript</label>
              <div className="mt-2 p-3 bg-gray-50 rounded-md text-sm text-gray-800 whitespace-pre-wrap leading-relaxed border border-gray-100">
                {selectedTask?.content || "No transcript content."}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium text-gray-500">Category</label>
                <p className="text-sm">{selectedTask?.category}</p>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-500">Created</label>
                <p className="text-sm">{selectedTask && format(selectedTask.createdAt, 'PPP p')}</p>
              </div>
            </div>
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
}
