import Link from 'next/link'
import { ClockIcon, MapPinIcon, TagIcon } from '@heroicons/react/24/outline'

interface MopCardProps {
  mop: {
    id: string
    title: string
    category: string
    region: string
    variables_file: string
  }
}

const categoryColors = {
  'patch-linux': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
  'agent-upgrade': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
  'pipeline-only': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
  'git-ops': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
  'infrastructure': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300',
  'default': 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
}

export default function MopCard({ mop }: MopCardProps) {
  const categoryColor = categoryColors[mop.category as keyof typeof categoryColors] || categoryColors.default

  return (
    <div className="card hover:shadow-xl transition-shadow duration-200">
      <div className="card-header flex justify-between items-start">
        <h3 className="text-lg font-semibold text-white truncate">
          {mop.title}
        </h3>
        <span className={`badge ${categoryColor} ml-2 flex-shrink-0`}>
          {mop.category}
        </span>
      </div>
      
      <div className="card-body">
        <div className="space-y-2 mb-4">
          <div className="flex items-center text-sm text-gray-400">
            <TagIcon className="h-4 w-4 mr-2" />
            <span className="font-mono">{mop.id}</span>
          </div>
          
          <div className="flex items-center text-sm text-gray-400">
            <MapPinIcon className="h-4 w-4 mr-2" />
            <span>{mop.region}</span>
          </div>
          
          <div className="flex items-center text-sm text-gray-400">
            <ClockIcon className="h-4 w-4 mr-2" />
            <span>{mop.variables_file}</span>
          </div>
        </div>
        
        <div className="flex justify-end space-x-2">
          <Link
            href={`/mops/${mop.id}`}
            className="btn btn-primary text-sm"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  )
}